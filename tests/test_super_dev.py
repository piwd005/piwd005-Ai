#!/usr/bin/env python3
"""
Unit tests for the Universal Super-AI Developer Suite (super_engine & super-dev CLI).
"""

import os
import sys
import tempfile
import unittest

# Add plugins/super-dev to sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(repo_root, "plugins", "super-dev"))
import super_engine


class SuperDevEngineTests(unittest.TestCase):
    """Test suite for Universal Super-AI Engine functions."""

    def test_super_doctor_runs_and_reports_status(self):
        """Test that super_doctor() executes cleanly and outputs structured diagnostic sections."""
        report = super_engine.super_doctor()
        self.assertIn("UNIVERSAL SUPER-AI DEVELOPER HEALTH CHECK", report)
        self.assertIn("Python Runtime:", report)
        self.assertIn("AI Engineering Skills:", report)
        self.assertIn("UNIVERSAL STATUS:", report)

    def test_super_sec_audit_detects_eval_and_sqli(self):
        """Test that super_sec_audit() catches dangerous eval() and f-string SQL injection."""
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write("""
def dangerous_func(user_input):
    eval(user_input)
    cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")
""")
            temp_path = f.name

        try:
            audit_result = super_engine.super_sec_audit(temp_path)
            self.assertIn("Code Injection", audit_result)
            self.assertIn("SQL Injection", audit_result)
            self.assertIn("⛔ SECURITY VERDICT: ACTION REQUIRED", audit_result)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_super_sec_audit_passes_clean_code(self):
        """Test that super_sec_audit() returns 0 vulnerabilities on safe code."""
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write("""
def safe_func(cursor, user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
    return True
""")
            temp_path = f.name

        try:
            audit_result = super_engine.super_sec_audit(temp_path)
            self.assertIn("✅ SECURITY VERDICT: 0 VULNERABILITIES DETECTED", audit_result)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_super_blueprint_generates_mermaid_and_matrix(self):
        """Test that super_blueprint() generates valid Mermaid diagrams and API matrices."""
        bp = super_engine.super_blueprint("OrderService", blueprint_type="microservice", stack="FastAPI + PostgreSQL")
        self.assertIn("graph TD", bp)
        self.assertIn("erDiagram", bp)
        self.assertIn("stateDiagram-v2", bp)
        self.assertIn("/api/v1/orderservice", bp)
        self.assertIn("Idempotency Keys", bp)

    def test_super_api_test_handles_connection_error_gracefully(self):
        """Test that super_api_test() returns graceful error message on unreachable endpoint."""
        result = super_engine.super_api_test("http://127.0.0.1:59999/unreachable-test")
        self.assertIn("API Request Failed", result)

    def test_super_sec_audit_detects_php_vulnerabilities(self):
        """Test that super_sec_audit() detects CodeIgniter and Laravel SQL injection and unescaped Blade."""
        with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False) as f:
            f.write("""<?php
// Vulnerable CodeIgniter Query
$this->db->query("SELECT * FROM users WHERE email = '$email'");

// Vulnerable Laravel Query
User::whereRaw("status = '$status'")->get();

// Insecure Deserialization
$data = unserialize($userInput);
""")
            temp_path = f.name

        try:
            audit_result = super_engine.super_sec_audit(temp_path)
            self.assertIn("CodeIgniter SQL Injection", audit_result)
            self.assertIn("Laravel SQL Injection", audit_result)
            self.assertIn("Insecure PHP Deserialization", audit_result)
            self.assertIn("⛔ SECURITY VERDICT: ACTION REQUIRED", audit_result)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_super_php_scaffold_generates_laravel_and_ci(self):
        """Test that super_php_scaffold() generates valid Laravel and CodeIgniter templates."""
        laravel_action = super_engine.super_php_scaffold("laravel", "action", "CreateInvoice")
        self.assertIn("class CreateInvoiceAction", laravel_action)
        self.assertIn("DB::transaction", laravel_action)

        ci_service = super_engine.super_php_scaffold("ci3", "service", "Invoice")
        self.assertIn("class Invoice_service", ci_service)
        self.assertIn("$this->CI->db->trans_start()", ci_service)

    def test_odoo_generate_tests_produces_transaction_case(self):
        """Test that odoo_generate_tests() parses model and outputs production TransactionCase test."""
        sys.path.insert(0, os.path.join(repo_root, "plugins", "odoo-dev"))
        import mcp_server

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write("""
from odoo import models, fields

class TestOrder(models.Model):
    _name = 'test.order'
    _description = 'Test Order Model'

    name = fields.Char(string='Name', required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done')], default='draft')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'
""")
            temp_model = f.name

        out_test = temp_model.replace(".py", "_test.py")
        try:
            result = mcp_server.odoo_generate_tests(temp_model, out_test)
            self.assertIn("✓ Production-grade test suite generated successfully", result)
            self.assertTrue(os.path.exists(out_test))
            with open(out_test, "r") as tf:
                content = tf.read()
            self.assertIn("class TestTestOrder(TransactionCase):", content)
            self.assertIn("def test_01_lifecycle_flow(self):", content)
            self.assertIn("action_confirm()", content)
        finally:
            if os.path.exists(temp_model):
                os.remove(temp_model)
            if os.path.exists(out_test):
                os.remove(out_test)


if __name__ == "__main__":
    unittest.main()
