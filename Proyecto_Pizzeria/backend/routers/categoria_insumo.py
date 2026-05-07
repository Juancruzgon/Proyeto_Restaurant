from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import Usuario
from schemas.categoria_insumo import CategoriaInsumoCreate, CategoriaInsumoModify
import crud
from auth import get_current_user

router = APIRouter(
    prefix="/categorias-insumos",
    tags=["categorias-insumos"]
)

@router.get("/")
def obtener_categorias_insumo(parent_id: int = None, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_categorias_insumo(session, parent_id)
@router.post("/")
def crear_categoria_insumo(categoria: CategoriaInsumoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_categoria_insumo(categoria, session)

@router.put("/{categoria_id}")
def modificar_categoria_insumo(categoria_id: int, categoria: CategoriaInsumoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_categoria_insumo(categoria_id, categoria, session)

@router.delete("/{categoria_id}")
def eliminar_categoria_insumo(categoria_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_categoria_insumo(categoria_id, session)