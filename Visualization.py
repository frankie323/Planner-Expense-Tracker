import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

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

def visualize_expenses():
  """Visualize expenses by category"""
  expenses = view_expenses()
  df = pd.DataFrame(expenses, columns=["id", "date", "category", "amount", "description"])
  category_totals = df.groupby("category")["amount"].sum()
  plt.figure(figsize=(10, 5))
  sns.barplot(x=category_totals.index, y=category_totals.values)
  plt.title("Total Expenses by Category")
  plt.xlabel("Category")
  plt.ylabel("Total Amount")
  plt.show()
  
def fetch_expense_data():
  """Fetch expense data for visualization"""
  conn = sqlite3.connect("expenses.db")
  df = pd.read_sql_query("SELECT * FROM expenses", conn)
  conn.close()
  return df

def plot_category_distribution():
  """Plot category distribution of expenses"""
  df = fetch_expense_data()
  if df.empty:
    print("No data available to plot")
    return
  
  category_counts = df.groupby("category")["category"].sum()
  plt.figure(figsize=(10, 5))
  plt.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%", startangle=140)
  plt.title("Category Distribution of Expenses")
  plt.ylabel("")
  plt.show()
  
def plot_monthly_expenses():
  """Plot monthly expenses"""
  df = fetch_expense_data()
  if df.empty:
    print("No data available to plot")
    return
  
  df["date"] = pd.to_datetime(df["date"])
  df["month"] = df["date"].dt.strftime("Y-%m") # Convert to Year-Month format
  monthly_totals = df.groupby("month")["amount"].sum()
  plt.figure(figsize=(10, 5))
  sns.barplot(x=monthly_totals.index, y=monthly_totals.values, palette="viridis")
  monthly_totals.plot(kind="bar")
  plt.xticks(rotation=45)
  plt.title("Monthly Expenses")
  plt.xlabel("Month")
  plt.ylabel("Total Amount")
  plt.show()