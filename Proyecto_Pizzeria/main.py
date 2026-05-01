from fastapi import FastAPI, Depends, HTTPException
from database import get_session
from sqlmodel import Session, select
from models import Usuario
import schemas
from auth import oauth2_scheme, verificar_token, verificar_password, crear_token
from fastapi.security import OAuth2PasswordRequestForm 
import crud

app = FastAPI()


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> Usuario:
    payload = verificar_token(token)
    email = payload.get("sub")
    usuario = session.exec(select(Usuario).where(Usuario.email == email)).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    usuario = session.exec(select(Usuario).where(Usuario.email == form_data.username)).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not verificar_password(form_data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = crear_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}

#Endopints Pedidos

@app.get("/pedidos/")
def obtener_pedidos(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_pedidos(session)

@app.post("/pedidos/")
def crear_pedido(pedido: schemas.PedidoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_pedido(pedido, session)

@app.put("/pedidos/{pedido_id}")
def modificar_pedido(pedido_id: int, pedido: schemas.PedidoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_pedido(pedido_id, pedido, session)

@app.delete("/pedidos/{pedido_id}")
def eliminar_pedido(pedido_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_pedido(pedido_id, session)


#Endopoints Productos

@app.get("/productos")
def obtener_productos(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_productos(session)

@app.post("/productos")
def crear_producto(producto: schemas.ProductoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_producto(producto, session)

@app.put("/productos/{producto_id}")
def modificar_producto(producto_id: int, producto: schemas.ProductoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_producto(producto_id, producto, session)

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_producto(producto_id, session)


#Endpoints Usuario

@app.post("/usuarios/")
def crear_usuario(usuario: schemas.UsuarioCreate, session: Session = Depends(get_session)):
    return crud.crear_usuario(usuario, session)

@app.get("/usuarios/")
def obtener_usuarios(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_usuarios(session)

@app.put("/usuarios/{usuario_id}")
def modificar_usuario(usuario_id: int, usuario: schemas.UsuarioModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_usuario(usuario_id, usuario, session)

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_usuario(usuario_id, session)

#Endpoints Roles

@app.post("/roles/")
def crear_rol(rol: schemas.RolCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_rol(rol, session)

@app.get("/roles/")
def obtener_roles(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_roles(session)

@app.put("/roles/{rol_id}")
def modificar_rol(rol_id: int, rol: schemas.RolModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_rol(rol_id, rol, session)

@app.delete("/roles/{rol_id}")
def eliminar_rol(rol_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_rol(rol_id, session)

#ENDPOINTS MESAS

@app.get("/mesas/")
def obtener_mesas(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_mesas(session)

@app.post("/mesas/")
def crear_mesa(mesa: schemas.MesaCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_mesa(mesa, session)

@app.put("/mesas/{mesa_id}")
def modificar_mesa(mesa_id: int, mesa: schemas.MesaModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_mesa(mesa_id, mesa, session)

@app.delete("/mesas/{mesa_id}")
def eliminar_mesa(mesa_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_mesa(mesa_id, session)

#ENDOPOINTS CATEGORIAS_PRODUCTOS

@app.get("/categorias-productos/")
def obtener_categorias_productos(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_categoria_productos(session)

@app.post("/categorias-productos/")
def crear_categoria_producto(categoria: schemas.CategoriaProductoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_categoria_producto(categoria, session)

@app.put("/categorias-productos/{categoria_id}")
def modificar_categoria_producto(categoria_id: int, categoria: schemas.CategoriaProductoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_categoria_producto(categoria_id, categoria, session)

@app.delete("/categorias-productos/{categoria_id}")
def eliminar_categoria_producto(categoria_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_categoria_producto(categoria_id, session)

#ENDPOINTS CATEGORIA_GASTOS

@app.get("/categorias-gastos/")
def obtener_categorias_gastos(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_categoria_gastos(session)

@app.post("/categorias-gastos/")
def crear_categoria_gasto(categoria: schemas.CategoriaGastoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_categoria_gasto(categoria, session)

@app.put("/categorias-gastos/{categoria_id}")
def modificar_categoria_gasto(categoria_id: int, categoria: schemas.CategoriaGastoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_categoria_gasto(categoria_id, categoria, session)

@app.delete("/categorias-gastos/{categoria_id}")
def eliminar_categoria_gasto(categoria_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_categoria_gasto(categoria_id, session)

#ENDOPOINTS GASTOS

@app.get("/gastos/")
def obtener_gastos(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_gastos(session)

@app.post("/gastos/")
def crear_gasto(gasto: schemas.GastoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_gasto(gasto, session)

@app.put("/gastos/{gasto_id}")
def modificar_gasto(gasto_id: int, gasto: schemas.GastoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_gasto(gasto_id, gasto, session)

@app.delete("/gastos/{gasto_id}")
def eliminar_gasto(gasto_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_gasto(gasto_id, session)

#ENDPOINTS INSUMOS

@app.get("/insumos/")
def obtener_insumos(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.obtener_insumos(session)

@app.post("/insumos/")
def crear_insumo(insumo: schemas.InsumoCreate, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.crear_insumo(insumo, session)

@app.put("/insumos/{insumo_id}")
def modificar_insumo(insumo_id: int, insumo: schemas.InsumoModify, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.modificar_insumo(insumo_id, insumo, session)

@app.delete("/insumos/{insumo_id}")
def eliminar_insumo(insumo_id: int, session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    return crud.eliminar_insumo(insumo_id, session)