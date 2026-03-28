#!/usr/bin/env python3

import os
import json
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
FILE_PATH = 'expenses.json'

def get_expenses():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(FILE_PATH, 'w') as f:
        json.dump(expenses, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get data from the form
        item_name = request.form.get('item')
        item_amount = request.form.get('amount')
        
        # Save it
        expenses = get_expenses()
        expenses.append({"name": item_name, "amount": float(item_amount)})
        save_expenses(expenses)
        return redirect('/')

    data = get_expenses()
    table_rows = "".join([f"<tr><td>{ex.get('name', 'Item')}</td><td>₹{ex.get('amount')}</td></tr>" for ex in data])

    return render_template_string(f"""
    <html>
        <head>
            <title>Expense Tracker</title>
            <style>
                body {{ font-family: sans-serif; background: #FF914D; text-align: center; padding: 20px; }}
                .container {{ background: white; padding: 20px; border-radius: 15px; display: inline-block; width: 80%; max-width: 500px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                th, td {{ border-bottom: 1px solid #ddd; padding: 10px; }}
                input {{ padding: 10px; margin: 5px; width: 80%; border-radius: 5px; border: 1px solid #ccc; }}
                button {{ padding: 10px 20px; background: #333; color: white; border: none; border-radius: 5px; cursor: pointer; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>💰 My Expenses</h1>
                <table>
                    <tr><th>Item</th><th>Amount</th></tr>
                    {table_rows if table_rows else "<tr><td colspan='2'>No data</td></tr>"}
                </table>
                <hr>
                <h3>Add New Expense</h3>
                <form method="POST">
                    <input type="text" name="item" placeholder="Item name (e.g. Coffee)" required>
                    <input type="number" name="amount" placeholder="Amount (₹)" required>
                    <button type="submit">Add Expense</button>
                </form>
            </div>
        </body>
    </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
