import { useState, FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../lib/api'
import { useAuth } from '../lib/auth'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { refresh } = useAuth()

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      refresh()
      navigate('/')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Falha no login')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-bg px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-sm border border-line rounded-lg p-8 bg-panel/40">
        <p className="font-display text-cyan text-xl tracking-widest text-center mb-1">SEC4DATA</p>
        <p className="text-xs text-slate-500 tracking-wider text-center mb-8">[ ACESSO AO BACK OFFICE ]</p>

        <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">Email</label>
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          required
          autoFocus
          className="w-full bg-bg border border-line rounded px-3 py-2 mb-4 focus:outline-none focus:border-cyan text-sm"
        />

        <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">Password</label>
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          required
          className="w-full bg-bg border border-line rounded px-3 py-2 mb-6 focus:outline-none focus:border-cyan text-sm"
        />

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        <button
          disabled={loading}
          className="w-full bg-cyan text-bg font-semibold py-2 rounded hover:bg-cyan/80 disabled:opacity-50 text-sm"
        >
          {loading ? 'A entrar…' : 'Entrar'}
        </button>
      </form>
    </div>
  )
}
