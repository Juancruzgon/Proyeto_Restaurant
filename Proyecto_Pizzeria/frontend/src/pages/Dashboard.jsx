import { useNavigate } from 'react-router-dom'

function Dashboard() {
  const navigate = useNavigate()
  const rolId = localStorage.getItem('rol_id')
  const nombre = localStorage.getItem('nombre')

  const cerrarSesion = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('rol_id')
    localStorage.removeItem('nombre')
    navigate('/')
  }

  return (
    <div>
      <h1>Bienvenido, {nombre}</h1>
      
      <button onClick={() => navigate('/mesas')}>Mesas</button>
      <button onClick={() => navigate('/pedidos')}>Pedidos</button>

      {rolId === '1' && (
        <>
          <button onClick={() => navigate('/productos')}>Productos</button>
          <button onClick={() => navigate('/usuarios')}>Usuarios</button>
          <button onClick={() => navigate('/gastos')}>Gastos</button>
          <button onClick={() => navigate('/insumos')}>Insumos</button>
        </>
      )}

      <button onClick={cerrarSesion}>Cerrar sesión</button>
    </div>
  )
}

export default Dashboard