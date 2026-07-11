import { useEffect, useState } from 'react'
import { Clock3, Database, Navigation, ShieldCheck, Sparkles } from 'lucide-react'
import { fetchBenchmarks, fetchMeta, fetchProfile, fetchUsers, postRecommend, postRefine } from './api'
import type { Benchmark, Meta, RecommendResponse, UserProfile, UserSummary } from './types'
import PersonaRail from './components/PersonaRail'
import ProfilePanel from './components/ProfilePanel'
import TripConsole from './components/TripConsole'
import ResultsView from './components/ResultsView'
import BenchmarkTab from './components/BenchmarkTab'

function LoadingSkeleton() {
  return (
    <div className="space-y-3">
      <div className="skeleton h-14" />
      <div className="skeleton h-24" />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
        <div className="skeleton h-56" />
        <div className="skeleton h-56" />
      </div>
      <div className="skeleton h-40" />
      <div className="text-center muted text-sm animate-pulse pt-1" role="status" aria-live="polite">
        Searching 50,000 itineraries — routing, scoring, explaining…
      </div>
    </div>
  )
}

export default function App() {
  const [meta, setMeta] = useState<Meta | null>(null)
  const [users, setUsers] = useState<UserSummary[]>([])
  const [benchmarks, setBenchmarks] = useState<Benchmark[]>([])
  const [selected, setSelected] = useState<string>('U01')
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [query, setQuery] = useState('')
  const [lastRun, setLastRun] = useState<{ userId: string; query: string } | null>(null)
  const [response, setResponse] = useState<RecommendResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [refining, setRefining] = useState(false)
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
      setLastRun({ userId, query: q })
    } catch (e) {
      setError(String(e))
    } finally {
      setLoading(false)
    }
  }

  async function refine(followup: string) {
    if (!lastRun || !followup.trim()) return
    setRefining(true); setError('')
    try {
      setResponse(await postRefine(lastRun.userId, lastRun.query, followup))
    } catch (e) {
      setError(String(e))
    } finally {
      setRefining(false)
    }
  }

  const benchUsers = new Map(benchmarks.map(b => [b.user_id, b.prompt_id]))

  return (
    <div className="h-full flex flex-col">
      <header className="flex items-center gap-4 px-5 py-3 border-b hairline shrink-0"
        style={{ background: 'var(--surface)' }}>
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'var(--accent-grad)' }}>
            <Navigation size={17} color="#fff" strokeWidth={2.5} />
          </div>
          <div>
            <div className="text-[17px] font-bold tracking-tight leading-none">
              Way<span className="wordmark">Finder</span>
            </div>
            <div className="muted text-[11px] mt-0.5">reads the traveler, not just the query</div>
          </div>
        </div>
        <div className="flex-1" />
        {meta && (
          <div className="flex items-center gap-2 text-xs">
            <span className="chip" title="All relative dates resolve against this simulated travel clock (dataset spans 2025-01 → 2026-07)">
              <Clock3 size={13} /> <b className="tabular">{meta.sim_today}</b>
            </span>
            <span className="chip" title="Bundled hackathon dataset — searched fully offline">
              <Database size={13} /> {meta.flights.toLocaleString()} flights · {meta.routes.toLocaleString()} routes
            </span>
            {meta.llm_mode === 'assist' && meta.llm_live ? (
              <span className="chip chip-accent"
                title={`Local ${meta.llm_model} assists parsing & prose — every number is verified against the deterministic engine; any failure falls back instantly`}>
                <Sparkles size={13} /> AI: {meta.llm_model} · guarded
              </span>
            ) : (
              <span className="chip"
                title="Deterministic reasoning engine — same architecture, zero external dependencies. Start Ollama to enable the AI assist layer.">
                <ShieldCheck size={13} /> AI: deterministic engine
              </span>
            )}
          </div>
        )}
      </header>

      <div className="flex flex-1 min-h-0">
        <PersonaRail users={users} selected={selected} onSelect={setSelected} benchUsers={benchUsers} />

        <main className="flex-1 min-w-0 overflow-y-auto">
          <div className="max-w-5xl mx-auto p-4 space-y-4">
            <div className="flex gap-1.5 text-sm">
              {([['plan', 'Plan a trip'], ['bench', 'Benchmark self-grading']] as const).map(([key, label]) => (
                <button key={key} onClick={() => setTab(key)}
                  className="px-4 py-2 rounded-lg font-medium transition-colors"
                  style={tab === key
                    ? { background: 'var(--surface-2)', color: 'var(--ink)', border: '1px solid var(--border-strong)' }
                    : { color: 'var(--muted)', border: '1px solid transparent' }}>
                  {label}
                </button>
              ))}
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
                {error && (
                  <div className="card p-3 text-sm" style={{ borderColor: 'var(--status-critical)' }}>{error}</div>
                )}
                {loading && <LoadingSkeleton />}
                {!loading && response && (
                  <ResultsView r={response} onRefine={refine} refining={refining} />
                )}
                {!loading && !response && !error && (
                  <div className="card p-10 text-center rise-in">
                    <div className="mx-auto w-10 h-10 rounded-full flex items-center justify-center mb-3"
                      style={{ background: 'var(--accent-soft)' }}>
                      <Navigation size={18} style={{ color: 'var(--accent)' }} />
                    </div>
                    <div className="font-semibold mb-1">Where to?</div>
                    <div className="muted text-sm">
                      Pick a traveler on the left, then ask for a trip — or click a benchmark prompt above.
                    </div>
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
