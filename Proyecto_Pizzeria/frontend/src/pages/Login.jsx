import { useState } from 'react'
import { login } from '../services/api'
import { useNavigate } from 'react-router-dom'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()
  const handleLogin = async () => {
  try {
    const data = await login(email, password)
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('rol_id', data.rol_id)
    localStorage.setItem('nombre', data.nombre)
    navigate('/dashboard')
  } catch (error) {
    console.error('Error de login')
  }
}
    return (
    <div>
      <h1>Iniciar sesión</h1>
      <input 
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input 
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Contraseña"
      />
      <button onClick={handleLogin}>Ingresar</button>
    </div>
  )
}

export default Login    