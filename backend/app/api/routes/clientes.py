from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DbSession, UsuarioAuditoria
from app.crud import cliente as crud
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["clientes"])


def _obtener_o_404(db: DbSession, cliente_id: int) -> Cliente:
    cliente = crud.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


def _email_duplicado() -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")


@router.get("", response_model=list[ClienteRead])
def listar_clientes(
    db: DbSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    return crud.list_clientes(db, skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteRead)
def obtener_cliente(cliente_id: int, db: DbSession):
    return _obtener_o_404(db, cliente_id)


@router.post("", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def crear_cliente(data: ClienteCreate, db: DbSession, usuario: UsuarioAuditoria):
    try:
        return crud.create_cliente(db, data, usuario)
    except crud.EmailDuplicadoError:
        raise _email_duplicado()


@router.patch("/{cliente_id}", response_model=ClienteRead)
def actualizar_cliente(cliente_id: int, data: ClienteUpdate, db: DbSession, usuario: UsuarioAuditoria):
    cliente = _obtener_o_404(db, cliente_id)
    try:
        return crud.update_cliente(db, cliente, data, usuario)
    except crud.EmailDuplicadoError:
        raise _email_duplicado()


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int, db: DbSession, usuario: UsuarioAuditoria):
    cliente = _obtener_o_404(db, cliente_id)
    crud.delete_cliente(db, cliente, usuario)
