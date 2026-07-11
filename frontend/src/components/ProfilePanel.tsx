import type { Preference, UserProfile } from '../types'

const STRENGTH_COLOR: Record<string, string> = {
  hard: 'var(--status-critical)',
  strong: 'var(--status-warn)',
  soft: 'var(--muted)',
}

function PrefChip({ p }: { p: Preference }) {
  const icon = p.source === 'raw_history' ? '💬' : p.source === 'structured' ? '🗂' : '✳'
  const val = typeof p.value === 'object' ? JSON.stringify(p.value) : String(p.value)
  return (
    <span className="chip cursor-help" title={`${p.evidence}${p.note ? ` — ${p.note}` : ''} (${p.source}, confidence ${p.confidence})`}>
      <span className="mr-1" style={{ color: STRENGTH_COLOR[p.strength] }}>●</span>
      {icon} {p.key.replaceAll('_', ' ')}: <b style={{ color: 'var(--ink)' }}>{val.length > 26 ? val.slice(0, 26) + '…' : val}</b>
    </span>
  )
}

export default function ProfilePanel({ profile }: { profile: UserProfile }) {
  return (
    <div className="card p-3 space-y-2">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="font-semibold">{profile.user_id}</span>
        <span className="ink2 text-sm">{profile.home_city} ({profile.home_airport}) · age {profile.age}
          {profile.party_size > 1 && <> · <b style={{ color: 'var(--ink)' }}>travels as a party of {profile.party_size}</b></>}
        </span>
        <span className="flex-1" />
        <span className="muted text-xs">● hard&nbsp; ● strong&nbsp; ● soft — hover any chip for its evidence</span>
      </div>
      <div className="flex flex-wrap gap-1.5">
        {profile.preferences.filter(p => !['home_airport', 'purpose', 'multi_city_tendency', 'date_flexibility_days'].includes(p.key))
          .slice(0, 14).map((p, i) => <PrefChip key={i} p={p} />)}
      </div>
      {profile.contradictions.length > 0 && (
        <div className="rounded-lg px-3 py-2 text-xs"
          style={{ background: 'rgba(250,178,25,0.08)', border: '1px solid rgba(250,178,25,0.35)' }}>
          <b style={{ color: 'var(--status-warn)' }}>⚠ Conflicting signals reconciled:</b>
          {profile.contradictions.map((c, i) => <div key={i} className="ink2 mt-1">{c}</div>)}
        </div>
      )}
      <details className="text-xs muted">
        <summary className="cursor-pointer">Raw booking history ({profile.raw_history.length} notes — the messy data we mine)</summary>
        <div className="mt-1.5 flex flex-wrap gap-1.5">
          {profile.raw_history.map((h, i) => (
            <span key={i} className="chip" style={{ fontStyle: 'italic' }}>“{h}”</span>
          ))}
        </div>
      </details>
    </div>
  )
}
