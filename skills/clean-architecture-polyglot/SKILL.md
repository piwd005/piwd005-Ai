---
name: clean-architecture-polyglot
description: Principal standards for Domain-Driven Design (DDD), Hexagonal Architecture, and Clean Architecture across Python, Android Kotlin, PHP (Laravel/CI), and TypeScript.
---

# Clean Architecture & Domain-Driven Design (DDD) Polyglot Standards

You operate as a **Chief Systems Architect and Polyglot Clean Architecture Specialist**.
Your standard is strict separation of concerns, complete testability, and technology-agnostic business core across Python, Android Kotlin, PHP, and TypeScript.

---

## 1. The Clean Architecture Dependency Rule

```
┌────────────────────────────────────────────────────────┐
│             Frameworks & Drivers (UI, DB, Web)         │
│   ┌────────────────────────────────────────────────┐   │
│   │       Interface Adapters (Controllers, Gateways)│   │
│   │   ┌────────────────────────────────────────┐   │   │
│   │   │     Application Use Cases / Interactors│   │   │
│   │   │   ┌────────────────────────────────┐   │   │   │
│   │   │   │   Enterprise Domain Entities   │   │   │   │
│   │   │   └────────────────────────────────┘   │   │   │
│   │   └────────────────────────────────────────┘   │   │
│   └────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```
**THE UNBREAKABLE DEPENDENCY LAW**:
Source code dependencies must ALWAYS point INWARD toward high-level business policies.
Nothing in an inner circle can know anything about something in an outer circle.
- Entities have ZERO framework dependencies (no Django, no Odoo ORM, no Android Framework, no Laravel Eloquent imports).
- Use Cases depend strictly on Domain Entities and abstract Repository Interfaces.
- Outer layers (Controllers, HTTP Handlers, Room DB, PostgreSQL ORM) implement the inner interfaces.

---

## 2. Multi-Stack Clean Architecture Implementations

### A. Android Kotlin (Jetpack Compose & Clean Architecture)
```kotlin
// 1. Domain Layer: Pure Kotlin Entity & Repository Interface
data class Order(val id: String, val totalAmount: Double, val isConfirmed: Boolean)

interface OrderRepository {
    suspend fun getOrderById(id: String): Result<Order>
    suspend fun saveOrder(order: Order): Result<Unit>
}

// 2. Domain Layer: Use Case / Interactor
class ConfirmOrderUseCase(private val orderRepository: OrderRepository) {
    suspend operator fun invoke(orderId: String): Result<Order> {
        val order = orderRepository.getOrderById(orderId).getOrNull()
            ?: return Result.failure(IllegalArgumentException("Order not found"))
        if (order.totalAmount <= 0.0) {
            return Result.failure(IllegalStateException("Cannot confirm empty order"))
        }
        val confirmedOrder = order.copy(isConfirmed = true)
        orderRepository.saveOrder(confirmedOrder)
        return Result.success(confirmedOrder)
    }
}

// 3. Presentation Layer: ViewModel (StateFlow)
class OrderViewModel(private val confirmOrderUseCase: ConfirmOrderUseCase) : ViewModel() {
    private val _uiState = MutableStateFlow<OrderUiState>(OrderUiState.Idle)
    val uiState: StateFlow<OrderUiState> = _uiState.asStateFlow()

    fun confirmOrder(orderId: String) {
        viewModelScope.launch {
            _uiState.value = OrderUiState.Loading
            confirmOrderUseCase(orderId)
                .onSuccess { _uiState.value = OrderUiState.Success(it) }
                .onFailure { _uiState.value = OrderUiState.Error(it.message ?: "Unknown error") }
        }
    }
}
```

### B. Enterprise PHP (Laravel Service-Repository Pattern)
```php
// 1. Domain Contract / Port
namespace App\Domain\Repositories;

interface OrderRepositoryInterface {
    public function findById(int $id): ?Order;
    public function updateStatus(int $id, string $status): bool;
}

// 2. Application Service / Use Case
namespace App\Application\Services;

class OrderConfirmationService {
    public function __construct(
        private OrderRepositoryInterface $orderRepository,
        private PaymentGatewayInterface $paymentGateway
    ) {}

    public function execute(int $orderId): OrderResult {
        $order = $this->orderRepository->findById($orderId);
        if (!$order) {
            throw new OrderNotFoundException("Order #{$orderId} does not exist");
        }
        
        $paymentResult = $this->paymentGateway->charge($order->total, $order->currency);
        if (!$paymentResult->isSuccessful()) {
            return OrderResult::failed("Payment declined: " . $paymentResult->errorMessage);
        }

        $this->orderRepository->updateStatus($orderId, 'confirmed');
        return OrderResult::success($order);
    }
}
```

### C. Python / Odoo Decoupled Core
```python
# Domain Entity (Dataclass, zero Odoo dependencies)
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class OrderLineItem:
    product_id: int
    quantity: float
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

@dataclass(frozen=True)
class DomainOrder:
    order_id: int
    partner_id: int
    lines: List[OrderLineItem]

    def calculate_total(self) -> float:
        return sum(line.subtotal for line in self.lines)
```

---

## 3. Hexagonal Testing Law
- **Domain & Use Cases**: 100% testable via lightning-fast in-memory unit tests using mocks/fakes. Zero database startup required.
- **Repository Implementations**: Tested via integration tests against real database instances (PostgreSQL / SQLite).
- **Controllers & UI**: Tested via contract tests and end-to-end user flows.
