from datetime import date
from sqlmodel import Session, select, col
from models import Pedido, Producto, EstadoPedido, Salon, Usuario, Rol, Mesa, CategoriaProducto, CategoriaGasto, Gasto, Insumo, DetallePedido, CategoriaInsumo, MovimientoStock, Promocion, PromocionProducto
import schemas
from fastapi import HTTPException
from auth import hashear_password


TRANSICIONES_VALIDAS = {
    1: 2,  # Creado → En preparación
    2: 3,  # En preparación → Listo
    3: 4,  # Listo → Pagado
}


#CRUD DE PRODUCTOS

def obtener_productos(session: Session, categoria_id: int = None):
    statement = select(Producto).where(Producto.activo == True)
    if categoria_id:
        statement = statement.where(Producto.categoria_id == categoria_id)
    resultados = session.exec(statement)
    return resultados.all()

def crear_producto(producto: schemas.ProductoCreate, session: Session):
    nuevo_producto = Producto(**producto.model_dump())
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)
    return nuevo_producto

def modificar_producto(producto_id: int, producto: schemas.ProductoModify, session: Session):
    producto_existente = session.exec(select(Producto).where(Producto.id == producto_id)).first()
    if not producto_existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for attr, value in producto.model_dump(exclude_unset=True).items():
        setattr(producto_existente, attr, value)
    session.add(producto_existente)
    session.commit()
    session.refresh(producto_existente)
    return producto_existente

def eliminar_producto(producto_id: int, session: Session):
    producto_existente = session.exec(select(Producto).where(Producto.id == producto_id)).first()
    if not producto_existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto_existente.activo = False
    session.commit()
    return {"detail": "Producto eliminado"}

#CRUD DE PEDIDOS

def obtener_pedidos(session: Session, mesa_id: int = None):
    statement = select(Pedido).where(Pedido.activo == True)
    if mesa_id:
        statement = statement.where(Pedido.mesa_id == mesa_id)
    resultados = session.exec(statement)
    return resultados.all()



def crear_pedido(pedido: schemas.PedidoCreate, session: Session):
    ultimo_pedido = session.exec(
        select(Pedido)
        .where(Pedido.fecha == date.today())
        .order_by(Pedido.nro_pedido.desc())
    ).first()
    nro_pedido = (ultimo_pedido.nro_pedido + 1) if ultimo_pedido else 1
    nuevo_pedido = Pedido(**pedido.model_dump(), estado_id=1, nro_pedido=nro_pedido)  # Asignar estado "Pendiente" por defecto
    if pedido.mesa_id:
        mesa = session.exec(select(Mesa).where(Mesa.id == pedido.mesa_id)).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")
        if mesa.estado_id != 1:
            raise HTTPException(status_code=400, detail="La mesa ya está ocupada")
        mesa.estado_id = 2  # Cambiar estado de la mesa a "Ocupada"
    session.add(nuevo_pedido)
    session.commit()
    session.refresh(nuevo_pedido)
    return nuevo_pedido

def modificar_pedido(pedido_id: int, pedido: schemas.PedidoModify, session: Session):
    pedido_existente = session.exec(select(Pedido).where(Pedido.id == pedido_id)).first()
    if not pedido_existente:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for attr, value in pedido.model_dump(exclude_unset=True).items():
        setattr(pedido_existente, attr, value)
    session.add(pedido_existente)
    session.commit()
    session.refresh(pedido_existente)
    return pedido_existente

def eliminar_pedido(pedido_id: int, session: Session):
    pedido_existente = session.exec(select(Pedido).where(Pedido.id == pedido_id)).first()
    if not pedido_existente:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido_existente.activo = False
    if pedido_existente.mesa_id:
        mesa = session.exec(select(Mesa).where(Mesa.id == pedido_existente.mesa_id)).first()
        if mesa:
            mesa.estado_id = 1
            session.add(mesa)
    session.add(pedido_existente)
    session.commit()
    session.refresh(pedido_existente)
    return pedido_existente

