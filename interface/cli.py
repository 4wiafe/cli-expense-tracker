from storage.expense_storage import ExpenseStorage
from services.expense_service import ExpenseService
from storage.category_storage import CategoryStorage
from services.category_service import CategoryService
from storage.salary_storage import SalaryStorage
from services.salary_service import SalaryService
from storage.budget_storage import BudgetStorage
from services.budget_service import BudgetService
from reports.reports import Reports
from storage.user_storage import UserStorage
from services.user_service import UserService


def login_or_signup() -> None:
    user_storage = UserStorage()
    user_service = UserService(user_storage)

    print("========== Login/Sign-up ==========")
    print("1. Sign-up")
    print("2. Login")

    option = input("Select an option: ")

    if option == "1":
        name = input("Enter your name: ").strip()
        email = input("Enter your email address: ").strip()
        password = input("Enter your password").strip()
        contact = int(input("Enter your number: "))

        user = user_service.add_user(name, email, password, contact)

        if user:
            print("Welcome")
            run_cli()

        else:
            print("Something went wrong. Please try again.")

    elif option == "2":
        user_id = int(input("Enter user id: "))
        user = user_service.get_user(user_id)

        if user_id == user["user_id"]:
            print("Welcome back.")
            run_cli()

        else:
            print("Invalid user id. Please try again.")

    else:
        print("Invalid option. Please try again.")


def run_cli() -> None:
    expense_storage = ExpenseStorage()
    category_storage = CategoryStorage()
    category_service = CategoryService(category_storage)
    expense_service = ExpenseService(expense_storage, category_service)
    salary_storage = SalaryStorage()
    salary_service = SalaryService(salary_storage)
    budget_storage = BudgetStorage()
    budget_service = BudgetService(budget_storage, category_service)
    reoprts = Reports(expense_storage, budget_storage, category_service)

    is_running = True

    print("========== EXPENSE TRACKER ==========")

    while is_running:
        print("1. Expenses")
        print("2. Salary")
        print("3. Budget")
        print("4. Reports")
        print("5. Exit")

        option = input("Select an option: ")

        if option == "1":
            show_expense_menu(expense_service)

        elif option == "2":
            show_salary_menu(salary_service)

        elif option == "3":
            show_budget_menu(budget_service)

        elif option == "4":
            show_reports(reoprts)

        elif option == "5":
            is_running = False

        else:
            print("Invalid option. Please try again.")


def show_expense_menu(expense_service: ExpenseService) -> None:
    print("1. Add expense")
    print("2. Edit expense")
    print("3. View all expenses")
    print("4. View expense")
    print("5. Delete expense")
    print("6. Back")

    option = input("Select an option: ")

    if option == "1":
        user_id = int(input("Enter user_id: "))
        category_name = input(
            "Select one of these category options (Food, Transportation, Entertainment, Bills, Donation, Education, Health, Household, Remittance, Shopping, Savings, Others): "
        ).strip()
        description = input("Add a description(eg. I bought lunch): ").strip()
        amount = int(input("Enter amount (eg. 50): "))
        date = input("Expense date(15-06-2026): ").strip()

        expense = expense_service.add_expense(
            user_id, category_name, description, amount, date
        )

        print(expense)

    elif option == "2":
        user_id = int(input("Enter user id: "))
        expense_id = int(input("Enter expense id: "))
        updates = {}

        is_running = True

        while is_running:
            edit_field = input(
                "Enter field to edit (category, description, amount, date): "
            ).strip()
            edit_value = input("Enter edit value: ")

            if edit_field == "amount":
                updates[edit_field] = int(edit_value)
            else:
                updates[edit_field] = edit_value.strip()

            edit_another_field = input("Edit another field? (y/n): ").strip().lower()

            if edit_another_field == "n" or edit_another_field == "no":
                edited_expense = expense_service.update_expense(
                    user_id, expense_id, updates
                )

                print(edited_expense)
                is_running = False

            elif edit_another_field == "y" or edit_another_field == "yes":
                is_running = True

            else:
                print("Invalid option. Please try again.")
                is_running = True

    elif option == "3":
        user_id = int(input("Enter user id: "))
        all_expenses = expense_service.list_all_expenses(user_id)

        for expense in all_expenses:
            print(expense)

    elif option == "4":
        user_id = int(input("Enter user id: "))
        expense_id = int(input("Enter expense id: "))

        expense = expense_service.find_expense_by_id(user_id, expense_id)

        print(expense)

    elif option == "5":
        user_id = int(input("Enter user id: "))
        expense_id = int(input("Enter expense id: "))

        deleted_expense = expense_service.delete_expense(user_id, expense_id)

        if deleted_expense:
            print("Expense deleted successfully.")
        else:
            print("Failed to delete expense. Please try again.")

    elif option == "6":
        return

    else:
        print("Invalid option. Please try again.")


