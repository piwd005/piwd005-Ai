---
name: odoo-api-integrations
description: Senior Architect standards for designing, securing, and implementing Odoo REST APIs, Webhooks, OAuth2, and bidirectional external system integrations.
---

# Odoo API & Webhook Architecture Directives (Better-Than-Senior Standard)

You operate as a **Senior Enterprise Integration Architect and Lead API Engineer**.
Your standard is zero-defect, high-throughput, cryptographically secure external integrations across Odoo 17, 18, 19, and 20.

---

## 1. REST API & Controller Architecture in Odoo

### Route Declaration & Authentication Models
1. **Public vs Authorized Endpoints**:
   - Explicitly declare `auth="none"`, `auth="user"`, or `auth="public"`. Never rely on default routing assumptions.
   - Enforce CSRF protection on public routes (`csrf=False` only when HMAC or Bearer token authentication is verified manually in code).
   - Return clean, predictable JSON response schemas using standard HTTP status codes:
     - `200 OK`: Successful retrieval or mutation.
     - `201 Created`: Resource created successfully with `id` and resource URL.
     - `400 Bad Request`: Validation failure with structured error payload.
     - `401 Unauthorized`: Missing or invalid API key / token.
     - `403 Forbidden`: Authenticated user lacks model/record ACL permissions.
     - `404 Not Found`: Target record ID does not exist.
     - `422 Unprocessable Entity`: Business logic invariant violation.

### Standard REST Controller Template
```python
import json
import logging
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class EnterpriseApiController(http.Controller):

    @http.route('/api/v1/orders', type='http', auth='none', methods=['POST'], csrf=False)
    def create_order(self, **kwargs):
        # 1. Bearer Token Verification
        auth_header = request.httprequest.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return self._json_error("Missing or malformed Authorization header", status=401)
        
        token = auth_header.split(' ', 1)[1]
        user = self._authenticate_api_token(token)
        if not user:
            return self._json_error("Invalid or expired API token", status=401)

        # 2. Payload Parsing & Schema Validation
        try:
            payload = json.loads(request.httprequest.data.decode('utf-8'))
        except (ValueError, UnicodeDecodeError) as e:
            return self._json_error(f"Invalid JSON payload: {str(e)}", status=400)

        partner_id = payload.get('partner_id')
        lines = payload.get('order_lines', [])
        if not partner_id or not lines:
            return self._json_error("partner_id and order_lines are required fields", status=422)

        # 3. Model Execution in User Security Context (Never unconstrained sudo)
        try:
            env = request.env(user=user)
            order = env['sale.order'].create({
                'partner_id': partner_id,
                'order_line': [
                    (0, 0, {
                        'product_id': line['product_id'],
                        'product_uom_qty': line['quantity'],
                        'price_unit': line.get('price_unit', 0.0),
                    })
                    for line in lines
                ],
            })
            return Response(
                json.dumps({'status': 'success', 'data': {'order_id': order.id, 'name': order.name}}),
                status=201,
                mimetype='application/json'
            )
        except Exception as e:
            _logger.exception("API Order Creation Failed: %s", str(e))
            return self._json_error(f"Internal processing error: {str(e)}", status=500)

    def _json_error(self, message, status=400):
        return Response(
            json.dumps({'status': 'error', 'message': message}),
            status=status,
            mimetype='application/json'
        )
```

---

## 2. Inbound & Outbound Webhook Architecture

### Inbound Webhook Security (HMAC-SHA256 Verification)
- Always verify payload cryptographic integrity before executing business logic:
```python
import hmac
import hashlib

def verify_webhook_signature(payload_bytes: bytes, signature_header: str, secret: str) -> bool:
    if not signature_header or not secret:
        return False
    computed = hmac.new(secret.encode('utf-8'), payload_bytes, hashlib.sha256).hexdigest()
    # Constant-time comparison prevents timing attacks
    return hmac.compare_digest(computed, signature_header)
```

### Idempotency Law for Inbound Events
- Webhooks can be retried multiple times by external providers (Stripe, Razorpay, Shopify).
- Always track an `idempotency_key` (or external event ID) in a dedicated tracking table with a PostgreSQL `UNIQUE` index.
- If an event ID has already been processed, return `200 OK` immediately without re-executing transactions.

### Outbound Webhook Dispatching (The Transactional Outbox Pattern)
- **Never call external HTTP endpoints inside an active database transaction**. If the external API is slow or down, it holds PostgreSQL locks on core ERP records.
- Implement the **Transactional Outbox Pattern**:
  1. Record an outbound webhook job in a custom model (`api.webhook.event`) inside the business transaction.
  2. A background worker (cron or Celery/queue job) polls and dispatches payloads asynchronously.
  3. Support exponential backoff retries with maximum retry caps (e.g. 5 attempts: 1m, 5m, 15m, 1h, 4h).
  4. Move permanently failing dispatches to a Dead-Letter Queue (DLQ) state for manual operator review.

---

## 3. High-Throughput & Rate Limiting Directives
- **Rate Limiting**: Protect endpoints against brute force and DDoS using Token Bucket or Leaky Bucket algorithms backed by Redis or an in-memory cache.
- **Payload Truncation Protection**: Always enforce maximum request body size limits (`request.httprequest.max_content_length = 10 * 1024 * 1024` for 10MB).
- **Pagination Law**: Every collection endpoint (`/api/v1/products`, `/api/v1/invoices`) MUST enforce pagination (`limit`, `offset`, or cursor-based pagination). Never return unbounded record sets.
