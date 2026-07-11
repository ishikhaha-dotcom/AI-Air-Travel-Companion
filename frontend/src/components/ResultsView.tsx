import { marked } from 'marked'
import type { RecommendResponse } from '../types'
import TradeoffStrip from './TradeoffStrip'
import PriceCalendar from './PriceCalendar'
import RouteMap from './RouteMap'
import ResultCard from './ResultCard'
import { AIRPORTS } from '../airports'

export default function ResultsView({ r }: { r: RecommendResponse }) {
  const i = r.intent
  const dests = i.destinations.length
    ? i.destinations.map(d => `${AIRPORTS[d]?.city ?? d} (${d})`).join(' + ')
    : `${i.region || 'open-ended'} discovery`

  return (
    <div className="space-y-3">
      {/* intent understanding */}
      <div className="card p-3">
        <div className="text-sm">
          <b>Understood:</b> <span className="ink2">{i.trip_type.replaceAll('_', ' ')}</span> from{' '}
          <b>{AIRPORTS[i.origin]?.city} ({i.origin})</b> to <b>{dests}</b>,{' '}
          <span className="tabular ink2">{i.window_start} → {i.window_end}</span>
          {i.party_size > 1 && <> · party of <b>{i.party_size}</b></>}
          {i.purpose && <> · {i.purpose}</>}
          {i.emphasis && <> · optimizing for <b>{i.emphasis}</b></>}
          <span className="muted"> — {r.total_candidates} candidates scored in {r.elapsed_ms}ms</span>
        </div>
        {i.notes.length > 0 && (
          <div className="mt-1.5 flex flex-wrap gap-1.5">
            {i.notes.map((n, k) => <span key={k} className="chip">🧠 {n}</span>)}
          </div>
        )}
      </div>

      {/* honesty banners */}
      {r.route_facts.map((f, k) => (
        <div key={k} className="rounded-lg px-3 py-2 text-sm"
          style={{ background: 'rgba(236,131,90,0.08)', border: '1px solid rgba(236,131,90,0.4)' }}>
          <b style={{ color: 'var(--status-serious)' }}>Route reality:</b> <span className="ink2">{f}</span>
        </div>
      ))}
      {r.relaxations.map((x, k) => (
        <div key={k} className="rounded-lg px-3 py-2 text-sm"
          style={{ background: 'rgba(250,178,25,0.08)', border: '1px solid rgba(250,178,25,0.35)' }}>
          <b style={{ color: 'var(--status-warn)' }}>Adjusted:</b>{' '}
          <span className="ink2">{x.detail} → {x.count} option(s)</span>
        </div>
      ))}

      {r.recommendations.length > 0 && (
        <>
          <TradeoffStrip t={r.tradeoffs} party={i.party_size} />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
            <RouteMap option={r.recommendations[0]} />
            {r.price_by_date.length > 1
              ? <PriceCalendar series={r.price_by_date} recommendedDate={r.recommendations[0].dep_date} />
              : (
                <div className="card p-3">
                  <div className="text-xs muted mb-2">Scoring weights derived from this traveler's profile</div>
                  {Object.entries(r.weights).map(([k, v]) => (
                    <div key={k} className="flex items-center gap-2 text-xs mb-1.5">
                      <span className="w-24 ink2 capitalize">{k}</span>
                      <div className="flex-1 h-2 rounded-full" style={{ background: 'var(--grid)' }}>
                        <div className="h-2 rounded-full" style={{ width: `${v * 100}%`, background: 'var(--series-1)' }} />
                      </div>
                      <span className="tabular w-10 text-right ink2">{(v * 100).toFixed(0)}%</span>
                    </div>
                  ))}
                  {r.weight_notes.map((n, k) => <div key={k} className="muted text-[11px] mt-1">· {n}</div>)}
                </div>
              )}
          </div>

          {(r.insights.length > 0 || r.flex_insight) && (
            <div className="card p-3 space-y-1">
              <div className="text-xs muted">Season · demand · availability intelligence</div>
              {r.insights.map((s, k) => <div key={k} className="text-sm ink2">📈 {s}</div>)}
              {r.flex_insight && <div className="text-sm ink2">📅 {r.flex_insight}</div>}
            </div>
          )}

          <div className="space-y-3">
            {r.recommendations.map((o, idx) => (
              <ResultCard key={o.key} option={o} rank={idx + 1} party={i.party_size} weights={r.weights} />
            ))}
          </div>
        </>
      )}

      <details className="card p-3" open={r.recommendations.length === 0}>
        <summary className="cursor-pointer text-sm font-semibold">
          Full reasoning narrative (deterministic, evidence-cited)
        </summary>
        <div className="narrative text-sm mt-2"
          dangerouslySetInnerHTML={{ __html: marked.parse(r.narrative) as string }} />
      </details>
    </div>
  )
}
