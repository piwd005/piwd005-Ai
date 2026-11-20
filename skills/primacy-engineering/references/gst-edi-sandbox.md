# PriERP GST integration sandbox

E-invoicing, e-way bills and GST filing are deferred to a future PriERP GST
integration. Keep the sandbox procedure below as a reference for that work.

Verify the installed addon and its Odoo series before selecting a filing path.
The pinned Odoo 19 `pi_gst_accounting` handles return preparation, local
workflow states and GSTR-2B JSON import. Its local submission status is a
manual record. Use a provider acknowledgment to establish remote acceptance.
A configured GST username alone does not establish an active GSP connection.

On a disposable database with an explicit loopback listener and outbound
network blocked, install the matching private `prierp_core` and
`pi_gst_accounting` addons, followed by the original `primacy_gst_edi_qa`
fixture in `assets/native_odoo`. Run the fixture against the reviewed
application fixes. The private fixes are retained in the application
workspace. The published fixture contains no application implementation.

Select the case groups below with Odoo's `--test-tags`. Update the owning
modules to rerun their post-install tests.

```text
/primacy_gst_edi_qa,/l10n_in_edi:TestEdiJson,/l10n_in_ewaybill:TestEwaybillJson,/l10n_in_ewaybill_irn:TestEwaybillJson
```

Use synthetic records and capture the payload values, response transitions,
and journal/report totals. For local e-invoice and e-way bill tests,
stub the provider boundary and assert errors do not create success
artifacts. Assert the successful retry attaches the expected receipt and
updates the document status. For GSTR-2B, test supplier and document type
distinctions before treating a matched bill as evidence. Reconcile GSTR-1
and GSTR-3B against posted invoice amounts.

For external validation, provision approved test-only NIC/IRP, e-way bill
and GSP accounts using the provider's sandbox onboarding process. Verify
the provider endpoint, tenant, test GSTIN and enabled operations. Odoo's
Production Environment setting must remain off for test traffic. Use the
connector that actually implements the specific return operation. Where
the local addon only records a manual status, use the authorized sandbox
connector or portal to perform the filing and verify the acknowledgment
for the exact return type and period. Record remote acknowledgments and
local state in separate evidence fields.

[Odoo India integration](https://www.odoo.com/documentation/19.0/applications/finance/fiscal_localizations/india.html) ·
[NIC e-way bill sandbox onboarding](https://docs.ewaybillgst.gov.in/apidocs/on-boarding-process.html)
