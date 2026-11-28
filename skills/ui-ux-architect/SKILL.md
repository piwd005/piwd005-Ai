---
name: ui-ux-architect
description: >-
  Principal UI/UX Architect and Design Systems Lead standards: design tokens,
  semantic color systems, typographic scales, component state machines, visual hierarchy,
  cognitive ergonomics, and WCAG 2.2 AAA accessibility compliance. Use when designing
  user interfaces, establishing design systems, structuring user flows, or auditing UI/UX.
---

# Principal UI/UX Architect & Design Systems Guide

Architect production-grade, human-centered, accessible user interfaces and design systems across enterprise web and mobile applications.

---

## 1. Design Token Architecture & Scalable Theming

Every robust design system must be founded on atomic, decoupled design tokens rather than hardcoded magic values:

1. **Primitive Tokens**:
   - Define raw palette values:
     - Color primitives: Neutral palette (`slate-50` to `slate-950`), brand primaries, and status accents (`emerald`, `amber`, `rose`, `sky`).
     - Base unit: Strict 4px/8px grid system (`0.25rem`, `0.5rem`, `0.75rem`, `1rem`, `1.5rem`, `2rem`, `3rem`).
     - Radii primitives: `sm: 4px`, `md: 8px`, `lg: 12px`, `xl: 16px`, `full: 9999px`.
2. **Semantic / Intent Tokens**:
   - Map primitives to context-independent intent:
     - Surfaces: `bg-surface-canvas`, `bg-surface-elevated`, `bg-surface-sunken`, `bg-surface-overlay`.
     - Typography: `text-primary`, `text-secondary`, `text-muted`, `text-on-accent`.
     - Borders: `border-subtle`, `border-strong`, `border-focus`.
     - Status: `status-info`, `status-success`, `status-warning`, `status-danger`.
3. **Dark / Light Mode Consistency**:
   - Define color tokens as CSS custom properties (`--color-surface-canvas`, etc.).
   - Switch themes by swapping CSS variables at the container or root level without altering component utility classes.

---

## 2. Visual Hierarchy & Cognitive Ergonomics

1. **Visual Scanning Patterns**:
   - Design for standard eye-tracking patterns: **F-pattern** for dense data/list views, **Z-pattern** for landing pages and high-impact cards.
   - Anchor primary calls-to-action (CTA) along natural fixation paths.
2. **Typographic Rhythm & Scale**:
   - Maintain a mathematical type scale (Major Third 1.25 or Perfect Fourth 1.333):
     - Display: `32px` - `40px` (Weight 700, Line-height 1.15)
     - H1 / Page Header: `24px` - `28px` (Weight 700, Line-height 1.25)
     - H2 / Section Header: `18px` - `20px` (Weight 600, Line-height 1.35)
     - Body Text: `14px` - `16px` (Weight 400, Line-height 1.5)
     - Caption / Meta: `11px` - `12px` (Weight 500, Line-height 1.4)
3. **Intentional Whitespace**:
   - Group related elements closely (Law of Proximity). Separate distinct functional blocks by $\ge 2\times$ the internal element spacing.

---

## 3. The 9-Stage Component State Machine

Never deliver a UI component that only handles the ideal "sunny day" scenario. Every component, form, and widget must explicitly handle all 9 lifecycle states:

1. **Default (Resting)**: Clean, balanced presentation with clear visual affordance.
2. **Hover**: Subtle elevation or background tint ($\approx 5-10\%$ contrast delta) to indicate interactability.
3. **Active / Pressed**: Scaled slightly down (`transform: scale(0.98)`) or deeper contrast indicating tactile engagement.
4. **Focus-Visible**: Distinct, high-contrast outline (`2px solid var(--focus-ring)`, `outline-offset: 2px`) for keyboard accessibility. Never suppress `outline` without custom focus styling.
5. **Disabled**: Reduced opacity ($40-50\%$), `cursor: not-allowed`, `pointer-events: none`, `aria-disabled="true"`.
6. **Loading Skeleton**: Shimmer pulse animation matching the exact geometry of expected content. Avoid abrupt page shifts when data arrives.
7. **Empty State**: Friendly illustration/icon, clear description explaining *why* it is empty, and a primary action button encouraging content creation.
8. **Error State**: Non-aggressive visual cues (red border, exclamation icon), human-readable error text explaining the issue, and an actionable retry button.
9. **Success / Completed State**: Transient confirmation feedback (toast, green badge, checkmark animation) confirming successful submission.

