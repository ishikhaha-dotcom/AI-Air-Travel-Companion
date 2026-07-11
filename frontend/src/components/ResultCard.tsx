import { Check, Plane } from 'lucide-react'
import type { LegJson, OptionJson } from '../types'
import { fmtDuration, fmtMoney } from '../airports'
import { featureLabel, FEATURE_COLORS } from '../labels'
import FitRing from './FitRing'

function DeltaVsTop({ option, top, party }: { option: OptionJson; top: OptionJson; party: number }) {
  const price = party > 1 ? option.total_price_party : option.total_price_pp
  const topPrice = party > 1 ? top.total_price_party : top.total_price_pp
  const priceDelta = price - topPrice
  const timeDelta = option.total_duration_minutes - top.total_duration_minutes
  const fitDelta = option.fit_score - top.fit_score
  if (Math.abs(priceDelta) < 1 && Math.abs(timeDelta) < 15 && Math.abs(fitDelta) < 1) return null
  return (
    <div className="text-[10.5px] muted tabular mt-1" title="Compared to the #1 recommended pick">
      vs #1:{' '}
      {Math.abs(priceDelta) >= 1 && <span>{priceDelta > 0 ? '+' : ''}{fmtMoney(priceDelta)} </span>}
      {Math.abs(timeDelta) >= 15 && <span>· {timeDelta > 0 ? '+' : '−'}{fmtDuration(Math.abs(timeDelta))} </span>}
      {Math.abs(fitDelta) >= 1 && <span>· fit {fitDelta > 0 ? '+' : ''}{fitDelta.toFixed(0)}</span>}
    </div>
  )
}

const FEATURE_ORDER = ['price', 'time', 'convenience', 'reliability', 'preffit']

function badgeStyle(b: string): { background: string; color: string } {
  const mk = (c: string, alpha = 0.15) => ({ background: `color-mix(in oklab, ${c} ${alpha * 100}%, transparent)`, color: c })
  if (b === 'Best fit') return mk('var(--accent)', 0.18)
  if (b === 'Cheapest') return mk('var(--series-2)')
  if (b === 'Fastest') return mk('var(--series-3)')
  if (b === 'Direct') return mk('var(--status-good)')
  if (b.startsWith('Only')) return mk('var(--status-critical)')
  if (b === 'Holiday peak' || b === 'High demand' || b === 'Self-transfer') return mk('var(--status-warn)')
  if (b === 'Red-eye') return mk('var(--status-serious)')
  return mk('var(--muted)', 0.2)
}

/** One leg as an airline-style timeline: times/codes at the ends, duration+stops on the line. */
function LegTimeline({ leg }: { leg: LegJson }) {
  const f0 = leg.flights[0], fl = leg.flights[leg.flights.length - 1]
  const stops = [
    ...leg.flights.flatMap(f => f.layover_airports),
    ...(leg.self_transfer ? [leg.transfer_airport] : []),
  ].filter((v, i, a) => v && a.indexOf(v) === i)
  const airlines = [...new Set(leg.flights.map(f => f.airline_name))].join(' + ')
  const cabins = [...new Set(leg.flights.map(f => f.cabin))].join(' / ')

  return (
    <div className="py-2.5">
      <div className="flex items-center gap-4">
        <div className="w-20 shrink-0">
          <div className="text-[17px] font-bold tabular leading-none">{f0.dep_local.slice(11, 16)}</div>
          <div className="text-xs font-semibold mt-1" style={{ color: 'var(--accent)' }}>{leg.origin}</div>
          <div className="muted text-[10.5px] tabular">{f0.dep_local.slice(5, 10)}</div>
        </div>

        <div className="flex-1 min-w-28">
          <div className="text-center muted text-[10.5px] tabular mb-1">
            {fmtDuration(leg.duration_minutes)}
            {leg.stops > 0 && ` · layover ${fmtDuration(leg.layover_total)}`}
          </div>
          <div className="relative h-4 flex items-center">
            <div className="absolute inset-x-0 h-px" style={{ background: 'var(--baseline)' }} />
            <div className="absolute left-0 w-1.5 h-1.5 rounded-full" style={{ background: 'var(--ink-2)' }} />
            {stops.map((_, i) => (
              <div key={i} className="absolute w-2 h-2 rounded-full border-2"
                style={{
                  left: `${((i + 1) / (stops.length + 1)) * 100}%`,
                  background: 'var(--surface)', borderColor: 'var(--status-warn)',
                  transform: 'translateX(-50%)',
                }} />
            ))}
            <Plane size={13} className="absolute" style={{
              left: stops.length ? '25%' : '50%', transform: 'translate(-50%, 0) rotate(45deg)',
              color: 'var(--ink-2)', background: 'var(--surface)',
            }} />
            <div className="absolute right-0 w-1.5 h-1.5 rounded-full" style={{ background: 'var(--ink-2)' }} />
          </div>
          <div className="text-center text-[10.5px] mt-1">
            {leg.stops === 0
              ? <span style={{ color: 'var(--status-good)' }}>direct</span>
              : <span className="muted">{leg.stops} stop{leg.stops > 1 ? 's' : ''}{stops.length ? ` via ${stops.join(', ')}` : ''}</span>}
          </div>
        </div>

        <div className="w-20 shrink-0 text-right">
          <div className="text-[17px] font-bold tabular leading-none">{fl.arr_local.slice(11, 16)}</div>
          <div className="text-xs font-semibold mt-1" style={{ color: 'var(--accent)' }}>{leg.destination}</div>
          <div className="muted text-[10.5px] tabular">{fl.arr_local.slice(5, 10)}</div>
        </div>
      </div>
      <div className="muted text-[11px] mt-1.5 flex items-center gap-1.5 flex-wrap">
        <span>{airlines}</span>
        <span>·</span><span>{cabins}</span>
        <span>·</span><span>{leg.seats_min} seats left</span>
        {leg.self_transfer && (
          <span style={{ color: 'var(--status-warn)' }}>
            · self-transfer at {leg.transfer_airport} ({fmtDuration(leg.transfer_minutes)})
          </span>
        )}
      </div>
    </div>
  )
}

