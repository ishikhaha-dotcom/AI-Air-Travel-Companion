import { useState } from 'react'
import { PanelLeftClose, Search } from 'lucide-react'
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

/** The full 50-traveler sidebar (restored from the pre-P8 rail), now
 * collapsible: an in-flow flex column that animates its width to zero, so it
 * never overlaps other content — the header's toggle reopens it. */
export default function TravelerSidebar({ users, selected, onSelect, benchUsers, open, onToggle }: {
  users: UserSummary[]
  selected: string
  onSelect: (id: string) => void
  benchUsers: Map<string, string>
  open: boolean
  onToggle: () => void
}) {
  const [filter, setFilter] = useState('')
  const list = users.filter(u =>
    !filter || `${u.user_id} ${u.home_city} ${u.trip_purpose}`.toLowerCase().includes(filter.toLowerCase()))

  return (
    <aside
      className="shrink-0 border-r hairline overflow-hidden"
      style={{
        width: open ? 264 : 0,
        transition: 'width 0.22s ease',
        background: 'var(--surface)',
        borderRightWidth: open ? 1 : 0,
      }}
      aria-hidden={!open}>
      {/* fixed inner width so text doesn't reflow while the drawer animates */}
      <div className="w-[264px] h-full flex flex-col">
        <div className="flex items-center gap-2 px-3 pt-2.5 pb-1.5">
          <span className="text-[12px] font-bold uppercase tracking-wider muted">
            Travelers <span className="tabular">({users.length})</span>
          </span>
          <span className="flex-1" />
          <button onClick={onToggle} title="Collapse sidebar"
            className="btn-ghost !p-1.5 flex items-center">
            <PanelLeftClose size={15} />
          </button>
        </div>
        <div className="px-2.5 pb-2 border-b hairline">
          <div className="relative">
            <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 muted" />
            <input
              value={filter} onChange={e => setFilter(e.target.value)}
              placeholder="Filter travelers…"
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
                className="w-full text-left px-2.5 py-1.5 transition-colors hover:bg-[var(--surface-2)]"
                style={{ background: active ? 'var(--surface-2)' : 'transparent',
                         boxShadow: active ? 'inset 3px 0 0 var(--accent)' : 'none' }}>
                <div className="flex items-center gap-2.5">
                  <Avatar u={u} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5">
                      <span className="font-semibold text-[13px] truncate">{u.home_city}</span>
                      <span className="muted text-[11px] tabular">{u.user_id}</span>
                      <span className="flex-1" />
                      {bench && <span className="badge chip-ai">{bench}</span>}
                    </div>
                    <div className="muted text-[11px] truncate capitalize">
                      {u.trip_purpose} · {u.preferred_cabin} · {u.price_sensitivity} price sens.
                    </div>
                  </div>
                </div>
              </button>
            )
          })}
          {list.length === 0 && <div className="muted text-xs text-center py-4">No match</div>}
        </div>
        <div className="px-3 py-2 border-t hairline muted text-[10.5px] flex items-center gap-3">
          {Object.entries(PURPOSE_COLORS).map(([k, c]) => (
            <span key={k} className="flex items-center gap-1 capitalize">
              <span className="w-2 h-2 rounded-full inline-block" style={{ background: c }} /> {k}
            </span>
          ))}
        </div>
      </div>
    </aside>
  )
}
