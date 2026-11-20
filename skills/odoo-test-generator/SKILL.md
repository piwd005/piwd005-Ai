---
name: odoo-test-generator
description: >-
  Generate comprehensive, production-grade test suites for Odoo addons:
  backend unit and integration tests (TransactionCase), tour and HTTP endpoint
  tests (HttpCase), and modern frontend OWL unit tests (Hoot framework).
  Use when writing, improving, or generating tests for Odoo modules.
---

# Odoo Automated Test Suite Generator

Generate robust automated tests for Odoo addons across Python backend logic and frontend OWL components.

## 1. Backend Business Logic (`TransactionCase`)

Place in `my_addon/tests/test_model.py`. Remember to import all test files in `my_addon/tests/__init__.py`.

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, AccessError

class TestMyModel(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Master test data
        cls.company = cls.env.company
        cls.partner = cls.env['res.partner'].create({
            'name': 'Acme Corp',
            'email': 'acme@example.com',
            'is_company': True,
        })
        cls.user_restricted = cls.env['res.users'].create({
            'name': 'Test Restricted User',
            'login': 'restricted_user',
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])],
        })
        cls.record = cls.env['my.model'].create({
            'name': 'Test Record 1',
            'partner_id': cls.partner.id,
        })

    def test_state_flow(self):
        """Verify normal workflow state transitions."""
        self.assertEqual(self.record.state, 'draft')
        self.record.action_confirm()
        self.assertEqual(self.record.state, 'confirmed')
        self.record.action_done()
        self.assertEqual(self.record.state, 'done')

    def test_validation_constraints(self):
        """Ensure invalid field values trigger ValidationError."""
        with self.assertRaises(ValidationError):
            self.record.write({'amount': -50.0})

    def test_access_rights(self):
        """Verify record security permissions for non-manager users."""
        with self.assertRaises(AccessError):
            self.record.with_user(self.user_restricted).unlink()
```

## 2. HTTP & Web Controller Tests (`HttpCase`)

Place in `my_addon/tests/test_controllers.py`:

```python
import json
from odoo.tests.common import HttpCase

class TestMyController(HttpCase):

    def test_public_endpoint(self):
        """Test public API or web endpoint."""
        response = self.url_open('/my_addon/public_endpoint')
        self.assertEqual(response.status_code, 200)

    def test_authenticated_jsonrpc(self):
        """Test JSON-RPC controller endpoint."""
        self.authenticate('admin', 'admin')
        payload = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'filter': 'active',
            },
            'id': 1,
        }
        response = self.url_open(
            '/my_addon/api/get_data',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertNotIn('error', data)
        self.assertIn('result', data)
```

## 3. Frontend OWL Tests (Hoot Framework - Odoo 18, 19, 20)

Place in `my_addon/static/tests/my_custom_widget.test.js`:

```javascript
import { describe, expect, test } from "@odoo/hoot";
import { mountWithCleanup } from "@web/../tests/web_test_helpers";
import { MyCustomWidget } from "@my_addon/js/my_custom_widget";

describe("MyCustomWidget", () => {
    test("renders widget title and button", async () => {
        const fixture = await mountWithCleanup(MyCustomWidget, {
            props: { title: "Test Dashboard" },
        });

        expect(fixture.querySelector("h4")).toHaveText("Test Dashboard");
        expect(fixture.querySelector("button")).toHaveCount(1);
    });
});
```

## 4. Running the Tests via CLI

```bash
# Run all tests for a specific addon
odoo-bin -c odoo.conf -d test_db -u my_addon --test-enable --stop-after-init

# Run only a specific test class
odoo-bin -c odoo.conf -d test_db --test-enable --test-tags /my_addon:TestMyModel --stop-after-init
```
