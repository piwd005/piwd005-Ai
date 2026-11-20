import base64
import json
from datetime import date
from unittest.mock import patch

from odoo.addons.l10n_in.tests.common import L10nInTestInvoicingCommon
from odoo.addons.l10n_in_ewaybill.tools.ewaybill_api import EWayBillApi, EWayBillError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPrimacyGSTIntegration(L10nInTestInvoicingCommon):
    def test_e_invoice_gateway_error_and_retry(self):
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner_a,
            products=self.product_a,
            post=True,
        )
        responses = [
            {"error": [{"code": "timeout", "message": "Synthetic timeout"}]},
            {"data": {"Irn": "a" * 64}},
        ]
        with patch.object(
            type(invoice), "_l10n_in_edi_connect_to_server", side_effect=responses
        ) as gateway:
            invoice._l10n_in_edi_send_invoice()
            self.assertIn("Synthetic timeout", invoice.l10n_in_edi_error)
            self.assertFalse(invoice.l10n_in_edi_attachment_id)
            invoice._l10n_in_edi_send_invoice()
        self.assertEqual(gateway.call_count, 2)
        request = gateway.call_args.kwargs
        self.assertEqual(request["url_end_point"], "generate")
        self.assertEqual(
            request["json_payload"]["ValDtls"]["TotInvVal"], invoice.amount_total
        )
        self.assertEqual(invoice.l10n_in_edi_status, "sent")
        self.assertEqual(
            json.loads(invoice.l10n_in_edi_attachment_id.raw)["Irn"], "a" * 64
        )
        self.assertFalse(invoice.l10n_in_edi_error)

    def test_direct_ewaybill_gateway_success(self):
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner_a,
            products=self.product_a,
            post=True,
        )
        bill = self.env["l10n.in.ewaybill"].create(
            {
                "account_move_id": invoice.id,
                "distance": 20,
                "mode": "1",
                "vehicle_no": "GJ11AA1234",
                "vehicle_type": "R",
            }
        )
        response = {
            "data": {
                "ewayBillNo": 100000000001,
                "ewayBillDate": "20/05/2023 09:00:00",
                "validUpto": "21/05/2023 23:59:00",
            }
        }
        rejection = EWayBillError(
            {"error": [{"code": "9999", "message": "Synthetic rejection"}]}
        )
        # Keep the production commit inside Odoo's rollback-only test boundary.
        with (
            patch.object(
                EWayBillApi, "_ewaybill_generate", side_effect=[rejection, response]
            ) as gateway,
            patch.object(self.env.cr, "commit") as commit,
        ):
            self.assertFalse(bill._generate_ewaybill())
            self.assertIn("Synthetic rejection", bill.error_message)
            self.assertNotEqual(bill.state, "generated")
            commit.assert_not_called()
            bill._generate_ewaybill()
            commit.assert_called_once()
        self.assertEqual(gateway.call_count, 2)
        self.assertEqual(gateway.call_args.args[0]["transDistance"], "20")
        self.assertEqual(bill.state, "generated")
        self.assertEqual(bill.name, "100000000001")

    def test_gstr1_and_gstr3b_reconcile_to_posted_b2b_sale(self):
        tax = self.env["account.chart.template"].ref("sgst_sale_18")
        invoice = self.init_invoice(
            "out_invoice",
            partner=self.partner_a,
            amounts=[1000],
            taxes=tax,
            invoice_date="2023-05-20",
            post=True,
        )
        self.assertEqual(invoice.amount_tax, 180)
        day = date(2023, 5, 20)
        for model, section in (
            ("pi.gstr1.report", "sec_4a"),
            ("pi.gstr3b.report", "s31a"),
        ):
            with self.subTest(report=model):
                values = self.env[model]._compute_period_data(
                    day, day, self.env.company, False
                )
                self.assertEqual(
                    tuple(
                        values[section][key] for key in ("base", "cgst", "sgst", "igst")
                    ),
                    (1000, 90, 90, 0),
                )

    def return_for_month(self, return_type):
        return self.env["account.return"].create(
            {
                "name": "Synthetic GST return",
                "return_type": return_type,
                "date_from": "2023-05-01",
                "date_to": "2023-05-31",
                "company_id": self.env.company.id,
            }
        )

    def test_manual_filing_and_import_are_explicit(self):
        gstr1 = self.return_for_month("gstr1")
        gstr1.action_validate()
        self.assertEqual(gstr1.state, "reviewed")
        view = self.env["account.return"].get_view(view_type="form")["arch"]
        self.assertIn("Mark Submitted Manually", view)
        gstr1.action_submit()
        self.assertEqual(gstr1.state, "submitted")

        gstr2b = self.return_for_month("gstr2b")
        self.env.company.l10n_in_gstr_gst_username = "synthetic-sandbox"
        self.assertEqual(
            gstr2b.action_gstr2b_fetch()["res_model"], "pi.gstr2b.upload.wizard"
        )

    def test_import_does_not_match_wrong_supplier_or_document_type(self):
        real = self.init_invoice(
            "in_invoice",
            partner=self.partner_a,
            amounts=[100],
            invoice_date="2023-05-20",
            post=True,
        )
        real.ref = "SYN-QA-100"
        wrong = self.init_invoice(
            "in_invoice",
            partner=self.partner_b,
            amounts=[100],
            invoice_date="2023-05-20",
            post=True,
        )
        wrong.ref = "SYN-QA-200"
        credit = self.init_invoice(
            "in_refund",
            partner=self.partner_a,
            amounts=[100],
            invoice_date="2023-05-20",
            post=True,
        )
        credit.ref = wrong.ref
        gstr2b = self.return_for_month("gstr2b")
        payload = {
            "b2b": [
                {
                    "ctin": self.partner_a.vat,
                    "inv": [
                        {"inum": bill.ref, "dt": "20-05-2023", "val": bill.amount_total}
                        for bill in (real, wrong)
                    ],
                }
            ]
        }
        self.env["pi.gstr2b.upload.wizard"].create(
            {
                "return_id": gstr2b.id,
                "json_file": base64.b64encode(json.dumps(payload).encode()),
            }
        ).action_upload_and_match()
        self.assertEqual(real.l10n_in_gstr2b_reconciliation_status, "matched")
        self.assertEqual(
            wrong.l10n_in_gstr2b_reconciliation_status, "bills_not_in_gstr2"
        )
        self.assertEqual(
            credit.l10n_in_gstr2b_reconciliation_status, "bills_not_in_gstr2"
        )
        self.assertEqual(gstr2b.state, "partially_matched")
