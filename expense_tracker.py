"""Personal Expense Tracker for the IS 3020 final project."""

import csv
from datetime import datetime
from pathlib import Path

DATA_FOLDER = Path(__file__).parent / "data"
DATA_FILE = DATA_FOLDER / "expenses.csv"
FIELDNAMES = ["expense_id", "date", "category", "description", "amount"]


def display_menu():
    """Show the main menu and return the user's choice."""
    print("\n" + "=" * 45)
    print("PERSONAL EXPENSE TRACKER")
    print("=" * 45)
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. View total spending")
    print("4. View totals by category")
    print("5. Search expenses")
    print("6. Delete an expense")
    print("7. View expenses by month")
    print("8. Exit")
    return input("Choose an option (1-8): ").strip()


def load_expenses(file_path=DATA_FILE):
    """Load valid expense records from the CSV file."""
    expenses = []

    if not file_path.exists():
        return expenses

    try:
        with file_path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != FIELDNAMES:
                print("The expense file has the wrong columns. Starting with an empty list.")
                return []

            for row_number, row in enumerate(reader, start=2):
                try:
                    expense_id = int(row["expense_id"])
                    amount = float(row["amount"])
                    datetime.strptime(row["date"], "%Y-%m-%d")

                    if expense_id <= 0 or amount <= 0:
                        raise ValueError

                    expenses.append(
                        {
                            "expense_id": expense_id,
                            "date": row["date"],
                            "category": row["category"].strip(),
                            "description": row["description"].strip(),
                            "amount": amount,
                        }
                    )
                except (TypeError, ValueError):
                    print(f"Skipped an invalid expense on row {row_number}.")
    except OSError:
        print("The expense file could not be opened. Starting with an empty list.")
        return []

    return expenses


def save_expenses(expenses, file_path=DATA_FILE):
    """Save the current list of expenses to the CSV file."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

            for expense in expenses:
                writer.writerow(
                    {
                        "expense_id": expense["expense_id"],
                        "date": expense["date"],
                        "category": expense["category"],
                        "description": expense["description"],
                        "amount": f'{expense["amount"]:.2f}',
                    }
                )
        return True
    except OSError:
        print("The expenses could not be saved. Check the file and try again.")
        return False


def get_valid_date():
    """Ask for a real date in YYYY-MM-DD format."""
    while True:
        date_text = input("Enter the date (YYYY-MM-DD), or press Enter for today: ").strip()

        if date_text == "":
            return datetime.today().strftime("%Y-%m-%d")

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            print("Use a real date in YYYY-MM-DD format, such as 2026-07-28.")


def get_required_text(prompt):
    """Ask for text and do not allow a blank answer."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be left blank.")


def get_positive_amount():
    """Ask for a positive expense amount."""
    while True:
        try:
            amount = float(input("Enter the amount: $").strip())
            if amount <= 0:
                print("The amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Enter the amount as a number, such as 12.50.")


def add_expense(expenses):
    """Create and save a new expense."""
    print("\nAdd an Expense")
    date = get_valid_date()
    category = get_required_text("Enter the category: ").title()
    description = get_required_text("Enter a description: ")
    amount = get_positive_amount()

    next_id = max((expense["expense_id"] for expense in expenses), default=0) + 1
    new_expense = {
        "expense_id": next_id,
        "date": date,
        "category": category,
        "description": description,
        "amount": amount,
    }
    expenses.append(new_expense)

    if save_expenses(expenses):
        print(f"Expense #{next_id} was added and saved.")
    else:
        expenses.remove(new_expense)


def print_expense_table(expenses):
    """Print expenses in a readable table."""
    print("\n" + "-" * 88)
    print(f'{"ID":<5}{"Date":<13}{"Category":<20}{"Description":<32}{"Amount":>12}')
    print("-" * 88)

    for expense in expenses:
        category = expense["category"][:18]
        description = expense["description"][:30]
        print(
            f'{expense["expense_id"]:<5}'
            f'{expense["date"]:<13}'
            f'{category:<20}'
            f'{description:<32}'
            f'${expense["amount"]:>11.2f}'
        )

    print("-" * 88)