def cambiar_estado_pedido(pedido_id: int, session: Session):
    pedido_existente = session.exec(select(Pedido).where(Pedido.id == pedido_id)).first()
    if not pedido_existente:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    siguiente_estado = TRANSICIONES_VALIDAS.get(pedido_existente.estado_id)
    if not siguiente_estado:
        raise HTTPException(status_code=400, detail="No existen mas estados")
    else:
        pedido_existente.estado_id = siguiente_estado
    mesa = session.exec(select(Mesa).where(Mesa.id == pedido_existente.mesa_id)).first()
    if siguiente_estado == 4 and pedido_existente.mesa_id:
        pedido_existente.activo = False
        mesa.estado_id = 1
    session.add(pedido_existente)
    session.commit()
    session.refresh(pedido_existente)
    return pedido_existente

def detalle_pedido(pedido_id: int, detalle: schemas.DetallePedidoCreate, session: Session):
    pedido_existente = session.exec(select(Pedido).where(Pedido.id == pedido_id)).first()
    if not pedido_existente:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    producto = session.exec(select(Producto).where(Producto.id == detalle.producto_id)).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    nuevo_detalle = DetallePedido(
    pedido_id=pedido_id,
    producto_id=detalle.producto_id,
    cantidad=detalle.cantidad,
    precio_unitario=producto.precio,
    subtotal=producto.precio * detalle.cantidad
)
    pedido_existente.total += nuevo_detalle.subtotal
    session.add(pedido_existente)
    session.add(nuevo_detalle)
    session.commit()
    session.refresh(nuevo_detalle)
    return nuevo_detalle

def mostrar_detalle_pedido(pedido_id: int, session: Session):
    if not session.exec(select(Pedido).where(Pedido.id == pedido_id)).first():
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    detalles = session.exec(select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)).all()
    return detalles

def eliminar_producto_pedido(detalle_id: int, session: Session):
    detalle_existente = session.exec(select(DetallePedido).where(DetallePedido.id == detalle_id)).first()
    if not detalle_existente:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    pedido_existente = session.exec(select(Pedido).where(Pedido.id == detalle_existente.pedido_id)).first()
    if not pedido_existente:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido_existente.total -= detalle_existente.subtotal
    session.add(pedido_existente)
    session.delete(detalle_existente)
    session.commit()
    return {"detail": "Producto eliminado del pedido"}

def modificar_cantidad_pedido(detalle_id: int, cantidad: int, session: Session):
    detalle_existente = session.exec(select(DetallePedido).where(DetallePedido.id == detalle_id)).first()
    if not detalle_existente:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    pedido_existente = session.exec(select(Pedido).where(Pedido.id == detalle_existente.pedido_id)).first()
    if not pedido_existente:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedido_existente.total -= detalle_existente.subtotal
    detalle_existente.cantidad = cantidad
    detalle_existente.subtotal = detalle_existente.precio_unitario * cantidad
    pedido_existente.total += detalle_existente.subtotal
    session.add(pedido_existente)
    session.add(detalle_existente)
    session.commit()
    session.refresh(detalle_existente)
    return detalle_existente

#CRUD USUARIO

def obtener_usuarios(session: Session):
    statement = select(Usuario)
    resultados = session.exec(statement)
    return resultados.all()

def crear_usuario(usuario: schemas.UsuarioCreate, session: Session):
    nuevo_usuario = Usuario(**usuario.model_dump(exclude={"password"}), password=hashear_password(usuario.password))
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return nuevo_usuario


def modificar_usuario(usuario_id: int, usuario: schemas.UsuarioModify, session: Session):
    usuario_existente = session.exec(select(Usuario).where(Usuario.id == usuario_id)).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    datos = usuario.model_dump(exclude_unset=True)
    if 'password' in datos:
        datos['password'] = hashear_password(datos['password'])
    
    for attr, value in datos.items():
        setattr(usuario_existente, attr, value)
    
    session.add(usuario_existente)
    session.commit()
    session.refresh(usuario_existente)
    return usuario_existente

