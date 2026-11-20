"""Prepare only drafts/stock in a disposable Odoo shell; completion is browser-driven."""

import json
import os
import secrets
from pathlib import Path

from odoo import Command, fields, release
from odoo.tests import Form

env = globals()["env"]
if not env.cr.dbname.startswith("primacy_native") or release.version_info[0] not in (
    19,
    20,
):
    raise ValueError("Disposable Odoo 19/20 QA database required")
output = Path(os.environ["PRIMACY_NATIVE_FIXTURE"])
if output.exists():
    raise FileExistsError("Fresh private fixture path required")
password = secrets.token_urlsafe(24)
admin = env.ref("base.user_admin")
admin.write({"password": password})
finished, component = env["product.product"].create(
    [
        {"name": "Primacy UI finished item", "is_storable": True},
        {"name": "Primacy UI component", "is_storable": True},
    ]
)
bom = env["mrp.bom"].create(
    {
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_id": finished.id,
        "product_qty": 1,
        **({"consumption": "flexible"} if release.version_info[0] == 19 else {}),
        "bom_line_ids": [
            Command.create({"product_id": component.id, "product_qty": 2})
        ],
    }
)
with Form(env["mrp.production"]) as form:
    form.product_id = finished
    form.bom_id = bom
    form.product_qty = 1
production = form.record
env["stock.quant"]._update_available_quantity(component, production.location_src_id, 10)
suffix = secrets.token_hex(3)
payable = env["account.account"].create(
    {
        "name": "Primacy UI payable",
        "code": "QA21" + suffix,
        "account_type": "liability_payable",
        "reconcile": True,
        "company_ids": [Command.link(env.company.id)],
    }
)
expense = env["account.account"].create(
    {
        "name": "Primacy UI expense",
        "code": "QA61" + suffix,
        "account_type": "expense",
        "company_ids": [Command.link(env.company.id)],
    }
)
journal = env["account.journal"].create(
    {
        "name": "Primacy UI purchases",
        "code": "Q" + secrets.token_hex(2),
        "type": "purchase",
    }
)
vendor = env["res.partner"].create(
    {"name": "Primacy UI supplier", "property_account_payable_id": payable.id}
)
bill = env["account.move"].create(
    {
        "move_type": "in_invoice",
        "partner_id": vendor.id,
        "journal_id": journal.id,
        "invoice_date": fields.Date.today(),
        "invoice_line_ids": [
            Command.create(
                {
                    "name": "Synthetic service",
                    "quantity": 2,
                    "price_unit": 50,
                    "account_id": expense.id,
                    "tax_ids": [Command.clear()],
                }
            )
        ],
    }
)
fixture = {
    "db": env.cr.dbname,
    "series": release.version_info[0],
    "login": admin.login,
    "password": password,
    "production": production.id,
    "finished": finished.id,
    "component": component.id,
    "source_location": production.location_src_id.id,
    "destination_location": production.location_dest_id.id,
    "bill": bill.id,
    "payable": payable.id,
    "expense": expense.id,
}
if "prierp.license" in env:
    status = env["prierp.license"].status()
    if status["locked"]:
        raise ValueError("Normal core licensing locked; no bypass permitted")
    fixture["core_status"] = status["status"]
with open(
    output, "x", opener=lambda path, flags: os.open(path, flags, 0o600)
) as handle:
    json.dump(fixture, handle)
env.cr.commit()
print("Draft manufacturing/bill fixtures prepared; no completion or posting invoked")
