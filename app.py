from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

# Create database if not exists
with app.app_context():
    db.create_all()
    
# Home page - view all expenses
@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return redirect(url_for("view_expenses"))

# Add an expense
@app.route("/add_expense", methods=["POST"])
def add_expense():
    if request.method == "POST":
        date = request.form.get["date"]
        category = request.form.get["category"]
        amount = float(request.form.get["amount"])
        description = request.form.get["description"]
        
        new_expense = Expense(date=date, category=category, amount=amount, description=description)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for("index"))
      
    return render_template("add_expense.html")
          
# Delete an expense  
@app.route("/delete_expense", methods=["GET"])
def delete_expense(id):
    """Delete an expense from the database"""
    expense_id = request.args.get("id")
    if expense_id:
        expense = Expense.query.get(expense_id)
        if expense:
            db.session.delete(expense)
            db.session.commit()
            return redirect(url_for("view_expenses"))
    return redirect(url_for("view_expenses"))
  
# Update an expense
@app.route("/update_expense", methods=["POST"])
def update_expense():
    if request.method == "POST":
        expense_id = request.form.get("id")
        date = request.form.get("date")
        category = request.form.get("category")
        amount = float(request.form.get("amount"))
        description = request.form.get("description")
        
        expense = Expense.query.get(expense_id)
        if expense:
            expense.date = date
            expense.category = category
            expense.amount = amount
            expense.description = description
            db.session.commit()
            return redirect(url_for("view_expenses"))
    return redirect(url_for("view_expenses"))
  
# Generate visualization of expenses
@app.route("/report", methods=["GET"])
def report():
    if request.method == "GET":
        expenses = Expense.query.all()
        if not expenses:
            return "No data available to plot"
          
        df = pd.DataFrame([(expense.id, expense.date, expense.category, expense.amount, expense.description) for expense in expenses],
                          columns=["id", "date", "category", "amount", "description"])
        
        # Pie Chart of Category Distribution
        category_totals = df.groupby("category")["category"].sum()
        plt.figure(figsize=(10, 5))
        category_totals.plot.pie(autopct="%1.1f%%", startangle=140, cmap="Pastel1")
        sns.barplot(x=category_totals.index, y=category_totals.values, palette="Blues_r")
        plt.title("Monthly Spending Trends")
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.savefig("static/expense_report.png")
        plt.close()
        return render_template("report.html")
      
    return redirect(url_for("index"))
  
  
if __name__ == "__main__":
    app.run(debug=True)