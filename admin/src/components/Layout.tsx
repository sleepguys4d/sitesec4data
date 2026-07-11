import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { LayoutDashboard, LogOut, Settings as SettingsIcon } from 'lucide-react'
import { MODULES } from '../config/modules'
import { useAuth } from '../lib/auth'
import { logout } from '../lib/api'

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `flex items-center gap-3 px-5 py-2.5 text-sm transition-colors ${
    isActive ? 'text-cyan border-r-2 border-cyan bg-panel/60' : 'text-slate-400 hover:text-slate-200'
  }`

export default function Layout() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const visibleModules = MODULES.filter((m) => !m.roles || (user && m.roles.includes(user.role)))

  return (
    <div className="min-h-screen flex bg-bg">
      <aside className="w-64 border-r border-line flex flex-col shrink-0">
        <div className="px-5 py-6 border-b border-line">
          <p className="font-display text-cyan text-lg tracking-widest">SEC4DATA</p>
          <p className="text-xs text-slate-500 tracking-wider mt-0.5">[ BACK OFFICE ]</p>
        </div>
        <nav className="flex-1 py-4 space-y-1 overflow-y-auto">
          <NavLink to="/" end className={linkClass}>
            <LayoutDashboard size={16} /> Painel
          </NavLink>
          {visibleModules.map((m) => (
            <NavLink key={m.key} to={`/modulo/${m.key}`} className={linkClass}>
              <m.icon size={16} /> {m.label}
            </NavLink>
          ))}
          <NavLink to="/definicoes" className={linkClass}>
            <SettingsIcon size={16} /> Definições
          </NavLink>
        </nav>
        <div className="px-5 py-4 border-t border-line text-xs text-slate-500">
          <p className="truncate text-slate-300">{user?.nome}</p>
          <p className="truncate text-slate-600 uppercase tracking-wider">{user?.role}</p>
          <button
            onClick={() => {
              logout()
              navigate('/login')
            }}
            className="flex items-center gap-2 mt-3 text-red-400 hover:text-red-300"
          >
            <LogOut size={14} /> Sair
          </button>
        </div>
      </aside>
      <main className="flex-1 p-8 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  )
}
