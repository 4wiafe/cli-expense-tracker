from services.expense_service import ExpenseService
from storage.json_storage import JsonStorage
from utils.validators import to_cents

FILE_PATH = "data/expenses.json"


def run_cli():
    storage = JsonStorage(FILE_PATH)
    service = ExpenseService(storage)
    is_running = True

    while is_running:
        print("\n=== EXPENSE TRACKER ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Delete expense")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            date = input("Date (eg, 6-26-2026): ")
            category = input("Category (eg, food): ")
            description = input("Description (eg, Bought breakfast): ")
            amount = to_cents(input("Amount (eg, 25.00): "))

            expense = service.add_expense(date, category, description, amount)
            print("===========Expense added============")
            print(f"Added expense with id: {expense.id}")
            print("====================================")
        elif choice == "2":
            print("=============== All Expenses ===============")

            all_expenses = service.list_expenses()

            for expense in all_expenses:
                print(f"id: {expense.id}")
                print(f"Date: {expense.date}")
                print(f"Category: {expense.category}")
                print(f"Description: {expense.description}")
                print(f"Amount: {expense.amount / 100:.2f}")
                print("======================================")

        elif choice == "3":
            expense_id = input("Enter id: ")
            service.delete_expense(expense_id)
            print("Expense deleted!")
        elif choice == "4":
            is_running = False
        else:
            print("Invalid option, please try again")
