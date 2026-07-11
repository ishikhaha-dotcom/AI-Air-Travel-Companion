import { useState } from 'react'
import { Search } from 'lucide-react'
import type { UserSummary } from '../types'

const PURPOSE_COLORS: Record<string, string> = {
  business: 'var(--series-1)',
  leisure: 'var(--series-2)',
  mixed: 'var(--series-5)',
}

function Avatar({ u }: { u: UserSummary }) {
  const color = PURPOSE_COLORS[u.trip_purpose] ?? 'var(--muted)'
  return (
    <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-[11px] font-bold tabular"
      style={{ background: `color-mix(in oklab, ${color} 18%, var(--surface-2))`, color }}>
      {u.user_id.replace('U', '')}
    </div>
  )
}

export default function PersonaRail({ users, selected, onSelect, benchUsers }: {
  users: UserSummary[]
  selected: string
  onSelect: (id: string) => void
  benchUsers: Map<string, string>
}) {
  const [filter, setFilter] = useState('')
  const list = users.filter(u =>
    !filter || `${u.user_id} ${u.home_city} ${u.trip_purpose}`.toLowerCase().includes(filter.toLowerCase()))

  return (
    <aside className="w-64 shrink-0 border-r hairline flex flex-col" style={{ background: 'var(--surface)' }}>
      <div className="p-2.5 border-b hairline">
        <div className="relative">
          <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 muted" />
          <input
            value={filter} onChange={e => setFilter(e.target.value)}
            placeholder="Filter 50 travelers…"
            className="input w-full pl-8 pr-2.5 py-1.5 text-sm"
          />
        </div>
      </div>
      <div className="flex-1 overflow-y-auto py-1">
        {list.map(u => {
          const bench = benchUsers.get(u.user_id)
          const active = u.user_id === selected
          return (
            <button key={u.user_id} onClick={() => onSelect(u.user_id)}
              className="w-full text-left px-2.5 py-1.5 transition-colors"
              style={{ background: active ? 'var(--surface-2)' : 'transparent',
                       boxShadow: active ? 'inset 3px 0 0 var(--accent)' : 'none' }}>
              <div className="flex items-center gap-2.5">
                <Avatar u={u} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className="font-semibold text-[13px] truncate">{u.home_city}</span>
                    <span className="muted text-[11px] tabular">{u.user_id}</span>
                    <span className="flex-1" />
                    {bench && (
                      <span className="badge" style={{ background: 'var(--accent-soft)', color: 'var(--accent)' }}>
                        {bench}
                      </span>
                    )}
                  </div>
                  <div className="muted text-[11px] truncate capitalize">
                    {u.trip_purpose} · {u.preferred_cabin} · {u.price_sensitivity} price sens.
                  </div>
                </div>
              </div>
            </button>
          )
        })}
      </div>
      <div className="px-3 py-2 border-t hairline muted text-[10.5px] flex items-center gap-3">
        {Object.entries(PURPOSE_COLORS).map(([k, c]) => (
          <span key={k} className="flex items-center gap-1 capitalize">
            <span className="w-2 h-2 rounded-full inline-block" style={{ background: c }} /> {k}
          </span>
        ))}
      </div>
    </aside>
  )
}
