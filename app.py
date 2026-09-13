import os
import sqlite3
from datetime import date
from functools import wraps
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "finanzas.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-change-me")
app.config["DATABASE"] = str(DATABASE)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with open(BASE_DIR / "schema.sql", encoding="utf-8") as schema:
        db.executescript(schema.read())
    transaction_columns = {
        row["name"] for row in db.execute("PRAGMA table_info(transactions)").fetchall()
    }
    if "payment_method" not in transaction_columns:
        db.execute(
            "ALTER TABLE transactions ADD COLUMN payment_method TEXT NOT NULL DEFAULT 'cash'"
        )
    if "category_id" not in transaction_columns:
        db.execute("ALTER TABLE transactions ADD COLUMN category_id INTEGER")
    category_columns = {
        row["name"] for row in db.execute("PRAGMA table_info(money_categories)").fetchall()
    }
    if "spent_amount" not in category_columns:
        db.execute(
            "ALTER TABLE money_categories ADD COLUMN spent_amount NUMERIC NOT NULL DEFAULT 0"
        )
    db.commit()


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Inicia sesion para continuar.", "warning")
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


def signed_in_user():
    if "user_id" not in session:
        return None
    return get_db().execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()


def monthly_salary_amount(db, user_id):
    salary = db.execute(
        "SELECT amount FROM monthly_salaries WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return salary["amount"] if salary else 0


@app.context_processor
def inject_user():
    return {"current_user": signed_in_user()}


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Base de datos inicializada.")


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("landing.html")


@app.route("/registro", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not email or "@" not in email:
            flash("Escribe un correo electronico valido.", "error")
        elif len(password) < 8:
            flash("La contrasena debe tener al menos 8 caracteres.", "error")
        else:
            try:
                db = get_db()
                cursor = db.execute(
                    "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                    (email, generate_password_hash(password)),
                )
                db.commit()
                session.clear()
                session["user_id"] = cursor.lastrowid
                flash("Cuenta creada. Bienvenido a AhorraU.", "success")
                return redirect(url_for("dashboard"))
            except sqlite3.IntegrityError:
                flash("Ese correo ya tiene una cuenta.", "error")
    return render_template("auth.html", mode="register")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], request.form.get("password", "")):
            flash("Correo o contrasena incorrectos.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))
    return render_template("auth.html", mode="login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY transaction_date DESC, id DESC LIMIT 8",
        (session["user_id"],),
    ).fetchall()
    goals = db.execute(
        "SELECT * FROM savings_goals WHERE user_id = ? ORDER BY deadline ASC",
        (session["user_id"],),
    ).fetchall()
    salary = db.execute(
        "SELECT amount FROM monthly_salaries WHERE user_id = ?",
        (session["user_id"],),
    ).fetchone()
    money_categories = db.execute(
        "SELECT * FROM money_categories WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],),
    ).fetchall()
    category_total = db.execute(
        "SELECT COALESCE(SUM(amount - spent_amount), 0) AS total FROM money_categories WHERE user_id = ?",
        (session["user_id"],),
    ).fetchone()["total"]
    totals = db.execute(
        """SELECT COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) AS income,
                  COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) AS expense
           FROM transactions WHERE user_id = ?""",
        (session["user_id"],),
    ).fetchone()
    categories = db.execute(
        """SELECT category, SUM(amount) AS total FROM transactions
           WHERE user_id = ? AND type = 'expense' GROUP BY category ORDER BY total DESC LIMIT 5""",
        (session["user_id"],),
    ).fetchall()
    monthly_salary = salary["amount"] if salary else 0
    balance = monthly_salary + totals["income"] - totals["expense"]
    recommendation = build_recommendation(balance, totals["expense"], categories)
    return render_template(
        "dashboard.html", transactions=transactions, goals=goals, totals=totals,
        balance=balance, categories=categories, recommendation=recommendation,
        today=date.today().isoformat(), salary=salary, money_categories=money_categories,
        category_total=category_total,
    )


def build_recommendation(balance, expenses, categories):
    if not expenses:
        return "Registra tu primer gasto para recibir una recomendacion personalizada."
    if balance < 0:
        return "Tus egresos superan tus ingresos. Revisa la categoria con mayor gasto y define un limite semanal."
    if categories:
        return f"Tu categoria de mayor gasto es {categories[0]['category']}. Prueba reducirla un 10% este mes."
    return "Vas bien. Define una meta de ahorro para convertir tu saldo disponible en un objetivo concreto."


@app.post("/transacciones")
@login_required
def add_transaction():
    transaction_type = request.form.get("type")
    payment_method = request.form.get("payment_method")
    category_id = request.form.get("category_id", "")
    try:
        amount = float(request.form.get("amount", "0"))
    except ValueError:
        amount = 0
    category = request.form.get("category", "").strip()
    selected_category_id = None
    if category_id:
        selected_category = get_db().execute(
            "SELECT id, name FROM money_categories WHERE id = ? AND user_id = ?",
            (category_id, session["user_id"]),
        ).fetchone()
        if selected_category is None:
            category_id = ""
        else:
            selected_category_id = selected_category["id"]
            category = selected_category["name"]
    transaction_date = request.form.get("transaction_date", "")
    if transaction_type not in ("income", "expense") or payment_method not in ("cash", "card", "transfer") or amount <= 0 or not category or not transaction_date or (transaction_type == "expense" and not selected_category_id):
        flash("Completa tipo, monto, categoria y fecha correctamente.", "error")
    else:
        db = get_db()
        db.execute(
            "INSERT INTO transactions (user_id, type, amount, category, description, payment_method, category_id, transaction_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (session["user_id"], transaction_type, amount, category, request.form.get("description", "").strip(), payment_method, selected_category_id, transaction_date),
        )
        if transaction_type == "expense":
            db.execute(
                "UPDATE money_categories SET spent_amount = spent_amount + ? WHERE id = ? AND user_id = ?",
                (amount, selected_category_id, session["user_id"]),
            )
        db.commit()
        flash("Transaccion registrada correctamente.", "success")
    return redirect(url_for("dashboard"))


@app.post("/sueldo")
@login_required
def save_salary():
    try:
        amount = float(request.form.get("amount", "0"))
    except ValueError:
        amount = 0
    if amount <= 0:
        flash("Escribe un sueldo mensual mayor que cero.", "error")
    else:
        db = get_db()
        db.execute(
            """INSERT INTO monthly_salaries (user_id, amount) VALUES (?, ?)
               ON CONFLICT(user_id) DO UPDATE SET amount = excluded.amount,
               updated_at = CURRENT_TIMESTAMP""",
            (session["user_id"], amount),
        )
        db.commit()
        flash("Sueldo mensual guardado correctamente.", "success")
    return redirect(url_for("dashboard"))


@app.post("/sueldo/eliminar")
@login_required
def delete_salary():
    db = get_db()
    user_id = session["user_id"]
    deleted = db.execute(
        "DELETE FROM monthly_salaries WHERE user_id = ?",
        (user_id,),
    )
    db.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
    db.execute("DELETE FROM savings_goals WHERE user_id = ?", (user_id,))
    db.execute("DELETE FROM money_categories WHERE user_id = ?", (user_id,))
    db.commit()
    if deleted.rowcount:
        flash("Datos financieros reiniciados. Todo quedo en cero.", "success")
    else:
        flash("Datos financieros reiniciados. Todo quedo en cero.", "success")
    return redirect(url_for("dashboard"))


@app.post("/categorias/guardar")
@login_required
def save_money_category():
    name = request.form.get("name", "").strip()
    try:
        amount = float(request.form.get("amount", "0"))
    except ValueError:
        amount = 0
    salary = monthly_salary_amount(get_db(), session["user_id"])
    if not name or amount <= 0:
        flash("Escribe un nombre y un monto mayor que cero.", "error")
    elif salary and amount > salary:
        flash("Alerta: el monto reservado supera tu sueldo mensual.", "error")
    else:
        db = get_db()
        try:
            db.execute(
                "INSERT INTO money_categories (user_id, name, amount) VALUES (?, ?, ?)",
                (session["user_id"], name, amount),
            )
            db.commit()
            flash("Categoria de ahorro creada.", "success")
        except sqlite3.IntegrityError:
            flash("Ya tienes una categoria con ese nombre.", "error")
    return redirect(url_for("dashboard"))


@app.post("/categorias/<int:category_id>/editar")
@login_required
def edit_money_category(category_id):
    name = request.form.get("name", "").strip()
    try:
        amount = float(request.form.get("amount", "0"))
    except ValueError:
        amount = 0
    salary = monthly_salary_amount(get_db(), session["user_id"])
    if not name or amount <= 0:
        flash("Escribe un nombre y un monto mayor que cero.", "error")
    elif salary and amount > salary:
        flash("Alerta: el monto reservado supera tu sueldo mensual.", "error")
    else:
        db = get_db()
        try:
            updated = db.execute(
                "UPDATE money_categories SET name = ?, amount = ? WHERE id = ? AND user_id = ?",
                (name, amount, category_id, session["user_id"]),
            )
            db.commit()
            if updated.rowcount:
                flash("Categoria actualizada correctamente.", "success")
            else:
                flash("No se encontro esa categoria.", "error")
        except sqlite3.IntegrityError:
            flash("Ya tienes otra categoria con ese nombre.", "error")
    return redirect(url_for("dashboard"))


@app.post("/categorias/<int:category_id>/eliminar")
@login_required
def delete_money_category(category_id):
    db = get_db()
    deleted = db.execute(
        "DELETE FROM money_categories WHERE id = ? AND user_id = ?",
        (category_id, session["user_id"]),
    )
    db.commit()
    if deleted.rowcount:
        flash("Categoria eliminada correctamente.", "success")
    else:
        flash("No se encontro esa categoria.", "error")
    return redirect(url_for("dashboard"))


@app.post("/metas")
@login_required
def add_goal():
    name = request.form.get("name", "").strip()
    deadline = request.form.get("deadline", "")
    try:
        target = float(request.form.get("target_amount", "0"))
    except ValueError:
        target = 0
    if not name or not deadline or target <= 0:
        flash("Completa nombre, monto objetivo y fecha limite.", "error")
    else:
        db = get_db()
        db.execute(
            "INSERT INTO savings_goals (user_id, name, target_amount, deadline) VALUES (?, ?, ?, ?)",
            (session["user_id"], name, target, deadline),
        )
        db.commit()
        flash("Meta de ahorro creada.", "success")
    return redirect(url_for("dashboard"))


@app.post("/transacciones/<int:transaction_id>/eliminar")
@login_required
def delete_transaction(transaction_id):
    db = get_db()
    transaction = db.execute(
        "SELECT amount, type, category_id FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, session["user_id"]),
    ).fetchone()
    deleted = db.execute(
        "DELETE FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, session["user_id"]),
    )
    if transaction and transaction["type"] == "expense" and transaction["category_id"]:
        db.execute(
            "UPDATE money_categories SET spent_amount = spent_amount - ? WHERE id = ? AND user_id = ?",
            (transaction["amount"], transaction["category_id"], session["user_id"]),
        )
    db.commit()
    if deleted.rowcount:
        flash("Monto eliminado correctamente.", "success")
    else:
        flash("No se encontro ese movimiento.", "error")
    return redirect(url_for("dashboard"))


@app.post("/metas/<int:goal_id>/aporte")
@login_required
def contribute_goal(goal_id):
    try:
        amount = float(request.form.get("amount", "0"))
    except ValueError:
        amount = 0
    salary = monthly_salary_amount(get_db(), session["user_id"])
    if amount <= 0:
        flash("El aporte debe ser mayor que cero.", "error")
    elif salary and amount > salary:
        flash("Alerta: el aporte supera tu sueldo mensual.", "error")
    else:
        db = get_db()
        goal = db.execute(
            "SELECT name FROM savings_goals WHERE id = ? AND user_id = ?",
            (goal_id, session["user_id"]),
        ).fetchone()
        if goal is None:
            flash("No se encontro esa meta.", "error")
        else:
            db.execute(
                "UPDATE savings_goals SET current_amount = current_amount + ? WHERE id = ? AND user_id = ?",
                (amount, goal_id, session["user_id"]),
            )
            db.execute(
                "INSERT INTO transactions (user_id, type, amount, category, description, payment_method, category_id, transaction_date) VALUES (?, 'expense', ?, ?, ?, 'cash', NULL, ?)",
                (session["user_id"], amount, goal["name"], f"Aporte a meta: {goal['name']}", date.today().isoformat()),
            )
            db.commit()
            flash("Aporte agregado a la meta y registrado en gastos.", "success")
    return redirect(url_for("dashboard"))


@app.post("/metas/<int:goal_id>/eliminar")
@login_required
def delete_goal(goal_id):
    db = get_db()
    deleted = db.execute(
        "DELETE FROM savings_goals WHERE id = ? AND user_id = ?",
        (goal_id, session["user_id"]),
    )
    db.commit()
    if deleted.rowcount:
        flash("Meta eliminada correctamente.", "success")
    else:
        flash("No se encontro esa meta.", "error")
    return redirect(url_for("dashboard"))


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)