def eliminar_usuario(usuario_id: int, session: Session):
    usuario_existente = session.exec(select(Usuario).where(Usuario.id == usuario_id)).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario_existente.activo = False
    session.commit()
    return {"detail": "Usuario eliminado"}

#CRUD ROLES

def obtener_roles(session: Session):
    statement = select(Rol)
    resultados = session.exec(statement)
    return resultados.all()

def crear_rol(rol: schemas.RolCreate, session: Session):
    nuevo_rol = Rol(**rol.model_dump())
    session.add(nuevo_rol)
    session.commit()
    session.refresh(nuevo_rol)
    return nuevo_rol

def modificar_rol(rol_id: int, rol: schemas.RolModify, session: Session):
    rol_existente = session.exec(select(Rol).where(Rol.id == rol_id)).first()
    if not rol_existente:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    for attr, value in rol.model_dump(exclude_unset=True).items():
        setattr(rol_existente, attr, value)
    session.add(rol_existente)
    session.commit()
    session.refresh(rol_existente)
    return rol_existente

def eliminar_rol(rol_id: int, session: Session):
    rol_existente = session.exec(select(Rol).where(Rol.id == rol_id)).first()
    if not rol_existente:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    session.delete(rol_existente)
    session.commit()
    return {"detail": "Rol eliminado"}


#CRUD MESAS

def obtener_mesas(session: Session, salon_id: int = None):
    statement = select(Mesa).where(col(Mesa.activo) == True)
    if salon_id:
        statement = statement.where(col(Mesa.salon_id) == salon_id)
    return session.exec(statement).all()

def crear_mesa(mesa: schemas.MesaCreate, session: Session):
    nueva_mesa = Mesa(**mesa.model_dump(), estado_id=1)  # Asignar estado "Disponible" por defecto
    session.add(nueva_mesa)
    session.commit()
    session.refresh(nueva_mesa)
    return nueva_mesa

def modificar_mesa(mesa_id: int, mesa: schemas.MesaModify, session: Session):
    mesa_existente = session.exec(select(Mesa).where(Mesa.id == mesa_id)).first()
    if not mesa_existente:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    for attr, value in mesa.model_dump(exclude_unset=True).items():
        setattr(mesa_existente, attr, value)
    session.add(mesa_existente)
    session.commit()
    session.refresh(mesa_existente)
    return mesa_existente

def eliminar_mesa(mesa_id: int, session: Session):
    mesa_existente = session.exec(select(Mesa).where(Mesa.id == mesa_id)).first()
    if not mesa_existente:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    session.delete(mesa_existente)
    session.commit()
    return {"detail": "Mesa eliminada"}


#CRUD CATEGORIA PRODUCTOS

def obtener_categoria_productos(session: Session):
    statement = select(CategoriaProducto)
    resultados = session.exec(statement)
    return resultados.all()

def crear_categoria_producto(categoria: schemas.CategoriaProductoCreate, session: Session):
    nueva_categoria = CategoriaProducto(**categoria.model_dump())
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria

def modificar_categoria_producto(categoria_id: int, categoria: schemas.CategoriaProductoModify, session: Session):
    categoria_existente = session.exec(select(CategoriaProducto).where(CategoriaProducto.id == categoria_id)).first()
    if not categoria_existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for attr, value in categoria.model_dump(exclude_unset=True).items():
        setattr(categoria_existente, attr, value)
    session.add(categoria_existente)
    session.commit()
    session.refresh(categoria_existente)
    return categoria_existente

def eliminar_categoria_producto(categoria_id: int, session: Session):
    categoria_existente = session.exec(select(CategoriaProducto).where(CategoriaProducto.id == categoria_id)).first()
    if not categoria_existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    session.delete(categoria_existente)
    session.commit()
    return {"detail": "Categoría eliminada"}

