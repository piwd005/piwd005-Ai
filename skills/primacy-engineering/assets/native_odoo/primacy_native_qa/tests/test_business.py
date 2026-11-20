"""Real ORM transactions, synthetic records, independent quantity/account expectations."""

from odoo import Command, fields, release
from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPrimacyNativeBusiness(TransactionCase):
    def test_partial_receipt_backorder_and_quant_reconcile(self):
        product = self.env["product.product"].create(
            {"name": "Primacy QA receipt", "is_storable": True}
        )
        operation = self.env["stock.picking.type"].search(
            [("code", "=", "incoming"), ("company_id", "=", self.env.company.id)],
            limit=1,
        )
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": operation.id,
                "location_id": operation.default_location_src_id.id,
                "location_dest_id": operation.default_location_dest_id.id,
                "move_ids": [
                    Command.create(
                        {
                            "product_id": product.id,
                            "product_uom_qty": 5,
                            (
                                "product_uom"
                                if release.version_info[0] == 19
                                else "uom_id"
                            ): product.uom_id.id,
                            "location_id": operation.default_location_src_id.id,
                            "location_dest_id": operation.default_location_dest_id.id,
                        }
                    )
                ],
            }
        )
        operation.create_backorder = "ask"
        picking.action_confirm()
        picking.move_ids.quantity = 3
        picking.move_ids.picked = True
        action = picking.button_validate()
        self.assertEqual(action["res_model"], "stock.backorder.confirmation")
        wizard = (
            self.env[action["res_model"]].with_context(action["context"]).create({})
        )
        wizard.process()
        self.assertEqual(picking.state, "done")
        backorder = self.env["stock.picking"].search(
            [("backorder_id", "=", picking.id)]
        )
        self.assertEqual(len(backorder), 1)
        self.assertEqual(backorder.move_ids.product_uom_qty, 2)
        self.assertAlmostEqual(
            self.env["stock.quant"]._get_available_quantity(
                product, picking.location_dest_id
            ),
            3,
        )

    def test_manufacturing_completion_reconciles_finished_and_consumed(self):
        finished, component = self.env["product.product"].create(
            [
                {"name": "Primacy QA finished", "is_storable": True},
                {"name": "Primacy QA component", "is_storable": True},
            ]
        )
        bom = self.env["mrp.bom"].create(
            {
                "product_tmpl_id": finished.product_tmpl_id.id,
                "product_id": finished.id,
                "product_qty": 1,
                **(
                    {"consumption": "flexible"} if release.version_info[0] == 19 else {}
                ),
                "bom_line_ids": [
                    Command.create({"product_id": component.id, "product_qty": 2})
                ],
            }
        )
        with Form(self.env["mrp.production"]) as form:
            form.product_id = finished
            form.bom_id = bom
            form.product_qty = 1
        production = form.record
        self.env["stock.quant"]._update_available_quantity(
            component, production.location_src_id, 10
        )
        production.action_confirm()
        production.action_assign()
        production.qty_producing = 1
        production._set_qty_producing()
        production.move_raw_ids.quantity = 2
        production.move_raw_ids.picked = True
        production.button_mark_done()
        self.assertEqual(production.state, "done")
        self.assertEqual(production.move_raw_ids.quantity, 2)
        self.assertEqual(production.move_finished_ids.quantity, 1)
        self.assertAlmostEqual(
            self.env["stock.quant"]._get_available_quantity(
                component, production.location_src_id
            ),
            8,
        )
        self.assertAlmostEqual(
            self.env["stock.quant"]._get_available_quantity(
                finished, production.location_dest_id
            ),
            1,
        )

    def test_supplier_bill_and_credit_reconcile(self):
        company = self.env.company
        payable = self.env["account.account"].create(
            {
                "name": "QA payable",
                "code": "QA210001",
                "account_type": "liability_payable",
                "reconcile": True,
                "company_ids": [Command.link(company.id)],
            }
        )
        expense = self.env["account.account"].create(
            {
                "name": "QA expense",
                "code": "QA610001",
                "account_type": "expense",
                "company_ids": [Command.link(company.id)],
            }
        )
        journal = self.env["account.journal"].create(
            {"name": "QA purchase", "code": "QAP", "type": "purchase"}
        )
        vendor = self.env["res.partner"].create(
            {"name": "Primacy QA vendor", "property_account_payable_id": payable.id}
        )
        bill = self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": vendor.id,
                "journal_id": journal.id,
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "QA service",
                            "quantity": 2,
                            "price_unit": 50,
                            "account_id": expense.id,
                            "tax_ids": [Command.clear()],
                        }
                    )
                ],
            }
        )
        bill.action_post()
        self.assertEqual(bill.state, "posted")
        self.assertEqual(bill.amount_total, 100)
        self.assertAlmostEqual(sum(bill.line_ids.mapped("balance")), 0)
        credit = bill._reverse_moves(
            default_values_list=[
                {"date": fields.Date.today(), "invoice_date": fields.Date.today()}
            ],
            cancel=False,
        )
        credit.action_post()
        self.assertEqual(credit.move_type, "in_refund")
        self.assertEqual(credit.amount_total, 100)
        self.assertAlmostEqual(
            sum(
                (bill.line_ids + credit.line_ids)
                .filtered(lambda line: line.account_id == expense)
                .mapped("balance")
            ),
            0,
        )
        self.assertEqual(bill.amount_residual, 0)
        self.assertEqual(credit.amount_residual, 0)
