from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Initialize Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Ensure static directory exists
os.makedirs("static", exist_ok=True)

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
    return render_template("index.html", expenses=expenses)

# Add an expense
@app.route("/add_expense", methods=["POST"])
def add_expense():
    if request.method == "POST":
        try:
            date = request.form.get("date")
            category = request.form.get("category")
            amount = float(request.form.get("amount"))  # Ensure amount is numeric
            description = request.form.get("description")

            new_expense = Expense(date=date, category=category, amount=amount, description=description)
            db.session.add(new_expense)
            db.session.commit()
        except ValueError:
            return "Invalid amount entered. Please enter a valid number.", 400
        except Exception as e:
            db.session.rollback()
            return f"Database error: {str(e)}", 500
        
        return redirect(url_for("index"))
      
    return render_template("add_expense.html")

# Delete an expense  
@app.route("/delete_expense/<int:id>", methods=["POST"])
def delete_expense(id):
    """Delete an expense from the database"""
    expense = Expense.query.get(id)
    if expense:
        try:
            db.session.delete(expense)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"Error deleting expense: {str(e)}", 500
    return redirect(url_for("index"))

# Update an expense
@app.route("/update_expense", methods=["POST"])
def update_expense():
    try:
        expense_id = int(request.form.get("id"))  # Ensure ID is an integer
        expense = Expense.query.get(expense_id)

        if expense:
            expense.date = request.form.get("date")
            expense.category = request.form.get("category")
            expense.amount = float(request.form.get("amount"))  # Ensure numeric
            expense.description = request.form.get("description")
            db.session.commit()
    except ValueError:
        return "Invalid expense ID or amount.", 400
    except Exception as e:
        db.session.rollback()
        return f"Error updating expense: {str(e)}", 500
    
    return redirect(url_for("index"))

# Generate visualization of expenses
@app.route("/report", methods=["GET"])
def report():
    expenses = Expense.query.all()
    if not expenses:
        return "No data available to plot"
    
    # Convert expenses to DataFrame
    df = pd.DataFrame([(exp.category, exp.amount) for exp in expenses], columns=["category", "amount"])
    
    # Aggregate total spending per category
    category_totals = df.groupby("category")["amount"].sum()

    # Plot Pie Chart
    plt.figure(figsize=(10, 5))
    category_totals.plot.pie(autopct="%1.1f%%", startangle=140, colors=sns.color_palette("pastel"))
    plt.title("Spending Breakdown by Category")

    # Save plot
    report_path = os.path.join("static", "expense_report.png")
    plt.savefig(report_path)
    plt.close()

    return render_template("report.html", image_url=report_path)

if __name__ == "__main__":
    app.run(debug=True)


