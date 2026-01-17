from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv
import os
import hmac
import hashlib
import git
import logging

from db import db_read, db_write
from auth import login_manager, authenticate, register_user
from flask_login import login_user, logout_user, login_required

logging.basicConfig(level=logging.DEBUG)

load_dotenv()
W_SECRET = os.getenv("W_SECRET")

app = Flask(__name__)
app.secret_key = "supersecret"
app.config["DEBUG"] = True

login_manager.init_app(app)
login_manager.login_view = "login"


def is_valid_signature(x_hub_signature, data, private_key):
    if not x_hub_signature or not private_key:
        return False
    parts = x_hub_signature.split("=", 1)
    if len(parts) != 2:
        return False
    hash_algorithm, github_signature = parts
    algorithm = getattr(hashlib, hash_algorithm, None)
    if algorithm is None:
        return False
    mac = hmac.new(private_key.encode("latin-1"), msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


def _first_value(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return next(iter(row.values()), None)
    if isinstance(row, (list, tuple)) and len(row) > 0:
        return row[0]
    return row


@app.post("/update_server")
def webhook():
    x_hub_signature = request.headers.get("X-Hub-Signature")
    if is_valid_signature(x_hub_signature, request.data, W_SECRET):
        repo = git.Repo("./mysite")
        repo.remotes.origin.pull()
        return "OK", 200
    return "Unauthorized", 401


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = authenticate(username, password)
        if user:
            login_user(user)
            return redirect(url_for("mitglieder"))
        error = "Benutzername oder Passwort ist falsch."
    return render_template("auth.html", error=error, show_member_fields=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        vorname = request.form.get("vorname", "").strip()
        nachname = request.form.get("nachname", "").strip()
        email = request.form.get("email", "").strip()

        if not username or not password:
            error = "Benutzername und Passwort sind Pflicht."
        elif not vorname or not nachname or not email:
            error = "Vorname, Nachname und E-Mail sind Pflicht."
        else:
            ok = register_user(username, password)
            if not ok:
                error = "Benutzername existiert bereits."
            else:
                try:
                    db_write(
                        "INSERT INTO mitglied (vorname, nachname, email) VALUES (%s, %s, %s)",
                        (vorname, nachname, email),
                    )
                    return redirect(url_for("login"))
                except Exception as e:
                    error = f"Datenbankfehler: {e}"

    return render_template("auth.html", error=error, show_member_fields=True)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/mitglieder")
@login_required
def mitglieder():
    rows = db_read("SELECT * FROM mitglied ORDER BY nachname, vorname", ())
    return render_template("mitglieder.html", rows=rows)


@app.route("/dbexplorer")
@login_required
def dbexplorer():
    error = request.args.get("error")
    selected_table = request.args.get("table")
    limit_raw = request.args.get("limit", "50")
    filter_column = request.args.get("filter_column", "")
    filter_value = request.args.get("filter_value", "")

    try:
        limit = max(1, min(int(limit_raw), 500))
    except ValueError:
        limit = 50

    raw_tables = db_read("SHOW TABLES", ())
    tables = [str(_first_value(r)) for r in raw_tables if _first_value(r)]
    tables = [t for t in tables if t.lower() != "todos"]
    tables.sort()

    rows = []
    columns = []

    if selected_table and selected_table in tables:
        raw_cols = db_read(f"SHOW COLUMNS FROM `{selected_table}`", ())
        columns = [r["Field"] if isinstance(r, dict) else _first_value(r) for r in raw_cols]

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





    