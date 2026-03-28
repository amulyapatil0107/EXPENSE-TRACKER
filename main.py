#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    # This tells Flask to look inside your 'templates' folder for the file
    return render_template('index.html') 

# Keep your delete and add logic here too!

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
