import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getCategorias, crearCategoria } from '../services/api'

function Productos() {
  const [categorias, setCategorias] = useState([])
  const [nombreCategoria, setNombreCategoria] = useState('')
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    getCategorias().then(data => setCategorias(data))
  }, [])

  const handleCrearCategoria = () => {
    crearCategoria(nombreCategoria, '').then(() => {
      getCategorias().then(data => setCategorias(data))
      setNombreCategoria('')
      setMostrarFormulario(false)
    })
  }

  return (
    <div>
      <button onClick={() => navigate(-1)}>← Volver</button>
      <h1>Categorias</h1>

      {categorias.map(c => (
        <div key={c.id}>
          <span>{c.nombre}</span>
          <button onClick={() => navigate(`/productos/${c.id}`)}>Ver productos</button>
        </div>
      ))}

      {mostrarFormulario ? (
        <div>
          <input
            value={nombreCategoria}
            onChange={(e) => setNombreCategoria(e.target.value)}
            placeholder="Nombre de la categoría"
          />
          <button onClick={handleCrearCategoria}>Confirmar</button>
          <button onClick={() => setMostrarFormulario(false)}>Cancelar</button>
        </div>
      ) : (
        <button onClick={() => setMostrarFormulario(true)}>+ Agregar categoría</button>
      )}
    </div>
  )
}

export default Productos