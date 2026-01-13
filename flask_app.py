# ----------------------------
# Imports (alles ganz oben)
# ----------------------------
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

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

load_dotenv()
W_SECRET = os.getenv("W_SECRET")


app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "supersecret"


login_manager.init_app(app)
login_manager.login_view = "login"



# DON'T CHANGE
def is_valid_signature(x_hub_signature, data, private_key):
    hash_algorithm, github_signature = x_hub_signature.split("=", 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, "latin-1")
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


def _first_value(row):
    """Robustly extract first value from tuple/dict/str returned by db_read."""
    if row is None:
        return None
    if isinstance(row, dict):
        return next(iter(row.values()), None)
    if isinstance(row, (list, tuple)) and len(row) > 0:
        return row[0]
    return row



# DON'T CHANGE
@app.post("/update_server")
def webhook():
    x_hub_signature = request.headers.get("X-Hub-Signature")
    if is_valid_signature(x_hub_signature, request.data, W_SECRET):
        repo = git.Repo("./mysite")
        origin = repo.remotes.origin
        origin.pull()
        return "Updated PythonAnywhere successfully", 200
    return "Unathorized", 401



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

    return render_template(
        "auth.html",
        title="In dein Konto einloggen",
        action=url_for("login"),
        button_label="Einloggen",
        error=error,
        footer_text="Noch kein Konto?",
        footer_link_url=url_for("register"),
        footer_link_label="Registrieren"
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        ok = register_user(username, password)
        if ok:
            return redirect(url_for("login"))

        error = "Benutzername existiert bereits."

    return render_template(
        "auth.html",
        title="Neues Konto erstellen",
        action=url_for("register"),
        button_label="Registrieren",
        error=error,
        footer_text="Du hast bereits ein Konto?",
        footer_link_url=url_for("login"),
        footer_link_label="Einloggen"
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # GET
    if request.method == "GET":
        todos = db_read(
            "SELECT id, content, due FROM todos WHERE user_id=%s ORDER BY due",
            (current_user.id,)
        )
        return render_template("main_page.html", todos=todos)

    # POST
    content = request.form["contents"]
    due = request.form["due_at"]
    db_write(
        "INSERT INTO todos (user_id, content, due) VALUES (%s, %s, %s)",
        (current_user.id, content, due,)
    )
    return redirect(url_for("index"))


@app.post("/complete")
@login_required
def complete():
    todo_id = request.form.get("id")
    db_write(
        "DELETE FROM todos WHERE user_id=%s AND id=%s",
        (current_user.id, todo_id,)
    )
    return redirect(url_for("index"))

@app.route("/dbexplorer", methods=["GET", "POST"])
@login_required
def dbexplorer():
    # 1) Get available tables
    try:
        raw_tables = db_read("SHOW TABLES")
        tables = [str(_first_value(r)) for r in raw_tables]
        tables = [t for t in tables if t]
        tables.sort()
    except Exception as e:
        return render_template(
            "dbexplorer.html",
            tables=[],
            selected_table=None,
            columns=[],
            rows=[],
            limit=50,
            filter_column="",
            filter_value="",
            error=f"Konnte Tabellen nicht laden: {e}",
        )

    # 2) Defaults
    selected_table = request.values.get("table")
    limit_str = request.values.get("limit", "50")
    filter_column = request.values.get("filter_column", "")
    filter_value = request.values.get("filter_value", "")

    # sanitize limit
    try:
        limit = int(limit_str)
        if limit < 1:
            limit = 1
        if limit > 500:
            limit = 500
    except ValueError:
        limit = 50

    rows = []
    columns = []
    error = None

    # 3) If a table is selected, validate and query it
    if selected_table:
        if selected_table not in tables:
            error = "Ungültige Tabelle ausgewählt."
            selected_table = None
        else:
            try:
                # Get column names for dropdown
                raw_cols = db_read(f"SHOW COLUMNS FROM `{selected_table}`")
                columns = []
                for r in raw_cols:
                    if isinstance(r, dict) and "Field" in r:
                        columns.append(r["Field"])
                    else:
                        columns.append(str(_first_value(r)))
                columns = [c for c in columns if c]

                # Optional filter (validated column only)
                where_sql = ""
                params = []

                if filter_column and filter_value:
                    if filter_column not in columns:
                        error = "Ungültige Spalte für Filter."
                    else:
                        where_sql = f" WHERE `{filter_column}` LIKE %s "
                        params.append(f"%{filter_value}%")

                # Main query (read-only)
                sql = f"SELECT * FROM `{selected_table}`{where_sql} LIMIT %s"
                params.append(limit)

                rows = db_read(sql, tuple(params))

            except Exception as e:
                error = f"Fehler beim Laden der Tabelle: {e}"

    # 4) Render
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
if __name__ == "__main__":
    app.run()