# CLI Expense Tracker

A command line expense tracking application built with Python and PostgreSQL. The project is being developed incrementally to practice backend engineering concepts including object oriented programming, layered architecture, SQL, database design, and data persistence.

## Features

### Expense Management

- Add a new expense
- View all expenses
- Find an expense by ID
- Delete an expense

### Expense Information

Each expense contains:

- Expense ID
- Category
- Description
- Amount
- Expense date

### Reporting

Generate summary reports including:

- Total expenses
- Total expenses by category
- Category with the highest expense
- Category with the lowest expense

### PostgreSQL Persistence

- Stores expenses in a PostgreSQL database
- Uses parameterized SQL queries
- Supports CRUD operations
- Retrieves database generated IDs
- Maps database records to Python objects

### Input Validation

- Validates dates
- Validates expense amounts
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
│   └── expense.py
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

---

## Running the Application

```bash
python main.py
```

---

## Technologies Used

- Python 3
- PostgreSQL
- Psycopg
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
- SQL
- PostgreSQL
- Database connections
- CRUD operations
- Parameterized SQL queries
- Transaction management
- Environment variable management
- Data modeling
- Separation of concerns
- Service layer architecture
- Storage abstraction
- Clean code principles

---

## Future Improvements

Planned enhancements include:

- Update expense functionality
- Monthly and yearly reports
- Filter expenses by category
- Filter expenses by date range
- Export reports to CSV
- Database migrations
- Unit and integration tests
- Logging
- Docker support
- REST API with FastAPI
- User authentication and authorization

---

## Author

**Richmond Kwame Wiafe Gyebi**

Aspiring Backend Engineer focused on building scalable backend systems while continuously strengthening my knowledge of Python, SQL, PostgreSQL, and software architecture through hands on projects.
