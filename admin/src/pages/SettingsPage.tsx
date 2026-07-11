import { useEffect, useState } from 'react'
import { apiFetch } from '../lib/api'

interface SettingRow {
  id: number
  chave: string
  valor: string
  grupo: string
  descricao?: string
}

const GRUPO_LABEL: Record<string, string> = {
  geral: 'Geral',
  contacto: 'Contacto',
  redes_sociais: 'Redes sociais',
}

export default function SettingsPage() {
  const [rows, setRows] = useState<SettingRow[]>([])
  const [saving, setSaving] = useState<string | null>(null)
  const [saved, setSaved] = useState<string | null>(null)

  useEffect(() => {
    apiFetch('/settings/').then(setRows)
  }, [])

  async function save(row: SettingRow) {
    setSaving(row.chave)
    setSaved(null)
    await apiFetch(`/settings/${row.chave}`, { method: 'PUT', body: JSON.stringify({ valor: row.valor }) })
    setSaving(null)
    setSaved(row.chave)
    setTimeout(() => setSaved(null), 1500)
  }

  const grupos = Array.from(new Set(rows.map((r) => r.grupo)))

  return (
    <div>
      <h1 className="font-display text-xl tracking-wide text-slate-100 mb-6">Definições</h1>
      {grupos.map((grupo) => (
        <div key={grupo} className="mb-8">
          <p className="text-xs uppercase tracking-wider text-cyan/80 mb-3">{GRUPO_LABEL[grupo] || grupo}</p>
          <div className="space-y-3">
            {rows
              .filter((r) => r.grupo === grupo)
              .map((row) => (
                <div key={row.chave} className="border border-line rounded-lg p-4 bg-panel/40 flex items-end gap-3">
                  <div className="flex-1">
                    <label className="block text-xs text-slate-500 mb-1">{row.descricao || row.chave}</label>
                    <input
                      value={row.valor ?? ''}
                      onChange={(e) =>
                        setRows((rs) => rs.map((r) => (r.chave === row.chave ? { ...r, valor: e.target.value } : r)))
                      }
                      className="w-full bg-bg border border-line rounded px-3 py-2 focus:outline-none focus:border-cyan text-sm"
                    />
                  </div>
                  <button
                    onClick={() => save(row)}
                    disabled={saving === row.chave}
                    className="bg-cyan text-bg text-sm font-semibold px-3 py-2 rounded hover:bg-cyan/80 disabled:opacity-50 shrink-0"
                  >
                    {saving === row.chave ? '…' : saved === row.chave ? 'Guardado ✓' : 'Guardar'}
                  </button>
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  )
}
