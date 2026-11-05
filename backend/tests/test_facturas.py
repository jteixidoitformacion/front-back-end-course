from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import engine
from app.models import Cliente, Factura

AUDIT = {"created_by": "test", "updated_by": "test"}


def _cliente(db: Session) -> Cliente:
    c = Cliente(nombre="Ana", email="ana@example.com", password_hash="x", **AUDIT)
    db.add(c)
    db.flush()
    return c


def test_tabla_facturas_columnas(client):
    columnas = {c["name"] for c in inspect(engine).get_columns("facturas")}
    assert {"id", "fecha", "base", "iva", "total", "cliente_id",
            "created_at", "created_by", "updated_at", "updated_by",
            "deleted_at", "deleted_by"} <= columnas


def test_crear_factura(client):
    with Session(engine) as db:
        c = _cliente(db)
        f = Factura(fecha=date(2026, 11, 5), base=Decimal("100.10"), iva=Decimal("21.02"),
                    total=Decimal("121.12"), cliente_id=c.id, **AUDIT)
        db.add(f)
        db.commit()
        assert f.id is not None
        assert f.created_at is not None


def test_factura_cliente_inexistente(client):
    with Session(engine) as db:
        db.add(Factura(fecha=date(2026, 11, 5), base=Decimal("10"), iva=Decimal("2.10"),
                       total=Decimal("12.10"), cliente_id=999, **AUDIT))
        with pytest.raises(IntegrityError):
            db.commit()


def test_factura_total_incoherente(client):
    with Session(engine) as db:
        c = _cliente(db)
        db.add(Factura(fecha=date(2026, 11, 5), base=Decimal("10"), iva=Decimal("2.10"),
                       total=Decimal("15"), cliente_id=c.id, **AUDIT))
        with pytest.raises(IntegrityError):
            db.commit()


URL = "/api/v1/facturas"
CLIENTE = {"nombre": "Ana", "email": "ana@example.com", "password": "secreta123"}


def _crear_cliente_api(client, email="ana@example.com") -> int:
    return client.post("/api/v1/clientes", json={**CLIENTE, "email": email}).json()["id"]


def _nueva(cliente_id: int) -> dict:
    return {"fecha": "2026-11-05", "base": "100.10", "iva": "21.02", "cliente_id": cliente_id}


def test_api_crear_y_obtener_factura(client):
    cid = _crear_cliente_api(client)
    r = client.post(URL, json=_nueva(cid), headers={"X-User": "admin"})
    assert r.status_code == 201
    body = r.json()
    assert Decimal(body["total"]) == Decimal("121.12")
    assert body["created_by"] == "admin"
    assert client.get(f"{URL}/{body['id']}").status_code == 200


def test_api_total_lo_calcula_el_servidor(client):
    cid = _crear_cliente_api(client)
    r = client.post(URL, json={**_nueva(cid), "total": "999"})
    assert Decimal(r.json()["total"]) == Decimal("121.12")


def test_api_cliente_inexistente_y_validaciones(client):
    assert client.post(URL, json=_nueva(999)).status_code == 422
    cid = _crear_cliente_api(client)
    assert client.post(URL, json={**_nueva(cid), "base": "-1"}).status_code == 422
    assert client.post(URL, json={**_nueva(cid), "iva": "1.234"}).status_code == 422


def test_api_actualizar_recalcula_total(client):
    cid = _crear_cliente_api(client)
    creada = client.post(URL, json=_nueva(cid), headers={"X-User": "admin"}).json()
    r = client.patch(f"{URL}/{creada['id']}", json={"base": "200"}, headers={"X-User": "editor"})
    assert r.status_code == 200
    body = r.json()
    assert Decimal(body["total"]) == Decimal("221.02")
    assert body["created_by"] == "admin" and body["updated_by"] == "editor"


def test_api_listar_filtrar_y_soft_delete(client):
    c1 = _crear_cliente_api(client)
    c2 = _crear_cliente_api(client, "otro@example.com")
    f1 = client.post(URL, json=_nueva(c1)).json()["id"]
    client.post(URL, json=_nueva(c2))
    assert len(client.get(URL).json()) == 2
    assert len(client.get(URL, params={"cliente_id": c1}).json()) == 1

    assert client.delete(f"{URL}/{f1}", headers={"X-User": "admin"}).status_code == 204
    assert client.get(f"{URL}/{f1}").status_code == 404
    assert len(client.get(URL).json()) == 1
    with Session(engine) as db:
        factura = db.get(Factura, f1)
        assert factura.deleted_at is not None and factura.deleted_by == "admin"
