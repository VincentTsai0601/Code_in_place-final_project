"""
Personal Budget Tracker
Code in Place Final Project

A console program that lets users view, summarize, and add personal finance
transactions. Data is saved in a CSV file, so it stays available between runs.

Dataset format expected:
Date, Description, Amount, Transaction Type, Category, Account Name, Month
"""

import csv
import os
from datetime import date, datetime

DATA_FILE = "personal_finance.csv"
print("CSV file location:", os.path.abspath(DATA_FILE))
FIELDNAMES = [
    "Date",
    "Description",
    "Amount",
    "Transaction Type",
    "Category",
    "Account Name",
    "Month",
]

# These categories come from the Kaggle personal finance dataset.
EXPENSE_CATEGORIES = [
    "Alcohol & Bars",
    "Auto Insurance",
    "Coffee Shops",
    "Electronics & Software",
    "Entertainment",
    "Fast Food",
    "Food & Dining",
    "Gas & Fuel",
    "Groceries",
    "Haircut",
    "Home Improvement",
    "Internet",
    "Mobile Phone",
    "Mortgage & Rent",
    "Movies & Dvds",
    "Music",
    "Restaurants",
    "Shopping",
    "Television",
    "Utilities",
]

INCOME_CATEGORIES = [
    "Paycheck",
    "Credit Card Payment",
]

ACCOUNT_NAMES = [
    "Checking",
    "Platinum Card",
    "Silver Card",
]

# Optional aliases make text input cleaner.
# For example: food, Food, foods -> Food & Dining
# restaurant, Restaurants -> Restaurants
CATEGORY_ALIASES = {
    "food": "Food & Dining",
    "foods": "Food & Dining",
    "food dining": "Food & Dining",
    "food & dining": "Food & Dining",
    "dining": "Food & Dining",
    "restaurant": "Restaurants",
    "restaurants": "Restaurants",
    "grocery": "Groceries",
    "groceries": "Groceries",
    "coffee": "Coffee Shops",
    "coffee shop": "Coffee Shops",
    "coffee shops": "Coffee Shops",
    "fast food": "Fast Food",
    "gas": "Gas & Fuel",
    "fuel": "Gas & Fuel",
    "rent": "Mortgage & Rent",
    "mortgage": "Mortgage & Rent",
    "phone": "Mobile Phone",
    "mobile": "Mobile Phone",
    "internet": "Internet",
    "shopping": "Shopping",
    "shop": "Shopping",
    "salary": "Paycheck",
    "paycheck": "Paycheck",
    "credit card": "Credit Card Payment",
    "credit card payment": "Credit Card Payment",
}


def clean_text(text):
    """Return a lowercase version of text without extra spaces."""
    return " ".join(text.strip().lower().split())


def normalize_category(user_input, options):
    """Convert messy category input into one official category name."""
    cleaned = clean_text(user_input)

    # 1. Exact match with official category, case-insensitive
    for option in options:
        if clean_text(option) == cleaned:
            return option

    # 2. Match common aliases
    if cleaned in CATEGORY_ALIASES:
        official_category = CATEGORY_ALIASES[cleaned]
        if official_category in options:
            return official_category

    return None


def main():
    print("Welcome to Personal Budget Tracker!")
    ensure_data_file_exists()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_recent_transactions()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            view_expenses_by_category()
        elif choice == "5":
            view_monthly_summary()
        elif choice == "6":
            search_transactions()
        elif choice == "7":
            print_categories()
        elif choice == "8":
            print("Goodbye! Your budget data has been saved.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")


def print_menu():
    print("\n========== Personal Budget Tracker ==========")
    print("1. Add a transaction")
    print("2. View recent transactions")
    print("3. View overall summary")
    print("4. View expenses by category")
    print("5. View monthly summary")
    print("6. Search transactions")
    print("7. View available categories")
    print("8. Exit")


