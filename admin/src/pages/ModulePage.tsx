import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { MODULES } from '../config/modules'
import { apiFetch } from '../lib/api'
import DataTable from '../components/DataTable'
import DynamicForm from '../components/DynamicForm'

interface Row {
  id: number
  [key: string]: unknown
}

export default function ModulePage() {
  const { moduleKey } = useParams()
  const config = MODULES.find((m) => m.key === moduleKey)
  const [rows, setRows] = useState<Row[]>([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState<Row | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [error, setError] = useState('')

  async function load() {
    if (!config) return
    setLoading(true)
    setError('')
    try {
      const data = await apiFetch(`${config.apiPath}/`)
      setRows(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    setShowForm(false)
    setEditing(null)
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [moduleKey])

  if (!config) return <p className="text-slate-400">Módulo não encontrado.</p>

  async function handleSubmit(values: Record<string, unknown>) {
    if (!config) return
    if (editing) {
      await apiFetch(`${config.apiPath}/${editing.id}`, { method: 'PUT', body: JSON.stringify(values) })
    } else {
      await apiFetch(`${config.apiPath}/`, { method: 'POST', body: JSON.stringify(values) })
    }
    setShowForm(false)
    setEditing(null)
    await load()
  }

  async function handleDelete(row: Row) {
    if (!config) return
    const label = (row.titulo as string) || (row.nome as string) || String(row.id)
    if (!confirm(`Apagar "${label}"?`)) return
    await apiFetch(`${config.apiPath}/${row.id}`, { method: 'DELETE' })
    await load()
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-xl tracking-wide text-slate-100">{config.label}</h1>
        {config.canCreate !== false && (
          <button
            onClick={() => {
              setEditing(null)
              setShowForm((v) => !v)
            }}
            className="bg-cyan text-bg font-semibold px-4 py-2 rounded text-sm hover:bg-cyan/80"
          >
            {showForm && !editing ? 'Fechar' : '+ Novo'}
          </button>
        )}
      </div>

      {showForm && (
        <DynamicForm
          config={config}
          initial={editing}
          onSubmit={handleSubmit}
          onCancel={() => {
            setShowForm(false)
            setEditing(null)
          }}
        />
      )}

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      {loading ? (
        <p className="text-slate-500 text-sm">A carregar…</p>
      ) : (
        <DataTable
          config={config}
          rows={rows}
          onEdit={(row) => {
            setEditing(row)
            setShowForm(true)
          }}
          onDelete={handleDelete}
        />
      )}
    </div>
  )
}
