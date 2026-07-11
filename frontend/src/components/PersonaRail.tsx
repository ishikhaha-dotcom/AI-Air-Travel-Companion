import { useState } from 'react'
import type { UserSummary } from '../types'

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
    <aside className="w-60 shrink-0 border-r hairline flex flex-col" style={{ background: 'var(--surface)' }}>
      <div className="p-2 border-b hairline">
        <input
          value={filter} onChange={e => setFilter(e.target.value)}
          placeholder="Filter 50 travelers…"
          className="w-full px-2.5 py-1.5 rounded-lg text-sm outline-none border hairline"
          style={{ background: 'var(--surface-2)', color: 'var(--ink)' }}
        />
      </div>
      <div className="flex-1 overflow-y-auto">
        {list.map(u => {
          const bench = benchUsers.get(u.user_id)
          const active = u.user_id === selected
          return (
            <button key={u.user_id} onClick={() => onSelect(u.user_id)}
              className="w-full text-left px-3 py-2 border-b hairline hover:brightness-125"
              style={{ background: active ? 'var(--surface-2)' : 'transparent',
                       boxShadow: active ? 'inset 3px 0 0 var(--accent)' : 'none' }}>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-sm tabular">{u.user_id}</span>
                <span className="ink2 text-xs truncate">{u.home_city}</span>
                <span className="flex-1" />
                {bench && <span className="chip" style={{ color: 'var(--accent)' }}>{bench}</span>}
              </div>
              <div className="muted text-[11px] truncate mt-0.5">
                {u.trip_purpose} · {u.preferred_cabin} · price {u.price_sensitivity} · direct {u.direct_preference}
              </div>
            </button>
          )
        })}
      </div>
    </aside>
  )
}
