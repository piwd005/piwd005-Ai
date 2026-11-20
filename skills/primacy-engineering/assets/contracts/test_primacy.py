"""Explicit PRIMACY_SOURCE_ROOT required; extracts reviewed methods, never imports Odoo."""
import ast
import hashlib
import hmac
import json
import os
import re
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

ROOT = Path(os.environ['PRIMACY_SOURCE_ROOT']).resolve()
BINDINGS = json.loads(Path(__file__).with_name('primacy-bindings.json').read_text())


def extract(path, names, namespace):
    data = (ROOT / path).read_bytes()
    if hashlib.sha256(data).hexdigest() != BINDINGS['sha256'][path]:
        raise ValueError('Source drift: review and re-pin ' + path)
    tree = ast.parse(data)
    methods = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name in names]
    if {node.name for node in methods} != set(names):
        raise ValueError('Missing reviewed method')
    for node in methods:
        node.decorator_list = []
    exec(compile(ast.Module(body=methods, type_ignores=[]), path, 'exec'), namespace)  # noqa: S102 -- reviewed hash-pinned methods only
    return namespace


class PrimacyContracts(unittest.TestCase):
    def setUp(self):
        ns = extract('pi_erp_agentic_ai/models/ai_execution.py',
                     ['canonical_plan', 'hash_plan', 'confirmation_token', 'verify_confirmation'],
                     {'json': json, 'hashlib': hashlib, 'hmac': hmac, 'fields': NS(Datetime=NS(now=lambda: 100))})
        cls = type('ExecutionFixture', (), {key: value for key, value in ns.items() if callable(value)})
        self.record = cls()
        r = self.record
        r.id, r.user_id, r.company_id = 7, NS(id=2), NS(id=3)
        config = NS(sudo=lambda: config, get_param=lambda *args: 'synthetic-db')
        class Env(dict):
            pass
        r.env = Env({'ir.config_parameter': config})
        r.env.user, r.env.company, r.env.cr = r.user_id, r.company_id, NS(dbname='fixture')
        r.database_uuid, r.confirmation_nonce = 'synthetic-db', 'fixture-nonce'
        r.status, r.confirmation_expires_at = 'pending_confirmation', 101
        r.ensure_one = lambda: None
        r._signing_key = lambda: b'synthetic-memory-only-key'
        r.plan_hash = r.hash_plan({'quantity': 2, 'record': 11})

    def test_canonical_hash_and_argument_binding(self):
        r = self.record
        self.assertEqual(r.hash_plan({'b': 2, 'a': 1}), r.hash_plan({'a': 1, 'b': 2}))
        token = r.confirmation_token()
        self.assertTrue(r.verify_confirmation(token))
        r.plan_hash = r.hash_plan({'quantity': 3, 'record': 11})
        self.assertFalse(r.verify_confirmation(token))

    def test_confirmation_denials(self):
        r = self.record
        token = r.confirmation_token()
        for attr, value in [('user_id', NS(id=99)), ('company_id', NS(id=99)),
                            ('database_uuid', 'other'), ('status', 'completed'),
                            ('status', 'cancelled'), ('confirmation_expires_at', 100),
                            ('confirmation_nonce', 'replaced')]:
            with self.subTest(attr=attr, value=value):
                old = getattr(r, attr)
                setattr(r, attr, value)
                self.assertFalse(r.verify_confirmation(token))
                setattr(r, attr, old)
        for invalid in [None, '', token + '0', 'forged']:
            self.assertFalse(r.verify_confirmation(invalid))

    def test_controller_rejects_tampered_plan_stale_snapshot_and_cancel(self):
        ns = extract('pi_erp_agentic_ai/controllers/chat.py', ['_execute_confirmation'], {'json': json})
        controller = NS(_snapshot_is_current=lambda snapshot: False)
        r = self.record
        r.plan_json = json.dumps({'quantity': 99})
        token = r.confirmation_token()
        execute = ns['_execute_confirmation']
        self.assertIn('integrity', execute(controller, r, token)['reply'])
        r.plan_json = json.dumps({'quantity': 2, 'record': 11})
        r.snapshot_json = '{}'
        r.sudo = lambda: r
        def write(values):
            for name, value in values.items():
                setattr(r, name, value)
        r.write = write
        r.public_result = lambda: {'status': r.status}
        self.assertFalse(execute(controller, r, token)['ok'])
        self.assertEqual(r.status, 'failed')
        self.assertIn('changed after preview', r.error)
        self.assertFalse(execute(controller, r, token)['ok'])
        r.status = 'pending_confirmation'
        self.assertTrue(execute(controller, r, token, cancel=True)['ok'])
        self.assertEqual(r.status, 'cancelled')
        self.assertFalse(execute(controller, r, token)['ok'])

    def test_functional_guidance_and_denied_scope(self):
        ns = extract('pi_erp_agentic_ai/models/ai_functional_engine.py',
                     ['_is_guidance_question', '_functional_guide'], {'re': re})
        cls = type('GuideFixture', (), {k: v for k, v in ns.items() if callable(v)})
        guide = cls()
        class Env(dict):
            def ref(self, *args, **kwargs):
                return None
        guide.env = Env({key: NS(has_access=lambda mode: True) for key in ['stock.picking', 'mrp.production']})
        quality = extract('scripts/evaluate_odoo_workflow_guidance.py', ['quality'], {'re': re})['quality']
        for kind, prompt in [('inventory', 'How do I process an inventory transfer?'),
                             ('manufacturing', 'How do I complete a manufacturing order?')]:
            with self.subTest(kind=kind):
                reply = guide._functional_guide(prompt)['reply']
                self.assertTrue(all(quality(kind, reply).values()), quality(kind, reply))
                denied = guide._functional_guide(prompt, allowed_models=[])['reply']
                self.assertIn('outside the configured scope', denied)
        guide.env['stock.picking'] = NS(has_access=lambda mode: False)
        self.assertIn('permissions', guide._functional_guide('How do I process an inventory transfer?')['reply'])
        self.assertIsNone(guide._functional_guide('Delete this transfer'))


if __name__ == '__main__':
    unittest.main()
