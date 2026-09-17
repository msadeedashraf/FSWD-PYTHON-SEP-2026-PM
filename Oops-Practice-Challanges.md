
# OOP Practice: Real-World Examples Using Classes, Inheritance, Polymorphism, Encapsulation, Abstraction

This document contains **5 real-world scenarios** designed to strengthen your understanding of:

- Class & Object  
- Properties & Methods  
- Inheritance  
- Polymorphism  
- Encapsulation  
- Abstraction  

Each example includes an explanation + tasks + questions.

---

## 1️⃣ Ride-Sharing App (Uber / Careem Simulation)
### Concepts: Class, Object, Properties, Methods

A ride-sharing platform wants a `Driver` class with:

- `name`
- `car_model`
- `rating`
- `total_rides`

Methods:

- `accept_ride()`
- `complete_ride()` → increases `total_rides`
- `show_profile()`

### Student Task
1. Create the `Driver` class.  
2. Create **three objects** of this class.  
3. Simulate each driver accepting and completing a ride.

### Questions
- What is the class?  
- What are the objects?  
- What are the properties?  
- What are the methods?

---

## 2️⃣ School System (Inheritance)
### Concepts: Inheritance, Method Reuse

A school has three types of users:

- `Student`  
- `Teacher`  
- `Admin`  

They all share:

- `name`  
- `email`  
- `account_created`  

Methods:

- `login()`  
- `logout()`

Each role adds:

- Student → `submit_assignment()`  
- Teacher → `grade_assignment()`  
- Admin → `create_course()`  

### Student Task
1. Create a base class `User`.  
2. Create `Student`, `Teacher`, `Admin` that **inherit** from `User`.  
3. Add the unique methods to each subclass.

### Questions
- What features belong in the parent class?  
- What features belong in each subclass?  
- Why is inheritance helpful here?

---

## 3️⃣ Payment Processing System (Polymorphism)
### Concepts: Polymorphism, Method Overriding

Three types of payments exist:

- `CreditCardPayment`  
- `PayPalPayment`  
- `ApplePayPayment`  

Each must implement:

```python
process_payment(amount)
```

But each processes differently:

- Credit card → “Processing credit card payment…”  
- PayPal → “Redirecting to PayPal…”  
- Apple Pay → “Using Apple Wallet…”  

### Student Task
1. Create a base class `Payment`.  
2. Create subclasses that override `process_payment()`.  
3. Run:

```python
payments = [CreditCardPayment(), PayPalPayment(), ApplePayPayment()]
for p in payments:
    p.process_payment(100)
```

### Questions
- How does the same method behave differently?  
- Why does polymorphism make payment systems easier to build?

---

## 4️⃣ Bank Account System (Encapsulation)
### Concepts: Encapsulation, Protecting Data

A bank wants to prevent direct modification of:

- `balance`  
- `account_number`  

These should be protected using `_balance`, `_account_number`, and updated only through:

- `deposit()`
- `withdraw()`
- `get_balance()`

### Student Task
1. Modify the `BankAccount` class so that balance is protected (`_balance`).  
2. Use property methods (`@property`) to allow read-only access.  

### Questions
- Why should financial data be protected?  
- What problems occur if balance can be changed directly?  
- How does encapsulation fix this?

---

## 5️⃣ Transportation System (Abstraction)
### Concepts: Abstraction, Abstract Classes

A transportation network includes:

- Bus  
- Train  
- Taxi  

All vehicles share:

- `start()`  
- `stop()`  
- `get_fare()`  

But each implements them differently.

### Student Task
1. Create an abstract class `Vehicle` with abstract methods:

```python
start()
stop()
get_fare()
```

2. Implement `Bus`, `Train`, and `Taxi` with their own logic.

### Questions
- What is the purpose of an abstract class?  
- Why do subclasses handle the details instead of the parent class?  
- How does abstraction improve large system design?

---

## Summary Table

| Example | Concept Focus | Real-World Context |
|--------|----------------|--------------------|
| Ride-Sharing | Class, Object | Uber / Careem drivers |
| School Users | Inheritance | Student / Teacher / Admin |
| Payment System | Polymorphism | Credit card vs PayPal vs Apple Pay |
| Bank Account | Encapsulation | Protecting sensitive data |
| Transportation | Abstraction | Bus, Train, Taxi system |
