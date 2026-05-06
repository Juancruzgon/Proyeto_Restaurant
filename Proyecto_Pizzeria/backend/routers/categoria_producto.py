from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import Usuario
from schemas.categoria_producto import CategoriaProductoCreate, CategoriaProductoModify
import crud
from auth import get_current_user

router = APIRouter(
    prefix="/categorias-productos",
    tags=["categorias-productos"]
)

@router.get("/")
def obtener_categorias_productos(parent_id: int = None, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_categorias_por_nivel(session, parent_id)
@router.post("/")
def crear_categoria_producto(categoria: CategoriaProductoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_categoria_producto(categoria, session)

@router.put("/{categoria_id}")
def modificar_categoria_producto(categoria_id: int, categoria: CategoriaProductoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_categoria_producto(categoria_id, categoria, session)

@router.delete("/{categoria_id}")
def eliminar_categoria_producto(categoria_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_categoria_producto(categoria_id, session)