def show_salary_menu(salary_service: SalaryService) -> None:
    print("1. Add salary")
    print("2. Edit salary")
    print("3. View salary")
    print("4. Delete salary")
    print("5. Back")

    option = input("Select an opion: ")

    if option == "1":
        user_id = int(input("Enter user id: "))
        amount = int(input("Enter amount: "))
        month = int(input("Enter month from 1 - 12: "))
        year = int(input("Enter year (eg. 2026): "))

        salary = salary_service.add_salary(user_id, amount, month, year)

        print(salary)

    elif option == "2":
        user_id = int(input("Enter user id: "))
        salary_id = int(input("Enter salary id: "))
        updates = {}

        is_running = True

        while is_running:
            edit_field = input(
                "Enter field field to edit (amount, month(1-12), year): "
            ).strip()
            edit_value = int(input("Enter edit value: "))

            updates[edit_field] = edit_value

            edit_another_field = input("Edit another field? (y/n): ").lower()

            if edit_another_field == "n" or edit_another_field == "no":
                edited_salary = salary_service.update_salary(
                    user_id, salary_id, updates
                )

                print(edited_salary)

                is_running = False

            elif edit_another_field == "y" or edit_another_field == "yes":
                is_running = True

            else:
                print("Invalid option. Please try again.")
                is_running = True

    elif option == "3":
        user_id = int(input("Enter user id: "))
        salary_id = int(input("Enter salary id: "))

        salary = salary_service.get_salary(user_id, salary_id)

        print(salary)

    elif option == "4":
        user_id = int(input("Enter user id: "))
        salary_id = int(input("Enter salary id: "))

        deleted_salary = salary_service.delete_salary(user_id, salary_id)

        if deleted_salary:
            print("Salary deleted successfully.")
        else:
            print("Failed to delete salary. Please try again.")

    elif option == "5":
        return

    else:
        print("Invalid option. Please try again.")


def show_budget_menu(budget_service: BudgetService) -> None:
    print("1. Add budget")
    print("2. Edit budget")
    print("3. View budget")
    print("4. Delete budget")
    print("5. Back")

    option = input("Select an option: ")

    if option == "1":
        user_id = int(input("Enter user id: "))
        category_name = input(
            "Select one of these category options (Food, Transportation, Entertainment, Bills, Donation, Education, Health, Household, Remittance, Shopping, Savings, Others):  "
        ).strip()
        amount = int(input("Enter amount: "))
        month = int(input("Enter month from 1 - 12: "))
        year = int(input("Enter year (eg. 2026): "))

        budget = budget_service.add_budget(user_id, category_name, amount, month, year)

        print(budget)

    elif option == "2":
        user_id = int(input("Enter user id: "))
        budget_id = int(input("Enter budget id: "))
        updates = {}

        is_running = True

        while is_running:
            edit_field = (
                input(
                    "Enter field to edit (category name, amount, month(1-12), year(eg. 2026))"
                )
                .strip()
                .lower()
            )
            edit_value = input("Enter edit value: ")

            if edit_field == "amount" or edit_field == "month" or edit_field == "year":
                updates[edit_field] = int(edit_value)
            else:
                updates[edit_field] = edit_value

            edit_another_field = input("Edit another field? (y/n): ")

            if edit_another_field == "n" or edit_another_field == "no":
                edited_budget = budget_service.update_budget(
                    user_id, budget_id, updates
                )

                print(edited_budget)

                is_running = False

            elif edit_another_field == "y" or edit_another_field == "yes":
                is_running = True

            else:
                print("Invalid option. Please try again.")
                is_running = True

    elif option == "3":
        user_id = int(input("Enter user id: "))
        budget_id = int(input("Enter budget id: "))

        budget = budget_service.get_budget(user_id, budget_id)

        print(budget)

    elif option == "4":
        user_id = int(input("Enter user id: "))
        budget_id = int(input("Enter budget"))

        deleted_budget = budget_service.delete_budget(user_id, budget_id)

        if deleted_budget:
            print("Budget deleted successfully.")
        else:
            print("Failed to delete budget. Please try again.")

    elif option == "5":
        return

    else:
        print("Invalid option. Please try again.")


def show_reports(reports: Reports) -> None:
    print("1. View total spending")
    print("2. View spending by category")
    print("3. View all spending by each category")
    print("4. View highest spending category")
    print("5. View lowest spnding category")
    print("6. View budget spending")
    print("7. Back")

    option = input("Select an option: ")

    if option == "1":
        user_id = int(input("Enter user id: "))

        total_spending = reports.get_total_expenses(user_id)

        print(total_spending)

    elif option == "2":
        user_id = int(input("Enter user id: "))
        category_name = input("Enter category name: ")

        category_spending = reports.get_spending_by_category(user_id, category_name)

        print(category_spending)

    elif option == "3":
        user_id = int(input("Enter user id: "))

        all_category_spendings = reports.get_all_category_spending(user_id)

        for category_spending in all_category_spendings:
            print(category_spending)

    elif option == "4":
        user_id = int(input("Enter user id: "))

        highest_sepnding_category = reports.get_highest_spending_category(user_id)

        for spending in highest_sepnding_category:
            print(spending)

    elif option == "5":
        user_id = int(input("Enter user id: "))

        lowest_sepnding_category = reports.get_lowest_spending_category(user_id)

        for spending in lowest_sepnding_category:
            print(spending)

    elif option == "6":
        user_id = int(input("Enter user_id: "))

        budget_spendings = reports.get_budget_spending(user_id)

        for spending in budget_spendings:
            print(spending)

    elif option == "7":
        return

    else:
        print("Invalid option. Please try again.")
