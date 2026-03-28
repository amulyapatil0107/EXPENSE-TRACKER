#!/usr/bin/env python3

import os
import json
from flask import Flask

app = Flask(__name__)

# Helper function to read your expenses
def get_expenses():
    file_path = 'expenses.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

@app.route('/')
def home():
    data = get_expenses()
    
    # Create a simple HTML table string
    table_rows = ""
    for item in data:
        table_rows += f"<tr><td>{item.get('name', 'N/A')}</td><td>₹{item.get('amount', 0)}</td></tr>"

    return f"""
    <html>
        <head>
            <title>Expense Dashboard</title>
            <style>
                body {{ font-family: sans-serif; background: #FF914D; text-align: center; padding: 20px; }}
                table {{ margin: auto; background: white; padding: 20px; border-radius: 10px; border-collapse: collapse; width: 80%; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; }}
                th {{ background-color: #333; color: white; }}
            </style>
        </head>
        <body>
            <h1>💰 My Expenses</h1>
            <table>
                <tr><th>Item</th><th>Amount</th></tr>
                {table_rows if table_rows else "<tr><td colspan='2'>No expenses found yet!</td></tr>"}
            </table>
            <p><br><i>Live on Render</i></p>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
