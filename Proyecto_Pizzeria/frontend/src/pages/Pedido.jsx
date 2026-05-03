import { useState, useEffect, use } from 'react'
import { useParams } from 'react-router-dom'
import { getPedidosPorMesa, getDetallePedido, getProductos, cambiarEstadoPedido, eliminarDetalle, agregarDetalle, getPedidos, crearPedido } from '../services/api'

function Pedido() {
  const { mesaId } = useParams()
  const [pedido, setPedido] = useState(null)
  const [detalles, setDetalles] = useState([])
  const [productos, setProductos] = useState([])
  const [productoSeleccionado, setProductoSeleccionado] = useState('')
  const [cantidad, setCantidad] = useState(1)

  const cargarDatos = () => {
    getPedidosPorMesa(mesaId).then(data => {
      if (data.length > 0) {
        setPedido(data[0])
        getDetallePedido(data[0].id).then(d => setDetalles(d))
      } else {
        setPedido(null)
        setDetalles([])
      }
    })
  }
useEffect(() => {
  getProductos().then(data => setProductos(data))
  
  getPedidosPorMesa(mesaId).then(data => {
    if (data.length > 0) {
      setPedido(data[0])
      getDetallePedido(data[0].id).then(d => setDetalles(d))
    } else {
      // Mesa libre - crear pedido automáticamente
      const usuarioId = localStorage.getItem('usuario_id')
      console.log('Creando pedido con:', mesaId, usuarioId, 'Salon')
      crearPedido(mesaId, usuarioId, 'Salon').then(() => cargarDatos())
    }
  })

  const ws = new WebSocket('ws://localhost:8000/ws')
  ws.onmessage = () => cargarDatos()

  return () => ws.close()
}, [mesaId])

  useEffect(() => {
    getProductos().then(data => setProductos(data))
    cargarDatos()

    const ws = new WebSocket('ws://localhost:8000/ws')
    ws.onmessage = () => cargarDatos()

    return () => ws.close()
  }, [mesaId])

  return (
    <div>
      <h1>Mesa {mesaId}</h1>
      {pedido ? (
        <div>
          <p>Pedido #{pedido.nro_pedido}</p>
          <p>Total: ${pedido.total}</p>

          <h2>Productos:</h2>
          {detalles.map(d => {
            const producto = productos.find(p => p.id === d.producto_id)
            return (
              <div key={d.id}>
                {d.cantidad}x {producto?.nombre || 'Cargando...'} - ${d.subtotal}
                <button onClick={() => eliminarDetalle(pedido.id, d.id).then(() => cargarDatos())}>
                  Eliminar
                </button>
              </div>
            )
          })}

          <h2>Agregar producto</h2>
          <select
            value={productoSeleccionado}
            onChange={(e) => setProductoSeleccionado(e.target.value)}
          >
            <option value="">Seleccionar producto</option>
            {productos.map(p => (
              <option key={p.id} value={p.id}>{p.nombre}</option>
            ))}
          </select>
          <input
            type="number"
            value={cantidad}
            onChange={(e) => setCantidad(e.target.value)}
            min="1"
          />
          <button onClick={() => agregarDetalle(pedido.id, productoSeleccionado, cantidad).then(() => cargarDatos())}>
            Agregar
          </button>

          <br /><br />
          <button onClick={() => cambiarEstadoPedido(pedido.id).then(() => cargarDatos())}>
            Avanzar estado
          </button>
        </div>
      ) : (
        <p>Mesa libre - Sin pedido activo</p>
      )}
    </div>
  )
}

export default Pedido


