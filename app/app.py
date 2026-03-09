# app/app.py
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Correction : suppression de la clé secrète codée en dur
app.config['SECRET_KEY'] = ''

@app.route('/')
def index():
    return '<h1>Bienvenue sur le lab DevSecOps !</h1>'

@app.route('/search')
def search():
    # Correction : requête SQL paramétrée
    query = request.args.get('q', '')
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (query,))
    return str(cursor.fetchall())

@app.route('/greet')
def greet():
    # Correction : éviter XSS
    name = request.args.get('name', 'World')
    return render_template_string('<h1>Hello {{ name }}!</h1>', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)