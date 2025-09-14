from datetime import datetime

import commit
import mysql.connector
from contextlib import contextmanager

"""
Context manager for creating and closing a MySQL database connection and cursor.

- Opens a connection to the 'expense_management_db' database using mysql.connector.
- Provides a dictionary-style cursor (results as dictionaries, not tuples).
- If `commit=True`, commits any changes (INSERT, UPDATE, DELETE) after the block exits.
- Ensures cursor and connection are always closed after use, even if an error occurs.

Usage:
    with get_db_cursor(commit=True) as cursor:
    cursor.execute("SQL_QUERY")
"""
    
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="expense_management_db"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

"""
Fetch all expense records from the 'expenses' table.

- Uses the `get_db_cursor` context manager (read-only mode).
- Executes: SELECT * FROM expenses
- Returns all rows as a list of dictionaries (each dictionary represents a row).
"""
def fetch_all_expenses():
    with get_db_cursor() as cursor:
        sql = "SELECT * FROM expenses"
        cursor.execute(sql)
        expenses = cursor.fetchall()
        return expenses

"""
Fetch expenses for a specific date.

- Takes `exp_date` (date object or ISO string 'YYYY-MM-DD').
- Executes: SELECT * FROM expenses WHERE expense_date = %s
- Uses parameterized query to prevent SQL injection.
- Returns matching expenses as a list of dictionaries.
"""
def fetch_expenses_for_date(exp_date):
    with get_db_cursor() as cursor:
        sql = "SELECT * FROM expenses WHERE expense_date = %s"
        cursor.execute(sql, (exp_date,))
        expense = cursor.fetchall()
        return expense

"""
Insert a new expense record into the 'expenses' table.

- Expects `expense` to be a tuple containing (expense_date, amount, category, notes).
- Executes parameterized INSERT query to add a new expense.
- Uses commit=True to save the transaction.
"""
def insert_expense(expense_date, amount, category, notes):
    with get_db_cursor(commit=True) as cursor:
        query = """
            INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (expense_date, amount, category, notes))

"""
Delete all expenses for a given date.
- Takes `expense_date` (date object or string).
- Executes: DELETE FROM expenses WHERE expense_date = %s
- Uses commit=True to persist deletion.
"""
def delete_expense_for_date(expense_ddate):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date='%s', (expense_date))"
        )

"""
Fetch a summary of expenses grouped by category for a given date range.

- Takes `start_date` and `end_date` as parameters.
- Executes:
    SELECT category, SUM(amount) AS Total
    FROM expenses
    WHERE expense_date BETWEEN %s AND %s
    GROUP BY category;
- Returns list of dictionaries where each dictionary contains:
    { "category": category_name, "Total": summed_amount }
"""
def fetch_expense_summery(start_date, end_date):
    with get_db_cursor(commit=True) as cursor:
        sql = """
            SELECT category, SUM(amount) AS Total
            FROM expenses
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY category;
        """
        cursor.execute(sql, (start_date, end_date))
        data = cursor.fetchall()
        return data

# if __name__ == '__main__':
#     summery = fetch_expense_summery("2024-08-01", "2024-08-05")
#     for expense in summery:
#         print(expense)
