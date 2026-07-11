import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { apiFetch, isAuthenticated } from './api'

type CurrentUser = { id: number; nome: string; email: string; role: string } | null

interface AuthContextValue {
  user: CurrentUser
  loading: boolean
  refresh: () => void
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  loading: true,
  refresh: () => {},
})

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser>(null)
  const [loading, setLoading] = useState(true)

  const refresh = () => {
    if (!isAuthenticated()) {
      setUser(null)
      setLoading(false)
      return
    }
    setLoading(true)
    apiFetch('/auth/me')
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }

  useEffect(refresh, [])

  return <AuthContext.Provider value={{ user, loading, refresh }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
