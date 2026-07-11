import { ArrowRight, Award } from 'lucide-react'
import type { OptionJson } from '../types'
import { fmtDuration, fmtMoney } from '../airports'

const FIT_COLOR = (s: number) => s >= 75 ? 'var(--status-good)' : s >= 55 ? 'var(--accent)' : 'var(--status-warn)'

function jumpTo(key: string) {
  document.getElementById(`option-${key}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

/** At-a-glance ranking across every shown recommendation — the thing a judge
 *  scans first before reading any single card in depth. Each row jumps to its
 *  full detail card below. */
export default function CompareTable({ options, party }: { options: OptionJson[]; party: number }) {
  if (options.length < 2) return null
  const top = options[0]

  return (
    <div className="card p-4 rise-in-2">
      <div className="text-[10.5px] font-semibold uppercase tracking-wider muted mb-2.5">
        Compare all {options.length} picks
      </div>
      <div className="overflow-x-auto -mx-1">
        <table className="w-full text-sm border-collapse min-w-[560px]">
          <thead>
            <tr className="text-left muted text-[10.5px] uppercase tracking-wide">
              <th className="font-medium pb-2 px-1">#</th>
              <th className="font-medium pb-2 px-1">Route</th>
              <th className="font-medium pb-2 px-1 text-right">Price</th>
              <th className="font-medium pb-2 px-1 text-right">Duration</th>
              <th className="font-medium pb-2 px-1 text-center">Stops</th>
              <th className="font-medium pb-2 px-1">Fit</th>
              <th className="font-medium pb-2 px-1" />
            </tr>
          </thead>
          <tbody>
            {options.map((o, idx) => {
              const price = party > 1 ? o.total_price_party : o.total_price_pp
              const priceDelta = idx === 0 ? 0 : price - (party > 1 ? top.total_price_party : top.total_price_pp)
              const timeDelta = idx === 0 ? 0 : o.total_duration_minutes - top.total_duration_minutes
              return (
                <tr key={o.key}
                  onClick={() => jumpTo(o.key)}
                  className="cursor-pointer transition-colors hover:bg-[var(--surface-2)] border-t hairline group"
                  title="Jump to this option's full detail">
                  <td className="py-2 px-1 tabular font-semibold" style={idx === 0 ? { color: 'var(--accent)' } : undefined}>
                    {idx === 0 ? <Award size={14} className="inline -mt-0.5" /> : idx + 1}
                  </td>
                  <td className="py-2 px-1">
                    <span className="font-medium">{o.legs[0].origin}</span>
                    <span className="muted mx-1">→</span>
                    <span className="font-medium">{o.legs[o.legs.length - 1].destination}</span>
                    {o.legs.length > 1 && <span className="muted text-[11px] ml-1">({o.legs.length} legs)</span>}
                  </td>
                  <td className="py-2 px-1 text-right tabular">
                    {fmtMoney(price)}
                    {idx > 0 && Math.abs(priceDelta) >= 1 && (
                      <div className="text-[10.5px] muted">{priceDelta > 0 ? '+' : ''}{fmtMoney(priceDelta)}</div>
                    )}
                  </td>
                  <td className="py-2 px-1 text-right tabular">
                    {fmtDuration(o.total_duration_minutes)}
                    {idx > 0 && Math.abs(timeDelta) >= 15 && (
                      <div className="text-[10.5px] muted">{timeDelta > 0 ? '+' : '−'}{fmtDuration(Math.abs(timeDelta))}</div>
                    )}
                  </td>
                  <td className="py-2 px-1 text-center tabular">
                    {o.total_stops === 0 ? <span style={{ color: 'var(--status-good)' }}>direct</span> : o.total_stops}
                  </td>
                  <td className="py-2 px-1">
                    <div className="flex items-center gap-2">
                      <div className="w-14 h-1.5 rounded-full overflow-hidden shrink-0" style={{ background: 'var(--grid)' }}>
                        <div className="h-1.5 rounded-full" style={{ width: `${o.fit_score}%`, background: FIT_COLOR(o.fit_score) }} />
                      </div>
                      <span className="tabular text-xs w-6" style={{ color: FIT_COLOR(o.fit_score) }}>{Math.round(o.fit_score)}</span>
                    </div>
                  </td>
                  <td className="py-2 px-1 text-right">
                    <ArrowRight size={13} className="muted opacity-0 group-hover:opacity-100 transition-opacity" />
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
