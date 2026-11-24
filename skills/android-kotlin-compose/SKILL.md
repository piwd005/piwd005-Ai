---
name: android-kotlin-compose
description: >-
  Senior Android Developer expertise for Modern Android Development (MAD):
  Kotlin idioms, Jetpack Compose (Material 3, state hoisting, performance optimization),
  MVVM / MVI Clean Architecture, Kotlin Coroutines & StateFlow, Room local database,
  Retrofit / Ktor networking, Dependency Injection (Hilt / Koin), Gradle build configuration,
  and Android CLI emulator testing. Use when building Android applications or learning mobile dev.
---

# Senior Android Developer Handbook (Kotlin & Jetpack Compose)

Build modern, production-grade Android applications using Modern Android Development (MAD) practices, declarative UI with Jetpack Compose, and robust reactive architecture.

---

## 1. Declarative UI with Jetpack Compose & Material 3

1. **State Hoisting & Unidirectional Data Flow (UDF)**:
   - State flows down, events flow up.
   - Composables must be stateless whenever possible:
     ```kotlin
     @Composable
     fun UserProfileScreen(
         uiState: UserProfileUiState,
         onRefresh: () -> Unit,
         onSave: (String) -> Unit
     ) { ... }
     ```
2. **Recomposition Optimization**:
   - Use `@Stable` or `@Immutable` on data classes passed to Composables.
   - Wrap expensive calculations in `remember(key) { ... }` or `derivedStateOf { ... }`.
   - Never perform side effects directly inside Composable functions; always use `LaunchedEffect`, `rememberCoroutineScope`, or `DisposableEffect`.
3. **Responsive Mobile Layouts**:
   - Use `Scaffold` with `topBar`, `bottomBar`, and `snackbarHost`.
   - Use `LazyColumn` and `LazyRow` with unique keys (`items(items, key = { it.id })`) for smooth 60/120fps scrolling.

---

## 2. Architecture: MVVM / MVI with Kotlin Coroutines & Flow

```
[View: Jetpack Compose UI]
       ↑ (observes StateFlow<UiState>)
       ↓ (dispatches User Actions/Intents)
[ViewModel: State management & business orchestration]
       ↑ (calls suspend functions / returns Flow<T>)
[Repository: Single Source of Truth]
      ↗                  ↖
[Local DB: Room]   [Remote API: Retrofit / OkHttp]
```

1. **UiState Pattern**:
   - Model UI state as a sealed interface or data class:
     ```kotlin
     sealed interface OrderListUiState {
         object Loading : OrderListUiState
         data class Success(val orders: List<Order>) : OrderListUiState
         data class Error(val message: String) : OrderListUiState
     }
     ```
2. **ViewModel Implementation**:
   - Use `viewModelScope.launch` with Coroutine Exception Handlers.
   - Expose state as `StateFlow`:
     ```kotlin
     val uiState: StateFlow<OrderListUiState> = repository.getOrders()
         .map { OrderListUiState.Success(it) }
         .stateIn(
             scope = viewModelScope,
             started = SharingStarted.WhileSubscribed(5000),
             initialValue = OrderListUiState.Loading
         )
     ```

---

## 3. Local Persistence (Room) & Networking (Retrofit)

1. **Room Database**:
   - Always return `Flow<List<Entity>>` for reactive database queries.
   - Mark insert/update/delete operations with `suspend`.
   - Never run database queries on the main thread.
2. **Retrofit & Moshi / Kotlinx Serialization**:
   - Use Kotlinx Serialization for fast, reflection-free JSON parsing.
   - Configure OkHttp timeouts (15s connect, 30s read) with auth interceptors.

---

## 4. Android Tooling & CLI Integration

- Use the `android` CLI tool for project creation and device interaction:
  - `android create empty-activity --name="App" --output=./app`
  - `android layout` to inspect active UI hierarchy in JSON.
  - `android screen` to capture visual snapshots of physical or emulator screens.