def view_expenses(expenses):
    """Display all expenses in date and ID order."""
    if not expenses:
        print("No expenses have been saved yet.")
        return

    sorted_expenses = sorted(
        expenses,
        key=lambda expense: (expense["date"], expense["expense_id"]),
    )
    print_expense_table(sorted_expenses)


def calculate_total(expenses, display=True):
    """Calculate the total amount spent."""
    total = sum(expense["amount"] for expense in expenses)
    if display:
        print(f"\nTotal spent: ${total:.2f}")
    return total


def summarize_by_category(expenses):
    """Display the total amount spent in each category."""
    if not expenses:
        print("No expenses have been saved yet.")
        return

    category_totals = {}
    for expense in expenses:
        category = expense["category"]
        category_totals[category] = category_totals.get(category, 0) + expense["amount"]

    print("\nSpending by Category")
    print("-" * 36)
    for category in sorted(category_totals):
        print(f"{category:<24}${category_totals[category]:>10.2f}")
    print("-" * 36)
    print(f'{"Overall Total":<24}${calculate_total(expenses, display=False):>10.2f}')


def search_expenses(expenses):
    """Search by ID, date, category, or description."""
    if not expenses:
        print("No expenses have been saved yet.")
        return

    search_word = input("Enter an ID, date, category, or search word: ").strip().lower()
    if not search_word:
        print("Enter something to search for.")
        return

    matches = []
    for expense in expenses:
        searchable_text = (
            f'{expense["expense_id"]} {expense["date"]} '
            f'{expense["category"]} {expense["description"]}'
        ).lower()
        if search_word in searchable_text:
            matches.append(expense)

    if matches:
        print(f"\nFound {len(matches)} matching expense(s).")
        print_expense_table(matches)
    else:
        print("No matching expenses were found.")


def delete_expense(expenses):
    """Delete an expense after the user confirms the choice."""
    if not expenses:
        print("No expenses are available to delete.")
        return

    view_expenses(expenses)

    try:
        expense_id = int(input("Enter the expense ID to delete: ").strip())
    except ValueError:
        print("Enter a whole-number expense ID.")
        return

    selected_expense = None
    for expense in expenses:
        if expense["expense_id"] == expense_id:
            selected_expense = expense
            break

    if selected_expense is None:
        print("That expense ID was not found.")
        return

    print(
        f'You selected: {selected_expense["description"]} '
        f'(${selected_expense["amount"]:.2f})'
    )
    confirm = input("Delete this expense? (y/n): ").strip().lower()

    if confirm not in ("y", "yes"):
        print("Delete canceled.")
        return

    expenses.remove(selected_expense)
    if save_expenses(expenses):
        print("Expense deleted.")
    else:
        expenses.append(selected_expense)
        expenses.sort(key=lambda expense: expense["expense_id"])


def filter_by_month(expenses):
    """Show expenses from a month entered as YYYY-MM."""
    if not expenses:
        print("No expenses have been saved yet.")
        return

    month_text = input("Enter a month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month_text, "%Y-%m")
    except ValueError:
        print("Use a real month in YYYY-MM format, such as 2026-07.")
        return

    matches = [
        expense for expense in expenses if expense["date"].startswith(month_text + "-")
    ]

    if not matches:
        print(f"No expenses were found for {month_text}.")
        return

    print(f"\nExpenses for {month_text}")
    print_expense_table(matches)
    print(f"Month total: ${calculate_total(matches, display=False):.2f}")


def main():
    """Load data and run the menu until the user exits."""
    expenses = load_expenses()
    print(f"Loaded {len(expenses)} saved expense(s).")

    while True:
        choice = display_menu()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            calculate_total(expenses)
        elif choice == "4":
            summarize_by_category(expenses)
        elif choice == "5":
            search_expenses(expenses)
        elif choice == "6":
            delete_expense(expenses)
        elif choice == "7":
            filter_by_month(expenses)
        elif choice == "8":
            print("Your expenses have been saved. Goodbye!")
            break
        else:
            print("Choose a number from 1 through 8.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThe program was closed. Saved expenses are still in data/expenses.csv.")
