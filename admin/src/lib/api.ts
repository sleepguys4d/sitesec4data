const BASE = '/api'

function getToken() {
  return localStorage.getItem('sec4data_token')
}

export async function apiFetch(path: string, options: RequestInit = {}) {
  const token = getToken()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> | undefined),
  }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${BASE}${path}`, { ...options, headers })

  if (res.status === 401) {
    localStorage.removeItem('sec4data_token')
    if (window.location.pathname !== '/admin/login') {
      window.location.href = '/admin/login'
    }
    throw new Error('Sessão expirada')
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Erro ${res.status}`)
  }
  if (res.status === 204) return null
  return res.json()
}

export async function login(email: string, password: string) {
  const form = new URLSearchParams()
  form.set('username', email)
  form.set('password', password)
  const res = await fetch(`${BASE}/auth/login`, { method: 'POST', body: form })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || 'Falha no login')
  }
  const data = await res.json()
  localStorage.setItem('sec4data_token', data.access_token)
  return data.user
}

export function logout() {
  localStorage.removeItem('sec4data_token')
}

export function isAuthenticated() {
  return !!getToken()
}
