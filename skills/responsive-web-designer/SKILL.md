---
name: responsive-web-designer
description: >-
  Lead Responsive Web Designer and Mobile Layout Architect standards: mobile-first
  methodology, boundless root architecture, fluid typography (clamp), CSS Grid & Subgrid,
  touch ergonomics (44px+ targets), viewport units (100dvh), safe area insets, and
  relational table panning. Use when building responsive layouts, solving layout overflow,
  or designing multi-device web apps.
---

# Lead Responsive Web Designer & Mobile Layout Guide

Architect fluid, accessible, multi-device layouts that perform flawlessly across screen sizes from 360px smartphones to 4K desktop workstations.

---

## 1. Mobile-First Methodology & Breakpoint System

Always design for the most constrained viewport first ($360\text{px}-430\text{px}$), layering enhancements as screen real estate increases:

```scss
// Standard Enterprise Responsive Breakpoint Tokens
$breakpoint-xs: 360px;   // Extra-small mobile (iPhone SE, compact Android)
$breakpoint-sm: 576px;   // Large mobile / phablets
$breakpoint-md: 768px;   // Tablets portrait (iPad, Android tablets)
$breakpoint-lg: 992px;   // Tablets landscape / small laptops
$breakpoint-xl: 1200px;  // Standard Desktop (1080p screens)
$breakpoint-xxl: 1440px; // Large Desktop / High-DPI displays
$breakpoint-ultra: 1920px; // Ultra-wide / 4K displays
```

- **Upward Media Queries Only**: Write `@media (min-width: ...)` rules. Avoid downward `@media (max-width: ...)` anti-patterns that fight default desktop styles.

---

## 2. The Boundless Root Architecture Law

1. **Zero Root Overflow Masking**:
   - **NEVER** declare `overflow-x: hidden !important` or `overflow: hidden` on root containers (`html`, `body`, `.o_action_manager`, `.o_content`, or top-level view wrappers).
   - *Why*: Root overflow masking breaks natural momentum scrolling on iOS/Android, breaks sticky control panels (`position: sticky`), and traps touch gestures on wide tables and kanbans.
2. **Dedicated Inner Scroll Containers**:
   - Confine horizontal overflow strictly to inner content containers:
     ```scss
     .o_table_responsive_container,
     .o_list_renderer,
     .o_field_x2many .o_list_renderer,
     .o_kanban_renderer.o_kanban_grouped {
       overflow-x: auto !important;
       -webkit-overflow-scrolling: touch !important;
       touch-action: pan-x pan-y !important;
     }
     ```

---

## 3. Fluid Typography & Spacing via `clamp()`

Eliminate jerky breakpoint jumps by calculating continuous fluid dimensions based on viewport width:

```scss
// Fluid Typography
--font-size-body: clamp(0.9rem, 0.82rem + 0.35vw, 1.05rem);
--font-size-h3:   clamp(1.15rem, 1.05rem + 0.5vw, 1.35rem);
--font-size-h2:   clamp(1.35rem, 1.2rem + 0.8vw, 1.75rem);
--font-size-h1:   clamp(1.75rem, 1.5rem + 1.25vw, 2.5rem);

// Fluid Spacing & Gutters
--spacing-page-gutter: clamp(1rem, 0.75rem + 1.25vw, 2.5rem);
--spacing-card-pad:    clamp(0.75rem, 0.5rem + 0.8vw, 1.5rem);
```

---

## 4. Modern Intrinsic Layouts (CSS Grid & Subgrid)

1. **Auto-Fitting Responsive Grids**:
   Avoid manual breakpoint classes (`col-12 col-md-6 col-lg-4`). Use intrinsic CSS Grid:
   ```css
   .responsive-card-grid {
     display: grid;
     grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
     gap: 1.25rem;
   }
   ```
2. **CSS Subgrid for Card Alignment**:
   Ensure card headers, bodies, and footer buttons line up perfectly across columns regardless of content length:
   ```css
   .responsive-card {
     display: grid;
     grid-template-rows: subgrid;
     grid-row: span 3;
   }
   ```

---

## 5. Mobile Touch Ergonomics & Safe Area Insets

1. **Minimum Touch Target Law**:
   - Every clickable button, link, toggle, or icon must maintain an accessible touch bounding box of **$\ge 44\text{px} \times 44\text{px}$** (WCAG 2.2 Target Size).
   - Provide visual spacing of $\ge 8\text{px}$ between adjacent touch targets to eliminate accidental taps.
2. **Dynamic Viewport Units**:
   - Never use `height: 100vh` on mobile browsers (causes vertical jumps as the URL bar appears and disappears).
   - Always use dynamic viewport units:
     ```css
     height: 100dvh;
     min-height: 100dvh;
     ```
3. **Safe Area Insets**:
   - Accommodate device notches, camera islands, and home indicator bars:
     ```css
     padding-top: env(safe-area-inset-top, 16px);
     padding-bottom: env(safe-area-inset-bottom, 24px);
     padding-left: env(safe-area-inset-left, 16px);
     padding-right: env(safe-area-inset-right, 16px);
     ```

