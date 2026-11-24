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


if __name__ == "__main__":
    unittest.main()