def ensure_data_file_exists():
    """Create the CSV file with headers if it does not exist yet."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_transactions():
    """Read all transactions from the CSV file and return them as dictionaries."""
    transactions = []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("Amount"):
                transactions.append(row)
    return transactions


def write_transaction(transaction):
    """Add one new transaction to the CSV file."""
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(transaction)


def add_transaction():
    print("\n--- Add a New Transaction ---")

    transaction_date = get_date_input("Date (YYYY-MM-DD), or press Enter for today: ")
    description = input("Description: ").strip()
    amount = get_positive_float("Amount: ")
    transaction_type = get_transaction_type()

    if transaction_type == "debit":
        category = choose_from_menu(EXPENSE_CATEGORIES, "expense category")
    else:
        category = choose_from_menu(INCOME_CATEGORIES, "income category")

    account_name = choose_from_menu(ACCOUNT_NAMES, "account")
    month = transaction_date[:7]

    transaction = {
        "Date": transaction_date,
        "Description": description,
        "Amount": f"{amount:.2f}",
        "Transaction Type": transaction_type,
        "Category": category,
        "Account Name": account_name,
        "Month": month,
    }

    write_transaction(transaction)

    print("\nTransaction added successfully!")
    print("Here is the transaction you added:")
    print_transaction_table([transaction])


def get_date_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input == "":
            return str(date.today())
        try:
            datetime.strptime(user_input, "%Y-%m-%d")
            return user_input
        except ValueError:
            print("Please enter the date in YYYY-MM-DD format.")


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return value
            print("Amount must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


def get_transaction_type():
    while True:
        print("\nTransaction type:")
        print("1. Expense")
        print("2. Income")
        choice = input("Choose 1 or 2: ").strip()
        if choice == "1":
            return "debit"
        if choice == "2":
            return "credit"
        print("Invalid choice. Please choose 1 or 2.")


def choose_from_menu(options, label):
    """Let the user choose one item from a numbered list or type a category name."""
    while True:
        print(f"\nChoose a {label}:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = input(
            f"Enter a number from 1 to {len(options)}, or type the name: "
        ).strip()

        # Option 1: user enters a number
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]

        # Option 2: user types words like food, Food, foods, restaurant
        normalized = normalize_category(choice, options)
        if normalized is not None:
            if normalized != choice:
                print(f"Using official category: {normalized}")
            return normalized

        print("Invalid choice. Please choose a number or type a valid category name.")


def print_categories():
    print("\n--- Available Expense Categories ---")
    for category in EXPENSE_CATEGORIES:
        print(f"- {category}")

    print("\n--- Available Income Categories ---")
    for category in INCOME_CATEGORIES:
        print(f"- {category}")

    print("\n--- Available Accounts ---")
    for account in ACCOUNT_NAMES:
        print(f"- {account}")


def view_recent_transactions():
    transactions = read_transactions()
    if len(transactions) == 0:
        print("No transactions found.")
        return

    print("\n--- Recent Transactions ---")
    recent = transactions[-10:]
    print_transaction_table(recent)


def print_transaction_table(transactions):
    print(f"{'Date':<12} {'Type':<8} {'Category':<22} {'Amount':>10}  Description")
    print("-" * 75)
    for row in transactions:
        transaction_type = "Income" if row["Transaction Type"].lower() == "credit" else "Expense"
        amount = float(row["Amount"])
        print(
            f"{row['Date']:<12} "
            f"{transaction_type:<8} "
            f"{row['Category'][:21]:<22} "
            f"${amount:>9.2f}  "
            f"{row['Description']}"
        )


def view_summary():
    transactions = read_transactions()
    total_income = 0
    total_expense = 0

    for row in transactions:
        amount = float(row["Amount"])
        if row["Transaction Type"].lower() == "credit":
            total_income += amount
        elif row["Transaction Type"].lower() == "debit":
            total_expense += amount

    balance = total_income - total_expense

    print("\n--- Overall Summary ---")
    print(f"Number of transactions: {len(transactions)}")
    print(f"Total income:  ${total_income:.2f}")
    print(f"Total expense: ${total_expense:.2f}")
    print(f"Balance:       ${balance:.2f}")

    if total_income > 0:
        spending_rate = total_expense / total_income * 100
        print(f"Spending rate: {spending_rate:.1f}% of income")


def view_expenses_by_category():
    transactions = read_transactions()
    category_totals = {}

    for row in transactions:
        if row["Transaction Type"].lower() == "debit":
            category = row["Category"]
            amount = float(row["Amount"])
            category_totals[category] = category_totals.get(category, 0) + amount

    if len(category_totals) == 0:
        print("No expense data found.")
        return

    print("\n--- Expenses by Category ---")
    sorted_categories = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)
    max_amount = sorted_categories[0][1]

    for category, amount in sorted_categories:
        bar_length = int(amount / max_amount * 30)
        bar = "#" * bar_length
        print(f"{category:<25} ${amount:>10.2f}  {bar}")


def view_monthly_summary():
    month = input("Enter month in YYYY-MM format, for example 2018-01: ").strip()
    transactions = read_transactions()

    total_income = 0
    total_expense = 0
    month_transactions = []

    for row in transactions:
        if row["Month"] == month:
            month_transactions.append(row)
            amount = float(row["Amount"])
            if row["Transaction Type"].lower() == "credit":
                total_income += amount
            elif row["Transaction Type"].lower() == "debit":
                total_expense += amount

    if len(month_transactions) == 0:
        print("No transactions found for that month.")
        return

    print(f"\n--- Monthly Summary for {month} ---")
    print(f"Transactions:  {len(month_transactions)}")
    print(f"Total income:  ${total_income:.2f}")
    print(f"Total expense: ${total_expense:.2f}")
    print(f"Balance:       ${total_income - total_expense:.2f}")


def search_transactions():
    keyword = input("Enter a keyword to search: ").strip().lower()
    transactions = read_transactions()
    results = []

    for row in transactions:
        text = f"{row['Description']} {row['Category']} {row['Account Name']}".lower()
        if keyword in text:
            results.append(row)

    print(f"\n--- Search Results for '{keyword}' ---")
    if len(results) == 0:
        print("No matching transactions found.")
    else:
        print_transaction_table(results[:20])
        if len(results) > 20:
            print(f"Showing first 20 of {len(results)} results.")




if __name__ == "__main__":
    main()
