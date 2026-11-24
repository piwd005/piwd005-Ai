# Indian GST and multicurrency verification

Local run on 2026-11-16. Kit release 0.3.3.

Both series passed all 23 selected tests with zero failures, errors or skips.
The test runs used fresh Indian accounting databases on Odoo Community
19 and 20. The selected upstream Indian localization tests cover fiscal
positions, including vendor bills, branch and bill-to/ship-to scenarios,
GSTR section classification, and HSN summaries across ORM and shared
JavaScript checks. The kit adds three transaction tests per series and
uses independently calculated fixture amounts.

| Check | Observed on both series |
| --- | --- |
| Intra-state customer invoice | INR 1,000 base, CGST 90, SGST 90, INR 1,180 total |
| Inter-state customer invoice | INR 1,000 base, IGST 180, INR 1,180 total |
| Tax-inclusive invoice | INR 1,180 total split into INR 1,000 base and INR 180 GST |
| Domestic credit notes | Linked reversals with opposite tax balances |
| Export with LUT tax configured | USD 100 invoice, zero net GST, INR 8,000 initial receivable |
| USD settlement through payment registration | INR 10,000 receipt, INR 2,000 posted exchange gain, zero residual |

The April 20 test rate is effective on that date in the pinned 19 build.
The pinned 20 build selects the prior rate on April 20 and the new rate
on April 21. The suite verifies the date boundary and uses April 21 for
the settlement on both series. Settlement assertions check the exchange
gain account and balance the exchange journal move.

The initial tests uncovered fixture issues. Enabling regular GST activates
the localization chart's GST taxes. Inclusive prices require inclusive
child taxes on the group. LUT tax and fiscal-position identifiers vary
across the two series, and the LUT fixture produces two offsetting IGST
lines. The exchange entry is linked from the partial reconciliation
records. The first parallel HSN run also used the same default test port.
The final run uses separate loopback ports. Changes are confined to the
test fixtures and skill guidance.

The official Odoo India and multicurrency guides describe how configuration
and currency affect accounting. The CBIC FAQ describes the intra-state and
inter-state distinction used in the fixtures. These scenarios use the
local chart's 18% fixture and fixed synthetic exchange rates. [Odoo India](https://www.odoo.com/documentation/19.0/applications/finance/fiscal_localizations/india.html),
[Odoo multicurrency](https://www.odoo.com/documentation/19.0/applications/finance/accounting/get_started/multi_currency.html),
[CBIC GST FAQ](https://cbic-gst.gov.in/hindi/sectoral-faq.html).

The tests ran against Odoo 19 revision `006220901d6b466fc296edbbcec962d2168a0782`
and Odoo 20 revision `50b51284b32960690293c5f9510e8ce6834664aa`.
The backend ran under localhost-only network confinement. See the
[reproduction recipe](../skills/primacy-engineering/references/gst-multicurrency-testing.md)
and [recorded counts](../evaluations/gst-multicurrency-2026-11-16.json).

Coverage is limited to the selected standard localization and accounting
workflows. Live GST filing, e-invoicing, e-way bills, GSP integration,
custom PriERP localization addons, and full invoice or payment browser
journeys remain unverified. Antigravity runs total zero.
