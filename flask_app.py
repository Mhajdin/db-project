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

# ----------------------------
# Env / Secrets
# ----------------------------
load_dotenv()
W_SECRET = os.getenv("W_SECRET")

# ----------------------------
# Flask App
# ----------------------------
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "supersecret"

# ----------------------------
# Auth init
# ----------------------------
login_manager.init_app(app)
login_manager.login_view = "login"

# ----------------------------
# Helpers
# ----------------------------
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


# ----------------------------
# Webhook (DON'T CHANGE)
# ----------------------------
@app.post("/update_server")
def webhook():
    x_hub_signature = request.headers.get("X-Hub-Signature")
    if is_valid_signature(x_hub_signature, request.data, W_SECRET):
        repo = git.Repo("./mysite")
        origin = repo.remotes.origin
        origin.pull()
        return "Updated PythonAnywhere successfully", 200
    return "Unauthorized", 401


# ----------------------------
# Auth Routes
# ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        user = authenticate(
            request.form.get("username", ""),
            request.form.get("password", "")
        )

        if user:
            login_user(user)
            return redirect(url_for("dbexplorer"))

        error = "Benutzername oder Passwort ist falsch."

    return render_template(
        "auth.html",
        title="In dein Konto einloggen",
        action=url_for("login"),
        button_label="Einloggen",
        error=error,
        footer_text="Noch kein Konto?",
        footer_link_url=url_for("register"),
        footer_link_label="Registrieren",
        show_member_fields=False
    )


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
            error = "Bitte Benutzername und Passwort ausfüllen."
        elif not vorname or not nachname or not email:
            error = "Bitte Vorname, Nachname und E-Mail ausfüllen."
        else:
            ok = register_user(username, password)
            if not ok:
                error = "Benutzername existiert bereits."
            else:
                # Mitglied speichern (falls E-Mail bereits existiert: updaten statt doppelt)
                try:
                    existing = db_read("SELECT mitglied_id FROM mitglied WHERE email=%s", (email,))
                except Exception as e:
                    # Falls Tabelle/Spalten anders sind, sieht man die echte Fehlermeldung
                    return render_template(
                        "auth.html",
                        title="Neues Konto erstellen",
                        action=url_for("register"),
                        button_label="Registrieren",
                        error=f"Datenbankfehler (mitglied): {e}",
                        footer_text="Du hast bereits ein Konto?",
                        footer_link_url=url_for("login"),
                        footer_link_label="Einloggen",
                        show_member_fields=True
                    )

                if existing and len(existing) > 0:
                    db_write(
                        "UPDATE mitglied SET vorname=%s, nachname=%s WHERE email=%s",
                        (vorname, nachname, email)
                    )
                else:
                    db_write(
                        "INSERT INTO mitglied (vorname, nachname, email) VALUES (%s, %s, %s)",
                        (vorname, nachname, email)
                    )

                return redirect(url_for("login"))

    return render_template(
        "auth.html",
        title="Neues Konto erstellen",
        action=url_for("register"),
        button_label="Registrieren",
        error=error,
        footer_text="Du hast bereits ein Konto?",
        footer_link_url=url_for("login"),
        footer_link_label="Einloggen",
        show_member_fields=True
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ----------------------------
# Mitglieder: immer alle anzeigen (ohne Suche)
# ----------------------------
@app.route("/mitglieder", methods=["GET"])
@login_required
def mitglieder():
    rows = db_read(
        "SELECT mitglied_id, vorname, nachname, email FROM mitglied ORDER BY nachname, vorname",
        ()
    )
    return render_template("mitglieder.html", rows=rows)


# ----------------------------
# DB EXPLORER (read-only Anzeige)
# - "todos" wird aus der Tabellenliste entfernt
# - Einfügen nur bei uebung (optional unten im Template)
# ----------------------------
@app.route("/dbexplorer", methods=["GET"])
@login_required
def dbexplorer():
    error = request.args.get("error")
    rows = []
    columns = []

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
    # "todos" ausblenden, weil nicht gebraucht
    tables = [t for t in tables if t.lower() != "todos"]
    tables.sort()

    if selected_table and selected_table in tables:
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


# ----------------------------
# Nur wenn table=uebung: Einfügen erlauben (Übung + Wiederholungen Pflicht, Dauer optional)
# ----------------------------
@app.post("/dbexplorer/insert_uebung")
@login_required
def insert_uebung():
    plan_id = request.form.get("plan_id")
    name = request.form.get("name", "").strip()
    wiederholungen = request.form.get("wiederholungen", "").strip()
    dauer = request.form.get("dauer", "").strip()  # optional

    try:
        plan_id = int(plan_id)
    except (TypeError, ValueError):
        return redirect(url_for("dbexplorer", table="uebung", error="Ungültiger Trainingsplan (plan_id)"))

    if not name:
        return redirect(url_for("dbexplorer", table="uebung", error="Übung darf nicht leer sein"))

    try:
        wiederholungen_int = int(wiederholungen)
        if wiederholungen_int <= 0:
            raise ValueError()
    except ValueError:
        return redirect(url_for("dbexplorer", table="uebung", error="Wiederholungen müssen > 0 sein"))

    if dauer == "":
        dauer_val = None
    else:
        try:
            dauer_val = int(dauer)
            if dauer_val <= 0:
                raise ValueError()
        except ValueError:
            return redirect(url_for("dbexplorer", table="uebung", error="Dauer muss eine positive Zahl sein"))

    db_write(
        "INSERT INTO uebung (plan_id, name, wiederholungen, dauer) VALUES (%s, %s, %s, %s)",
        (plan_id, name, wiederholungen_int, dauer_val)
    )

    return redirect(url_for("dbexplorer", table="uebung"))


# ----------------------------
# App Start
# ----------------------------
if __name__ == "__main__":
    app.run()