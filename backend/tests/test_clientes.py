from app.core.security import verify_password
from app.db.database import SessionLocal
from app.models.cliente import Cliente

URL = "/api/v1/clientes"
NUEVO = {"nombre": "Ana", "email": "Ana@Example.com", "password": "secreta123", "telefono": "+34 600 000 000"}


def test_crear_y_obtener_cliente(client):
    r = client.post(URL, json=NUEVO, headers={"X-User": "admin"})
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "ana@example.com"
    assert body["created_by"] == "admin" and body["updated_by"] == "admin"
    assert "password" not in body and "password_hash" not in body

    r = client.get(f"{URL}/{body['id']}")
    assert r.status_code == 200
    assert r.json()["nombre"] == "Ana"


def test_password_se_guarda_hasheada(client):
    cliente_id = client.post(URL, json=NUEVO).json()["id"]
    with SessionLocal() as db:
        cliente = db.get(Cliente, cliente_id)
        assert cliente.password_hash != NUEVO["password"]
        assert verify_password(NUEVO["password"], cliente.password_hash)


def test_email_duplicado(client):
    client.post(URL, json=NUEVO)
    r = client.post(URL, json={**NUEVO, "email": "ana@example.com"})
    assert r.status_code == 409


def test_validaciones(client):
    assert client.post(URL, json={**NUEVO, "email": "no-es-email"}).status_code == 422
    assert client.post(URL, json={**NUEVO, "password": "corta"}).status_code == 422


def test_actualizar_cliente_registra_auditoria(client):
    creado = client.post(URL, json=NUEVO, headers={"X-User": "admin"}).json()
    r = client.patch(f"{URL}/{creado['id']}", json={"telefono": "611111111"}, headers={"X-User": "editor"})
    assert r.status_code == 200
    body = r.json()
    assert body["telefono"] == "611111111"
    assert body["created_by"] == "admin"
    assert body["updated_by"] == "editor"
    assert body["updated_at"] >= creado["updated_at"]


def test_soft_delete(client):
    cliente_id = client.post(URL, json=NUEVO).json()["id"]
    r = client.delete(f"{URL}/{cliente_id}", headers={"X-User": "admin"})
    assert r.status_code == 204
    assert client.get(f"{URL}/{cliente_id}").status_code == 404
    assert client.get(URL).json() == []

    with SessionLocal() as db:
        cliente = db.get(Cliente, cliente_id)
        assert cliente.deleted_at is not None and cliente.deleted_by == "admin"

    # El email queda libre tras el borrado lógico.
    assert client.post(URL, json=NUEVO).status_code == 201


def test_listar_y_404(client):
    client.post(URL, json=NUEVO)
    client.post(URL, json={**NUEVO, "email": "otro@example.com"})
    assert len(client.get(URL).json()) == 2
    assert client.get(f"{URL}/999").status_code == 404
