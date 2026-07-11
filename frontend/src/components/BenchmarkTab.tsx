import { useState } from 'react'
import { marked } from 'marked'
import { runBenchmark } from '../api'
import type { Benchmark, BenchmarkRun } from '../types'

export default function BenchmarkTab({ benchmarks }: { benchmarks: Benchmark[] }) {
  const [runs, setRuns] = useState<Record<string, BenchmarkRun | 'running'>>({})

  async function runOne(id: string) {
    setRuns(r => ({ ...r, [id]: 'running' }))
    try {
      const res = await runBenchmark(id)
      setRuns(r => ({ ...r, [id]: res }))
    } catch {
      setRuns(r => { const c = { ...r }; delete c[id]; return c })
    }
  }

  async function runAll() {
    for (const b of benchmarks) await runOne(b.prompt_id)
  }

  const done = Object.values(runs).filter(r => r !== 'running') as BenchmarkRun[]
  const passed = done.reduce((s, r) => s + r.passed, 0)
  const total = done.reduce((s, r) => s + r.total, 0)

  return (
    <div className="space-y-3">
      <div className="card p-3 flex items-center gap-3 flex-wrap">
        <div className="text-sm ink2">
          Runs the judges' own <b>benchmark_prompts.json</b> live and verifies every
          <i> expected_behavior</i> programmatically against the actual response.
        </div>
        <span className="flex-1" />
        {total > 0 && (
          <span className="text-sm tabular font-semibold"
            style={{ color: passed === total ? 'var(--status-good)' : 'var(--status-warn)' }}>
            {passed}/{total} behaviors verified
          </span>
        )}
        <button onClick={runAll} className="px-4 py-1.5 rounded-lg font-semibold text-sm"
          style={{ background: 'var(--accent)', color: '#fff' }}>
          Run all 6
        </button>
      </div>

      {benchmarks.map(b => {
        const run = runs[b.prompt_id]
        return (
          <div key={b.prompt_id} className="card p-3">
            <div className="flex items-center gap-2 flex-wrap">
              <b style={{ color: 'var(--accent)' }}>{b.prompt_id}</b>
              <span className="chip">{b.user_id}</span>
              <span className="ink2 text-sm flex-1">“{b.request}”</span>
              {run === 'running'
                ? <span className="muted text-sm animate-pulse">running…</span>
                : run
                  ? <span className="tabular font-semibold text-sm"
                      style={{ color: run.passed === run.total ? 'var(--status-good)' : 'var(--status-warn)' }}>
                      {run.passed}/{run.total} ✓
                    </span>
                  : <button onClick={() => runOne(b.prompt_id)} className="chip hover:brightness-125 cursor-pointer">Run</button>}
            </div>
            {run && run !== 'running' && (
              <div className="mt-2 space-y-1">
                {run.checks.map((c, i) => (
                  <div key={i} className="text-xs flex gap-2">
                    <span style={{ color: c.passed ? 'var(--status-good)' : 'var(--status-critical)' }}>
                      {c.passed ? '✓' : '✗'}
                    </span>
                    <span className="ink2 w-72 shrink-0">{c.behavior}</span>
                    <span className="muted flex-1">{c.evidence}</span>
                  </div>
                ))}
                <details className="mt-1">
                  <summary className="cursor-pointer text-xs muted">
                    Full narrative · {run.response.total_candidates} candidates · {run.response.elapsed_ms}ms
                  </summary>
                  <div className="narrative text-sm mt-2"
                    dangerouslySetInnerHTML={{ __html: marked.parse(run.response.narrative) as string }} />
                </details>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
