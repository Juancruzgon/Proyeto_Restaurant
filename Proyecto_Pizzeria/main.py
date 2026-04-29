from fastapi import FastAPI, Depends, HTTPException
from database import get_session
from sqlmodel import Session, select
from models import Pedido, Producto, EstadoPedido, Usuario, Rol
import schemas
import auth
app = FastAPI()



@app.get("/pedidos/")
def obtener_pedidos(session: Session = Depends(get_session)):
    statement = select(Pedido)
    resultados = session.exec(statement)
    return resultados.all()

@app.post("/pedidos/")
def crear_pedido(pedido: schemas.PedidoCreate, session: Session = Depends(get_session)):
    estado = session.exec(select(EstadoPedido).where(EstadoPedido.id == pedido.estado_id)).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    nuevo_pedido = Pedido(**pedido.model_dump())
    session.add(nuevo_pedido)
    session.commit()
    session.refresh(nuevo_pedido)
    return nuevo_pedido

@app.get("/productos")
def obtener_productos(session: Session = Depends(get_session)):
    statement = select(Producto)
    resultados = session.exec(statement)
    return resultados.all()

@app.post("/productos")
def crear_producto(producto: schemas.ProductoCreate, session: Session = Depends(get_session)):
    nuevo_producto = Producto(**producto.model_dump())
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)
    return nuevo_producto

@app.post("/login")
def login(credenciales: schemas.Login, session: Session = Depends(get_session)):
    usuario = session.exec(select(Usuario).where(Usuario.email == credenciales.email)).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not auth.verificar_password(credenciales.password, usuario.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    token = auth.crear_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/usuarios/")
def crear_usuario(usuario: schemas.UsuarioCreate, session: Session = Depends(get_session)):
    # Verificar si el email ya está en uso
    email_existente = session.exec(select(Usuario).where(Usuario.email == usuario.email)).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="Email ya en uso")
    nuevo_usuario = Usuario(**usuario.model_dump(exclude={"password"}), password=auth.hashear_password(usuario.password))
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return nuevo_usuario

@app.post("/roles/")
def crear_rol(rol: schemas.RolCreate, session: Session = Depends(get_session)):
    nuevo_rol = Rol(**rol.model_dump())
    session.add(nuevo_rol)
    session.commit()
    session.refresh(nuevo_rol)
    return nuevo_rol