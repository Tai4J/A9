"""CodeQL demo: the fixed version of the vulnerable code."""
import re
import sqlite3
import subprocess  # noqa: S404 (used safely below, no shell)

from flask import Flask, abort, request

app = Flask(__name__)
HOST_PATTERN = re.compile(r"^[A-Za-z0-9.-]{1,253}$")


@app.route("/user")
def user():
    name = request.args.get("name", "")
    conn = sqlite3.connect(":memory:")
    # Fixed: parameterized query, the driver escapes the value
    rows = conn.execute(
        "SELECT * FROM users WHERE name = ?", (name,)
    ).fetchall()
    return {"rows": rows}


@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # Fixed: validate input with an allowlist, no shell, argument list
    if not HOST_PATTERN.fullmatch(host):
        abort(400)
    result = subprocess.run(  # noqa: S603,S607 (validated input, no shell)
        ["ping", "-c", "1", host], capture_output=True, text=True, check=False
    )
    return {"output": result.stdout}
