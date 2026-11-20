"""Run inside Odoo shell against a fresh disposable database; never publish output."""

import json
import os
import secrets
from pathlib import Path

from odoo import release

env = globals()["env"]
if not env.cr.dbname.startswith("primacy_native") or release.version_info[0] not in (
    19,
    20,
):
    raise ValueError("Disposable Odoo 19/20 QA database required")
output = Path(os.environ["PRIMACY_NATIVE_FIXTURE"])
if output.exists():
    raise FileExistsError("Use a fresh private fixture path")
password = secrets.token_urlsafe(24)
admin = env.ref("base.user_admin")
admin.write({"password": password})
product = env["product.product"].create(
    {"name": "Primacy Browser QA receipt", "is_storable": True}
)
op = env["stock.picking.type"].search(
    [("code", "=", "incoming"), ("company_id", "=", env.company.id)], limit=1
)
op.create_backorder = "ask"
picking = env["stock.picking"].create(
    {
        "picking_type_id": op.id,
        "location_id": op.default_location_src_id.id,
        "location_dest_id": op.default_location_dest_id.id,
        "move_ids": [
            (
                0,
                0,
                {
                    "product_id": product.id,
                    "product_uom_qty": 5,
                    (
                        "product_uom" if release.version_info[0] == 19 else "uom_id"
                    ): product.uom_id.id,
                    "location_id": op.default_location_src_id.id,
                    "location_dest_id": op.default_location_dest_id.id,
                },
            )
        ],
    }
)
picking.action_confirm()
picking.move_ids.quantity = 3
picking.move_ids.picked = True
agent = (
    env["ai.assistant.agent"].create({"name": "Primacy Native Browser QA"})
    if "ai.assistant.agent" in env
    else None
)
contact = env["res.partner"].create({"name": "Primacy Native Browser Contact"})
with open(
    output, "x", opener=lambda path, flags: os.open(path, flags, 0o600)
) as handle:
    json.dump(
        {
            "db": env.cr.dbname,
            "login": admin.login,
            "password": password,
            "picking": picking.id,
            "product": product.id,
            "location": picking.location_dest_id.id,
            "agent": agent.id if agent else None,
            "contact": contact.id,
            "chat_action": env.ref("pi_erp_agentic_ai.action_ai_chat").id
            if agent
            else None,
            "series": release.version_info[0],
        },
        handle,
    )
env.cr.commit()
print("Synthetic browser fixtures seeded")
