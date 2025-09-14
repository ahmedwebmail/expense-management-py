import commit
import mysql.connector
from contextlib import contextmanager

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

def fetch_all():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        return expenses

def fetch_expenses_for_date(exp_date):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE date=%s", (exp_date))
        expense = cursor.fetchall()
        return expense

def insert_expense(expense):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)"
        )

def delete_expense_for_date(expense_ddate):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date='%s', (expense_date))"
        )

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
