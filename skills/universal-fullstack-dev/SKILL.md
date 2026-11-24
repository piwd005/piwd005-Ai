---
name: universal-fullstack-dev
description: >-
  Lead Polyglot Developer engineering standards for modern fullstack applications:
  React 19, Next.js (App Router, Server Actions, SSR), TypeScript, TailwindCSS,
  Python (FastAPI, Django, Pydantic v2), Go (Gin, Fiber, goroutines), and Rust (Tokio, Axum).
  Covers clean architecture, async concurrency, zero N+1 queries, defensive null handling,
  and type-safe API communication. Use when authoring or reviewing fullstack application code.
---

# Lead Polyglot Fullstack Developer Handbook

Deliver production-grade, zero-defect code across modern frontend and backend technology stacks.

---

## 1. Frontend Engineering (React 19 & Next.js)

1. **Server vs Client Components**:
   - Default to Server Components (`RSC`) for data fetching, static rendering, and heavy dependencies.
   - Use `'use client'` strictly for interactivity, event listeners, state hooks (`useState`, `useReducer`), and browser APIs.
2. **Zero Hydration Mismatch**:
   - Never render nondeterministic browser data (`window.innerWidth`, `new Date().toLocaleTimeString()`, `localStorage`) directly during initial server render. Use `useEffect` with mounting flags.
3. **Data Mutation with Server Actions**:
   - Validate incoming form data using Zod schemas.
   - Revalidate caches explicitly using `revalidatePath()` or `revalidateTag()`.
4. **Responsive Mobile-First CSS**:
   - Use Tailwind utility classes with standard breakpoints (`sm:`, `md:`, `lg:`, `xl:`).
   - Ensure touch targets are at least 44x44px (`min-h-[44px] min-w-[44px]`).

---

## 2. Modern Backend Engineering (FastAPI & Node.js)

1. **Strict Type Safety & Schema Validation**:
   - In Python, use **Pydantic v2** models for request bodies, query params, and response models.
   - In TypeScript, use **Zod** or **TypeBox** for runtime validation.
2. **Defensive Async ORM & Zero N+1 Queries**:
   - In SQLAlchemy / Prisma / TypeORM, always eagerly load relationships using `joinedload` or `include` to eliminate N+1 database queries.
   - Never run database queries or HTTP calls inside loops. Collect IDs and query with `IN (...)`.
3. **Graceful Error Handling & RFC 7807 Problem Details**:
   - Return structured error responses:
     ```json
     {
       "type": "https://api.example.com/errors/validation-error",
       "title": "Invalid Request Payload",
       "status": 422,
       "detail": "Field 'email' must be a valid email address."
     }
     ```
