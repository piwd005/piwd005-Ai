# Mobile Responsive & Mobile-Safe Download Architecture (Odoo 19 & 20)

This architectural standard documents the 4 critical mobile issues resolved across `prierp_core`, `pi_shop_floor`, and related modules:

---

## 1. Mobile/WebView Safe Downloader (Fix for Flutter / Dart `blob:` Origin Crash)

### Symptom
When downloading reports or clicking "Print" on mobile apps wrapping Odoo (such as Flutter InAppWebView on PiCloud Mobile / `ecommerce.getpicloud.com`), the app crashed with:
`Download failed: Bad state: Origin is only applicable schemes http and https: blob:https://...`

### Root Cause
In Odoo 19, `@web/core/network/download.js` performs downloads using `XMLHttpRequest` with `responseType: "blob"`, then calls `URL.createObjectURL(blob)` and clicks `<a href="blob:https://..." download="...">`.
When Flutter's webview listener intercepts the download, Dart executes `Uri.parse(url).origin`. Dart's `Uri.origin` getter asserts that the scheme must be `http` or `https`, throwing a fatal `StateError` on `blob:`.

### Resolution Pattern
In `prierp_core/static/src/js/download_mobile.js`, patch `download._download` on mobile / webview clients (`isMobileOS() || window.flutter_inappwebview || /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent)`).
Instead of generating an in-memory `blob:` URL, submit a hidden `<form method="POST" action="/report/download">` with the CSRF token and data payload. The browser/webview makes an authentic HTTPS POST to the endpoint, which returns headers `Content-Disposition: attachment; filename=...`.
Because the URL is `https://.../report/download`, Flutter's `Uri.parse(url).origin` evaluates cleanly without error.

---

## 2. Relational Sub-Table Resizing & Horizontal Touch Panning (`.o_field_x2many`)

### Symptom
On mobile form views (e.g. Manufacturing Orders -> Components tab `move_raw_ids`), tables were squished and product names were clipped into short unreadable truncations like `SFB-00006...`.

### Root Cause
Default Odoo list renderers use `table-layout: fixed` and divide available width equally between columns without minimum boundary constraints on small screens.

### Resolution Pattern
In `responsive_global.scss` and `shop_floor_responsive.scss`:
1. Wrap `.o_field_x2many .o_list_renderer` in an overflow container:
   `overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; touch-action: pan-x pan-y !important;`
2. Enforce `table.o_list_table { min-width: 680px !important; table-layout: auto !important; }`.
3. Provide explicit minimum column dimensions:
   - `th[data-name="product_id"], td[name="product_id"]`: `min-width: 220px !important; max-width: 340px !important; white-space: normal !important;`
   - `th[data-name="product_uom_qty"], td[name="product_uom_qty"]`: `min-width: 105px !important;`
   - `th[data-name="quantity"], td[name="quantity"]`: `min-width: 105px !important;`
   - `th[data-name="product_uom"], td[name="product_uom"]`: `min-width: 80px !important;`
   - Left and right cell padding `0.85rem` so text never hugs the border.

---

## 3. Inline `.o_row` Quantity Field Alignment (Preventing 6-Line Vertical Stacking)

### Symptom
On mobile MO forms, the Quantity field row (`qty_producing / product_qty Nos To Produce [chart]`) stacked into a clumsy 6-line vertical tower.

### Root Cause
Mobile responsive CSS targeted `.o_wrap_field .o_field_widget` and `input` with `width: 100% !important; display: block !important;`. This forced every item inside `.o_row` to occupy 100% width, cascading onto its own line. Additionally, inner `.o_row` wrapper had `flex-grow: 1`.

### Resolution Pattern
Inside `.o_form_view`:
1. Restrict 100% width rules: `> .o_field_widget:not(.o_row):not([name="qty"])`.
2. Style `.o_row, .o_row[name="qty"], .oe_row`:
   `display: inline-flex !important; flex-wrap: wrap !important; align-items: center !important; gap: 0.25rem 0.4rem !important;`
3. Neutralize inner flex growth:
   `> .o_row, .o_row.flex-grow-1 { display: inline-flex !important; flex: 0 0 auto !important; flex-grow: 0 !important; width: auto !important; }`
4. Constrain numeric inputs: `input { min-width: 50px !important; max-width: 80px !important; min-height: 32px !important; text-align: right !important; }`.
5. Constrain UoM dropdowns: `min-width: 60px !important; max-width: 100px !important;`.
6. Make labels, spans, and icon buttons inline with touch-friendly dimensions.

---

## 4. Elimination of Redundant 3-Dots Adaptive Buttons & Empty Bottom Sheets

### Symptom
Clicking the 3-dots button `[ ⋮ ]` in mobile form control panels (e.g. `pos.session` which has `create="0" edit="0"`) opened an empty, blank bottom sheet.

### Root Cause
`web.ControlPanel` renders `<Dropdown t-if="env.isSmall" menuClass="'o-control-panel-adaptive-dropdown'">` unconditionally. Even when all button slots (`control-panel-create-button`, `layout-buttons`, etc.) are empty, the dropdown button rendered. Clicking it spawned an empty bottom sheet dialog.

### Resolution Pattern
1. In `core.xml`:
   `<xpath expr="//Dropdown[contains(@menuClass, 'o-control-panel-adaptive-dropdown')]" position="replace"/>`
2. In `responsive_global.scss`:
   `.o_control_panel_main_buttons { > .dropdown:has(.o-control-panel-adaptive-dropdown), .o-control-panel-adaptive-dropdown { display: none !important; } }`
3. Globally suppress empty bottom sheets:
   `.o_bottom_sheet:empty, .o_bottom_sheet:not(:has(:not(.d-none):not(.o_hidden):not(.visually-hidden))) { display: none !important; visibility: hidden !important; }`
