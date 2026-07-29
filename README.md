# IS 3020 Final Project

## Student and Project Information

- Student name: Christopher Forrester-Jack
- GitHub username: CFJ200
- Project title: Personal Expense Tracker
- Application purpose: This program gives college students a simple way to record purchases and see where their money is going. It organizes expenses and calculates totals so small purchases are easier to notice.

## How to Run the Application

1. Open the project folder in PyCharm.
2. Make sure Python 3 is selected as the project interpreter.
3. Open `expense_tracker.py`.
4. Click the green Run button.
5. Choose a menu number and follow the prompts.

The program only uses Python's standard library, so no extra packages are needed. Keep the `data` folder in the project because the application reads and writes `data/expenses.csv`.

## Major Features

- Add an expense with a date, category, description, and amount
- View all saved expenses in a readable table
- Calculate total spending
- View totals by category
- Search by ID, date, category, or description
- Delete an expense after confirming the choice
- Filter expenses by month and view the monthly total
- Save expenses to a CSV file and load them when the program opens
- Handle invalid dates, amounts, menu choices, and damaged CSV rows without crashing

## Python Concepts Used

The application uses functions to separate the major tasks. Expenses are stored in a list of dictionaries while the program is running. Conditionals control the menu choices and input checks. A while loop keeps the menu running, and for loops display, search, and total the records. The program also uses CSV file persistence and try/except blocks for invalid input and file-related errors.

## Data Files

`data/expenses.csv` stores the saved expense records. Each row is one purchase and contains these fields:

- `expense_id`: A unique whole-number ID
- `date`: The purchase date in YYYY-MM-DD format
- `category`: The spending category
- `description`: A short explanation of the purchase
- `amount`: The purchase amount stored as a decimal number

## Testing Summary

I tested adding multiple expenses, entering an invalid date, entering text instead of an amount, viewing the full list, calculating the total, viewing category totals, searching, filtering by month, deleting an expense, and closing and reopening the program to confirm the CSV data still loaded. I also tested the program with an empty CSV file and an invalid CSV row so it would not end with an unhandled error.
