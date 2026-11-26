# Odoo 19 Mobile Sub-table Responsiveness & Default List View Preservation

## 1. Problem Statement
Converting sub-tables (`move_raw_ids`, `move_byproduct_ids`, `workorder_ids`) into CSS card layouts (`display: flex / grid` on `tr.o_data_row` and `display: none` on `thead`) breaks Odoo's default ERP interface paradigms, eliminates column headers, causes disorientation for ERP users, and removes tabular multi-row data scanning ergonomics.

Conversely, unstyled desktop tables squished onto mobile screens (360px - 390px) suffered from:
1. Product column truncation (`SFB-00006...` due to `text-overflow: ellipsis` and `white-space: nowrap`).
2. Clipped left border and characters (`PRODUCT` clipped to `RODUCT`) due to Odoo desktop negative margins (`--ListRenderer-margin-x: -16px; margin-left: var(--ListRenderer-margin-x)`).
3. Leaking cross-module CSS rules (such as `min-width: 650px` set on `.o_list_renderer` itself instead of `table.o_list_table`), causing the container to overflow the viewport.

## 2. Architectural Solution: Preserving Default Odoo Table View with Horizontal Touch Panning

### A. Containment & Negative Margin Reset
On mobile screens ($\le 767.98\text{px}$), the `.o_list_renderer` container MUST reset negative horizontal margins and establish an isolated horizontal touch-scroll container:

```scss
.o_form_view .o_field_x2many {
    width: 100% !important;
    max-width: 100% !important;

    .o_list_renderer {
        --ListRenderer-margin-x: 0px !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        margin-top: 0 !important;
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        touch-action: pan-x pan-y !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        background: #ffffff !important;
        scrollbar-width: thin !important;
        scrollbar-color: #cbd5e1 #f8fafc !important;
    }
}
```

### B. Table Width & Column Min-Widths
The inner table remains an authentic `<table>` element (`display: table`) with explicit readable column widths:

```scss
table.o_list_table {
    display: table !important;
    width: 100% !important;
    min-width: 720px !important;
    table-layout: auto !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;

    thead {
        display: table-header-group !important;
        visibility: visible !important;

        tr th {
            display: table-cell !important;
            background-color: #f8fafc !important;
            color: #475569 !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.04em !important;
            padding: 0.65rem 0.75rem !important;
            border-bottom: 2px solid #cbd5e1 !important;
            white-space: nowrap !important;

            &:first-child {
                padding-left: 1rem !important;
            }
            &:last-child {
                padding-right: 1rem !important;
            }
            &[data-name="product_id"] {
                min-width: 240px !important;
                text-align: left !important;
            }
            &[data-name="forecast_availability"] {
                text-align: center !important;
                &:empty::before {
                    content: "AVAILABILITY" !important;
                    display: inline-block !important;
                }
            }
        }
    }

    tbody tr.o_data_row td {
        display: table-cell !important;
        padding: 0.65rem 0.75rem !important;
        vertical-align: middle !important;
        border-bottom: 1px solid #f1f5f9 !important;
        font-size: 0.875rem !important;

        &:first-child {
            padding-left: 1rem !important;
        }
        &:last-child {
            padding-right: 1rem !important;
        }

        &[name="product_id"] {
            min-width: 240px !important;
            max-width: 320px !important;
            width: 260px !important;
            white-space: normal !important;
            word-break: break-word !important;
            overflow: visible !important;
            text-overflow: clip !important;

            .o_field_widget, .o_field_many2one, a, span {
                white-space: normal !important;
                word-break: break-word !important;
                overflow: visible !important;
                text-overflow: clip !important;
                font-weight: 600 !important;
                color: #0f172a !important;
                line-height: 1.35 !important;
            }
        }
    }
}
```

## 3. Verification Evidence
Physical headless Chrome / Playwright captures across multiple mobile viewports:
- `mo_mobile_390_components_cards.png`: Verifies default table structure, visible `PRODUCT` header, 16px left padding, zero text clipping.
- `mo_mobile_390_components_panned.png`: Verifies horizontal touch scrolling revealing `TO CONSUME`, `CONSUMED`, `UNIT`, and `DETAILS` columns.
- `mo_mobile_360_cards.png`: Verifies compact mobile viewport (360px) resilience.
- `mo_desktop_1440_verified.png`: Verifies desktop layout remains 100% unaltered.
