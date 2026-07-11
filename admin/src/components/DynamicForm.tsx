import { useState, useEffect, FormEvent } from 'react'
import type { ModuleConfig } from '../config/modules'

interface Props {
  config: ModuleConfig
  initial?: Record<string, unknown> | null
  onSubmit: (values: Record<string, unknown>) => Promise<void>
  onCancel: () => void
}

export default function DynamicForm({ config, initial, onSubmit, onCancel }: Props) {
  const [values, setValues] = useState<Record<string, unknown>>({})
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const base: Record<string, unknown> = {}
    config.fields.forEach((f) => {
      if (f.type === 'password') {
        base[f.name] = ''
        return
      }
      base[f.name] = initial?.[f.name] ?? (f.type === 'boolean' ? false : f.type === 'tags' ? [] : '')
    })
    setValues(base)
  }, [initial, config])

  const set = (name: string, value: unknown) => setValues((v) => ({ ...v, [name]: value }))

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setSaving(true)
    try {
      const payload = { ...values }
      if (payload.password === '') delete payload.password
      await onSubmit(payload)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao guardar')
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border border-line rounded-lg p-5 mb-6 bg-panel/40 space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        {config.fields.map((f) => {
          const wide = f.type === 'textarea' || f.type === 'richtext' || f.type === 'tags'
          return (
            <div key={f.name} className={wide ? 'sm:col-span-2' : ''}>
              <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">
                {f.label}
                {f.required && ' *'}
              </label>

              {f.type === 'textarea' || f.type === 'richtext' ? (
                <textarea
                  className="w-full bg-bg border border-line rounded px-3 py-2 focus:outline-none focus:border-cyan text-sm"
                  rows={f.type === 'richtext' ? 8 : 3}
                  value={(values[f.name] as string) ?? ''}
                  onChange={(e) => set(f.name, e.target.value)}
                  required={f.required}
                />
              ) : f.type === 'boolean' ? (
                <label className="flex items-center gap-2 mt-2">
                  <input
                    type="checkbox"
                    checked={!!values[f.name]}
                    onChange={(e) => set(f.name, e.target.checked)}
                    className="accent-cyan h-4 w-4"
                  />
                  <span className="text-sm text-slate-400">{values[f.name] ? 'Sim' : 'Não'}</span>
                </label>
              ) : f.type === 'select' ? (
                <select
                  className="w-full bg-bg border border-line rounded px-3 py-2 focus:outline-none focus:border-cyan text-sm"
                  value={(values[f.name] as string) ?? ''}
                  onChange={(e) => set(f.name, e.target.value)}
                >
                  <option value="">—</option>
                  {f.options?.map((o) => (
                    <option key={o.value} value={o.value}>
                      {o.label}
                    </option>
                  ))}
                </select>
              ) : f.type === 'tags' ? (
                <input
                  className="w-full bg-bg border border-line rounded px-3 py-2 focus:outline-none focus:border-cyan text-sm"
                  placeholder="separar por vírgulas"
                  value={((values[f.name] as string[]) || []).join(', ')}
                  onChange={(e) =>
                    set(
                      f.name,
                      e.target.value.split(',').map((s) => s.trim()).filter(Boolean),
                    )
                  }
                />
              ) : (
                <input
                  type={f.type === 'number' ? 'number' : f.type === 'password' ? 'password' : 'text'}
                  className="w-full bg-bg border border-line rounded px-3 py-2 focus:outline-none focus:border-cyan text-sm"
                  value={(values[f.name] as string | number) ?? ''}
                  onChange={(e) => set(f.name, f.type === 'number' ? Number(e.target.value) : e.target.value)}
                  required={f.required}
                  placeholder={f.type === 'password' ? 'deixar em branco para não alterar' : undefined}
                />
              )}
            </div>
          )
        })}
      </div>
      {error && <p className="text-red-400 text-sm">{error}</p>}
      <div className="flex gap-3">
        <button
          type="submit"
          disabled={saving}
          className="bg-cyan text-bg font-semibold px-4 py-2 rounded hover:bg-cyan/80 disabled:opacity-50 text-sm"
        >
          {saving ? 'A guardar…' : 'Guardar'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="border border-line px-4 py-2 rounded text-slate-300 hover:border-cyan text-sm"
        >
          Cancelar
        </button>
      </div>
    </form>
  )
}
