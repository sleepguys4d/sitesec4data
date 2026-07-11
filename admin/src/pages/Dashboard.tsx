import { useEffect, useState } from 'react'
import { MODULES } from '../config/modules'
import { apiFetch } from '../lib/api'
import { useAuth } from '../lib/auth'

export default function Dashboard() {
  const { user } = useAuth()
  const [counts, setCounts] = useState<Record<string, number>>({})

  useEffect(() => {
    const visible = MODULES.filter((m) => !m.roles || (user && m.roles.includes(user.role)))
    Promise.all(
      visible.map(async (m) => {
        try {
          const data = await apiFetch(`${m.apiPath}/`)
          return [m.key, Array.isArray(data) ? data.length : 0] as const
        } catch {
          return [m.key, 0] as const
        }
      }),
    ).then((entries) => setCounts(Object.fromEntries(entries)))
  }, [user])

  return (
    <div>
      <h1 className="font-display text-xl tracking-wide text-slate-100 mb-1">Painel</h1>
      <p className="text-slate-500 text-sm mb-8">Bem-vindo, {user?.nome}.</p>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {MODULES.filter((m) => !m.roles || (user && m.roles.includes(user.role))).map((m) => (
          <div key={m.key} className="border border-line rounded-lg p-5 bg-panel/40">
            <m.icon size={18} className="text-cyan mb-3" />
            <p className="text-2xl font-display text-slate-100">{counts[m.key] ?? '—'}</p>
            <p className="text-xs text-slate-500 uppercase tracking-wider mt-1">{m.label}</p>
          </div>
        ))}
      </div>
      <div className="mt-8 border border-line rounded-lg p-5 bg-panel/20 text-sm text-slate-500">
        <p className="text-cyan/80 text-xs uppercase tracking-wider mb-2">[ Extensibilidade ]</p>
        Para acrescentar um novo módulo ao Back Office, ver{' '}
        <code className="text-slate-400">backend/app/core/module_registry.py</code> e{' '}
        <code className="text-slate-400">admin/src/config/modules.ts</code> — ou correr{' '}
        <code className="text-slate-400">scripts/new_module.py</code>.
      </div>
    </div>
  )
}
