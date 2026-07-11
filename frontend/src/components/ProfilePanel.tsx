import { AlertTriangle, MessageSquareQuote, Sparkles, Table2 } from 'lucide-react'
import type { Preference, UserProfile } from '../types'

const STRENGTH_META: Record<string, { color: string; label: string }> = {
  hard: { color: 'var(--status-critical)', label: 'Hard constraints' },
  strong: { color: 'var(--status-warn)', label: 'Strong preferences' },
  soft: { color: 'var(--muted)', label: 'Soft signals' },
}

function SourceIcon({ source }: { source: string }) {
  if (source === 'raw_history') return <MessageSquareQuote size={12} style={{ color: 'var(--series-5)' }} />
  if (source === 'structured') return <Table2 size={12} style={{ color: 'var(--series-1)' }} />
  return <Sparkles size={12} style={{ color: 'var(--series-3)' }} />
}

function PrefChip({ p }: { p: Preference }) {
  const val = typeof p.value === 'object' ? JSON.stringify(p.value) : String(p.value)
  const meta = STRENGTH_META[p.strength] ?? STRENGTH_META.soft
  return (
    <span className="chip cursor-help"
      title={`${p.evidence}${p.note ? ` — ${p.note}` : ''}\nsource: ${p.source.replaceAll('_', ' ')} · confidence ${p.confidence}`}
      style={{ borderColor: `color-mix(in oklab, ${meta.color} 40%, transparent)` }}>
      <SourceIcon source={p.source} />
      {p.key.replaceAll('_', ' ')}:
      <b style={{ color: 'var(--ink)' }}>{val.length > 26 ? val.slice(0, 26) + '…' : val}</b>
    </span>
  )
}

const HIDDEN_KEYS = ['home_airport', 'purpose', 'multi_city_tendency', 'date_flexibility_days']

export default function ProfilePanel({ profile }: { profile: UserProfile }) {
  const prefs = profile.preferences.filter(p => !HIDDEN_KEYS.includes(p.key)).slice(0, 14)
  const groups = (['hard', 'strong', 'soft'] as const)
    .map(s => ({ strength: s, items: prefs.filter(p => p.strength === s) }))
    .filter(g => g.items.length > 0)

  return (
    <div className="card p-4 space-y-3 rise-in">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="font-bold text-[15px]">{profile.home_city}</span>
        <span className="muted text-sm tabular">({profile.home_airport})</span>
        <span className="chip">{profile.user_id} · age {profile.age}</span>
        {profile.party_size > 1 && (
          <span className="chip chip-accent">travels as a party of {profile.party_size}</span>
        )}
        <span className="flex-1" />
        <span className="muted text-[11px] flex items-center gap-2.5">
          <span className="flex items-center gap-1"><MessageSquareQuote size={11} style={{ color: 'var(--series-5)' }} /> mined from history</span>
          <span className="flex items-center gap-1"><Table2 size={11} style={{ color: 'var(--series-1)' }} /> profile column</span>
        </span>
      </div>

      {groups.map(g => {
        const meta = STRENGTH_META[g.strength]
        return (
          <div key={g.strength}>
            <div className="text-[10.5px] font-semibold uppercase tracking-wider mb-1.5 flex items-center gap-1.5"
              style={{ color: meta.color }}>
              <span className="w-1.5 h-1.5 rounded-full inline-block" style={{ background: meta.color }} />
              {meta.label}
            </div>
            <div className="flex flex-wrap gap-1.5">
              {g.items.map((p, i) => <PrefChip key={i} p={p} />)}
            </div>
          </div>
        )
      })}

      {profile.contradictions.length > 0 && (
        <div className="rounded-lg px-3 py-2.5 text-xs flex gap-2.5"
          style={{ background: 'rgba(245,184,61,0.08)', border: '1px solid rgba(245,184,61,0.35)' }}>
          <AlertTriangle size={15} className="shrink-0 mt-0.5" style={{ color: 'var(--status-warn)' }} />
          <div>
            <b style={{ color: 'var(--status-warn)' }}>Conflicting signals detected & reconciled</b>
            {profile.contradictions.map((c, i) => <div key={i} className="ink2 mt-1 leading-relaxed">{c}</div>)}
          </div>
        </div>
      )}

      <details className="text-xs muted">
        <summary className="cursor-pointer hover:text-[var(--ink-2)] transition-colors">
          Raw booking history ({profile.raw_history.length} notes — the messy data we mine)
        </summary>
        <div className="mt-2 space-y-1.5">
          {profile.raw_history.map((h, i) => (
            <div key={i} className="px-3 py-1.5 rounded-lg italic ink2"
              style={{ background: 'var(--surface-2)', borderLeft: '2px solid var(--series-5)' }}>
              “{h}”
            </div>
          ))}
        </div>
      </details>
    </div>
  )
}
