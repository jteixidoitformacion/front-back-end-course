from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import DbSession, UsuarioAuditoria
from app.crud import factura as crud
from app.models.factura import Factura
from app.schemas.factura import FacturaCreate, FacturaRead, FacturaUpdate

router = APIRouter(prefix="/facturas", tags=["facturas"])


def _obtener_o_404(db: DbSession, factura_id: int) -> Factura:
    factura = crud.get_factura(db, factura_id)
    if not factura:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
    return factura


def _cliente_no_encontrado() -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="El cliente no existe")


@router.get("", response_model=list[FacturaRead])
def listar_facturas(
    db: DbSession,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    cliente_id: int | None = Query(None, gt=0),
):
    return crud.list_facturas(db, skip=skip, limit=limit, cliente_id=cliente_id)


@router.get("/{factura_id}", response_model=FacturaRead)
def obtener_factura(factura_id: int, db: DbSession):
    return _obtener_o_404(db, factura_id)


@router.post("", response_model=FacturaRead, status_code=status.HTTP_201_CREATED)
def crear_factura(data: FacturaCreate, db: DbSession, usuario: UsuarioAuditoria):
    try:
        return crud.create_factura(db, data, usuario)
    except crud.ClienteNoEncontradoError:
        raise _cliente_no_encontrado()


@router.patch("/{factura_id}", response_model=FacturaRead)
def actualizar_factura(factura_id: int, data: FacturaUpdate, db: DbSession, usuario: UsuarioAuditoria):
    factura = _obtener_o_404(db, factura_id)
    try:
        return crud.update_factura(db, factura, data, usuario)
    except crud.ClienteNoEncontradoError:
        raise _cliente_no_encontrado()


@router.delete("/{factura_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura(factura_id: int, db: DbSession, usuario: UsuarioAuditoria):
    factura = _obtener_o_404(db, factura_id)
    crud.delete_factura(db, factura, usuario)
