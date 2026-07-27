# CLI Expense Tracker

A command line expense and budget tracking application built with Python and PostgreSQL. The project is being developed incrementally to practice backend engineering concepts including relational database design, SQL, object oriented programming, layered architecture, and data persistence.

---

## Features

### User Management

- Create a user account
- View user profile details
- Update user profile (name, email, contact)
- Delete a user account

### Expense Management

- Add a new expense, linked to a user and a category
- View all expenses (with category names, not raw IDs)
- Find an expense by ID
- Update an expense (category, description, amount, date)
- Delete an expense

### Category Management

- Predefined, shared list of categories (Food, Transportation, Entertainment, Bills, Donation, Education, Health, Household, Remittance, Shopping, Savings, Others)

### Salary Management

- Add a monthly salary entry per user
- View a salary entry
- Update a salary entry
- Delete a salary entry
- Prevents duplicate salary entries for the same user, month, and year

### Budget Management

- Set a monthly budget per user, per category
- View a budget entry
- Update a budget entry
- Delete a budget entry
- Prevents duplicate budgets for the same user, category, month, and year

### Reporting

Generate summary reports calculated directly in PostgreSQL, including:

- Total expenses
- Total expenses by category
- Category with the highest spending
- Category with the lowest spending
- Budget vs. actual spending comparison per category, per month, with over/under budget status

### PostgreSQL Persistence

- Relational schema with `users`, `categories`, `expenses`, `salaries`, and `budgets`
- Foreign key relationships with `ON DELETE RESTRICT` to protect financial history
- Database-level constraints (`NOT NULL`, `CHECK`, single-column and composite `UNIQUE`)
- Indexes on frequently filtered and joined columns, verified with `EXPLAIN`
- Uses parameterized SQL queries throughout
- Supports full CRUD operations across all tables
- Uses `INNER JOIN` and `LEFT JOIN` to combine related data
- Uses `GROUP BY`, `HAVING`, and subqueries for reporting
- Retrieves database-generated IDs via `RETURNING`
- Maps database records to Python objects
- Catches database-level constraint violations (e.g. `UniqueViolation`) and converts them into clear, user-friendly errors

### Input Validation

- Validates dates
- Validates expense, salary, and budget amounts
- Handles invalid user input gracefully
- Prevents application crashes using exception handling

---

## Project Structure

```text
cli-expense-tracker/
│
├── config/
│   └── settings.py
│
├── database/
│   └── connection.py
│
├── models/
│   ├── user.py
│   ├── expense.py
│   ├── salary.py
│   └── budget.py
│
├── services/
│   └── expense_service.py
│
├── storage/
│   ├── postgres_storage.py
│   └── json_storage.py
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

## Database Schema

- **users** — `user_id`, `name`, `email` (unique), `password_hash`, `contact`
- **categories** — `category_id`, `name` (unique, predefined list)
- **expenses** — `expense_id`, `user_id` (FK), `category_id` (FK), `description`, `amount`, `expense_date`
- **salaries** — `salary_id`, `user_id` (FK), `amount`, `month`, `year` — unique per user/month/year
- **budgets** — `budget_id`, `user_id` (FK), `category_id` (FK), `amount`, `month`, `year` — unique per user/category/month/year

---

## Installation

### Clone the repository

```bash
git clone https://github.com/4wiafe/cli-expense-tracker.git
cd cli-expense-tracker
```

### Create a virtual environment

```bash
python3 -m venv .venv
```

### Activate the virtual environment

#### macOS/Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root and add your PostgreSQL configuration:

```text
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Set up the database schema

Run the schema script against your PostgreSQL database to create all tables, constraints, and indexes.

---

## Running the Application

```bash
python main.py
```

---

## Technologies Used

- Python 3
- PostgreSQL
- Psycopg (v3)
- SQL
- python-dotenv
- Object Oriented Programming
- Layered Architecture
- Exception Handling

---

## Backend Concepts Practiced

This project is being built to strengthen my understanding of backend engineering by practicing:

- Python fundamentals
- Object Oriented Programming
- Relational database design (entities, relationships, normalization)
- One-to-many relationships and foreign keys
- Database constraints (`NOT NULL`, `CHECK`, `UNIQUE`, composite `UNIQUE`)
- SQL: `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- `INNER JOIN` and `LEFT JOIN`
- Aggregate functions, `GROUP BY`, `HAVING`, and subqueries
- Indexing and query plan analysis with `EXPLAIN`
- PostgreSQL and Psycopg (v3)
- CRUD operations across multiple related tables
- Parameterized SQL queries
- Catching and translating database exceptions (e.g. constraint violations) into application-level errors
- Transaction management
- Environment variable management
- Data modeling
- Separation of concerns
- Service layer architecture
- Storage abstraction
- Clean code principles

---

## Future Improvements

### Near-term

- Monthly and yearly reports
- Filter expenses by category
- Filter expenses by date range
- Export reports to CSV
- Database migrations
- Unit and integration tests
- Logging
- Docker support
- Soft-delete for user accounts (grace period before permanent deletion)
- User authentication and authorization (password hashing already scaffolded at the storage layer)

### Next Phase — FastAPI

The next phase of development converts this CLI application into a REST API.

**Learn:**

- FastAPI routing
- Request validation
- Response models
- Dependency injection
- API design principles
- OpenAPI documentation

**Build — Fintech v2:**
Convert the CLI application into an API with endpoints including:

- `POST /transactions`
- `GET /transactions`
- `DELETE /transactions`
- `GET /reports`
- `GET /categories`

**Goal:** build a first real backend service, exposing the existing PostgreSQL-backed storage layer through a documented, validated REST API rather than a command-line interface.

---

## Author

**Richmond Kwame Wiafe Gyebi**
Aspiring Backend Engineer focused on building scalable backend systems while continuously strengthening my knowledge of Python, SQL, PostgreSQL, and software architecture through hands-on projects.
