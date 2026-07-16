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
        print("2. Edit an expense")
        print("3. View all expenses")
        print("4. View an expense")
        print("5. View summary")
        print("6. Delete expense")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            expense_date = input("Date (eg, 26-6-2026): ")
            category = input("Category (eg, food): ")
            description = input("Description (eg, Bought breakfast): ")
            amount = to_cents(input("Amount (eg, 25.00): "))

            expense = service.add_expense(category, description, amount, expense_date)
            print("===========Expense added============")
            print(f"Added expense: {expense.to_dict()}")
            print("====================================")

        elif choice == "2":
            expense_id = input("Enter expense id: ")
            updates = {}
            done = False

            while not done:
                field = input(
                    "Enter field to edit (category/description/amount/expense date): "
                )
                normalized_field = field.strip().lower()

                edit_data = input("Enter edit data: ")
                normalized_edit_data = edit_data.strip().lower()

                updates[normalized_field] = normalized_edit_data

                edit_another_field = (
                    input("Do you want to edit another field(Y/N): ").strip().upper()
                )

                if edit_another_field in ("NO", "N"):
                    updated_expense = service.update_expense(expense_id, updates)
                    print("============ Edited expense successfully ============")
                    print(updated_expense.to_dict())
                    done = True
                elif edit_another_field in ("YES", "Y"):
                    done = False
                else:
                    print("Please enter Y or N")

        elif choice == "3":
            print("=============== All Expenses ===============")

            all_expenses = service.list_expenses()

            for expense in all_expenses:
                print(f"expense_id: {expense.expense_id}")
                print(f"Date: {expense.expense_date.strftime("%d-%m-%Y")}")
                print(f"Category: {expense.category}")
                print(f"Description: {expense.description}")
                print(f"Amount: {expense.amount / 100:.2f}")
                print("======================================")

        elif choice == "4":
            expense_id = int(input("Enter expense id: "))
            expense = service.find_by_id(expense_id)
            print("========== Expense ==========")
            print(expense.to_dict())

        elif choice == "5":
            print("1. View total expenses")
            print("2. View total by category")
            print("3. View highest expense")
            print("4. View lowest expense")

            summary_choice = input("Select an option: ")

            if summary_choice == "1":
                total_expenses = reports.total_expenses()
                print(f"Total expenses: {total_expenses / 100:.2f}")

            elif summary_choice == "2":
                category = input("Enter a category: ")
                total_by_category = reports.total_by_category(category)
                print(
                    f"{total_by_category["category"]}: {total_by_category["total"] / 100:.2f}"
                )

            elif summary_choice == "3":
                highest_expense = reports.highest_expense_category()
                print(highest_expense)

            elif summary_choice == "4":
                lowest_expense = reports.lowest_expense_cateory()
                print(lowest_expense)

        elif choice == "6":
            expense_id = input("Enter id: ")
            deleted_expense = service.delete_expense(int(expense_id))

            if deleted_expense:
                print("Expense deleted.")
            else:
                print("Expense not found.")

        elif choice == "7":
            is_running = False

        else:
            print("Invalid option, please try again")
