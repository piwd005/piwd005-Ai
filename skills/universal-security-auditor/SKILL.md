---
name: universal-security-auditor
description: >-
  Principal Application Security (AppSec) and Cryptography Auditor expertise for
  OWASP Top 10 vulnerabilities, Static Application Security Testing (SAST),
  SQL injection prevention, Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF),
  Server-Side Request Forgery (SSRF), secret leakage prevention, JWT token validation,
  and role-based access control (RBAC). Use when auditing code security or fixing vulnerabilities.
---

# Principal Application Security Auditor Handbook

Enforce zero-trust security architecture, eliminate code vulnerabilities, and guarantee compliance with OWASP Top 10 across all languages.

---

## 1. OWASP Top 10 Prevention Directives

### A01: Broken Access Control
- Always enforce server-side authorization checks on every endpoint. Never rely on frontend UI hiding (`display: none` or conditional rendering).
- Use attribute-based (ABAC) or role-based (RBAC) access guards (e.g. `@require_permission('order:edit')`).

### A02: Cryptographic Failures
- Never store raw passwords or use obsolete hashing algorithms (MD5, SHA1). Use **Argon2id** or **bcrypt** with cost factor $\ge 12$.
- Sensitive data at rest (SSN, credit cards, API secrets) must be encrypted using **AES-256-GCM** or **ChaCha20-Poly1305** with managed keys.
- Enforce TLS 1.3 in transit with HSTS headers.

### A03: Injection (SQL, Command, Template, NoSQL)
- **SQL Injection**: Never interpolate, concatenate (`+`), or use f-strings in SQL execution. Always use parameterized queries (`%s`, `?`, or `$1`).
- **Command Injection**: Never use `os.system()` or `shell=True` in `subprocess`. Always pass commands as token lists (`['git', 'status']`).
- **XSS**: In React/Vue, never use `dangerouslySetInnerHTML` or `v-html` with unsanitized user content. Always sanitize with DOMPurify.

### A04: Insecure Design & Secret Leakage
- Zero hardcoded API keys, JWT secrets, database passwords, or private keys in source code.
- Run `super-dev sec audit .` before committing to detect exposed secrets.
- Use `.env` files added to `.gitignore` and manage secrets via cloud vaults (Vault, AWS Secrets Manager, GCP Secret Manager).

### A05: Security Misconfiguration
- Disable debug mode (`DEBUG = False`) in production.
- Implement strict Content Security Policy (CSP), `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`.
- Implement rate limiting on authentication routes (login, forgot-password) using Redis token-bucket.
