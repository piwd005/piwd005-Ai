# SCSS and CSS

- Formatting: 4-space indent (no tabs), ~80-column lines, opening brace on the
  selector line, closing brace on its own line, one declaration per line.
- Order properties from the outside in (start at `position`, end with decorative
  rules like `font`/`filter`); put scoped SCSS and CSS variables at the top,
  separated by a blank line.
- Class naming: avoid `id` selectors; prefix classes with `o_<module>` (just
  `o_` for the webclient). Use the flat "grandchild" approach
  (`o_element_entry`), not hyper-specific nested names. Classes use
  underscores (`o_`); SCSS variables, mixins and functions below use hyphens
  (`o-`).
- Variable conventions: SCSS `$o-[root]-[element]-[property]-[modifier]`, scoped
  SCSS `$-[name]`, mixins/functions `o-[name]` (imperative verbs) with
  optional arguments named in scoped form (`@mixin o-avatar($-size: 1.5em)`), CSS variables
  in BEM `--[root]__[element]-[property]--[modifier]`. Don't define CSS variables
  on `:root` (use SCSS for global design; core's few `:root` definitions are
  deliberate utility APIs); CSS variables are for contextual DOM adaptation.
  The variable conventions bind *new* code; much of core (plain mixin
  arguments, `--ComponentName-property` CSS variables) predates them.

# Mobile Responsiveness Best Practices

- **Zero Root Overflow Masking**: Never set `overflow-x: hidden !important` or `overflow: hidden` on root containers (`html`, `body`, `.o_action_manager`, `.o_content`). Isolate horizontal scrolling to dedicated inner containers.
- **Relational Sub-Table Resizing & Horizontal Touch Panning (`.o_field_x2many`)**: To prevent truncated text on small viewports, relational sub-tables (`.o_field_x2many .o_list_renderer`) must enable touch panning (`overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; touch-action: pan-x pan-y !important;`) with `table.o_list_table { min-width: 680px !important; table-layout: auto !important; }` and explicit minimum readable column widths.
- **Compound Form Row (`.o_row`, `.oe_row`) Anti-Stacking**: Avoid blanket `width: 100% !important; display: block !important;` on form inputs. Compound row containers must use `display: inline-flex !important; flex-wrap: wrap !important; align-items: center !important; gap: 0.25rem 0.4rem !important;`, exclude `.o_row` children from 100% width rules, neutralize inner flex growth (`flex: 0 0 auto !important; width: auto !important;`), and constrain numeric input widths (`min-width: 50px; max-width: 90px; text-align: right;`) and unit dropdowns (`min-width: 60px; max-width: 110px;`).
- **Phantom Adaptive Dropdown & Empty Bottom Sheet Suppression**: On mobile control panels, suppress 3-dots adaptive dropdowns when all action buttons are hidden or empty. Globally suppress empty bottom sheets via CSS: `.o_bottom_sheet:empty, .o_bottom_sheet:not(:has(:not(.d-none):not(.o_hidden):not(.visually-hidden))) { display: none !important; visibility: hidden !important; }`.
