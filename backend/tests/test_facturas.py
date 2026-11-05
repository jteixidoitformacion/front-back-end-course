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
