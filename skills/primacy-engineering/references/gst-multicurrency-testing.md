# Indian GST and multicurrency testing

Use a disposable Odoo database for each target series. Install `l10n_in` with
the Indian chart and use synthetic partners, place-of-supply states, products
and fixed currency rates. Keep scheduled jobs disabled and use the local network
confinement described in [native Odoo testing](native-odoo-testing.md).

The original `primacy_gst_qa` addon under `assets/native_odoo` depends on
`l10n_in`. With the matching Odoo source and Python runtime, stage the addon in
a temporary addon path. For Odoo 20, set the staged manifest version to
`20.0.1.0.0`. Include the standard Odoo addons directory in the addon path.
Run with an explicit disposable database, an empty config and these test options:

```text
--without-demo=all -i primacy_gst_qa --test-enable
--test-tags /primacy_gst_qa,/l10n_in:TestFiscal,/l10n_in:TestGstrSection,/l10n_in:TestL10nInHSNSummary
--http-interface 127.0.0.1 --http-port <unused-port> --no-database-list
--stop-after-init --no-http --max-cron-threads 0
```

For a repeat run on the same disposable database, update both `l10n_in` and
`primacy_gst_qa` so both sets of post-install tests run. Check actual test
counts, errors and skips in the Odoo log. The shared HSN JavaScript checks
start an internal HTTP listener even with `--no-http`. Give each concurrent
test run its own loopback port.

| Synthetic case | Expected results |
| --- | --- |
| Gujarat supplier and Gujarat place of supply | INR 1,000 base, CGST 90 and SGST 90 |
| Gujarat supplier and Maharashtra place of supply | INR 1,000 base, IGST 180 |
| Tax-inclusive INR 1,180 | INR 1,000 base and INR 180 split GST |
| Full credit note | Linked reversal with equal and opposite tax balances |
| USD 100 export fixture with LUT tax selected | Zero GST, INR 8,000 receivable at INR 80/USD |
| USD 100 settlement on April 21 at INR 100/USD | INR 10,000 receipt, INR 2,000 realized gain, zero receivable |

Confirm fiscal position, journal balance, tax tags, document currency and
company currency independently. Derive expected tax amounts from the fixture,
and check settled residuals and the posted exchange difference. Treat these
rates and the 18% scenario as test inputs. Use the upstream GSTR section and
HSN tests for classification and aggregation coverage, and keep government
filing or gateway acceptance as separate verification.

In these pinned builds, the April 20 rate entry applies on April 20 in
Odoo 19 and on April 21 in Odoo 20. The fixture checks April 20 independently,
then uses April 21 for settlement on both series. Verify rate selection at
the date boundary before investigating a discrepancy in the exchange entry.
Find the exchange move through the full reconciliation's partial
reconciliation records. The LUT invoice can carry paired IGST lines with
equal and opposite amounts while net GST remains zero.

References [Odoo India localization](https://www.odoo.com/documentation/19.0/applications/finance/fiscal_localizations/india.html),
[Odoo multicurrency](https://www.odoo.com/documentation/19.0/applications/finance/accounting/get_started/multi_currency.html)
and [CBIC GST FAQs](https://cbic-gst.gov.in/hindi/sectoral-faq.html).

E-invoicing, e-way bills and GST filing are deferred to the PriERP GST integration. Prior local tests are documented in the [GST sandbox reference](gst-edi-sandbox.md).
