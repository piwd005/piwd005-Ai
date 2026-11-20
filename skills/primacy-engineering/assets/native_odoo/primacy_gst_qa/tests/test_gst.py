from collections import Counter
from datetime import date

from odoo import Command, release
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestPrimacyGST(AccountTestInvoicingCommon):
    @classmethod
    @AccountTestInvoicingCommon.setup_country("in")
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.write(
            {"state_id": cls.env.ref("base.state_in_gj").id, "vat": "24ZZZZZ0000Z1Z0"}
        )
        if "l10n_in_gst_registration_type" in cls.company._fields:
            cls.company.l10n_in_gst_registration_type = "regular"
        else:
            cls.company.l10n_in_is_gst_registered = True
        cls.chart = cls.env["account.chart.template"]
        cls.local_tax = cls.chart.ref("sgst_sale_18")
        cls.product_a.write(
            {
                "taxes_id": [Command.set(cls.local_tax.ids)],
                "l10n_in_hsn_code": "998314",
            }
        )
        cls.local, cls.inter, cls.export = cls.env["res.partner"].create(
            [
                {
                    "name": "QA Gujarat",
                    "country_id": cls.env.ref("base.in").id,
                    "state_id": cls.company.state_id.id,
                },
                {
                    "name": "QA Maharashtra",
                    "country_id": cls.env.ref("base.in").id,
                    "state_id": cls.env.ref("base.state_in_mh").id,
                },
                {"name": "QA overseas", "country_id": cls.env.ref("base.us").id},
            ]
        )

    def invoice(self, partner, price, tax=None, currency=None):
        line = {"product_id": self.product_a.id, "price_unit": price, "quantity": 1}
        if tax:
            line["tax_ids"] = [Command.set(tax.ids)]
        return self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": partner.id,
                "invoice_date": date(2026, 4, 10),
                "date": date(2026, 4, 10),
                "currency_id": (currency or self.company.currency_id).id,
                "invoice_line_ids": [Command.create(line)],
            }
        )

    def assert_tax(self, invoice, base, total, components):
        self.assertEqual(invoice.amount_untaxed, base)
        self.assertEqual(invoice.amount_total, total)
        self.assertEqual(invoice.amount_tax, total - base)
        tax_lines = invoice.line_ids.filtered("tax_line_id")
        self.assertEqual(
            Counter(
                (
                    line.tax_line_id.l10n_in_gst_tax_type,
                    round(abs(line.amount_currency), 2),
                )
                for line in tax_lines
                if line.amount_currency
            ),
            Counter(components),
        )
        self.assertAlmostEqual(sum(invoice.line_ids.mapped("balance")), 0)
        self.assertEqual(invoice.state, "posted")

    def test_domestic_tax_mapping_and_credit(self):
        for partner, fiscal, expected in [
            (
                self.local,
                "fiscal_position_in_intra_state",
                [("cgst", 90), ("sgst", 90)],
            ),
            (self.inter, "fiscal_position_in_inter_state", [("igst", 180)]),
        ]:
            with self.subTest(partner=partner.name):
                invoice = self.invoice(partner, 1000)
                self.assertEqual(invoice.fiscal_position_id, self.chart.ref(fiscal))
                invoice.action_post()
                self.assert_tax(invoice, 1000, 1180, expected)
                self.assertTrue(
                    all(
                        line.tax_tag_ids
                        for line in invoice.line_ids.filtered("tax_line_id")
                    )
                )
                credit = invoice._reverse_moves(
                    default_values_list=[
                        {
                            "date": invoice.date,
                            "invoice_date": invoice.invoice_date,
                        }
                    ],
                    cancel=False,
                )
                credit.action_post()
                self.assert_tax(credit, 1000, 1180, expected)
                self.assertEqual(credit.reversed_entry_id, invoice)
                self.assertAlmostEqual(
                    sum(
                        (credit | invoice)
                        .line_ids.filtered("tax_line_id")
                        .mapped("balance")
                    ),
                    0,
                )

    def test_tax_included(self):
        inclusive = self.local_tax.copy(
            {
                "children_tax_ids": [
                    Command.set(
                        [
                            tax.copy({"price_include_override": "tax_included"}).id
                            for tax in self.local_tax.children_tax_ids
                        ]
                    )
                ]
            }
        )
        invoice = self.invoice(self.local, 1180, inclusive)
        invoice.action_post()
        self.assert_tax(invoice, 1000, 1180, [("cgst", 90), ("sgst", 90)])

    def test_export_lut_zero_and_usd_settlement(self):
        usd = self.setup_other_currency(
            "USD",
            rates=[
                ("2026-04-10", 0.0125),
                ("2026-04-20", 0.01),
            ],
        )
        lut = self.chart.ref(
            "igst_sale_18_exp_lut", raise_if_not_found=False
        ) or self.chart.ref("igst_sale_18_sez_exp_lut")
        invoice = self.invoice(self.export, 100, lut, usd)
        export_position = self.chart.ref(
            "fiscal_position_in_export", raise_if_not_found=False
        ) or self.chart.ref("fiscal_position_in_export_sez_in")
        self.assertEqual(invoice.fiscal_position_id, export_position)
        self.assertEqual(invoice.invoice_line_ids.tax_ids, lut)
        invoice.action_post()
        self.assert_tax(invoice, 100, 100, [("igst", 18), ("igst", 18)])
        self.assertEqual(
            sorted(invoice.line_ids.filtered("tax_line_id").mapped("amount_currency")),
            [-18, 18],
        )
        self.assertEqual(self.company.currency_id.name, "INR")
        receivable = invoice.line_ids.filtered(
            lambda line: line.account_type == "asset_receivable"
        )
        self.assertEqual((receivable.amount_currency, receivable.balance), (100, 8000))
        bank = self.company_data["default_journal_bank"]
        method = bank.inbound_payment_method_line_ids[:1]
        method.payment_account_id = bank.default_account_id
        inr = self.company.currency_id
        rate_day_value = 8000 if release.version_info[0] == 20 else 10000
        self.assertEqual(
            usd._convert(100, inr, self.company, date(2026, 4, 20)), rate_day_value
        )
        payment_day = date(2026, 4, 21)
        self.assertEqual(usd._convert(100, inr, self.company, payment_day), 10000)
        payment = (
            self.env["account.payment.register"]
            .with_context(
                active_model="account.move",
                active_ids=invoice.ids,
            )
            .create(
                {
                    "payment_date": payment_day,
                    "journal_id": bank.id,
                    "currency_id": usd.id,
                    "payment_method_line_id": method.id,
                    "amount": 100,
                }
            )
            ._create_payments()
        )
        self.assertEqual(invoice.amount_residual, 0)
        self.assertTrue(receivable.reconciled)
        self.assertEqual(
            sum(
                payment.move_id.line_ids.filtered(
                    lambda line: line.account_id == bank.default_account_id
                ).mapped("balance")
            ),
            10000,
        )
        exchange = receivable.full_reconcile_id.partial_reconcile_ids.exchange_move_id
        self.assertEqual(exchange.state, "posted")
        self.assertAlmostEqual(sum(exchange.line_ids.mapped("balance")), 0)
        self.assertEqual(
            sum(
                exchange.line_ids.filtered(
                    lambda line: (
                        line.account_id
                        == self.company.income_currency_exchange_account_id
                    )
                ).mapped("balance")
            ),
            -2000,
        )
