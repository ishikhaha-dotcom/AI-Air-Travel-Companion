import { Loader2, Send } from 'lucide-react'
import type { Benchmark } from '../types'

export default function TripConsole({ query, setQuery, benchmarks, loading, onRun, onBenchmark }: {
  query: string
  setQuery: (q: string) => void
  benchmarks: Benchmark[]
  loading: boolean
  onRun: (q: string) => void
  onBenchmark: (b: Benchmark) => void
}) {
  return (
    <div className="card p-4 space-y-3 rise-in-1">
      <div className="flex gap-2.5">
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && onRun(query)}
          placeholder='Ask anything — “cheapest way to Bali this summer”, “multi-city Asia trip”…'
          className="input flex-1 px-3.5 py-2.5 text-[14px]"
        />
        <button onClick={() => onRun(query)} disabled={loading}
          className="btn-primary flex items-center gap-2 text-sm">
          {loading ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
          {loading ? 'Planning…' : 'Plan it'}
        </button>
      </div>
      <div>
        <div className="muted text-[11px] mb-1.5">
          Judge benchmarks — one click selects the right traveler and runs their exact prompt:
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-1.5">
          {benchmarks.map(b => (
            <button key={b.prompt_id} onClick={() => onBenchmark(b)} disabled={loading}
              className="text-left px-3 py-2 rounded-lg border hairline text-xs transition-colors hover:border-[var(--border-strong)] hover:bg-[var(--surface-2)] disabled:opacity-50"
              title={`${b.user_id}: ${b.request}`}>
              <b style={{ color: 'var(--accent)' }}>{b.prompt_id}</b>
              <span className="ink2 ml-1.5">
                {b.request.length > 60 ? b.request.slice(0, 60) + '…' : b.request}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
