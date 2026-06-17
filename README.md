# CLI Expense Tracker (v1)

A simple command-line expense tracking application built with Python. The application allows users to record expenses, store them persistently, and generate basic financial reports.

## Features

### Expense Management

- Add a new expense
- View all expenses
- Delete an expense
- Find an expense by ID

### Expense Information

Each expense contains:

- Unique ID
- Date
- Category
- Description
- Amount
- Created At timestamp

### Reporting

Generate summary reports including:

- Total expenses
- Total expenses by category
- Category with the highest expense
- Category with the lowest expense

### Data Persistence

- Expenses are stored in a JSON file
- Data is automatically loaded when the application starts
- Data is automatically saved after modifications

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
├── data/
│   └── expenses.json
│
├── models/
│   └── expense.py
│
├── services/
│   ├── expense_service.py
|
│── storage/
|   ├── json_storage.py
│
├── interface/
│   └── cli.py
│
├── utils/
│   ├── validators.py
│
├── main.py
├── .gitignore
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/4wiafe/cli-expense-tracker.git
cd cli-expense-tracker
```

### Create a Virtual Environment

```bash
python3 -m venv .venv
```

### Activate the Virtual Environment

#### macOS/Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

---

## Running the Application

```bash
python main.py
```

---

## Example Usage

### Add an Expense

```text
Enter expense date: 2026-08-17
Enter category: Food
Enter description: Lunch
Enter amount: 45
```

### View Expenses

```text
ID: 3f8d...
Date: August 17 2026
Category: Food
Description: Lunch
Amount: 45
```

### Generate Report

```text
Expense Summary Report

Total Expenses: 1,250

Expenses by Category:
Food: 450

Highest Spending Category:
Utilities (500)

Lowest Spending Category:
Transport (300)
```

---

## Technologies Used

- Python 3
- JSON
- Object-Oriented Programming (OOP)
- File Handling
- Exception Handling
- UUID
- Datetime

---

## Learning Objectives

This project was built to practice:

- Python fundamentals
- Classes and Objects
- Modules and Packages
- File I/O
- JSON serialization and deserialization
- Error handling
- Data validation
- Separation of concerns
- Service-based architecture
- Clean code principles

---

## Future Improvements (v2)

Potential enhancements for future versions:

- PostgreSQL database support
- Monthly and yearly reports
- Expense filtering by category
- Expense filtering by date range
- Export reports to CSV
- Budget tracking
- User accounts and authentication
- REST API version
- Web interface

---

## Author

**Richmond Kwame Wiafe Gyebi**

Aspiring Backend Engineer focused on building scalable backend systems and eventually developing an AI-powered WASSCE learning platform.
