import { useEffect, useRef, useState } from 'react'
import { ChevronsUpDown, Search } from 'lucide-react'
import type { UserSummary } from '../types'

const PURPOSE_COLORS: Record<string, string> = {
  business: 'var(--series-1)',
  leisure: 'var(--series-2)',
  mixed: 'var(--series-5)',
}

function Avatar({ u, size = 30 }: { u: UserSummary; size?: number }) {
  const color = PURPOSE_COLORS[u.trip_purpose] ?? 'var(--muted)'
  return (
    <div className="rounded-full flex items-center justify-center shrink-0 font-bold tabular"
      style={{
        width: size, height: size, fontSize: size * 0.36,
        background: `color-mix(in oklab, ${color} 18%, var(--surface-2))`, color,
      }}>
      {u.user_id.replace('U', '')}
    </div>
  )
}

/** Compact traveler picker: a single-line trigger showing the active persona,
 * expanding into a searchable list on click — replaces an always-visible
 * 50-row rail so the left "dossier" column stays tight. */
export default function TravelerSwitcher({ users, selected, onSelect, benchUsers }: {
  users: UserSummary[]
  selected: string
  onSelect: (id: string) => void
  benchUsers: Map<string, string>
}) {
  const [open, setOpen] = useState(false)
  const [filter, setFilter] = useState('')
  const ref = useRef<HTMLDivElement>(null)
  const active = users.find(u => u.user_id === selected)

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', onClick)
    return () => document.removeEventListener('mousedown', onClick)
  }, [])

  const list = users.filter(u =>
    !filter || `${u.user_id} ${u.home_city} ${u.trip_purpose}`.toLowerCase().includes(filter.toLowerCase()))

  return (
    <div className="card p-3 relative rise-in" ref={ref}>
      <button onClick={() => setOpen(o => !o)}
        className="w-full flex items-center gap-2.5 text-left"
        aria-expanded={open} aria-haspopup="listbox">
        {active && <Avatar u={active} size={34} />}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-1.5">
            <span className="font-bold text-[14px] truncate">{active?.home_city ?? 'Select traveler'}</span>
            <span className="muted text-[11.5px] tabular">{active?.user_id}</span>
          </div>
          <div className="muted text-[11px] truncate capitalize">
            {active ? `${active.trip_purpose} · ${active.preferred_cabin} · ${active.price_sensitivity} price sens.` : ''}
          </div>
        </div>
        <ChevronsUpDown size={15} className="muted shrink-0" />
      </button>

      {open && (
        <div className="absolute left-0 right-0 top-full mt-2 z-20 card p-2 shadow-2xl"
          style={{ background: 'var(--surface-2)', maxHeight: 380, display: 'flex', flexDirection: 'column' }}>
          <div className="relative mb-1.5 shrink-0">
            <Search size={13} className="absolute left-2.5 top-1/2 -translate-y-1/2 muted" />
            {/* eslint-disable-next-line jsx-a11y/no-autofocus */}
            <input autoFocus value={filter} onChange={e => setFilter(e.target.value)}
              placeholder="Search 50 travelers…" className="input w-full pl-8 pr-2.5 py-1.5 text-sm" />
          </div>
          <div className="overflow-y-auto">
            {list.map(u => {
              const bench = benchUsers.get(u.user_id)
              return (
                <button key={u.user_id}
                  onClick={() => { onSelect(u.user_id); setOpen(false); setFilter('') }}
                  className="w-full text-left px-2 py-1.5 rounded-lg flex items-center gap-2.5 hover:bg-[var(--surface-3)] transition-colors"
                  style={u.user_id === selected ? { background: 'var(--accent-soft)' } : undefined}>
                  <Avatar u={u} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5">
                      <span className="font-semibold text-[12.5px] truncate">{u.home_city}</span>
                      <span className="muted text-[10.5px] tabular">{u.user_id}</span>
                      <span className="flex-1" />
                      {bench && <span className="badge chip-ai">{bench}</span>}
                    </div>
                  </div>
                </button>
              )
            })}
            {list.length === 0 && <div className="muted text-xs text-center py-3">No match</div>}
          </div>
        </div>
      )}
    </div>
  )
}
