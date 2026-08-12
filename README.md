# CLI Expense Tracker

A command-line expense, salary, and budget tracking application built with **Python and PostgreSQL**.

The project is being developed incrementally as a backend engineering learning project. Month 2 focused on moving from a simple expense tracker into a **multi-user, PostgreSQL-backed personal finance system**, while practicing relational database design, SQL, layered architecture, service/storage separation, database constraints, indexing, and SQL-based reporting.

---

## Features

### User Management

Users can:

- Create a user
- View user information
- Update user information
- Delete a user

User data includes:

- Name
- Email
- Password hash
- Contact information

> Authentication and password verification are not implemented yet. The current CLI uses user IDs directly while the authentication layer is being developed.

---

### Expense Management

Users can:

- Add an expense
- View all their expenses
- View a specific expense
- Edit an expense
- Delete an expense

Expenses contain:

- Expense ID
- User ID
- Category
- Description
- Amount
- Expense date

Expenses are associated with predefined categories through a foreign key relationship.

The application stores monetary values as **integer cents** in PostgreSQL and converts them into human-readable amounts in the service layer.

---

### Category Management

The application uses a predefined shared category list:

- Food
- Transportation
- Entertainment
- Bills
- Donation
- Education
- Health
- Household
- Remittance
- Shopping
- Savings
- Others

Categories are stored separately from expenses and referenced through `category_id`.

A dedicated `CategoryService` provides in-memory lookups between:

```text
category_id → category_name
category_name → category_id
```

This keeps category resolution out of the storage layer and avoids repeatedly querying the small, static categories table.

---

### Salary Management

Users can:

- Add a monthly salary
- View a salary entry
- Update a salary entry
- Delete a salary entry

Each salary is associated with:

- User
- Amount
- Month
- Year

The database prevents duplicate salary records for the same user, month, and year.

---

### Budget Management

Users can:

- Create a monthly category budget
- View a budget
- Update a budget
- Delete a budget

Each budget contains:

- User
- Category
- Amount
- Month
- Year

The database prevents duplicate budgets for the same user, category, month, and year.

---

### Reporting

Reports are calculated directly by PostgreSQL rather than loading all expenses into Python.

The current reporting functionality includes:

- Total spending
- Spending by a specific category
- Spending across all categories
- Highest-spending category
- Lowest-spending category
- Budget vs. actual spending

Budget reports calculate:

- Budget amount
- Actual spending
- Remaining amount
- Budget status
- Month
- Year

The budget status is calculated by PostgreSQL as:

```text
Within Budget
Over Budget
```

---

## PostgreSQL Database

The application uses a relational PostgreSQL database with five primary tables:

```text
users
categories
expenses
salaries
budgets
```

### Relationships

```text
users
  │
  ├──< expenses >── categories
  │
  ├──< salaries
  │
  └──< budgets >── categories
```

This allows each user to maintain their own:

- Expenses
- Salaries
- Budgets

while categories remain shared across users.

---

## Database Schema

### users

```text
user_id
name
email
password_hash
contact
created_at
```

### categories

```text
category_id
category_name
```

Categories are predefined and uniquely identified.

### expenses

```text
expense_id
user_id
category_id
description
amount
expense_date
```

### salaries

```text
salary_id
user_id
amount
month
year
```

A composite uniqueness constraint prevents duplicate salary entries for the same:

```text
user + month + year
```

### budgets

```text
budget_id
user_id
category_id
amount
month
year
```

A composite uniqueness constraint prevents duplicate budgets for the same:

```text
user + category + month + year
```

---

# Architecture

The application follows a layered architecture that separates database access from business logic and the user interface.

```text
CLI
 │
 ▼
Service Layer
 │
 ▼
Storage Layer
 │
 ▼
PostgreSQL
```

### CLI

Responsible for:

- Displaying menus
- Collecting user input
- Calling service methods
- Displaying results

The CLI does not directly interact with PostgreSQL.

---

### Service Layer

Responsible for:

- Business logic
- Input normalization
- Converting user-friendly values into database values
- Resolving category names and IDs
- Converting raw database records into application-friendly data
- Coordinating storage operations

Current services include:

```text
ExpenseService
SalaryService
BudgetService
UserService
CategoryService
```

---

### Storage Layer

Responsible for:

- Opening database connections
- Executing SQL
- Returning raw database data
- Performing CRUD operations
- Performing SQL-based reporting queries

Storage methods intentionally return **raw database values**.

For example:

```text
(
    expense_id,
    category_id,
    description,
    amount,
    expense_date
)
```

The service layer is responsible for turning those raw values into application-level data.

This keeps the storage layer focused on database persistence.

---

## Dynamic SQL Query Building

The project contains a reusable query-building helper for dynamic `UPDATE` statements.

For example, multiple services can use the same logic to construct:

```sql
SET amount = %s, month = %s, year = %s
```

while still using parameterized values.

Column names are handled using `psycopg.sql.Identifier` when necessary to prevent unsafe dynamic SQL construction.

This avoids duplicating the same dynamic `UPDATE` construction logic across:

- Expense storage
- Salary storage
- Budget storage
- User storage

