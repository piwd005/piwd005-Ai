---
name: codeigniter-senior-dev
description: >-
  Super-Senior CodeIgniter (CI3 & CI4) Developer expertise for maintaining, securing,
  and modernizing legacy CodeIgniter applications: Query Builder security, SQL injection
  elimination, CSRF & XSS protection, database session management, HMVC modular architecture,
  Service-Repository refactoring, RESTful API design, and migrating from CodeIgniter 3 to 4.
  Use when maintaining, debugging, or modernizing CodeIgniter projects.
---

# Super-Senior CodeIgniter Developer Handbook (CI3 & CI4)

Maintain, secure, and modernize CodeIgniter applications, eliminate legacy security vulnerabilities, and build high-performance APIs.

---

## 1. Query Security & SQL Injection Elimination

Legacy CodeIgniter apps frequently suffer from raw SQL concatenation. Eliminate SQL injection strictly:

### A. CodeIgniter 3 Query Builder & Parameter Binding
```php
// Bad: Vulnerable to SQL Injection
$query = $this->db->query("SELECT * FROM users WHERE email = '" . $email . "'");

// Good: Query Bindings (Auto-escaped)
$sql = "SELECT * FROM users WHERE email = ? AND status = ?";
$query = $this->db->query($sql, array($email, 'active'));

// Good: Query Builder (Auto-escaped & sanitized)
$query = $this->db->get_where('users', array('email' => $email, 'status' => 'active'));
```

### B. CodeIgniter 4 Model & Query Builder
```php
// Good: CI4 Model with Parameterized Query
$userModel = new \App\Models\UserModel();
$user = $userModel->where('email', $email)
                  ->where('status', 'active')
                  ->first();
```

---

## 2. Hardening Legacy CodeIgniter 3 Applications

1. **Global CSRF Protection**:
   - In `application/config/config.php`, ensure CSRF protection is strictly enabled:
     ```php
     $config['csrf_protection'] = TRUE;
     $config['csrf_token_name'] = 'csrf_token_name';
     $config['csrf_cookie_name'] = 'csrf_cookie_name';
     $config['csrf_expire'] = 7200;
     $config['csrf_regenerate'] = TRUE;
     ```
   - In AJAX requests, always send the CSRF token in headers or form data.
2. **Database-Backed Sessions**:
   - Never use file-based sessions in production clusters. In `application/config/config.php`:
     ```php
     $config['sess_driver'] = 'database';
     $config['sess_save_path'] = 'ci_sessions';
     $config['sess_match_ip'] = TRUE;
     $config['sess_time_to_update'] = 300;
     ```
3. **Form Validation & Input Sanitization**:
   - Always run input through the Form Validation library before database queries:
     ```php
     $this->load->library('form_validation');
     $this->form_validation->set_rules('email', 'Email', 'required|valid_email|trim');
     if ($this->form_validation->run() == FALSE) {
         // Return validation errors
     }
     ```
   - Avoid legacy `$this->input->post('field', TRUE)` as a substitute for validation (XSS filtering is not data validation).

---

## 3. Refactoring Spaghetti CI3 into Modern Architecture

Break bloated 1000-line controllers into clean layers:

```text
application/
├── controllers/      # Thin controllers: request parsing & response rendering only
├── models/           # Data access: direct table operations
├── services/         # Business logic: transactions, validation, calculation
└── repositories/     # Complex queries & caching
```

### Controller Refactoring Pattern:
```php
class Order_controller extends CI_Controller {
    public function __construct() {
        parent::__construct();
        $this->load->service('order_service');
    }

    public function create() {
        if (! $this->validate_request()) {
            return $this->output_json(array('error' => validation_errors()), 422);
        }

        try {
            $order = $this->order_service->create_order($this->input->post());
            return $this->output_json(array('success' => true, 'order_id' => $order->id));
        } catch (Exception $e) {
            return $this->output_json(array('error' => $e->getMessage()), 500);
        }
    }
}
```

---

## 4. CodeIgniter 3 to CodeIgniter 4 Migration Pathway

1. **Step 1: PHP Version Upgrade**: Ensure codebase runs cleanly on PHP 8.1 / 8.2 with all deprecation notices fixed.
2. **Step 2: Namespace & Directory Reorganization**: Move from `application/controllers` to PSR-4 `app/Controllers`.
3. **Step 3: Database Models**: Convert CI3 `CI_Model` to CI4 `CodeIgniter\Model` with `$allowedFields` and built-in validation.
4. **Step 4: Routing**: Replace URI-segment auto-routing with explicit routes in `app/Config/Routes.php` to prevent unauthorized method calls.
