#app/app.py

from flask import Flask, request, render_template, abort
import sqlite3
import os

app = Flask(__name__)

#Secret stocké dans une variable d’environnement
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")

DATABASE = "db.sqlite3"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return "<h1>Bienvenue sur le lab DevSecOps !</h1>"


@app.route("/search")
def search():

    query = request.args.get("q")

    if not query:
        abort(400, "Paramètre q requis")

    conn = get_db_connection()
    cursor = conn.cursor()

    #Protection contre SQL Injection
    cursor.execute(
        "SELECT * FROM users WHERE name = ?",
        (query,)
    )

    results = cursor.fetchall()
    conn.close()

    return {"results": [dict(row) for row in results]}


@app.route("/greet")
def greet():

    name = request.args.get("name", "World")

    # Flask échappe automatiquement le HTML avec render_template
    return render_template("greet.html", name=name)


if __name__ == "__main__":

    # Debug désactivé en production
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=debug_mode
    )