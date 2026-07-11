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
    <div className="card p-3 space-y-2.5">
      <div className="flex gap-2">
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && onRun(query)}
          placeholder='Ask anything — “cheapest way to Bali this summer”, “multi-city Asia trip”…'
          className="flex-1 px-3 py-2 rounded-lg outline-none border hairline text-sm"
          style={{ background: 'var(--surface-2)', color: 'var(--ink)' }}
        />
        <button
          onClick={() => onRun(query)} disabled={loading}
          className="px-4 py-2 rounded-lg font-semibold text-sm disabled:opacity-50"
          style={{ background: 'var(--accent)', color: '#fff' }}>
          {loading ? 'Planning…' : 'Plan it'}
        </button>
      </div>
      <div className="flex flex-wrap gap-1.5 items-center">
        <span className="muted text-xs mr-1">Judge benchmarks (auto-selects the right traveler):</span>
        {benchmarks.map(b => (
          <button key={b.prompt_id} onClick={() => onBenchmark(b)} disabled={loading}
            className="chip hover:brightness-125 cursor-pointer disabled:opacity-50"
            title={`${b.user_id}: ${b.request}`}>
            <b style={{ color: 'var(--accent)' }}>{b.prompt_id}</b>
            <span className="ml-1">{b.request.length > 42 ? b.request.slice(0, 42) + '…' : b.request}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
