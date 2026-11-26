---
name: frontend-developer
description: >-
  Lead Frontend and Web Component Developer standards: modern reactive architecture
  (React 19 / Next.js, Odoo OWL 2.0), TypeScript, Web APIs, Core Web Vitals optimization
  (LCP, INP, CLS), state management, DOM isolation, and defensive client engineering.
  Use when building client-side components, optimizing frontend performance, or debugging UI reactivity.
---

# Lead Frontend & Reactive Web Component Developer Guide

Architect, build, and optimize high-performance, accessible, production-grade frontend interfaces across modern JavaScript/TypeScript and enterprise reactive web frameworks.

---

## 1. Modern Component Architecture & Framework Standards

### A. React 19 & Next.js App Router
1. **Server vs. Client Boundary Isolation**:
   - Keep components as **Server Components (`RSC`)** by default for direct database/API fetching, zero client bundle weight, and security isolation.
   - Introduce `'use client'` strictly at the leaf level where client state (`useState`, `useReducer`), browser events, or browser APIs (`window`, `localStorage`) are required.
2. **Streaming SSR & Suspense**:
   - Wrap dynamic data fetches in `<Suspense fallback={<Skeleton />}>` to avoid blocking page paint.
3. **Server Actions with Optimistic UI**:
   - Use `useOptimistic` and `useActionState` to deliver instantaneous UI updates before server confirmation.

### B. Odoo OWL 2.0 Component Engineering
1. **Service Consumption**:
   - Always inject core services using `useService`:
     ```javascript
     this.orm = useService("orm");
     this.action = useService("action");
     this.notification = useService("notification");
     ```
2. **Defensive Field Widget Architecture**:
   - Implement custom field widgets using `standardFieldProps`:
     ```javascript
     export class CustomStatusWidget extends Component {
         static template = "my_addon.CustomStatusWidget";
         static props = { ...standardFieldProps };
     }
     ```
3. **Relational Record ID Sanitization (`extractId`)**:
   - In Odoo 19/20, relational fields passed to OWL can arrive as integers, objects (`{id, displayName}`), or tuples `[id, name]`. Always normalize IDs before issuing RPC calls:
     ```javascript
     export function extractId(val) {
         if (!val) return false;
         if (typeof val === "object") return val.id ?? val[0] ?? false;
         return typeof val === "number" ? val : parseInt(val, 10);
     }
     ```

---

## 2. Core Web Vitals & Performance Engineering

Target 100% green Core Web Vitals on real mobile devices:

1. **Largest Contentful Paint (LCP < 2.5s)**:
   - Preload primary LCP assets (hero images, critical fonts) using `<link rel="preload" as="image" ...>`.
   - Never lazy-load the above-the-fold hero image (`loading="eager" fetchpriority="high"`).
2. **Interaction to Next Paint (INP < 200ms)**:
   - Break long tasks ($> 50\text{ms}$) using `scheduler.yield()` or `setTimeout(..., 0)`.
   - Never execute heavy synchronous operations or large array transformations inside click or keypress handlers.
3. **Cumulative Layout Shift (CLS < 0.1)**:
   - Always declare explicit `width` and `height` (or CSS `aspect-ratio`) on all images, icons, and video containers.
   - Reserve space for dynamic content, banners, and modals using skeleton placeholders.
   - Use CSS `contain: layout paint` on complex independent widgets.

---

## 3. Eliminating Layout Thrashing & Memory Leaks

1. **Batching DOM Reads and Writes**:
   - **Never** interleave DOM reads (`offsetHeight`, `getBoundingClientRect()`, `scrollTop`) with DOM writes (`style.width = ...`, `classList.add()`).
   - Read all layout properties first, then batch all DOM mutations in the next `requestAnimationFrame()` frame.
2. **Passive Event Listeners**:
   - Attach scroll and touch listeners with `{ passive: true }` to guarantee non-blocking compositor threads:
     ```javascript
     window.addEventListener("scroll", onScroll, { passive: true });
     ```
3. **Clean Component Teardown**:
   - Always disconnect `ResizeObserver`, `IntersectionObserver`, and remove window event listeners inside component cleanup hooks (`onWillUnmount` in OWL, cleanup return in React `useEffect`).

---

## 4. Mobile WebView Resilient File & Report Downloads

When serving PDF, CSV, or binary reports to embedded WebViews (Android WebView, iOS WKWebView, Flutter in-app webviews):

- **The Problem**: Standard browser XHR downloads generate in-memory `blob:` URLs (`URL.createObjectURL(blob)`). Native mobile WebView listeners crash when parsing `blob:` schemes (`Bad state: Origin is only applicable schemes http and https: blob:...`).
- **The Universal Pattern**:
  ```javascript
  export function downloadReportMobileSafe(url, data) {
      const isMobileWebView = /Android|iPhone|iPad|Mobile/i.test(navigator.userAgent) || window.flutter_inappwebview;
      if (isMobileWebView) {
          // Bypass blob generation: submit hidden POST form directly to endpoint
          const form = document.createElement("form");
          form.method = "POST";
          form.action = url;
          form.style.display = "none";
          
          const csrfInput = document.createElement("input");
          csrfInput.type = "hidden";
          csrfInput.name = "csrf_token";
          csrfInput.value = odoo.csrf_token || "";
          form.appendChild(csrfInput);

          const dataInput = document.createElement("input");
          dataInput.type = "hidden";
          dataInput.name = "data";
          dataInput.value = JSON.stringify(data);
          form.appendChild(dataInput);

          document.body.appendChild(form);
          form.submit();
          setTimeout(() => document.body.removeChild(form), 1000);
      } else {
          // Standard desktop blob download
          standardDownload(url, data);
      }
  }
  ```

---

## 5. Automated Frontend Testing

1. **Odoo OWL Hoot Tests (`@odoo/hoot`)**:
   - Write unit tests under `static/tests/` verifying mounting, reactivity, and user interaction.
2. **Component Isolation Testing**:
   - Assert accessibility compliance (`axe-core`), keyboard focus states, and zero console errors.
