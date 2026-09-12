import pytest

from app import app, get_db


@pytest.fixture()
def client(tmp_path):
    app.config.update(TESTING=True, DATABASE=str(tmp_path / "test.db"), SECRET_KEY="test")
    with app.test_client() as client:
        with app.app_context():
            from app import init_db
            init_db()
        yield client


def test_register_and_dashboard(client):
    response = client.post("/registro", data={"email": "ana@example.com", "password": "password123"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Tu panorama financiero" in response.data


def test_transaction_is_saved(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/categorias/guardar", data={"name": "Comida", "amount": "100000"})
    with app.app_context():
        category_id = get_db().execute("SELECT id FROM money_categories").fetchone()["id"]
    response = client.post("/transacciones", data={"type": "expense", "amount": "25000", "category_id": category_id, "payment_method": "cash", "transaction_date": "2026-09-11", "description": "Almuerzo"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Transaccion registrada correctamente" in response.data
    with app.app_context():
        row = get_db().execute("SELECT amount FROM transactions").fetchone()
        assert row["amount"] == 25000
        category = get_db().execute("SELECT spent_amount FROM money_categories").fetchone()
        assert category["spent_amount"] == 25000


def test_transaction_saves_payment_method(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/categorias/guardar", data={"name": "Trabajo", "amount": "100000"})
    with app.app_context():
        category_id = get_db().execute("SELECT id FROM money_categories").fetchone()["id"]
    response = client.post("/transacciones", data={"type": "income", "amount": "100000", "category_id": category_id, "payment_method": "card", "transaction_date": "2026-09-11"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Tarjeta" in response.data
    with app.app_context():
        row = get_db().execute("SELECT payment_method FROM transactions").fetchone()
        assert row["payment_method"] == "card"


def test_transaction_can_be_deleted(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/categorias/guardar", data={"name": "Comida", "amount": "100000"})
    with app.app_context():
        category_id = get_db().execute("SELECT id FROM money_categories").fetchone()["id"]
    client.post("/transacciones", data={"type": "expense", "amount": "25000", "category_id": category_id, "payment_method": "cash", "transaction_date": "2026-09-11"})
    with app.app_context():
        transaction_id = get_db().execute("SELECT id FROM transactions").fetchone()["id"]
    response = client.post(f"/transacciones/{transaction_id}/eliminar", follow_redirects=True)
    assert response.status_code == 200
    assert b"Monto eliminado correctamente" in response.data
    with app.app_context():
        category = get_db().execute("SELECT spent_amount FROM money_categories").fetchone()
        assert category["spent_amount"] == 0


def test_goal_accepts_contribution(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/metas", data={"name": "Viaje", "target_amount": "500000", "deadline": "2026-12-20"})
    with app.app_context():
        goal_id = get_db().execute("SELECT id FROM savings_goals").fetchone()["id"]
    response = client.post(f"/metas/{goal_id}/aporte", data={"amount": "50000"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Aporte agregado a la meta" in response.data
    with app.app_context():
        goal = get_db().execute("SELECT current_amount FROM savings_goals").fetchone()
        assert goal["current_amount"] == 50000
        expense = get_db().execute("SELECT amount, category, description FROM transactions").fetchone()
        assert expense["amount"] == 50000
        assert expense["category"] == "Viaje"
        assert expense["description"] == "Aporte a meta: Viaje"


def test_goal_can_be_deleted(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/metas", data={"name": "Viaje", "target_amount": "500000", "deadline": "2026-12-20"})
    with app.app_context():
        goal_id = get_db().execute("SELECT id FROM savings_goals").fetchone()["id"]
    response = client.post(f"/metas/{goal_id}/eliminar", follow_redirects=True)
    assert response.status_code == 200
    assert b"Meta eliminada correctamente" in response.data
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) AS total FROM savings_goals").fetchone()["total"] == 0


def test_monthly_salary_is_saved_separately(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    response = client.post("/sueldo", data={"amount": "1500000"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Sueldo mensual guardado correctamente" in response.data
    with app.app_context():
        salary = get_db().execute("SELECT amount FROM monthly_salaries").fetchone()
        transactions = get_db().execute("SELECT COUNT(*) AS total FROM transactions").fetchone()
        assert salary["amount"] == 1500000
        assert transactions["total"] == 0


def test_monthly_salary_is_included_in_available_balance(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    response = client.post("/sueldo", data={"amount": "700000"}, follow_redirects=True)
    assert b"$ 700.000" in response.data


def test_saved_category_is_not_an_expense(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    response = client.post("/categorias/guardar", data={"name": "Arriendo", "amount": "300000"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Arriendo" in response.data
    assert b"Categoria de ahorro creada" in response.data
    with app.app_context():
        category = get_db().execute("SELECT amount FROM money_categories").fetchone()
        transactions = get_db().execute("SELECT COUNT(*) AS total FROM transactions").fetchone()
        assert category["amount"] == 300000
        assert transactions["total"] == 0


def test_total_categories_shows_available_category_money(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/categorias/guardar", data={"name": "Comida", "amount": "100000"})
    response = client.get("/dashboard")
    assert b"Total categor" in response.data
    assert b"$ 100.000" in response.data


def test_saved_category_can_be_edited(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/categorias/guardar", data={"name": "Arriendo", "amount": "300000"})
    with app.app_context():
        category_id = get_db().execute("SELECT id FROM money_categories").fetchone()["id"]
    response = client.post(f"/categorias/{category_id}/editar", data={"name": "Casa", "amount": "350000"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Categoria actualizada correctamente" in response.data
    with app.app_context():
        category = get_db().execute("SELECT name, amount FROM money_categories").fetchone()
        assert category["name"] == "Casa"
        assert category["amount"] == 350000


def test_category_over_salary_is_rejected(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/sueldo", data={"amount": "700000"})
    response = client.post("/categorias/guardar", data={"name": "Arriendo", "amount": "700001"}, follow_redirects=True)
    assert b"supera tu sueldo mensual" in response.data
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) AS total FROM money_categories").fetchone()["total"] == 0


def test_category_can_be_deleted(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/categorias/guardar", data={"name": "Comida", "amount": "100000"})
    with app.app_context():
        category_id = get_db().execute("SELECT id FROM money_categories").fetchone()["id"]
    response = client.post(f"/categorias/{category_id}/eliminar", follow_redirects=True)
    assert response.status_code == 200
    assert b"Categoria eliminada correctamente" in response.data
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) AS total FROM money_categories").fetchone()["total"] == 0


def test_goal_contribution_over_salary_is_rejected(client):
    client.post("/registro", data={"email": "ana@example.com", "password": "password123"})
    client.post("/sueldo", data={"amount": "700000"})
    client.post("/metas", data={"name": "Viaje", "target_amount": "1000000", "deadline": "2026-12-20"})
    with app.app_context():
        goal_id = get_db().execute("SELECT id FROM savings_goals").fetchone()["id"]
    response = client.post(f"/metas/{goal_id}/aporte", data={"amount": "700001"}, follow_redirects=True)
    assert b"supera tu sueldo mensual" in response.data
    with app.app_context():
        goal = get_db().execute("SELECT current_amount FROM savings_goals").fetchone()
        assert goal["current_amount"] == 0
