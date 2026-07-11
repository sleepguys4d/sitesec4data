import { JSX } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './lib/auth'
import { isAuthenticated } from './lib/api'
import Layout from './components/Layout'
import LoginPage from './components/LoginPage'
import Dashboard from './pages/Dashboard'
import ModulePage from './pages/ModulePage'
import SettingsPage from './pages/SettingsPage'

function Private({ children }: { children: JSX.Element }) {
  const { loading } = useAuth()
  if (!isAuthenticated()) return <Navigate to="/login" replace />
  if (loading) {
    return <div className="min-h-screen flex items-center justify-center text-slate-500 text-sm">A carregar…</div>
  }
  return children
}

export default function App() {
  return (
    <BrowserRouter basename="/admin">
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/"
            element={
              <Private>
                <Layout />
              </Private>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="modulo/:moduleKey" element={<ModulePage />} />
            <Route path="definicoes" element={<SettingsPage />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