---

# Database Design Practices Practiced

Month 2 focused heavily on designing a proper relational database rather than simply storing application data.

The project practices:

- Identifying entities
- Identifying relationships
- Primary keys
- Foreign keys
- One-to-many relationships
- Normalization
- Separating categories into their own table
- Avoiding duplicated category names in expense records
- Database-level validation
- `NOT NULL` constraints
- `CHECK` constraints
- `UNIQUE` constraints
- Composite `UNIQUE` constraints
- Referential integrity
- Foreign key relationships
- Protecting related financial records

---

# SQL Concepts Practiced

Month 2 significantly expanded the SQL used by the application.

### CRUD

```sql
SELECT
INSERT
UPDATE
DELETE
```

### Filtering

```sql
WHERE
```

### Relationships

```sql
INNER JOIN
LEFT JOIN
```

### Aggregation

```sql
SUM()
MAX()
MIN()
COALESCE()
```

### Grouping

```sql
GROUP BY
HAVING
```

### Subqueries

Used to determine highest- and lowest-spending categories.

### Common Table Expressions

Used to make more complex reporting queries easier to structure.

```sql
WITH category_totals AS (...)
```

### Database-generated values

Used:

```sql
RETURNING
```

to retrieve newly created or updated records without issuing an additional query.

---

# Reporting with PostgreSQL

One of the main Month 2 goals was to move calculations from Python into the database.

Instead of:

```text
Fetch every expense
        ↓
Load everything into Python
        ↓
Calculate totals in Python
```

the application now allows PostgreSQL to perform the aggregation:

```text
PostgreSQL
    ↓
SUM()
GROUP BY
MAX()
MIN()
COALESCE()
    ↓
Return only the required result
```

For example, category spending is calculated using the database:

```sql
SELECT category_id, COALESCE(SUM(amount), 0)
FROM expenses
WHERE user_id = %s
GROUP BY category_id;
```

This gives the database responsibility for data aggregation while the service layer handles presentation and business-level transformation.

---

# Indexing and Query Performance

The database includes indexes on columns frequently used for:

- Filtering
- Foreign-key relationships
- Joining
- User-specific queries

Query performance was investigated using PostgreSQL:

```sql
EXPLAIN
```

This introduced the concept of understanding how PostgreSQL executes queries rather than assuming that a query is efficient simply because it works.

---

# Error Handling

The application handles errors at multiple layers.

Examples include:

- Invalid category IDs
- Invalid category names
- Missing expenses
- Missing salaries
- Missing budgets
- Missing users
- Empty update data
- Invalid update fields
- Duplicate salary records
- Duplicate budget records
- Database constraint violations

Database exceptions such as:

```python
UniqueViolation
```

are converted into application-level errors that can be understood by the service/CLI layer.

---

# Input and Data Transformation

The service layer handles transformations between user-friendly values and database values.

For example:

### Money

User input:

```text
50
```

Application/database representation:

```text
5000 cents
```

Display representation:

```text
50.00
```

### Dates

User input:

```text
15-06-2026
```

is converted into a Python:

```python
date
```

before being passed to PostgreSQL.

### Categories

User input:

```text
Food
```

is converted into:

```text
category_id
```

before being stored in the expenses/budgets tables.

The reverse conversion happens when data is returned to the user.

---

# Current CLI

The CLI is organized around the application's major domains:

```text
========== EXPENSE TRACKER ==========

1. Expenses
2. Salary
3. Budget
4. Reports
5. Exit
```

Each domain has its own submenu.

### Expenses

```text
1. Add expense
2. Edit expense
3. View all expenses
4. View expense
5. Delete expense
6. Back
```

### Salary

```text
1. Add salary
2. Edit salary
3. View salary
4. Delete salary
5. Back
```

### Budget

```text
1. Add budget
2. Edit budget
3. View budget
4. Delete budget
5. Back
```

### Reports

```text
1. View total spending
2. View spending by category
3. View all spending by each category
4. View highest spending category
5. View lowest spending category
6. View budget spending
7. Back
```

A temporary user ID is currently supplied through the CLI while the authentication layer is being developed.

---

# Project Structure