---

## 4. WCAG 2.2 AAA Accessibility Standards

1. **Color Contrast Ratios**:
   - Normal text ($< 18\text{px}$ or non-bold): Strictly $\ge 4.5:1$ against background.
   - Large text ($\ge 18\text{px}$ bold or $\ge 24\text{px}$ normal): Strictly $\ge 3.0:1$.
   - Interactive elements and graphical borders: Strictly $\ge 3.0:1$.
2. **Keyboard Navigation & Tab Order**:
   - Every interactive control must be reachable via `Tab` / `Shift+Tab`.
   - Modals and drawers must implement **focus trapping** while open, and restore focus to the triggering element upon close.
3. **Semantic HTML & Screen Reader Semantics**:
   - Use native HTML elements (`<button>`, `<dialog>`, `<nav>`, `<main>`, `<aside>`) over generic `<div>` with `onClick`.
   - Provide explicit `aria-label` or `aria-labelledby` for icon-only buttons.
   - Use `aria-expanded`, `aria-haspopup`, and `aria-controls` for dropdowns, accordions, and collapsibles.
4. **Motion Safety**:
   - Wrap transitions in `@media (prefers-reduced-motion: reduce)`:
     ```css
     @media (prefers-reduced-motion: reduce) {
       *, *::before, *::after {
         animation-duration: 0.01ms !important;
         animation-iteration-count: 1 !important;
         transition-duration: 0.01ms !important;
         scroll-behavior: auto !important;
       }
     }
     ```

---

## 5. Micro-Interactions & Perceived Performance

1. **Transition Timing Curves**:
   - Enter transitions: Ease-out (`cubic-bezier(0.0, 0.0, 0.2, 1)`) for swift appearance ($150\text{ms}-200\text{ms}$).
   - Exit transitions: Ease-in (`cubic-bezier(0.4, 0.0, 1, 1)`) for swift dismissal ($100\text{ms}-150\text{ms}$).
2. **Optimistic Feedback**:
   - When a user performs an action (e.g. toggles a favorite, likes a post, or changes a status), immediately reflect the change in the UI before waiting for the network round-trip. Revert gracefully with an error toast only if the server rejects the mutation.

---

## 6. The Turn 1 360° Interactive Journey Verification Checklist

Never conclude an interface task merely because the DOM loaded without errors. Actively verify the complete user journey:
1. **Relational AutoComplete Dropdown Parity**:
   - AutoComplete and Many2one fields must render inline floating dropdowns.
   - Never pop up a full-screen search dialog unless "Search More..." is explicitly clicked.
2. **Modal Wizard Footer Multi-Button Parity**:
   - Dialog footer actions must wrap gracefully without clipping any buttons on mobile.
   - Desktop button count must equal mobile button count.
3. **Sticky Sub-Table Add Row Pinning**:
   - Action rows ("Add a line") on horizontal scrolling tables must be pinned to `left: 0` so they are immediately reachable without scrolling across columns.
4. **Touch & Mouse Pointer Parity**:
   - All interactive draggable badges and canvases must support both touch and mouse events (`pointerdown`, `pointermove`, `pointerup`).
   - Coordinate canvases must include accessible Zoom In, Zoom Out, and Fit-to-Width controls.
5. **Swipe Bleed Isolation**:
   - Prevent horizontal swipe gestures within inner widgets from triggering accidental tab bar transitions.
6. **Phantom Trigger Suppression**:
   - Suppress empty adaptive 3-dots menus and empty bottom sheets when all actions are hidden.

