import type { LegJson, OptionJson } from '../types'
import { fmtDuration, fmtMoney } from '../airports'

const FEATURES: { key: string; label: string; color: string }[] = [
  { key: 'price', label: 'Price', color: 'var(--series-1)' },
  { key: 'time', label: 'Time', color: 'var(--series-2)' },
  { key: 'convenience', label: 'Convenience', color: 'var(--series-3)' },
  { key: 'reliability', label: 'Reliability', color: 'var(--series-4)' },
  { key: 'preffit', label: 'Pref-fit', color: 'var(--series-5)' },
]

function badgeColor(b: string): string {
  if (b === 'Best fit') return 'var(--accent)'
  if (b === 'Cheapest') return 'var(--series-2)'
  if (b === 'Fastest') return 'var(--series-3)'
  if (b === 'Direct') return 'var(--status-good)'
  if (b.startsWith('Only')) return 'var(--status-critical)'
  if (b === 'Holiday peak' || b === 'High demand' || b === 'Self-transfer') return 'var(--status-warn)'
  if (b === 'Red-eye') return 'var(--status-serious)'
  return 'var(--muted)'
}

function LegRow({ leg }: { leg: LegJson }) {
  const f0 = leg.flights[0], fl = leg.flights[leg.flights.length - 1]
  const vias = [
    ...leg.flights.flatMap(f => f.layover_airports),
    ...(leg.self_transfer ? [`${leg.transfer_airport}*`] : []),
  ]
  return (
    <div className="flex items-center gap-3 text-sm flex-wrap py-1">
      <div className="tabular">
        <b>{leg.origin}</b> <span className="ink2">{f0.dep_local.slice(5, 16)}</span>
      </div>
      <div className="flex-1 min-w-24 relative h-5">
        <div className="absolute inset-x-0 top-1/2 border-t hairline" />
        <div className="absolute inset-x-0 -top-0.5 text-center text-[10px] muted">
          {fmtDuration(leg.duration_minutes)} · {leg.stops === 0 ? 'direct' : `${leg.stops} stop(s)${vias.length ? ' via ' + vias.join(', ') : ''}`}
          {leg.stops > 0 && ` · layover ${fmtDuration(leg.layover_total)}`}
        </div>
      </div>
      <div className="tabular">
        <b>{leg.destination}</b> <span className="ink2">{fl.arr_local.slice(5, 16)}</span>
      </div>
      <div className="muted text-xs">
        {[...new Set(leg.flights.map(f => f.airline_name))].join(' + ')} · {[...new Set(leg.flights.map(f => f.cabin))].join('/')}
        {' '}· {leg.seats_min} seats
        {leg.self_transfer && <span style={{ color: 'var(--status-warn)' }}> · self-transfer {fmtDuration(leg.transfer_minutes)}</span>}
      </div>
    </div>
  )
}

export default function ResultCard({ option, rank, party, weights }: {
  option: OptionJson; rank: number; party: number; weights: Record<string, number>
}) {
  return (
    <div className="card p-3" style={rank === 1 ? { borderColor: 'var(--accent)' } : undefined}>
      <div className="flex items-start gap-3 flex-wrap">
        <div className="text-lg font-bold muted">#{rank}</div>
        <div className="flex-1 min-w-64">
          <div className="flex gap-1.5 flex-wrap mb-1">
            {option.badges.map(b => (
              <span key={b} className="chip" style={{ color: badgeColor(b), borderColor: badgeColor(b) }}>{b}</span>
            ))}
          </div>
          <div className="divide-y" style={{ borderColor: 'var(--border)' }}>
            {option.legs.map((leg, i) => <LegRow key={i} leg={leg} />)}
          </div>
        </div>
        <div className="text-right shrink-0 w-44">
          <div className="text-2xl font-bold tabular">{fmtMoney(party > 1 ? option.total_price_party : option.total_price_pp)}</div>
          {party > 1 && <div className="muted text-xs tabular">{fmtMoney(option.total_price_pp)} / person</div>}
          <div className="text-sm mt-1">
            fit <b className="tabular" style={{ color: 'var(--accent)' }}>{option.fit_score}</b><span className="muted">/100</span>
          </div>
          <div className="mt-1.5 space-y-1">
            {FEATURES.map(f => {
              const g = option.goodness[f.key] ?? 0
              const pts = option.breakdown[f.key] ?? 0
              const wmax = (weights[f.key] ?? 0) * 100
              return (
                <div key={f.key} className="flex items-center gap-1.5 text-[10px]"
                  title={`${f.label}: goodness ${(g * 100).toFixed(0)}% × weight ${wmax.toFixed(0)}% = ${pts.toFixed(1)} pts`}>
                  <span className="w-16 text-left muted">{f.label}</span>
                  <div className="flex-1 h-1.5 rounded-full" style={{ background: 'var(--grid)' }}>
                    <div className="h-1.5 rounded-full" style={{ width: `${g * 100}%`, background: f.color }} />
                  </div>
                  <span className="tabular w-8 text-right ink2">{pts.toFixed(1)}</span>
                </div>
              )
            })}
          </div>
        </div>
      </div>
      {option.why.length > 0 && (
        <details className="mt-2" open={rank === 1}>
          <summary className="cursor-pointer text-xs font-semibold ink2">
            Why this one — {option.why.length} evidence-cited reasons
          </summary>
          <div className="mt-1.5 space-y-1">
            {option.why.map((w, i) => (
              <div key={i} className="text-xs">
                <span className="ink2">✓ {w.reason}</span>{' '}
                <span className="muted italic">— {w.evidence} ({w.source.replaceAll('_', ' ')})</span>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  )
}
