from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import Usuario
from schemas.mesa import MesaCreate, MesaModify
import crud
from auth import get_current_user
from websocket_manager import manager
import json

router = APIRouter(
    prefix="/mesas",
    tags=["mesas"]
)

@router.get("/")
def obtener_mesas(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_mesas(session)

@router.post("/")
async def crear_mesa(mesa: MesaCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    resultado = crud.crear_mesa(mesa, session)
    await manager.broadcast(json.dumps({"evento": "nueva_mesa", "mesa_id": resultado.id}))
    return resultado

@router.put("/{mesa_id}")
def modificar_mesa(mesa_id: int, mesa: MesaModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_mesa(mesa_id, mesa, session)

@router.delete("/{mesa_id}")
def eliminar_mesa(mesa_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_mesa(mesa_id, session)