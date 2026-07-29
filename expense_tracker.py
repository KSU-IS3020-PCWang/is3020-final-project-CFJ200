"""Basic working version of a personal expense tracker."""

import csv
import os

FILE_NAME = "data/expenses.csv"
FIELDS = ["expense_id", "date", "category", "description", "amount"]


def load_expenses():
    expenses = []

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["expense_id"] = int(row["expense_id"])
                row["amount"] = float(row["amount"])
                expenses.append(row)
    except FileNotFoundError:
        pass
    except (ValueError, KeyError):
        print("Some saved data could not be loaded.")

    return expenses


def save_expenses(expenses):
    os.makedirs("data", exist_ok=True)

    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def display_menu():
    print("\nPersonal Expense Tracker")
    print("1. Add expense")
    print("2. View expenses")
    print("3. View total")
    print("4. Totals by category")
    print("5. Search expenses")
    print("6. Delete expense")
    print("7. Exit")
    return input("Choose an option: ").strip()


def add_expense(expenses):
    date = input("Date (YYYY-MM-DD): ").strip()
    category = input("Category: ").strip()
    description = input("Description: ").strip()

    while True:
        try:
            amount = float(input("Amount: $").strip())
            if amount <= 0:
                print("Amount needs to be more than zero.")
            else:
                break
        except ValueError:
            print("Enter a number for the amount.")

    next_id = max([item["expense_id"] for item in expenses], default=0) + 1
    expenses.append(
        {
            "expense_id": next_id,
            "date": date,
            "category": category,
            "description": description,
            "amount": round(amount, 2),
        }
    )
    save_expenses(expenses)
    print("Expense added.")


def view_expenses(expenses):
    if len(expenses) == 0:
        print("No expenses saved.")
        return

    print("\nSaved Expenses")
    for item in expenses:
        print(
            f'{item["expense_id"]}. {item["date"]} | '
            f'{item["category"]} | {item["description"]} | '
            f'${item["amount"]:.2f}'
        )


def calculate_total(expenses):
    total = 0
    for item in expenses:
        total += item["amount"]
    print(f"Total spent: ${total:.2f}")


def summarize_by_category(expenses):
    totals = {}

    for item in expenses:
        category = item["category"]
        if category not in totals:
            totals[category] = 0
        totals[category] += item["amount"]

    if len(totals) == 0:
        print("No expenses saved.")
    else:
        print("\nTotals by Category")
        for category in totals:
            print(f"{category}: ${totals[category]:.2f}")


def search_expenses(expenses):
    word = input("Enter a category or description to search: ").strip().lower()
    matches = []

    for item in expenses:
        if word in item["category"].lower() or word in item["description"].lower():
            matches.append(item)

    if len(matches) == 0:
        print("No matches found.")
    else:
        view_expenses(matches)


def delete_expense(expenses):
    view_expenses(expenses)
    if len(expenses) == 0:
        return

    try:
        expense_id = int(input("Enter the ID to delete: ").strip())
    except ValueError:
        print("Enter a whole number ID.")
        return

    for item in expenses:
        if item["expense_id"] == expense_id:
            expenses.remove(item)
            save_expenses(expenses)
            print("Expense deleted.")
            return

    print("Expense ID not found.")


def main():
    expenses = load_expenses()

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
            print("Goodbye!")
            break
        else:
            print("Choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