def obtener_categorias_por_nivel(session: Session, parent_id: int = None):
    if parent_id is None:
        statement = select(CategoriaProducto).where(CategoriaProducto.parent_id == None)
    else:
        statement = select(CategoriaProducto).where(CategoriaProducto.parent_id == parent_id)
    return session.exec(statement).all()

#CRUD CATEGORIA GASTOS

def obtener_categoria_gastos(session: Session):
    statement = select(CategoriaGasto)
    resultados = session.exec(statement)
    return resultados.all()

def crear_categoria_gasto(categoria: schemas.CategoriaGastoCreate, session: Session):
    nueva_categoria = CategoriaGasto(**categoria.model_dump())
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria

def modificar_categoria_gasto(categoria_id: int, categoria: schemas.CategoriaGastoModify, session: Session):
    categoria_existente = session.exec(select(CategoriaGasto).where(CategoriaGasto.id == categoria_id)).first()
    if not categoria_existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for attr, value in categoria.model_dump(exclude_unset=True).items():
        setattr(categoria_existente, attr, value)
    session.add(categoria_existente)
    session.commit()
    session.refresh(categoria_existente)
    return categoria_existente

def eliminar_categoria_gasto(categoria_id: int, session: Session):
    categoria_existente = session.exec(select(CategoriaGasto).where(CategoriaGasto.id == categoria_id)).first()
    if not categoria_existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    session.delete(categoria_existente)
    session.commit()
    return {"detail": "Categoría eliminada"}


#CRUD GASTOS

def obtener_gastos(session: Session):
    statement = select(Gasto)
    resultados = session.exec(statement)
    return resultados.all()

def crear_gasto(gasto: schemas.GastoCreate, session: Session):
    nuevo_gasto = Gasto(**gasto.model_dump())
    session.add(nuevo_gasto)
    session.commit()
    session.refresh(nuevo_gasto)
    return nuevo_gasto

def modificar_gasto(gasto_id: int, gasto: schemas.GastoModify, session: Session):
    gasto_existente = session.exec(select(Gasto).where(Gasto.id == gasto_id)).first()
    if not gasto_existente:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    for attr, value in gasto.model_dump(exclude_unset=True).items():
        setattr(gasto_existente, attr, value)
    session.add(gasto_existente)
    session.commit()
    session.refresh(gasto_existente)
    return gasto_existente

def eliminar_gasto(gasto_id: int, session: Session):
    gasto_existente = session.exec(select(Gasto).where(Gasto.id == gasto_id)).first()
    if not gasto_existente:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    session.delete(gasto_existente)
    session.commit()
    return {"detail": "Gasto eliminado"}


#CRUD INSUMOS

def obtener_insumos(session: Session):
    statement = select(Insumo)
    resultados = session.exec(statement)
    return resultados.all()

def crear_insumo(insumo: schemas.InsumoCreate, session: Session):
    nuevo_insumo = Insumo(**insumo.model_dump())
    session.add(nuevo_insumo)
    session.commit()
    session.refresh(nuevo_insumo)
    return nuevo_insumo

def modificar_insumo(insumo_id: int, insumo: schemas.InsumoModify, session: Session):
    insumo_existente = session.exec(select(Insumo).where(Insumo.id == insumo_id)).first()
    if not insumo_existente:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    for attr, value in insumo.model_dump(exclude_unset=True).items():
        setattr(insumo_existente, attr, value)
    session.add(insumo_existente)
    session.commit()
    session.refresh(insumo_existente)
    return insumo_existente

def eliminar_insumo(insumo_id: int, session: Session):
    insumo_existente = session.exec(select(Insumo).where(Insumo.id == insumo_id)).first()
    if not insumo_existente:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    session.delete(insumo_existente)
    session.commit()
    return {"detail": "Insumo eliminado"}

# CRUD CATEGORIA INSUMOS

