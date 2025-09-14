from datetime import date
from fastapi import  FastAPI, Body, HTTPException
import db_helper
from typing import List
from pydantic import BaseModel

"""
GetSingleExpense: Defines the structure of a single expense record 
returned to the client (amount, category, notes).
"""
class GetSingleExpense(BaseModel):
    amount: float
    category: str
    notes: str

"""
SaveExpense: Defines the structure of an expense entry provided 
by the client when creating a new record (expense_date, amount, 
category, notes).
"""
class SaveExpense(BaseModel):
    expense_date: date
    amount: float
    category: str
    notes: str
    
    
app = FastAPI()

"""
GET /expense/{exp_date}:
* Input: A specific date (exp_date).
* Output: A list of expenses recorded on that date, formatted 
    according to the GetSingleExpense model.
* Behavior: Fetches expense records from the database helper 
    function `fetch_expenses_for_date`.
"""
@app.get("/expense/{exp_date}", response_model=List[GetSingleExpense])
async def get_expense(exp_date: date):
    try:
        expense = db_helper.fetch_expenses_for_date(exp_date)
        return expense
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

"""
POST /save-expense:
* Input: An expense object defined by the SaveExpense model.
* Output: A success message on successful insertion.
* Behavior: Inserts a new expense record into the database using 
    the `insert_expense` function from the database helper.
    Returns HTTP 400 with error details if insertion fails.

Error Handling:
* The POST endpoint raises an HTTPException with status code 400 
    if any issue occurs during expense insertion.
"""
@app.post("/save-expense")
async def save_expense(expenses: SaveExpense):
    try:
        db_helper.insert_expense(expenses.expense_date, expenses.amount, expenses.category, expenses.notes)
        return {"message": "Expense inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))