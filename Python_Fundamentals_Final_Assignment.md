# Python Fundamentals Final Assignment
## Real-World Systems Using Core Python

Students must ONLY use:

- Variables
- Functions
- Conditions
- Loops
- Lists
- Dictionaries
- Tuples
- Sets
- File Handling

NOT ALLOWED:

- Classes
- OOP
- Databases
- External Libraries (except `datetime` and `os`)
- APIs
- Frameworks

The goal is:

> Learn how real software systems are modeled using core Python fundamentals.

---

# Assignment 1 — Banking Transaction Management System

## Real-World Scenario

Build a mini banking system that allows users to:

- Deposit money
- Withdraw money
- Apply overdraft rules
- Track transactions
- Generate statement files
- Read previous statement files

## Required Concepts

| Concept | Usage |
|---|---|
| Variables | balance, overdraft |
| Functions | deposit, withdraw |
| Conditions | insufficient funds |
| Loops | menu system |
| Lists | transaction history |
| Dictionaries | transaction records |
| Tuples | timestamps |
| Sets | unique transaction types |
| File Handling | statement exports |

## Required Features

### Must Have

- Deposit
- Withdraw
- Transaction fee
- Overdraft protection
- Transaction history
- Create statement TXT file
- Read statement files
- Dynamic file names with timestamps

### Bonus Features

- PIN system
- Multiple accounts
- Daily withdrawal limit
- Transfer between accounts

---

# Assignment 2 — Student Information & Attendance System

## Real-World Scenario

Build a classroom management system.

Teacher should be able to:

- Add students
- Mark attendance
- Search students
- View student reports
- Save attendance to files

## Required Concepts

| Concept | Usage |
|---|---|
| List | all students |
| Dictionary | student records |
| Set | unique courses |
| Tuple | attendance timestamp |
| File Handling | attendance reports |

## Student Record Example

```python
student = {
    "id": 1001,
    "name": "Ali",
    "courses": ["Python", "SQL"],
    "attendance": 90
}
```

## Required Features

### Must Have

- Add student
- Remove student
- Search student
- Mark attendance
- Show attendance percentage
- Save report to TXT file

### Bonus Features

- Grade calculator
- Fail/pass system
- Search by ID
- Multiple classes

---

# Assignment 3 — Inventory & Store Management System

## Real-World Scenario

Build a store inventory system.

Store owner should be able to:

- Add products
- Sell products
- Restock inventory
- Generate sales reports
- Detect low stock

## Required Concepts

| Concept | Usage |
|---|---|
| Dictionary | product info |
| List | all products |
| Set | unique categories |
| Tuple | invoice timestamp |
| File Handling | inventory reports |

## Product Example

```python
product = {
    "id": 101,
    "name": "Gaming Mouse",
    "price": 49.99,
    "stock": 15
}
```

## Required Features

### Must Have

- Add product
- Update stock
- Sell product
- Track inventory
- Low stock warning
- Create sales report file

### Bonus Features

- Invoice generator
- Discount system
- Tax calculations
- Product search

---

# Assignment 4 — Personal Expense Tracker

## Real-World Scenario

Build a budgeting and expense management application.

User should be able to:

- Add expenses
- Track categories
- View spending summary
- Export reports

## Required Concepts

| Concept | Usage |
|---|---|
| List | expense history |
| Dictionary | expense record |
| Set | unique categories |
| Tuple | timestamps |
| File Handling | reports |

## Expense Example

```python
expense = {
    "category": "Food",
    "amount": 25,
    "date": "2026-05-20"
}
```

## Required Features

### Must Have

- Add expense
- Show total spending
- Filter by category
- Generate report file
- Show largest expense

### Bonus Features

- Monthly budgets
- Savings goals
- Income tracking
- Spending warnings

---

# Assignment 5 — Hospital Patient Queue System

## Real-World Scenario

Build a hospital reception and patient tracking system.

Receptionist should be able to:

- Add patients
- Assign urgency
- Track waiting queue
- Search patients
- Generate daily reports

## Required Concepts

| Concept | Usage |
|---|---|
| List | patient queue |
| Dictionary | patient records |
| Set | unique diseases/departments |
| Tuple | check-in timestamp |
| File Handling | daily reports |

## Patient Example

```python
patient = {
    "id": 2001,
    "name": "Sarah",
    "department": "Cardiology",
    "urgency": "High"
}
```

## Required Features

### Must Have

- Add patient
- Show queue
- Search patient
- Remove treated patient
- Generate patient report

### Bonus Features

- Emergency priority queue
- Doctor assignment
- Billing system
- Appointment scheduling

---

# Assignment 6 — ATM Cash Withdrawal & Account Access System

## Real-World Scenario

Build a mini ATM system where a user can:

- Enter a PIN
- Check account balance
- Withdraw cash
- Deposit cash
- View recent ATM transactions
- Generate an ATM receipt file

This project is different from the full banking system because the focus is on **ATM-style user interaction**, **PIN validation**, **cash withdrawal rules**, and **receipt generation**.

## Required Concepts

| Concept | Usage |
|---|---|
| Variables | balance, pin, withdrawal limit |
| Functions | login, withdraw, deposit, print receipt |
| Conditions | wrong PIN, insufficient funds, limit exceeded |
| Loops | ATM menu and PIN attempts |
| Lists | recent ATM transactions |
| Dictionaries | transaction records |
| Tuples | transaction date and time |
| Sets | unique transaction types |
| File Handling | ATM receipt or mini statement |

## ATM Transaction Example

```python
transaction = {
    "type": "WITHDRAW",
    "amount": 100,
    "date": "2026-05-20",
    "time": "11:18:00 AM",
    "balance": 900
}
```

## Required Features

### Must Have

- PIN login system
- Maximum 3 PIN attempts
- Check balance
- Deposit cash
- Withdraw cash
- Prevent withdrawal if balance is too low
- Daily ATM withdrawal limit
- Store transaction history
- Generate ATM receipt TXT file
- Show recent transactions

### Bonus Features

- Change PIN
- Fast cash options: `$20`, `$50`, `$100`, `$200`
- Service fee after withdrawal
- Lock account after 3 failed PIN attempts
- Mini statement showing last 5 transactions

---

# IMPORTANT INSTRUCTIONS FOR STUDENTS

## You MUST:

- Use functions properly
- Break logic into reusable methods
- Avoid duplicate code (DRY principle)
- Use meaningful variable names
- Use comments
- Validate user input
- Build menu-driven applications

---

# REQUIRED SUBMISSION

| File | Purpose |
|---|---|
| `.py` | Main program |
| `.txt` | Sample generated reports |
| `README.txt` | Explanation of project |

---

