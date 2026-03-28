#!/usr/bin/env python3

import os
from flask import Flask

# 1. Initialize the Flask Web Server
app = Flask(__name__)

# 2. Define the Home Page (This is what the Live Link will show)
@app.route('/')
def home():
    return """
    <html>
        <head><title>Expense Tracker Live</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>💰 Expense Tracker is Live!</h1>
            <p>Your Python project has been successfully deployed to Render.</p>
            <p style="color: gray;">Status: Running on Port 10000</p>
        </body>
    </html>
    """

# 3. The Entry Point for Render
if __name__ == "__main__":
    # Render assigns a port dynamically. We must use it to stay 'Live'.
    port = int(os.environ.get("PORT", 10000))
    
    # host='0.0.0.0' is required to make the server accessible externally
    app.run(host='0.0.0.0', port=port)
