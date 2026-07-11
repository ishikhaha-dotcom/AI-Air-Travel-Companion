import { marked } from 'marked'
import { AlertOctagon, Brain, CalendarDays, SearchX, ShieldCheck, SlidersHorizontal, Sparkles, TrendingUp, Wrench } from 'lucide-react'
import type { RecommendResponse } from '../types'
import TradeoffStrip from './TradeoffStrip'
import PriceCalendar from './PriceCalendar'
import RouteMap from './RouteMap'
import CompareTable from './CompareTable'
import ResultCard from './ResultCard'
import RefineBar from './RefineBar'
import { AIRPORTS } from '../airports'
import { featureLabel } from '../labels'

export default function ResultsView({ r, onRefine, refining }: {
  r: RecommendResponse
  onRefine: (followup: string) => void
  refining: boolean
}) {
  const i = r.intent
  const dests = i.destinations.length
    ? i.destinations.map(d => `${AIRPORTS[d]?.city ?? d} (${d})`).join(' + ')
    : `${i.region || 'open-ended'} discovery`

  return (
    <div className="space-y-3">
      {/* intent understanding */}
      <div className="card p-4 rise-in">
        <div className="text-sm leading-relaxed">
          <b>Understood:</b> <span className="ink2">{i.trip_type.replaceAll('_', ' ')}</span> from{' '}
          <b>{AIRPORTS[i.origin]?.city} ({i.origin})</b> to <b>{dests}</b>,{' '}
          <span className="tabular ink2">{i.window_start} → {i.window_end}</span>
          {i.party_size > 1 && <> · party of <b>{i.party_size}</b></>}
          {i.purpose && <> · {i.purpose}</>}
          {i.emphasis && <> · optimizing for <b>{i.emphasis}</b></>}
          <span className="muted"> — {r.total_candidates} candidates scored in {r.elapsed_ms} ms</span>
        </div>
        {i.notes.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1.5">
            {i.notes.map((n, k) => (
              <span key={k} className="chip">
                <Brain size={12} style={{ color: 'var(--series-5)' }} /> {n}
              </span>
            ))}
          </div>
        )}
      </div>

      <RefineBar r={r} onRefine={onRefine} refining={refining} />

      {/* honesty banners */}
      {r.route_facts.map((f, k) => (
        <div key={k} className="rounded-xl px-3.5 py-2.5 text-sm flex gap-2.5 rise-in-1"
          style={{ background: 'rgba(240,138,92,0.08)', border: '1px solid rgba(240,138,92,0.4)' }}>
          <AlertOctagon size={16} className="shrink-0 mt-0.5" style={{ color: 'var(--status-serious)' }} />
          <div><b style={{ color: 'var(--status-serious)' }}>Route reality:</b> <span className="ink2">{f}</span></div>
        </div>
      ))}
      {r.relaxations.map((x, k) => (
        <div key={k} className="rounded-xl px-3.5 py-2.5 text-sm flex gap-2.5 rise-in-1"
          style={{ background: 'rgba(245,184,61,0.08)', border: '1px solid rgba(245,184,61,0.35)' }}>
          <Wrench size={16} className="shrink-0 mt-0.5" style={{ color: 'var(--status-warn)' }} />
          <div>
            <b style={{ color: 'var(--status-warn)' }}>Adjusted:</b>{' '}
            <span className="ink2">{x.detail} → {x.count} option{x.count !== 1 ? 's' : ''}</span>
          </div>
        </div>
      ))}

      {r.recommendations.length > 0 && (
        <>
          <TradeoffStrip t={r.tradeoffs} party={i.party_size} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 rise-in-2">
            <RouteMap option={r.recommendations[0]} />
            {r.price_by_date.length > 1
              ? <PriceCalendar series={r.price_by_date} recommendedDate={r.recommendations[0].dep_date} />
              : (
                <div className="card p-4">
                  <div className="text-[10.5px] font-semibold uppercase tracking-wider muted mb-2.5 flex items-center gap-1.5">
                    <SlidersHorizontal size={12} /> Scoring weights — derived from this traveler's profile
                  </div>
                  {Object.entries(r.weights).map(([k, v]) => (
                    <div key={k} className="flex items-center gap-2.5 text-xs mb-2">
                      <span className="w-26 ink2" style={{ width: 104 }}>{featureLabel(k)}</span>
                      <div className="flex-1 h-2 rounded-full overflow-hidden" style={{ background: 'var(--grid)' }}>
                        <div className="h-2 rounded-full" style={{ width: `${v * 100}%`, background: 'var(--accent-grad)' }} />
                      </div>
                      <span className="tabular w-10 text-right ink2 font-medium">{(v * 100).toFixed(0)}%</span>
                    </div>
                  ))}
                  {r.weight_notes.map((n, k) => <div key={k} className="muted text-[11px] mt-1.5 leading-relaxed">· {n}</div>)}
                </div>
              )}
          </div>

          {(r.insights.length > 0 || r.flex_insight) && (
            <div className="card p-4 space-y-1.5 rise-in-2">
              <div className="text-[10.5px] font-semibold uppercase tracking-wider muted">
                Season · demand · availability intelligence
              </div>
              {r.insights.map((s, k) => (
                <div key={k} className="text-sm ink2 flex gap-2 leading-relaxed">
                  <TrendingUp size={14} className="shrink-0 mt-0.5" style={{ color: 'var(--series-2)' }} />
                  <span>{s}</span>
                </div>
              ))}
              {r.flex_insight && (
                <div className="text-sm ink2 flex gap-2 leading-relaxed">
                  <CalendarDays size={14} className="shrink-0 mt-0.5" style={{ color: 'var(--series-1)' }} />
                  <span>{r.flex_insight}</span>
                </div>
              )}
            </div>
          )}

          <CompareTable options={r.recommendations} party={i.party_size} />

          <div className="space-y-3">
            {r.recommendations.map((o, idx) => (
              <ResultCard key={o.key} option={o} rank={idx + 1} party={i.party_size} weights={r.weights}
                top={r.recommendations[0]} />
            ))}
          </div>
        </>
      )}

      {r.recommendations.length === 0 && (
        <div className="card p-10 text-center rise-in-1">
          <div className="mx-auto w-10 h-10 rounded-full flex items-center justify-center mb-3"
            style={{ background: 'rgba(240,138,92,0.12)' }}>
            <SearchX size={18} style={{ color: 'var(--status-serious)' }} />
          </div>
          <div className="font-semibold mb-1">No itinerary could be built for this request</div>
          <div className="muted text-sm max-w-md mx-auto leading-relaxed">
            Even after relaxing constraints{r.relaxations.length > 0 ? ` (${r.relaxations.length} attempted, above)` : ''},
            the dataset has no matching service. Try a wider date range, a different destination,
            or check the full reasoning narrative below for exactly what was ruled out and why.
          </div>
        </div>
      )}

      <details className="card p-4 rise-in-3" open={r.recommendations.length === 0}>
        <summary className="cursor-pointer text-sm font-semibold flex items-center gap-2">
          Full reasoning narrative
          {r.llm_polished ? (
            <span className="badge" style={{ background: 'var(--accent-soft)', color: 'var(--accent)' }}>
              <Sparkles size={11} /> polished by AI · numbers verified
            </span>
          ) : (
            <span className="badge" style={{ background: 'var(--surface-3)', color: 'var(--ink-2)' }}>
              <ShieldCheck size={11} /> deterministic · evidence-cited
            </span>
          )}
        </summary>
        <div className="narrative text-sm mt-2"
          dangerouslySetInnerHTML={{ __html: marked.parse(r.narrative) as string }} />
      </details>
    </div>
  )
}
