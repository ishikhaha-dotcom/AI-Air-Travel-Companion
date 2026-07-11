import { Award, Scale, Timer, Wallet } from 'lucide-react'
import type { RecommendResponse, TradeoffBrief } from '../types'
import { fmtMoney } from '../airports'

const KIND_META = {
  recommended: { label: 'Recommended', color: 'var(--accent)', Icon: Award },
  cheapest: { label: 'Cheapest', color: 'var(--series-2)', Icon: Wallet },
  fastest: { label: 'Fastest', color: 'var(--series-3)', Icon: Timer },
} as const

function Tile({ b, kind, party, delta }: {
  b: TradeoffBrief; kind: keyof typeof KIND_META; party: number; delta?: string
}) {
  const { label, color, Icon } = KIND_META[kind]
  const highlight = kind === 'recommended'
  return (
    <div className="card p-3.5 flex-1 min-w-44"
      style={highlight ? { borderColor: 'rgba(79,143,247,0.5)', background: 'linear-gradient(180deg, rgba(79,143,247,0.06), transparent)' } : undefined}>
      <div className="flex items-center gap-1.5 text-xs font-semibold" style={{ color }}>
        <Icon size={13} /> {label}
      </div>
      <div className="text-[22px] font-bold tabular mt-1 leading-none">
        {fmtMoney(party > 1 ? b.price_party : b.price_pp)}
      </div>
      <div className="muted text-xs tabular mt-1.5">
        {b.duration} · {b.stops === 0 ? 'direct' : `${b.stops} stop${b.stops > 1 ? 's' : ''}`} · fit {b.fit_score}
      </div>
      {delta && <div className="text-[11px] mt-1" style={{ color: 'var(--ink-2)' }}>{delta}</div>}
    </div>
  )
}

export default function TradeoffStrip({ t, party }: { t: RecommendResponse['tradeoffs']; party: number }) {
  const rec = t.recommended
  if (!rec) return null

  const sameCheapest = t.cheapest && t.cheapest.key === rec.key
  const sameFastest = t.fastest && t.fastest.key === rec.key
  const allSame = (!t.cheapest || sameCheapest) && (!t.fastest || sameFastest)

  return (
    <div className="space-y-2.5 rise-in-2">
      {allSame ? (
        /* one flight wins on every axis — say it once, proudly */
        <div className="card p-4 flex items-center gap-4 flex-wrap"
          style={{ borderColor: 'rgba(79,143,247,0.5)', background: 'linear-gradient(180deg, rgba(79,143,247,0.06), transparent)' }}>
          <div className="flex items-center gap-1.5 text-xs font-semibold" style={{ color: 'var(--accent)' }}>
            <Award size={14} /> Recommended
          </div>
          <div className="text-[24px] font-bold tabular leading-none">
            {fmtMoney(party > 1 ? rec.price_party : rec.price_pp)}
          </div>
          <div className="muted text-sm tabular">
            {rec.duration} · {rec.stops === 0 ? 'direct' : `${rec.stops} stop${rec.stops > 1 ? 's' : ''}`} · fit {rec.fit_score}
          </div>
          <span className="flex-1" />
          <div className="flex gap-1.5">
            <span className="badge" style={{ background: 'rgba(45,185,140,0.15)', color: 'var(--series-2)' }}>also the cheapest</span>
            <span className="badge" style={{ background: 'rgba(224,166,58,0.15)', color: 'var(--series-3)' }}>also the fastest</span>
          </div>
        </div>
      ) : (
        <div className="flex gap-2.5 flex-wrap">
          <Tile b={rec} kind="recommended" party={party} />
          {t.cheapest && !sameCheapest && (
            <Tile b={t.cheapest} kind="cheapest" party={party}
              delta={`${fmtMoney(Math.abs((party > 1 ? rec.price_party : rec.price_pp) - (party > 1 ? t.cheapest.price_party : t.cheapest.price_pp)))} less than our pick`} />
          )}
          {t.fastest && !sameFastest && (
            <Tile b={t.fastest} kind="fastest" party={party}
              delta={`${Math.round(Math.abs(rec.duration_minutes - t.fastest.duration_minutes) / 60)}h quicker than our pick`} />
          )}
        </div>
      )}

      {t.statements && t.statements.length > 0 && (
        <div className="card p-3.5 space-y-1.5">
          <div className="text-[10.5px] font-semibold uppercase tracking-wider muted">Trade-offs, in plain terms</div>
          {t.statements.map((s, k) => (
            <div key={k} className="text-sm ink2 flex gap-2 leading-relaxed">
              <Scale size={14} className="shrink-0 mt-0.5" style={{ color: 'var(--series-3)' }} />
              <span>{s}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
