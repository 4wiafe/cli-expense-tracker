from services.expense_service import ExpenseService
from storage.postgres_storage import PostgresStorage
from reports.reports import Reports
from utils.validators import to_cents


def run_cli():
    storage = PostgresStorage()
    service = ExpenseService(storage)
    reports = Reports(storage)
    is_running = True

    while is_running:
        print("\n=== EXPENSE TRACKER ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. View summary")
        print("4. Delete expense")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            expense_date = input("Date (eg, 6-26-2026): ")
            category = input("Category (eg, food): ")
            description = input("Description (eg, Bought breakfast): ")
            amount = to_cents(input("Amount (eg, 25.00): "))

            expense = service.add_expense(category, description, amount, expense_date)
            print("===========Expense added============")
            print(f"Added expense with id: {expense.expense_id}")
            print("====================================")

        elif choice == "2":
            print("=============== All Expenses ===============")

            all_expenses = service.list_expenses()

            for expense in all_expenses:
                print(f"expense_id: {expense.expense_id}")
                print(f"Date: {expense.expense_date}")
                print(f"Category: {expense.category}")
                print(f"Description: {expense.description}")
                print(f"Amount: {expense.amount / 100:.2f}")
                print("======================================")

        elif choice == "3":
            print("1. View total expenses")
            print("2. View total by category")
            print("3. View category with highest expense")
            print("4. View category with lowest expense")

            summary_choice = input("Select an option: ")

            if summary_choice == "1":
                total_expenses = reports.total_expenses()
                print(f"Total expenses: {total_expenses / 100:.2f}")

            if summary_choice == "2":
                category = input("Enter a category: ")
                total_expense_by_category = reports.total_by_category(category)
                print(total_expense_by_category)

            if summary_choice == "3":
                highest_expense = reports.highest_expense_category()
                print(highest_expense)

            if summary_choice == "4":
                lowest_expense = reports.lowest_expense_cateory()
                print(lowest_expense)

        elif choice == "4":
            expense_id = input("Enter id: ")
            service.delete_expense(int(expense_id))
            print("Expense deleted!")

        elif choice == "5":
            is_running = False

        else:
            print("Invalid option, please try again")
