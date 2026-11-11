"""CodeQL demo: intentionally vulnerable code. Do not deploy."""
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/user")
def user():
    name = request.args.get("name", "")
    conn = sqlite3.connect(":memory:")
    # SQL injection: user input concatenated into the query
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    rows = conn.execute(query).fetchall()
    return {"rows": rows}


@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # Command injection: user input passed to a shell
    out = subprocess.check_output("ping -c 1 " + host, shell=True)
    return {"output": out.decode()}