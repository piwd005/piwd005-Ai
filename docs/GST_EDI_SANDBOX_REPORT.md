# PriERP GST integration sandbox results

| Workflow | Status in v0.3.5 |
| --- | --- |
| E-invoicing | Deferred to the PriERP GST integration |
| E-way bills, including by IRN | Deferred to the PriERP GST integration |
| GST filing | Deferred to the PriERP GST integration |

The results below are historical local sandbox evidence. External provider
acceptance remains unverified.

On November 17, 2026, the local Odoo 19 sandbox passed 13 distinct cases.
Five covered PriERP returns and simulated provider responses. Eight covered
upstream e-invoice, direct e-way bill and e-way bill by IRN payloads.
The selected case groups recorded zero failures after corrections.

| Workflow | Verified result |
| --- | --- |
| E-invoice | A mocked timeout left the invoice without a receipt. A successful retry sent the expected total and persisted the synthetic IRN. |
| Direct e-way bill | A mocked provider rejection left the record ungenerated. A successful retry sent the expected distance and saved the synthetic number and generated state. |
| E-way bill by IRN | The upstream payload case passed for domestic and export invoices. |
| GSTR-1 and GSTR-3B | Reports agreed with a posted B2B invoice at INR 1,000 taxable value, CGST 90, SGST 90 and IGST zero. |
| GSTR-2B | Synthetic JSON matched the correct posted bill. A same-reference bill from another supplier and a same-reference credit note remained unmatched. |
| Filing workflow | PriERP review and manual submission status passed. An external submission and acknowledgment require a supported GSP or portal workflow. |

The baseline reproduced a false GSTR-2B match and an ambiguous Submit
label. The private application fix limits matching to posted bills or
credits of the requested type and supplier, rejects ambiguous matches,
and keeps unresolved imports partial. The review form labels submission
as manual and asks the operator to confirm prior external submission.
The old fetch action opens JSON import even with a GST username configured.
The e-way bill test harness also stubs the production commit so Odoo can
roll back the transaction after the test.

The database was created without demo data. The backend ran with outbound
network blocked and cron disabled. The tested application source was
`0ee65fba1bb55c81bde9d61978b04e7ac8f9d4f2` with the local corrections,
on Odoo revision `006220901d6b466fc296edbbcec962d2168a0782`.
The cached 20-series application ref checked for this run lacked
`pi_gst_accounting`. The custom-addon results therefore apply to Odoo 19.

The publication contains the original QA addon, instructions and counts.
The private application patch remains available locally and passed
`git apply --check` against the source checkout.
[Sandbox recipe](../skills/primacy-engineering/references/gst-edi-sandbox.md) ·
[Recorded results](../evaluations/gst-edi-sandbox-2026-11-17.json)

External NIC/IRP and GSP sandbox acceptance remains unverified. The
session did not supply approved test-only accounts and endpoints. The
Community checkout also lacked `l10n_in_reports`, and the custom addon
did not implement submission to a GSP. External validation requires
both provisioned credentials and a connector or portal that supports the
specific filing operation. Antigravity runs total zero.
[Odoo India integration](https://www.odoo.com/documentation/19.0/applications/finance/fiscal_localizations/india.html) ·
[NIC sandbox onboarding](https://docs.ewaybillgst.gov.in/apidocs/on-boarding-process.html)
