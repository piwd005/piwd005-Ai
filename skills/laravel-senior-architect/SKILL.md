---
name: laravel-senior-architect
description: >-
  Super-Senior & Principal Laravel Architect standards for Laravel 10/11 and legacy migrations:
  Eloquent ORM optimization (zero N+1 queries, chunkById, database transactions), Action Classes,
  Form Requests, Service Providers, Job Queues (Redis/Horizon), Event-Listener architecture,
  API security (Sanctum/Passport, Policies, Gates, Rate Limiting), zero-downtime database migrations,
  and refactoring legacy Laravel applications. Use when building or refactoring Laravel projects.
---

# Super-Senior & Principal Laravel Architect Handbook

Architect, build, and refactor enterprise-grade Laravel applications with zero N+1 queries, bulletproof security, scalable queues, and clean domain-driven architecture.

---

## 1. Eloquent ORM Performance & Zero N+1 Queries

### A. Strict Lazy Loading Prevention
In development and staging, enforce zero lazy loading in `AppServiceProvider::boot()`:
```php
public function boot(): void
{
    Model::preventLazyLoading(! app()->isProduction());
    Model::preventSilentlyDiscardingAttributes(! app()->isProduction());
}
```

### B. Eager Loading & Constrained Eager Loading
Never access relationships in a loop without eager loading:
```php
// Bad: N+1 queries
$orders = Order::all();
foreach ($orders as $order) {
    echo $order->customer->name;
}

// Good: 2 queries total
$orders = Order::with(['customer:id,name,email', 'items.product:id,name,price'])
    ->where('status', 'confirmed')
    ->get();
```

### C. Large Dataset Processing: Memory Safety
Never call `Model::all()` or `->get()` on large tables. Use memory-safe chunking:
```php
// Best for mutations (prevents skipping rows when IDs change):
Order::where('status', 'pending')
    ->chunkById(500, function ($orders) {
        foreach ($orders as $order) {
            ProcessOrderAction::execute($order);
        }
    });

// Best for streaming/exporting large datasets without memory blowup:
Order::cursor()->each(function ($order) {
    // Process single record with minimal memory overhead
});
```

---

## 2. Database Transactions & Concurrency Safety

### A. Automatic Retries on Deadlocks
Wrap multi-table financial or inventory updates inside `DB::transaction()`:
```php
DB::transaction(function () use ($orderId, $paymentData) {
    // Pessimistic row locking to prevent race conditions:
    $order = Order::where('id', $orderId)->lockForUpdate()->firstOrFail();
    
    if ($order->status !== 'pending') {
        throw new OrderAlreadyProcessedException();
    }

    $order->update(['status' => 'paid']);
    $order->payments()->create($paymentData);
}, 5); // 5 retry attempts if a deadlock occurs
```

---

## 3. Architecture: Action Classes & Form Requests

Never write 500-line controllers. Use Single-Responsibility Actions:

```text
app/
├── Actions/
│   ├── Orders/
│   │   ├── CreateOrderAction.php
│   │   └── CancelOrderAction.php
├── Http/
│   ├── Controllers/
│   │   └── OrderController.php
│   └── Requests/
│       └── StoreOrderRequest.php
```

### Action Class Pattern:
```php
namespace App\Actions\Orders;

use App\Models\Order;
use App\DTOs\OrderData;
use Illuminate\Support\Facades\DB;

class CreateOrderAction
{
    public function execute(OrderData $data): Order
    {
        return DB::transaction(function () use ($data) {
            $order = Order::create($data->toArray());
            // Fire domain event
            event(new OrderCreated($order));
            return $order;
        });
    }
}
```

---

## 4. Application Security & OWASP Top 10

1. **SQL Injection**:
   - Never pass raw user inputs into `DB::raw()`, `whereRaw()`, or `orderByRaw()`:
     ```php
     // Bad (SQLi):
     User::whereRaw("name = '{$request->name}'")->get();

     // Good:
     User::whereRaw("name = ?", [$request->name])->get();
     ```
2. **XSS Prevention in Blade**:
   - Always use standard `{{ $variable }}` which automatically applies `htmlspecialchars()`.
   - Never use `{!! $variable !!}` unless the HTML has been sanitized with HTMLPurifier.
3. **Mass Assignment Protection**:
   - Never use `$request->all()` in `Model::create()` or `update()`.
   - Always use validated inputs: `$validated = $request->validated();`.
4. **Rate Limiting**:
   - Protect authentication and critical endpoints with custom rate limiters in `RouteServiceProvider`:
     ```php
     RateLimiter::for('api', function (Request $request) {
         return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
     });
     ```

---

## 5. Upgrading & Refactoring Legacy Laravel Apps

1. **Staged Version Upgrades**:
   - Upgrade step-by-step: 6.x → 7.x → 8.x → 9.x → 10.x → 11.x. Never skip major versions in a single jump.
   - Use **Rector** (`vendor/bin/rector process`) for automated syntax modernization.
2. **Safe Migration of Monolithic Blade to Modern APIs**:
   - Wrap legacy database models with API Resources (`JsonResource`) before building mobile (Android) or SPA frontends.
