# app/app.py
import os
from flask import Flask, request, render_template_string
import sqlite3
from markupsafe import escape

app = Flask(__name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback_dev_key')

@app.route('/')
def index():
    return '<h1>Bienvenue sur le lab DevSecOps !</h1>'

@app.route('/search')
def search():
    query = request.args.get('q', '')

    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE name = ?", (query,))

    return str(cursor.fetchall())

@app.route('/greet')
def greet():
    name = request.args.get('name', 'World')
    return f'<h1>Hello {escape(name)}!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)