def obtener_categorias_insumo(session: Session, parent_id: int = None):
    if parent_id is None:
        statement = select(CategoriaInsumo).where(CategoriaInsumo.parent_id == None)
    else:
        statement = select(CategoriaInsumo).where(CategoriaInsumo.parent_id == parent_id)
    return session.exec(statement).all()

def crear_categoria_insumo(categoria: schemas.CategoriaInsumoCreate, session: Session):
    nueva = CategoriaInsumo(**categoria.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva

def modificar_categoria_insumo(categoria_id: int, categoria: schemas.CategoriaInsumoModify, session: Session):
    existente = session.exec(select(CategoriaInsumo).where(CategoriaInsumo.id == categoria_id)).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for attr, value in categoria.model_dump(exclude_unset=True).items():
        setattr(existente, attr, value)
    session.add(existente)
    session.commit()
    session.refresh(existente)
    return existente

def eliminar_categoria_insumo(categoria_id: int, session: Session):
    existente = session.exec(select(CategoriaInsumo).where(CategoriaInsumo.id == categoria_id)).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    session.delete(existente)
    session.commit()
    return {"detail": "Categoría eliminada"}

def agregar_compra(insumo_id: int, cantidad: int, session: Session):
    insumo = session.exec(select(Insumo).where(Insumo.id == insumo_id)).first()
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")
    insumo.stock_actual += cantidad
    movimiento = MovimientoStock(
        nro_id=insumo_id,
        id_insumo=insumo_id,
        cantidad=cantidad,
        tipo="entrada"
    )
    session.add(movimiento)
    session.add(insumo)
    session.commit()
    session.refresh(insumo)
    return insumo

# CRUD SALONES

def obtener_salon(session: Session):
    return session.exec(select(Salon)).all()

def crear_salon(salon: schemas.SalonCreate, session: Session):
    nuevo_salon = Salon(**salon.model_dump())
    session.add(nuevo_salon)
    session.commit()
    session.refresh(nuevo_salon)
    return nuevo_salon

def modificar_salon(salon_id: int, salon: schemas.SalonModify, session: Session):
    salon_existente = session.exec(select(Salon).where(Salon.id == salon_id)).first()
    if not salon_existente:
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    for attr, value in salon.model_dump(exclude_unset=True).items():
        setattr(salon_existente, attr, value)
    session.add(salon_existente)
    session.commit()
    session.refresh(salon_existente)
    return salon_existente

def eliminar_salon(salon_id: int, session: Session):
    salon_existente = session.exec(select(Salon).where(Salon.id == salon_id)).first()
    if not salon_existente:
        raise HTTPException(status_code=404, detail="Salón no encontrado")
    session.delete(salon_existente)
    session.commit()
    return {"detail": "Salón eliminado"}

# CRUD PROMOCIONES

def obtener_promociones(session: Session):
    return session.exec(select(Promocion).where(Promocion.activo == True)).all()

def crear_promocion(promocion: schemas.PromocionCreate, session: Session):
    nueva = Promocion(**promocion.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva

def modificar_promocion(promocion_id: int, promocion: schemas.PromocionModify, session: Session):
    existente = session.exec(select(Promocion).where(Promocion.id == promocion_id)).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")
    for attr, value in promocion.model_dump(exclude_unset=True).items():
        setattr(existente, attr, value)
    session.add(existente)
    session.commit()
    session.refresh(existente)
    return existente

def eliminar_promocion(promocion_id: int, session: Session):
    existente = session.exec(select(Promocion).where(Promocion.id == promocion_id)).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")
    existente.activo = False
    session.commit()
    return {"detail": "Promoción eliminada"}

def agregar_producto_promocion(promocion_id: int, detalle: schemas.PromocionProductoCreate, session: Session):
    nuevo = PromocionProducto(promocion_id=promocion_id, **detalle.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

def obtener_productos_promocion(promocion_id: int, session: Session):
    return session.exec(select(PromocionProducto).where(PromocionProducto.promocion_id == promocion_id)).all()