---

## 6. Enterprise Relational Tables & Compound Rows Architecture

1. **Relational Sub-Table Resizing (`.o_field_x2many`)**:
   - On mobile viewports ($\le 768\text{px}$), enable touch panning on relational sub-tables:
     ```scss
     .o_field_x2many .o_list_renderer {
       overflow-x: auto !important;
       -webkit-overflow-scrolling: touch !important;
       table.o_list_table {
         min-width: 680px !important;
         table-layout: auto !important;
       }
       th[data-name="product_id"], td[name="product_id"] {
         min-width: 200px !important;
         white-space: normal !important;
       }
     }
     ```
2. **Compound Form Row (`.o_row`) Anti-Stacking**:
   - Never apply blanket `width: 100% !important; display: block !important;` to all form inputs.
   - Maintain inline groupings via `display: inline-flex !important; flex-wrap: wrap !important; align-items: center !important; gap: 0.25rem 0.4rem !important;`.
   - Constrain numeric inputs (`min-width: 50px; max-width: 90px; text-align: right;`) and unit dropdowns (`min-width: 60px; max-width: 110px;`).
3. **Phantom Adaptive Dropdown Suppression**:
   - Suppress empty bottom sheets and adaptive dropdowns when all action buttons are hidden:
     ```scss
     .o_bottom_sheet:empty,
     .o_bottom_sheet:not(:has(:not(.d-none):not(.o_hidden):not(.visually-hidden))) {
       display: none !important;
       visibility: hidden !important;
     }
     ```
4. **Operational Sub-Table Responsive Cards Architecture**:
   - For mission-critical operational line items (e.g. BOM components, work order routing, inventory move lines), simple horizontal table panning degrades user comprehension. Transform sub-tables into responsive cards on mobile viewports ($\le 768\text{px}$):
     ```scss
     .o_field_x2many[name="operational_lines"] {
       .o_list_renderer {
         border: none !important;
         background: transparent !important;
         overflow-x: visible !important;

         table.o_list_table {
           display: block !important;
           width: 100% !important;
           min-width: 0 !important;

           th, td { min-width: 0 !important; max-width: none !important; }
           thead { display: none !important; }

           tbody {
             display: flex !important;
             flex-direction: column !important;
             gap: 0.75rem !important;

             tr.o_data_row {
               display: grid !important;
               grid-template-columns: repeat(3, 1fr) !important;
               grid-template-areas:
                 "title title trash"
                 "status . details"
                 "metric1 metric2 metric3" !important;
               row-gap: 0.6rem !important;
               column-gap: 0.5rem !important;
               padding: 0.85rem !important;
               background: #ffffff !important;
               border: 1px solid #e2e8f0 !important;
               border-radius: 12px !important;
               box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
             }
           }
         }
       }
     }
     ```
   - Reset cell dimensions (`min-width: 0 !important; max-width: none !important;`) across all card children to eliminate unintended horizontal scroll overflows caused by conflicting table column definitions.

5. **Sticky Sub-Table Action Row Left-Pinning (`.o_field_x2many`)**:
   - In relational tables that scroll horizontally (`min-width: 650px+`), action rows containing "Add a line", "Add a section", or "Add a note" must never scroll off-screen to the right.
   - Enforce sticky left pinning:
     ```scss
     .o_field_x2many .o_field_x2many_list_row_add,
     .o_field_x2many .o_list_table tr:last-child td:first-child,
     .o_field_x2many tfoot tr td:first-child {
       position: sticky !important;
       left: 0 !important;
       z-index: 2 !important;
       width: fit-content !important;
     }
     ```
   - On mobile/tablet viewports ($\le 768\text{px}$), the action row stays fixed at the left edge of the scroll container so users can tap "Add a line" immediately without horizontal panning.

6. **Dialog & Wizard Multi-Button Footer Parity**:
   - In modal dialogs and wizard popups (`.modal-dialog`, `.o_dialog`, `.modal-footer`), mobile viewports must never clip or hide footer buttons.
   - Desktop button count must strictly equal mobile button count:
     ```scss
     .modal-footer,
     .o_dialog footer {
       display: flex !important;
       flex-wrap: wrap !important;
       gap: 0.5rem !important;
       justify-content: flex-end !important;

       .btn {
         flex: 1 1 auto !important;
         min-width: 80px !important;
         max-width: 100% !important;
       }
     }
     ```

7. **Touch Gesture Isolation & Swipe Bleed Containment**:
   - Inner scrollable elements (tables, kanban columns, signature pads, slider widgets) must isolate touch panning using `touch-action: pan-x pan-y !important;` or `touch-action: none;` on drag canvases.
   - Notebook tab transitions (e.g. settings pages, chatter tabs) must require explicit, deliberate tap/click events; accidental horizontal swipes within inner content areas must NEVER cause spontaneous tab navigation.


