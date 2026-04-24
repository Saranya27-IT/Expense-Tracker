from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

@app.route("/")
def index():
    expenses = load_expenses()
    total = sum(e["amount"] for e in expenses)
    category_totals = {}
    for e in expenses:
        category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]
    return render_template("index.html", expenses=expenses, total=total, category_totals=category_totals)

@app.route("/add", methods=["POST"])
def add():
    expenses = load_expenses()
    new_expense = {
        "id": int(datetime.now().timestamp() * 1000),
        "title": request.form["title"],
        "amount": float(request.form["amount"]),
        "category": request.form["category"],
        "date": request.form["date"]
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    return redirect(url_for("index"))

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    expenses = load_expenses()
    expenses = [e for e in expenses if e["id"] != expense_id]
    save_expenses(expenses)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)