import { useEffect, useState } from 'react'
import { fetchBenchmarks, fetchMeta, fetchProfile, fetchUsers, postRecommend } from './api'
import type { Benchmark, Meta, RecommendResponse, UserProfile, UserSummary } from './types'
import PersonaRail from './components/PersonaRail'
import ProfilePanel from './components/ProfilePanel'
import TripConsole from './components/TripConsole'
import ResultsView from './components/ResultsView'
import BenchmarkTab from './components/BenchmarkTab'

export default function App() {
  const [meta, setMeta] = useState<Meta | null>(null)
  const [users, setUsers] = useState<UserSummary[]>([])
  const [benchmarks, setBenchmarks] = useState<Benchmark[]>([])
  const [selected, setSelected] = useState<string>('U01')
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState<RecommendResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [tab, setTab] = useState<'plan' | 'bench'>('plan')

  useEffect(() => {
    fetchMeta().then(setMeta).catch(() => setError('Backend not reachable — start uvicorn on :8000'))
    fetchUsers().then(setUsers).catch(() => {})
    fetchBenchmarks().then(setBenchmarks).catch(() => {})
  }, [])

  useEffect(() => {
    fetchProfile(selected).then(setProfile).catch(() => setProfile(null))
  }, [selected])

  async function run(userId: string, q: string) {
    if (!q.trim()) return
    setLoading(true); setError(''); setTab('plan')
    try {
      setResponse(await postRecommend(userId, q))
    } catch (e) {
      setError(String(e))
    } finally {
      setLoading(false)
    }
  }

  const benchUsers = new Map(benchmarks.map(b => [b.user_id, b.prompt_id]))

  return (
    <div className="h-full flex flex-col">
      <header className="flex items-center gap-3 px-4 py-2.5 border-b hairline shrink-0"
        style={{ background: 'var(--surface)' }}>
        <div className="text-lg font-semibold tracking-tight">
          <span style={{ color: 'var(--accent)' }}>◆</span> WayFinder
        </div>
        <div className="muted text-xs">AI Air Travel Companion — reads the traveler, not just the query</div>
        <div className="flex-1" />
        {meta && (
          <div className="flex items-center gap-2 text-xs">
            <span className="chip" title="All relative dates resolve against this simulated travel clock">
              🕑 travel clock: <b className="tabular">{meta.sim_today}</b>
            </span>
            <span className="chip">{meta.flights.toLocaleString()} flights · {meta.routes.toLocaleString()} routes</span>
            <span className="chip" title="Fully deterministic pipeline — no LLM required">
              LLM: {meta.llm_mode}{meta.llm_mode === 'off' ? ' (deterministic)' : ''}
            </span>
          </div>
        )}
      </header>

      <div className="flex flex-1 min-h-0">
        <PersonaRail users={users} selected={selected} onSelect={setSelected} benchUsers={benchUsers} />

        <main className="flex-1 min-w-0 overflow-y-auto">
          <div className="max-w-5xl mx-auto p-4 space-y-4">
            <div className="flex gap-1 text-sm">
              <button onClick={() => setTab('plan')}
                className={`px-3 py-1.5 rounded-t-lg border hairline border-b-0 ${tab === 'plan' ? 'font-semibold' : 'muted'}`}
                style={{ background: tab === 'plan' ? 'var(--surface)' : 'transparent' }}>
                Plan a trip
              </button>
              <button onClick={() => setTab('bench')}
                className={`px-3 py-1.5 rounded-t-lg border hairline border-b-0 ${tab === 'bench' ? 'font-semibold' : 'muted'}`}
                style={{ background: tab === 'bench' ? 'var(--surface)' : 'transparent' }}>
                Benchmark self-grading
              </button>
            </div>

            {tab === 'plan' ? (
              <>
                {profile && <ProfilePanel profile={profile} />}
                <TripConsole
                  query={query} setQuery={setQuery} benchmarks={benchmarks}
                  loading={loading}
                  onRun={(q) => run(selected, q)}
                  onBenchmark={(b) => { setSelected(b.user_id); setQuery(b.request); run(b.user_id, b.request) }}
                />
                {error && <div className="card p-3 text-sm" style={{ borderColor: 'var(--status-critical)' }}>{error}</div>}
                {loading && <div className="card p-6 text-center muted animate-pulse">Searching 50,000 itineraries…</div>}
                {!loading && response && <ResultsView r={response} />}
                {!loading && !response && !error && (
                  <div className="card p-8 text-center muted">
                    Pick a traveler on the left, then ask for a trip — or click a benchmark prompt above.
                  </div>
                )}
              </>
            ) : (
              <BenchmarkTab benchmarks={benchmarks} />
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
