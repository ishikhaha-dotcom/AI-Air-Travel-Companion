import type { RecommendResponse, TradeoffBrief } from '../types'
import { fmtMoney } from '../airports'

function Tile({ b, accent, party }: { b: TradeoffBrief; accent: string; party: number }) {
  return (
    <div className="card p-3 flex-1 min-w-40" style={{ borderColor: accent }}>
      <div className="text-xs font-semibold" style={{ color: accent }}>{b.label}</div>
      <div className="text-xl font-semibold tabular mt-0.5">{fmtMoney(party > 1 ? b.price_party : b.price_pp)}</div>
      <div className="muted text-xs tabular">
        {b.duration} · {b.stops === 0 ? 'direct' : `${b.stops} stop(s)`} · fit {b.fit_score}
      </div>
    </div>
  )
}

export default function TradeoffStrip({ t, party }: { t: RecommendResponse['tradeoffs']; party: number }) {
  if (!t.recommended) return null
  return (
    <div className="space-y-2">
      <div className="flex gap-3 flex-wrap">
        <Tile b={t.recommended} accent="var(--accent)" party={party} />
        {t.cheapest && <Tile b={t.cheapest} accent="var(--series-2)" party={party} />}
        {t.fastest && <Tile b={t.fastest} accent="var(--series-3)" party={party} />}
      </div>
      {t.statements && t.statements.length > 0 && (
        <div className="card p-3 space-y-1">
          <div className="text-xs muted">Trade-offs, in plain terms</div>
          {t.statements.map((s, k) => <div key={k} className="text-sm ink2">⚖ {s}</div>)}
        </div>
      )}
    </div>
  )
}
