from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import Usuario
from schemas.producto import ProductoCreate, ProductoModify
import crud
from auth import get_current_user

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)
@router.get("/")
def obtener_productos(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_productos(session)

@router.post("/")
def crear_producto(producto: ProductoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_producto(producto, session)

@router.put("/{producto_id}")
def modificar_producto(producto_id: int, producto: ProductoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_producto(producto_id, producto, session)

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_producto(producto_id, session)

