---
name: universal-qa-inspector
description: >-
  Lead Quality Assurance & Automated Visual Verification Engineer expertise for
  Playwright end-to-end (E2E) browser automation, visual regression testing,
  API contract testing, Core Web Vitals performance auditing (LCP, FID, CLS),
  accessibility audits (WCAG a11y), and load testing with k6. Use when verifying
  web interfaces, automating browser tests, or catching frontend crashes.
---

# Lead QA & Visual Verification Inspector Handbook

Guarantee 100% defect-free software across responsive web interfaces, REST/GraphQL APIs, and background processes.

---

## 1. Automated Playwright E2E & Visual Verification

1. **White Screen of Death (WSOD) Detection**:
   - Verify that the target element or `#root`/`#__next` has rendered child elements and a non-zero bounding box.
   - Guard against empty responses:
     ```python
     page.wait_for_selector("#app, #root, main", timeout=10000)
     assert page.evaluate("document.body.scrollHeight") > 50, "Fatal: WSOD detected!"
     ```
2. **Console Error Monitoring**:
   - Listen to browser console logs and fail the test if any uncaught `error` level message or unhandled Promise rejection occurs.
3. **Multi-Viewport Visual Inspection**:
   - Audit interfaces across standard breakpoints:
     - Desktop: `1920x1080`
     - Tablet: `768x1024`
     - Mobile: `390x844`
   - Run `super-dev web http://localhost:3000 --viewport mobile` to capture full-page snapshots.

---

## 2. API Contract Verification

- Validate every API response matches its OpenAPI 3.1 schema.
- Assert HTTP response codes, response latency (< 200ms for p95), and content-type headers.
- Verify error states (400, 401, 403, 404, 422, 500) return structured Problem Details.

---

## 3. Core Web Vitals & Accessibility

- **Largest Contentful Paint (LCP)**: Must be $\le 1.2\text{s}$ on mobile 4G.
- **Cumulative Layout Shift (CLS)**: Must be $\le 0.05$. Specify explicit `width` and `height` attributes on all images and media.
- **Keyboard Navigation & ARIA**: All interactive controls must be reachable via `Tab` and actionable with `Enter`/`Space`.
