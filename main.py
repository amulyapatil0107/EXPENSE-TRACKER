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
    expenses = get_expenses()
    
    if request.method == 'POST':
        item_name = request.form.get('item')
        item_amount = request.form.get('amount')
        item_desc = request.form.get('description', '')
        
        # Add new entry
        expenses.append({
            "name": item_name, 
            "amount": float(item_amount),
            "description": item_desc,
            "date": "2026-03-29" # You can use datetime here later!
        })
        save_expenses(expenses)
        return redirect('/')

    # Calculate Total
    total_spent = sum(item.get('amount', 0) for item in expenses)

    table_rows = ""
    for i, ex in enumerate(expenses):
        table_rows += f"""
        <tr>
            <td>{ex.get('date', '-')}</td>
            <td><b>{ex.get('name', 'Item')}</b><br><small>{ex.get('description', '')}</small></td>
            <td>₹{ex.get('amount')}</td>
            <td>
                <form action="/delete/{i}" method="POST" style="margin:0;">
                    <button type="submit" style="background:#ff4d4d; padding: 5px 8px; font-size: 11px;">Delete</button>
                </form>
            </td>
        </tr>
        """

    return render_template_string(f"""
    <html>
        <head>
            <title>Expense Tracker Pro</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #FF914D; text-align: center; padding: 20px; }}
                .container {{ background: white; padding: 25px; border-radius: 20px; display: inline-block; width: 95%; max-width: 700px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border-bottom: 1px solid #eee; padding: 12px; text-align: left; }}
                th {{ background: #f8f8f8; }}
                .total-box {{ background: #333; color: white; padding: 15px; border-radius: 10px; margin: 20px 0; font-size: 1.2em; }}
                input {{ padding: 10px; margin: 5px; border: 1px solid #ddd; border-radius: 8px; width: 30%; }}
                .btn-add {{ background: #2ecc71; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Expense Dashboard</h1>
                
                <div class="total-box">
                    Total Spent: <b>₹{total_spent}</b>
                </div>

                <table>
                    <tr><th>Date</th><th>Item</th><th>Amount</th><th>Action</th></tr>
                    {table_rows if table_rows else "<tr><td colspan='4'>No expenses recorded.</td></tr>"}
                </table>

                <h3 style="margin-top:30px;">Add New Transaction</h3>
                <form method="POST">
                    <input type="text" name="item" placeholder="Item Name" required>
                    <input type="number" name="amount" placeholder="Amount (₹)" required>
                    <input type="text" name="description" placeholder="Notes (Optional)">
                    <button type="submit" class="btn-add">Add Expense</button>
                </form>
            </div>
        </body>
    </html>
    """)

@app.route('/delete/<int:index>', methods=['POST'])
def delete_expense(index):
    expenses = get_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