```text
cli-expense-tracker/
│
├── config/
│   └── settings.py
│
├── database/
│   ├── connection.py
│   └── dynamic_query_builder.py
│
├── models/
│   ├── user.py
│   ├── expense.py
│   ├── salary.py
│   └── budget.py
│
├── services/
│   ├── user_service.py
│   ├── expense_service.py
│   ├── salary_service.py
│   ├── budget_service.py
│   └── category_service.py
│
├── storage/
│   ├── user_storage.py
│   ├── expense_storage.py
│   ├── salary_storage.py
│   ├── budget_storage.py
│   └── category_storage.py
│
├── reports/
│   └── reports.py
│
├── interface/
│   └── cli.py
│
├── utils/
│   └── validators.py
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

---

# Month 2 KPIs

Month 2 was focused on progressing from a basic Python application into a structured PostgreSQL-backed backend system.

### Database Design

- [x] Designed a relational database around multiple entities
- [x] Created relationships between users, expenses, categories, salaries, and budgets
- [x] Used primary keys and foreign keys
- [x] Applied normalization principles
- [x] Added database-level constraints
- [x] Added single-column and composite uniqueness constraints
- [x] Protected relational integrity with foreign keys
- [x] Added indexes for commonly queried columns
- [x] Investigated query performance using `EXPLAIN`

### PostgreSQL

- [x] Connected Python to PostgreSQL using Psycopg 3
- [x] Implemented CRUD operations
- [x] Used parameterized SQL
- [x] Used `RETURNING`
- [x] Used `INNER JOIN`
- [x] Used `LEFT JOIN`
- [x] Used `GROUP BY`
- [x] Used `HAVING`
- [x] Used aggregate functions
- [x] Used `COALESCE`
- [x] Used subqueries
- [x] Used CTEs
- [x] Used PostgreSQL to calculate financial reports
- [x] Handled database constraint violations

### Architecture

- [x] Introduced a storage layer
- [x] Introduced a service layer
- [x] Separated database access from business logic
- [x] Kept storage methods focused on raw database data
- [x] Moved data transformation into services
- [x] Created a dedicated `CategoryService`
- [x] Created reusable dynamic SQL query-building logic
- [x] Organized the CLI around application domains

### Application Features

- [x] Multi-user expense tracking
- [x] Expense CRUD
- [x] Salary CRUD
- [x] Budget CRUD
- [x] User CRUD
- [x] Category lookup and validation
- [x] Spending reports
- [x] Category spending reports
- [x] Highest/lowest spending reports
- [x] Budget vs. actual spending reports

### Engineering Goal

The main Month 2 progression was:

```text
Python CLI
    ↓
Relational Database
    ↓
PostgreSQL
    ↓
CRUD
    ↓
Database Constraints
    ↓
Indexes
    ↓
SQL Aggregation
    ↓
Reporting
    ↓
Storage Layer
    ↓
Service Layer
    ↓
Domain-oriented CLI
```

The project is no longer just an expense tracker. It is becoming a small **multi-user personal finance backend**.

---

# Technologies Used

- Python 3
- PostgreSQL
- Psycopg 3
- SQL
- python-dotenv
- Object-Oriented Programming
- Relational Database Design
- Layered Architecture
- Exception Handling

---

# Backend Concepts Practiced

### Python

- Functions
- Classes
- Objects
- Type hints
- Dictionaries
- Lists
- Tuples
- Exception handling
- Modules and packages
- Data transformation

### SQL

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `WHERE`
- `GROUP BY`
- `HAVING`
- `ORDER BY`
- `SUM`
- `MAX`
- `MIN`
- `COALESCE`
- `INNER JOIN`
- `LEFT JOIN`
- Subqueries
- CTEs
- `RETURNING`
- Parameterized queries
- Dynamic SQL
- `EXPLAIN`

### Database Engineering

- Relational modeling
- Normalization
- Primary keys
- Foreign keys
- Composite uniqueness
- Constraints
- Indexes
- Referential integrity
- Query performance
- Transaction management

### Backend Architecture

- Layered architecture
- Separation of concerns
- Service layer
- Storage/repository layer
- Data transformation
- Domain-oriented application structure
- Reusable database utilities

---

# Installation

## Clone the repository

```bash
git clone https://github.com/4wiafe/cli-expense-tracker.git
cd cli-expense-tracker
```

## Create a virtual environment

```bash
python3 -m venv .venv
```

## Activate the virtual environment

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure environment variables

Create a `.env` file in the project root:

```text
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Set up PostgreSQL

Create the database and run the project's schema to create the required tables, constraints, relationships, and indexes.

---

# Running the Application

```bash
python main.py
```

---

# Current Limitations

The project is still intentionally a CLI application.

Current limitations include:

- Authentication is not fully implemented
- Password hashing/verification is not yet part of the login flow
- User IDs are currently entered manually through the CLI
- Input validation can still be improved
- The CLI presentation layer is still being refined
- Automated tests have not yet been added
- API layer has not yet been implemented

These are deliberate next steps rather than missing core Month 2 functionality.

---

# Future Improvements

## Month 3 — Backend API

The next major phase will convert the application from a CLI-oriented application into a backend API.

Planned technologies:

- FastAPI
- Pydantic
- REST API design
- Dependency injection
- Request validation
- Response models
- Authentication
- Authorization
- OpenAPI documentation

The existing:

```text
Service Layer
      ↓
Storage Layer
      ↓
PostgreSQL
```

will be reused rather than rewritten.

FastAPI will become another interface on top of the existing application logic:

```text
             ┌── CLI
             │
FastAPI ─────┤
             │
             ▼
        Service Layer
             │
             ▼
        Storage Layer
             │
             ▼
         PostgreSQL
```

The long-term goal is to turn this project into a real backend service and use the experience gained here to build larger software systems.

---

## Author

**Richmond Kwame Wiafe Gyebi**

Aspiring Backend Engineer building backend systems while continuously strengthening my knowledge of Python, SQL, PostgreSQL, software architecture, and database engineering through hands-on projects.
