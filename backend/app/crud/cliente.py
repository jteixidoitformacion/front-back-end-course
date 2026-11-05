from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.audit import utcnow
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class EmailDuplicadoError(Exception):
    pass


def _activos():
    return select(Cliente).where(Cliente.deleted_at.is_(None))


def get_cliente(db: Session, cliente_id: int) -> Cliente | None:
    return db.scalar(_activos().where(Cliente.id == cliente_id))


def get_cliente_por_email(db: Session, email: str) -> Cliente | None:
    return db.scalar(_activos().where(func.lower(Cliente.email) == email.lower()))


def list_clientes(db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
    return list(db.scalars(_activos().order_by(Cliente.id).offset(skip).limit(limit)))


def create_cliente(db: Session, data: ClienteCreate, usuario: str) -> Cliente:
    email = data.email.lower()
    if get_cliente_por_email(db, email):
        raise EmailDuplicadoError(email)
    cliente = Cliente(
        nombre=data.nombre,
        email=email,
        telefono=data.telefono,
        password_hash=hash_password(data.password),
        created_by=usuario,
        updated_by=usuario,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def update_cliente(db: Session, cliente: Cliente, data: ClienteUpdate, usuario: str) -> Cliente:
    cambios = data.model_dump(exclude_unset=True)
    if "email" in cambios and cambios["email"] is not None:
        cambios["email"] = cambios["email"].lower()
        existente = get_cliente_por_email(db, cambios["email"])
        if existente and existente.id != cliente.id:
            raise EmailDuplicadoError(cambios["email"])
    if "password" in cambios:
        password = cambios.pop("password")
        if password is not None:
            cliente.password_hash = hash_password(password)
    for campo, valor in cambios.items():
        if campo in ("nombre", "email") and valor is None:
            continue
        setattr(cliente, campo, valor)
    cliente.updated_by = usuario
    cliente.updated_at = utcnow()
    db.commit()
    db.refresh(cliente)
    return cliente


def delete_cliente(db: Session, cliente: Cliente, usuario: str) -> None:
    ahora = utcnow()
    cliente.deleted_at = ahora
    cliente.deleted_by = usuario
    cliente.updated_at = ahora
    cliente.updated_by = usuario
    db.commit()
