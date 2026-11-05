from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.cliente import get_cliente
from app.models.audit import utcnow
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate, FacturaUpdate


class ClienteNoEncontradoError(Exception):
    pass


def _activas():
    return select(Factura).where(Factura.deleted_at.is_(None))


def _validar_cliente(db: Session, cliente_id: int) -> None:
    if not get_cliente(db, cliente_id):
        raise ClienteNoEncontradoError(cliente_id)


def get_factura(db: Session, factura_id: int) -> Factura | None:
    return db.scalar(_activas().where(Factura.id == factura_id))


def list_facturas(
    db: Session, skip: int = 0, limit: int = 100, cliente_id: int | None = None
) -> list[Factura]:
    query = _activas()
    if cliente_id is not None:
        query = query.where(Factura.cliente_id == cliente_id)
    return list(db.scalars(query.order_by(Factura.id).offset(skip).limit(limit)))


def create_factura(db: Session, data: FacturaCreate, usuario: str) -> Factura:
    _validar_cliente(db, data.cliente_id)
    factura = Factura(
        fecha=data.fecha,
        base=data.base,
        iva=data.iva,
        total=data.base + data.iva,
        cliente_id=data.cliente_id,
        created_by=usuario,
        updated_by=usuario,
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura


def update_factura(db: Session, factura: Factura, data: FacturaUpdate, usuario: str) -> Factura:
    cambios = {k: v for k, v in data.model_dump(exclude_unset=True).items() if v is not None}
    if "cliente_id" in cambios:
        _validar_cliente(db, cambios["cliente_id"])
    for campo, valor in cambios.items():
        setattr(factura, campo, valor)
    factura.total = factura.base + factura.iva
    factura.updated_by = usuario
    factura.updated_at = utcnow()
    db.commit()
    db.refresh(factura)
    return factura


def delete_factura(db: Session, factura: Factura, usuario: str) -> None:
    ahora = utcnow()
    factura.deleted_at = ahora
    factura.deleted_by = usuario
    factura.updated_at = ahora
    factura.updated_by = usuario
    db.commit()
