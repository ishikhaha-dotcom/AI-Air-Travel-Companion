import { useState } from 'react'
import { CornerDownRight, Loader2, Wand2 } from 'lucide-react'
import type { RecommendResponse } from '../types'

const SUGGESTIONS = ['make it cheaper', 'no redeyes', 'direct only', 'under $1,000', 'a week later']

/** Follow-up refinement: patch the parsed intent conversationally and re-plan. */
export default function RefineBar({ r, onRefine, refining }: {
  r: RecommendResponse
  onRefine: (followup: string) => void
  refining: boolean
}) {
  const [text, setText] = useState('')
  const go = (t: string) => { if (t.trim() && !refining) { onRefine(t); setText('') } }

  return (
    <div className="card p-3 space-y-2 rise-in-2">
      <div className="flex items-center gap-2.5">
        <Wand2 size={15} className="shrink-0" style={{ color: 'var(--accent)' }} />
        <input
          value={text} onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && go(text)}
          placeholder="Refine this plan — “make it cheaper”, “no redeyes”, “under $900”…"
          className="input flex-1 px-3 py-2 text-sm"
        />
        <button onClick={() => go(text)} disabled={refining || !text.trim()}
          className="btn-ghost flex items-center gap-1.5 text-sm disabled:opacity-40">
          {refining ? <Loader2 size={14} className="animate-spin" /> : <CornerDownRight size={14} />}
          Refine
        </button>
      </div>
      <div className="flex flex-wrap items-center gap-1.5">
        {SUGGESTIONS.map(s => (
          <button key={s} onClick={() => go(s)} disabled={refining}
            className="chip cursor-pointer hover:brightness-125 disabled:opacity-50">
            {s}
          </button>
        ))}
        {r.refinement && r.refinement.applied.length > 0 && (
          <>
            <span className="muted text-[11px] ml-1">applied:</span>
            {r.refinement.applied.map((a, i) => (
              <span key={i} className="chip chip-accent">{a}</span>
            ))}
          </>
        )}
      </div>
    </div>
  )
}