export default function ResultCard({ option, rank, party, weights, top }: {
  option: OptionJson; rank: number; party: number; weights: Record<string, number>; top?: OptionJson
}) {
  return (
    <div id={`option-${option.key}`} className="card p-4 rise-in-2 transition-shadow hover:shadow-[0_4px_24px_rgba(0,0,0,0.25)] scroll-mt-4"
      style={rank === 1
        ? { borderColor: 'rgba(79,143,247,0.5)', background: 'linear-gradient(180deg, rgba(79,143,247,0.05), transparent 40%)' }
        : undefined}>
      <div className="flex gap-4 flex-wrap">
        <div className="flex-1 min-w-72">
          <div className="flex items-center gap-1.5 flex-wrap mb-1">
            <span className="muted text-xs font-bold tabular mr-0.5">#{rank}</span>
            {option.badges.map(b => (
              <span key={b} className="badge" style={badgeStyle(b)}>{b}</span>
            ))}
          </div>
          <div className="divide-y" style={{ borderColor: 'var(--border)' }}>
            {option.legs.map((leg, i) => <LegTimeline key={i} leg={leg} />)}
          </div>
        </div>

        <div className="shrink-0 w-52 flex flex-col items-end gap-2.5 pt-1">
          <div className="flex items-start gap-3">
            <div className="text-right">
              <div className="text-[24px] font-bold tabular leading-none">
                {fmtMoney(party > 1 ? option.total_price_party : option.total_price_pp)}
              </div>
              {party > 1 && (
                <div className="muted text-[11px] tabular mt-1">{fmtMoney(option.total_price_pp)} / person</div>
              )}
              {top && rank > 1 && <DeltaVsTop option={option} top={top} party={party} />}
            </div>
            <FitRing score={option.fit_score} size={54} />
          </div>
          <div className="w-full space-y-1.5">
            {FEATURE_ORDER.filter(k => k in (option.goodness ?? {})).map(k => {
              const g = option.goodness[k] ?? 0
              const pts = option.breakdown[k] ?? 0
              const wmax = (weights[k] ?? 0) * 100
              return (
                <div key={k} className="flex items-center gap-2 text-[10.5px]"
                  title={`${featureLabel(k)}: goodness ${(g * 100).toFixed(0)}% × weight ${wmax.toFixed(0)}% = ${pts.toFixed(1)} pts`}>
                  <span className="w-[74px] text-left muted truncate">{featureLabel(k)}</span>
                  <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ background: 'var(--grid)' }}>
                    <div className="h-1.5 rounded-full" style={{ width: `${g * 100}%`, background: FEATURE_COLORS[k] }} />
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
          <summary className="cursor-pointer text-xs font-semibold ink2 hover:text-[var(--ink)] transition-colors">
            Why this one — {option.why.length} evidence-cited reason{option.why.length > 1 ? 's' : ''}
          </summary>
          <div className="mt-2 space-y-1.5">
            {option.why.map((w, i) => (
              <div key={i} className="text-xs flex gap-2 leading-relaxed">
                <Check size={13} className="shrink-0 mt-0.5" style={{ color: 'var(--status-good)' }} />
                <span>
                  <span className="ink2">{w.reason}</span>{' '}
                  <span className="muted italic">— {w.evidence} ({w.source.replaceAll('_', ' ')})</span>
                </span>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  )
}
