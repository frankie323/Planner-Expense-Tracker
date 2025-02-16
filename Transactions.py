import sqlite3
def add_expense(date, category, amount, description=""):
  """Add a new expense to the database"""
  conn = sqlite3.connect("expenses.db")
  cursor = conn.cursor()
  cursor.execute('''
                 INSERT INTO expenses (date, category, amount, description)
                 VALUES (?, ?, ?, ?)
                 ''', (date, category, amount, description))
  conn.commit()
  conn.close()
  print("Expense added successfully")
 
  
def view_expenses():
  """View all expenses in the database"""
  conn = sqlite3.connect("expenses.db")
  cursor = conn.cursor()
  cursor.execute('''
                 SELECT * FROM expenses ORDER BY date DESC
                 ''')
  expenses = cursor.fetchall()
  conn.close()
  return expenses

  print("\n === All Expenses ===")
  for expense in expenses:
    print(f"{expense[0]} | Date: {expense[1]} | Category: {expense[2]} | { Amount: expense[3]:.2f} | Description: {expense[4]}")
  print("=====================\n")
  
  
def delete_expense(expense_id):
  """Delete an expense from the database"""
  conn = sqlite3.connect("expenses.db")
  cursor = conn.cursor()
  cursor.execute('''
                 DELETE FROM expenses WHERE id = ?
                 ''', (expense_id,))
  conn.commit()
  conn.close()
  print("Expense deleted successfully")
  
  
def update_expense(expense_id, date, category, amount, description=""):
  """Update an expense in the database"""
  conn = sqlite3.connect("expenses.db")
  cursor = conn.cursor()
  cursor.execute('''
                 UPDATE expenses
                 SET date = ?, category = ?, amount = ?, description = ?
                 WHERE id = ?
                 ''', (date, category, amount, description, expense_id))
  conn.commit()
  conn.close()
  print("Expense updated successfully")
  
  
def search_expenses(category):
  """Search for expenses by category"""
  conn = sqlite3.connect("expenses.db")
  cursor = conn.cursor()
  cursor.execute('''
                  SELECT * FROM expenses WHERE category = ?
                  ''', (category,))
  expenses = cursor.fetchall()
  conn.close()