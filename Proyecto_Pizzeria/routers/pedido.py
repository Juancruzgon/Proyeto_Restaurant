import os
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models import Usuario
from schemas.pedido import PedidoCreate, PedidoModify, DetallePedidoCreate
import crud
from auth import get_current_user
from websocket_manager import manager
from prynter import imprimir_comanda
import json

router = APIRouter(
    prefix="/pedidos",
    tags=["pedidos"]
)

@router.get("/")
def obtener_pedidos(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_pedidos(session)

@router.post("/")
async def crear_pedido(pedido: PedidoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    resultado = crud.crear_pedido(pedido, session)
    await manager.broadcast(json.dumps({
        "evento": "nuevo_pedido", 
        "pedido_id": resultado.id,
        "mesa_id": resultado.mesa_id
    }))
    detalles = crud.mostrar_detalle_pedido(resultado.id, session)
    imprimir_comanda(resultado, detalles, os.getenv("PRINTER_IP", "192.168.1.100"))
    return resultado

@router.put("/{pedido_id}")
def modificar_pedido(pedido_id: int, pedido: PedidoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_pedido(pedido_id, pedido, session)

@router.delete("/{pedido_id}")
async def eliminar_pedido(pedido_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    resultado = crud.eliminar_pedido(pedido_id, session)
    await manager.broadcast(json.dumps({"evento": "eliminar_pedido", "pedido_id": pedido_id, "mesa_id": resultado.mesa_id}))
    return resultado

@router.put("/{pedido_id}/estado")
async def cambiar_estado_pedido(pedido_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    resultado = crud.cambiar_estado_pedido(pedido_id, session)
    await manager.broadcast(json.dumps({"evento": "estado_pedido", "pedido_id": pedido_id, "estado_id": resultado.estado_id}))
    return resultado    

@router.post("/{pedido_id}/detalle")
async def agregar_detalle_pedido(pedido_id: int, detalle: DetallePedidoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    resultado = crud.detalle_pedido(pedido_id, detalle, session)
    await manager.broadcast(json.dumps({"evento": "detalle_agregado", "pedido_id": pedido_id, "producto_id": detalle.producto_id, "cantidad": detalle.cantidad}))
    return resultado

@router.get("/{pedido_id}/detalle")
def mostrar_detalle_pedido(pedido_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.mostrar_detalle_pedido(pedido_id, session)

@router.delete("/{pedido_id}/detalle/{detalle_id}")
async def eliminar_producto_pedido(pedido_id: int, detalle_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    resultado = crud.eliminar_producto_pedido(detalle_id, session)
    await manager.broadcast(json.dumps({"evento": "Producto_eliminado", "pedido_id": pedido_id, "detalle_id": detalle_id}))
    return resultado

@router.put("/{pedido_id}/detalle/{detalle_id}")
async def modificar_cantidad_pedido(pedido_id: int, detalle_id: int, cantidad: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    resultado = crud.modificar_cantidad_pedido(detalle_id, cantidad, session)
    await manager.broadcast(json.dumps({"evento": "Producto_modificado", "pedido_id": pedido_id, "detalle_id": detalle_id, "nueva_cantidad": cantidad}))
    return resultado
