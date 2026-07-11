import { useState } from 'react'
import { marked } from 'marked'
import { CheckCircle2, CircleDashed, Play, Trophy, XCircle } from 'lucide-react'
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
  const avgMs = done.length
    ? Math.round(done.reduce((s, r) => s + r.response.elapsed_ms, 0) / done.length)
    : 0
  const allGreen = total > 0 && passed === total && done.length === benchmarks.length

  return (
    <div className="space-y-3">
      <div className="card p-4 rise-in">
        <div className="flex items-center gap-3 flex-wrap">
          <div className="text-sm ink2 leading-relaxed flex-1 min-w-64">
            Runs the judges' own <b style={{ color: 'var(--ink)' }}>benchmark_prompts.json</b> live
            and verifies every <i>expected_behavior</i> programmatically against the actual response
            — the system grades itself on the official rubric.
          </div>
          <button onClick={runAll} className="btn-primary flex items-center gap-2 text-sm">
            <Play size={14} /> Run all 6
          </button>
        </div>
        {total > 0 && (
          <div className="flex items-center gap-4 mt-3 pt-3 border-t hairline">
            <div className="flex items-center gap-2">
              {allGreen && <Trophy size={18} style={{ color: 'var(--status-good)' }} />}
              <span className="text-[22px] font-bold tabular"
                style={{ color: passed === total ? 'var(--status-good)' : 'var(--status-warn)' }}>
                {passed}/{total}
              </span>
              <span className="muted text-xs">behaviors<br />verified</span>
            </div>
            <div className="h-8 w-px" style={{ background: 'var(--border)' }} />
            <div>
              <span className="text-[22px] font-bold tabular">{avgMs}<span className="text-sm muted"> ms</span></span>
              <div className="muted text-xs">avg response</div>
            </div>
            <div className="h-8 w-px" style={{ background: 'var(--border)' }} />
            <div>
              <span className="text-[22px] font-bold tabular">{done.length}/6</span>
              <div className="muted text-xs">prompts run</div>
            </div>
          </div>
        )}
      </div>

      {benchmarks.map(b => {
        const run = runs[b.prompt_id]
        return (
          <div key={b.prompt_id} className="card p-4 rise-in-1">
            <div className="flex items-center gap-2.5 flex-wrap">
              <b style={{ color: 'var(--accent)' }}>{b.prompt_id}</b>
              <span className="chip">{b.user_id}</span>
              <span className="ink2 text-sm flex-1">“{b.request}”</span>
              {run === 'running'
                ? <span className="muted text-sm animate-pulse flex items-center gap-1.5">
                    <CircleDashed size={14} className="animate-spin" /> running…
                  </span>
                : run
                  ? <span className="tabular font-bold text-sm flex items-center gap-1.5"
                      style={{ color: run.passed === run.total ? 'var(--status-good)' : 'var(--status-warn)' }}>
                      <CheckCircle2 size={15} /> {run.passed}/{run.total}
                    </span>
                  : <button onClick={() => runOne(b.prompt_id)}
                      className="btn-ghost text-xs flex items-center gap-1.5 !py-1.5">
                      <Play size={12} /> Run
                    </button>}
            </div>
            {run && run !== 'running' && (
              <div className="mt-2.5 space-y-1.5">
                {run.checks.map((c, i) => (
                  <div key={i} className="text-xs flex gap-2 leading-relaxed">
                    {c.passed
                      ? <CheckCircle2 size={14} className="shrink-0 mt-0.5" style={{ color: 'var(--status-good)' }} />
                      : <XCircle size={14} className="shrink-0 mt-0.5" style={{ color: 'var(--status-critical)' }} />}
                    <span className="ink2 w-72 shrink-0">{c.behavior}</span>
                    <span className="muted flex-1">{c.evidence}</span>
                  </div>
                ))}
                <details className="mt-1">
                  <summary className="cursor-pointer text-xs muted hover:text-[var(--ink-2)]">
                    Full narrative · {run.response.total_candidates} candidates · {run.response.elapsed_ms} ms
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
