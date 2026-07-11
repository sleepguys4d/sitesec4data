import type { ModuleConfig } from '../config/modules'

interface Row {
  id: number
  [key: string]: unknown
}

interface Props {
  config: ModuleConfig
  rows: Row[]
  onEdit: (row: Row) => void
  onDelete: (row: Row) => void
}

function displayValue(value: unknown, type: string): string {
  if (type === 'boolean') return value ? 'Sim' : 'Não'
  if (Array.isArray(value)) return value.join(', ')
  if (value === null || value === undefined || value === '') return '—'
  return String(value)
}

export default function DataTable({ config, rows, onEdit, onDelete }: Props) {
  const columns = config.fields.filter((f) => !f.hideInTable).slice(0, 5)

  if (rows.length === 0) {
    return (
      <div className="border border-line rounded-lg p-10 text-center text-slate-500 text-sm">
        {config.emptyLabel || `Ainda não há registos em ${config.label}.`}
      </div>
    )
  }

  return (
    <div className="overflow-x-auto border border-line rounded-lg">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-line text-left uppercase tracking-wider text-xs text-cyan/80">
            {columns.map((c) => (
              <th key={c.name} className="px-4 py-3 font-normal whitespace-nowrap">
                {c.label}
              </th>
            ))}
            <th className="px-4 py-3" />
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="border-b border-line/60 hover:bg-panel/60 transition-colors">
              {columns.map((c) => (
                <td key={c.name} className="px-4 py-3 max-w-xs truncate text-slate-300">
                  {displayValue(row[c.name], c.type)}
                </td>
              ))}
              <td className="px-4 py-3 text-right whitespace-nowrap">
                <button onClick={() => onEdit(row)} className="text-cyan hover:underline mr-4 text-xs uppercase tracking-wide">
                  Editar
                </button>
                {config.canDelete !== false && (
                  <button onClick={() => onDelete(row)} className="text-red-400 hover:underline text-xs uppercase tracking-wide">
                    Apagar
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
