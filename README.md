# Personal Budget Tracker

![image](https://github.com/VincentTsai0601/Code_in_place-final_project/blob/main/stanford_code_in_place_cover.jfif)

This is a Code in Place final project based on a Kaggle personal finance dataset.
It is a console-based Python program that helps users track income and expenses.

The program can:

1. Add a transaction
2. View recent transactions
3. View an overall income / expense / balance summary
4. View expenses by category
5. View a monthly summary
6. Search transactions
7. View available categories
8. Save all data to a CSV file

## Dataset

The program uses `personal_finance.csv` with these columns:

```text
Date, Description, Amount, Transaction Type, Category, Account Name, Month
```

`Transaction Type` uses the original Kaggle style:

- `debit` means expense
- `credit` means income or money coming into the account

## Category Input Feature

When users add a new transaction, they do not need to type the category manually.
Instead, the program shows a numbered menu of categories from the Kaggle dataset.

Expense categories include:

- Alcohol & Bars
- Auto Insurance
- Coffee Shops
- Electronics & Software
- Entertainment
- Fast Food
- Food & Dining
- Gas & Fuel
- Groceries
- Haircut
- Home Improvement
- Internet
- Mobile Phone
- Mortgage & Rent
- Movies & Dvds
- Music
- Restaurants
- Shopping
- Television
- Utilities

Income categories include:

- Paycheck
- Credit Card Payment

Users also choose an account from:

- Checking
- Platinum Card
- Silver Card

## How to Run

Put `budget_tracker.py` and `personal_finance.csv` in the same folder, then run:

```bash
python budget_tracker.py
```

## Example Project Description

I built a Python console-based Personal Budget Tracker using a Kaggle personal finance dataset. The program allows users to add income and expense records, choose categories from the dataset, save transactions to a CSV file, view financial summaries, search transactions, and analyze spending by category and month.
# Code_in_place-final_project
