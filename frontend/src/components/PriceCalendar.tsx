import { useState } from 'react'
import { fmtMoney } from '../airports'

interface Row { date: string; price: number; fit_score: number; stops: number }

/** Price-vs-departure-date bar chart (single sequential series, hand-rolled SVG
 *  per dataviz mark specs: thin bars, 4px rounded data-end, hairline grid,
 *  hover tooltip, selective direct labels: min + recommended only). */
export default function PriceCalendar({ series, recommendedDate }: {
  series: Row[]; recommendedDate: string
}) {
  const [hover, setHover] = useState<Row | null>(null)
  const W = 460, H = 180, m = { t: 18, r: 8, b: 26, l: 44 }
  const iw = W - m.l - m.r, ih = H - m.t - m.b
  const max = Math.max(...series.map(d => d.price)) * 1.08
  const minRow = series.reduce((a, b) => (b.price < a.price ? b : a))
  const bw = Math.max(3, Math.min(18, iw / series.length - 2))

  const x = (i: number) => m.l + (iw / series.length) * i + (iw / series.length - bw) / 2
  const y = (v: number) => m.t + ih * (1 - v / max)

  return (
    <div className="card p-3">
      <div className="text-xs muted mb-1">
        Cheapest fare by departure date <span className="tabular">({series.length} dates)</span>
        {hover && (
          <span className="ml-2" style={{ color: 'var(--ink)' }}>
            {hover.date}: <b className="tabular">{fmtMoney(hover.price)}</b>
            {' '}· {hover.stops === 0 ? 'direct' : `${hover.stops} stop(s)`} · fit {hover.fit_score}
          </span>
        )}
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img"
        aria-label="Cheapest price per departure date">
        {[0.25, 0.5, 0.75, 1].map(f => (
          <g key={f}>
            <line x1={m.l} x2={W - m.r} y1={y(max * f)} y2={y(max * f)}
              stroke="var(--grid)" strokeWidth={1} />
            <text x={m.l - 5} y={y(max * f) + 3} textAnchor="end" fontSize={9}
              fill="var(--muted)" className="tabular">{fmtMoney(max * f)}</text>
          </g>
        ))}
        <line x1={m.l} x2={W - m.r} y1={m.t + ih} y2={m.t + ih}
          stroke="var(--baseline)" strokeWidth={1} />
        {series.map((d, i) => {
          const isRec = d.date === recommendedDate
          const isMin = d.date === minRow.date
          const by = y(d.price)
          return (
            <g key={d.date}
              onMouseEnter={() => setHover(d)} onMouseLeave={() => setHover(null)}>
              {/* hit target larger than the mark */}
              <rect x={x(i) - 2} y={m.t} width={bw + 4} height={ih} fill="transparent" />
              <path d={`M${x(i)},${m.t + ih} L${x(i)},${by + 4} Q${x(i)},${by} ${x(i) + 4},${by} L${x(i) + bw - 4},${by} Q${x(i) + bw},${by} ${x(i) + bw},${by + 4} L${x(i) + bw},${m.t + ih} Z`}
                fill={isRec ? 'var(--series-1)' : 'color-mix(in oklab, var(--series-1) 55%, var(--surface))'}
                stroke={hover?.date === d.date ? 'var(--ink)' : 'none'} strokeWidth={1} />
              {(isMin || isRec) && (
                <text x={x(i) + bw / 2} y={by - 4} textAnchor="middle" fontSize={9}
                  fill={isRec ? 'var(--ink)' : 'var(--ink-2)'} className="tabular">
                  {isRec ? '▲ pick' : fmtMoney(d.price)}
                </text>
              )}
            </g>
          )
        })}
        <text x={m.l} y={H - 8} fontSize={9} fill="var(--muted)">{series[0].date}</text>
        <text x={W - m.r} y={H - 8} fontSize={9} fill="var(--muted)" textAnchor="end">
          {series[series.length - 1].date}
        </text>
      </svg>
    </div>
  )
}
