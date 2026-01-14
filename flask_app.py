from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv
import os
import git
import hmac
import hashlib
from db import db_read, db_write
from auth import login_manager, authenticate, register_user
from flask_login import login_user, logout_user, login_required, current_user
import logging
import re

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# -------------------------------------------------
# Env / Secrets
# -------------------------------------------------
load_dotenv()
W_SECRET = os.getenv("W_SECRET")

# -------------------------------------------------
# Flask App
# -------------------------------------------------
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "supersecret"

# -------------------------------------------------
# Login Manager
# -------------------------------------------------
login_manager.init_app(app)
login_manager.login_view = "login"

# -------------------------------------------------
# Helper Functions
# -------------------------------------------------

# DON'T CHANGE
def is_valid_signature(x_hub_signature, data, private_key):
    hash_algorithm, github_signature = x_hub_signature.split("=", 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, "latin-1")
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


def _first_value(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return next(iter(row.values()), None)
    if isinstance(row, (list, tuple)) and len(row) > 0:
        return row[0]
    return row

# -------------------------------------------------
# Webhook (DON'T CHANGE)
# -------------------------------------------------
@app.post("/update_server")
def webhook():
    x_hub_signature = request.headers.get("X-Hub-Signature")
    if is_valid_signature(x_hub_signature, request.data, W_SECRET):
        repo = git.Repo("./mysite")
        origin = repo.remotes.origin
        origin.pull()
        return "Updated PythonAnywhere successfully", 200
    return "Unauthorized", 401

# -------------------------------------------------
# Auth Routes
# -------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = authenticate(
            request.form["username"],
            request.form["password"]
        )
        if user:
            login_user(user)
            return redirect(url_for("index"))
        error = "Benutzername oder Passwort ist falsch."
    return render_template("auth.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        ok = register_user(
            request.form["username"],
            request.form["password"]
        )
        if ok:
            return redirect(url_for("login"))
        error = "Benutzername existiert bereits."
    return render_template("auth.html", error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# -------------------------------------------------
# Main App Route (Todos – unverändert)
# -------------------------------------------------
@app.route("/")
@login_required
def index():
    todos = db_read(
        "SELECT id, content, due FROM todos WHERE user_id=%s ORDER BY due",
        (current_user.id,)
    )
    return render_template("main_page.html", todos=todos)

# -------------------------------------------------
# DB EXPLORER (READ ONLY)
# -------------------------------------------------
@app.route("/dbexplorer", methods=["GET"])
@login_required
def dbexplorer():
    error = request.args.get("error")
    rows = []
    columns = []

    # URL-Parameter
    selected_table = request.args.get("table")
    limit_raw = request.args.get("limit", "50")
    filter_column = request.args.get("filter_column", "")
    filter_value = request.args.get("filter_value", "")

    # Limit absichern
    try:
        limit = max(1, min(int(limit_raw), 500))
    except ValueError:
        limit = 50

    # Tabellen laden
    raw_tables = db_read("SHOW TABLES", ())
    tables = [str(_first_value(r)) for r in raw_tables if _first_value(r)]
    tables.sort()

    if selected_table and selected_table in tables:
        # Spalten laden
        raw_cols = db_read(f"SHOW COLUMNS FROM `{selected_table}`", ())
        columns = [
            r["Field"] if isinstance(r, dict) else _first_value(r)
            for r in raw_cols
        ]

        where_sql = ""
        params = []

        if filter_column and filter_value and filter_column in columns:
            where_sql = f" WHERE `{filter_column}` LIKE %s "
            params.append(f"%{filter_value}%")

        sql = f"SELECT * FROM `{selected_table}`{where_sql} LIMIT %s"
        params.append(limit)
        rows = db_read(sql, tuple(params))

    return render_template(
        "dbexplorer.html",
        tables=tables,
        selected_table=selected_table,
        columns=columns,
        rows=rows,
        limit=limit,
        filter_column=filter_column,
        filter_value=filter_value,
        error=error,
    )

# -------------------------------------------------
# EINZIGE ERLAUBTE ÄNDERUNG: abo.enddatum
# -------------------------------------------------
@app.post("/dbexplorer/update_enddatum")
@login_required
def update_abo_enddatum():
    abo_id = request.form.get("abo_id")
    enddatum = request.form.get("enddatum", "").strip()

    try:
        abo_id = int(abo_id)
    except (TypeError, ValueError):
        return redirect(url_for("dbexplorer", table="abo", error="Ungültige ID"))

    if enddatum == "":
        db_write("UPDATE abo SET enddatum=NULL WHERE abo_id=%s", (abo_id,))
    else:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", enddatum):
            return redirect(
                url_for("dbexplorer", table="abo", error="Datum muss YYYY-MM-DD sein")
            )
        db_write(
            "UPDATE abo SET enddatum=%s WHERE abo_id=%s",
            (enddatum, abo_id)
        )

    return redirect(url_for("dbexplorer", table="abo"))

# -------------------------------------------------
# App Start
# -------------------------------------------------
if __name__ == "__main__":
    app.run()

    