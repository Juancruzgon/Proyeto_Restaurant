import { useNavigate } from 'react-router-dom'

function NuevoPedido() {
  const navigate = useNavigate()

  return (
    <div>
      <h1>Nuevo Pedido</h1>
      <button onClick={() => navigate('/mesas?modo=nuevo')}>Salón</button>
      <button>Delivery</button>
      <button>Takeaway</button>
    </div>
  )
}

export default NuevoPedido