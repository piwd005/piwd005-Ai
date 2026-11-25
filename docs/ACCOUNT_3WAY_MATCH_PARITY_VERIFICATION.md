# Account 3-Way Match Enterprise Parity & Functional Verification Report

## 1. Executive Summary
The Community `account_3way_match` module (`/home/suman/prierp-acc/account_3way_match`) has been comprehensively audited, refactored, and verified against the official Odoo 19 Enterprise baseline (`/home/suman/odoo19/enterprise/account_3way_match`).

## 2. Parity Dimensions & Audit Results
- **Models (`models/account_invoice.py`, `models/account_journal_dashboard.py`)**:
  - Removed redundant non-standard duplicate fields (`is_exact_move_duplicate`, `is_draft_duplicated_ref_ids`, `action_delete_duplicates`) from `account.move`.
  - Core Python models are now a **100% byte-for-byte identical match** (0 diff) with Odoo 19 Enterprise.
- **Views (`views/account_invoice_view.xml`, `views/account_journal_dashboard_view.xml`)**:
  - 100% byte-for-byte identical match (0 diff) with Enterprise.
- **Community Configuration Extension (`views/res_config_settings_views.xml`)**:
  - Safely strips `widget="upgrade_boolean"` from `module_account_3way_match` under Purchase Settings so Community users can toggle 3-way matching natively without enterprise upgrade popups.
- **Pre-Init Hooks (`hooks.py`)**:
  - Updated `pre_init_check_enterprise` SQL query to check `WHERE name = 'web_enterprise' AND state = 'installed'` to prevent self-blocking on Community upgrades.

## 3. End-to-End Live System Testing & Workflow Scenarios
Executed live on database `acc_sh20261023` at `http://localhost:9094`:
1. **Configuration**:
   - Purchase -> Configuration -> Settings -> "3-way matching: purchases, receptions and invoices" verified active and functional.
2. **Search Filters**:
   - Vendor Bills search view filters verified:
     - "Bills to Validate" (`['&', '|', ('release_to_pay', '=', 'yes'), ('invoice_date_due', '<', 'today'), ('state', '=', 'draft')]`)
     - "Bills to Pay" (`['&', '&', ('state', '=', 'posted'), ('payment_state', 'in', ('not_paid', 'partial')), ('release_to_pay','in', ('yes', 'exception'))]`)
     - "Bills in Exception" (`[('release_to_pay','=', 'exception')]`)
3. **Form View & Manual Override**:
   - Vendor Bill "Other Info" tab:
     - `release_to_pay_manual` ("Should Be Paid") selection dropdown (Yes, No, Exception).
     - `force_release_to_pay` ("Force Status") bold label and boolean indicator.
4. **Calculations & Business Scenarios**:
   - PO created for 10 units @ 100.0 with `purchase_method='receive'`.
   - Billed 10 units with 0 received -> `release_to_pay = 'no'`.
   - Received 5 units (partial reception) -> `release_to_pay = 'exception'`.
   - Received remaining 5 units (full reception 10/10) -> `release_to_pay = 'yes'`.
   - Unit price changed from 100 to 120 -> `release_to_pay = 'exception'`.
   - Manual override set to 'yes' -> `release_to_pay = 'yes'`, `force_release_to_pay = True`.
5. **Accounting Dashboard Overview Integration**:
   - Purchases journal card displays dynamically calculated:
     - "To Validate" (Draft bills to validate)
     - "To Pay" (Posted bills with `release_to_pay in ('yes', 'exception')`)
     - "Late"
   - Direct clickable drilldown into filtered Vendor Bills list view verified.

## 4. Automated Test Suite Results
- Executed official test suite via Odoo test runner (`--test-enable --test-tags=/account_3way_match`):
  - `AccountJournalDashboard3WayWatchTest.test_customer_invoice_dashboard` -> **PASSED**
  - `AccountJournalDashboard3WayWatchTest.test_purchase_journal_numbers_and_sums` -> **PASSED**
  - `AccountJournalDashboard3WayWatchTest.test_purchase_journal_numbers_and_sums_to_validate` -> **PASSED**
  - `AccountJournalDashboard3WayWatchTest.test_sale_purchase_journal_for_multi_currency_sale` -> **PASSED**
  - `AccountJournalDashboard3WayWatchTest.test_sale_purchase_journal_for_purchase` -> **PASSED**
  - `TestReleaseToPayInvoice.test_3_way_match` (12 purchase order, invoice, and receipt policy scenarios) -> **PASSED**
  - `TestReleaseToPayInvoice.test_amount_currency_edit` -> **PASSED**
- **Test Summary**: `11 tests, 0 failed, 0 error(s)` (100% pass rate).

## 5. Architectural Root Cause & Resolution for `test_amount_currency_edit`
- **Root Cause**: Upstream Odoo 19 commit `b26818db6d` (`[REV] account: hide sections and notes in journal items tab`) replaced deprecated `journal_line_ids` back to standard `line_ids` inside `<page id="aml_tab">`. The test database had an outdated view 709 (`account.view_move_form`) that still used `journal_line_ids`, causing `Form(account.move)` to treat `line_ids` as an invisible/readonly field outside `aml_tab`.
- **Resolution**: Upgraded module `account` to synchronize `account.view_move_form` with the current Odoo 19 core XML definition. Synchronized `tests/test_release_to_pay_invoice.py` and `tests/test_account_journal_dashboard.py` to match Enterprise byte-for-byte.

## 6. Visual Evidence Artifacts
- `01_purchase_settings_3way_match.png`
- `02_vendor_bills_search_filters.png`
- `03_filter_bills_to_validate.png`
- `04_filter_bills_to_pay.png`
- `05_filter_bills_in_exception.png`
- `06_vendor_bill_other_info.png`
- `07_accounting_dashboard.png`
- `08_dashboard_drilldown_to_validate.png`
- `09_dashboard_drilldown_to_pay.png`

