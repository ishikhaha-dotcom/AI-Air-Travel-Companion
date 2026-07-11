import { useEffect, useState } from 'react'

/** Animated fit-score donut, 0–100. Color shifts with score band. */
export default function FitRing({ score, size = 56 }: { score: number; size?: number }) {
  const [shown, setShown] = useState(0)
  useEffect(() => {
    const t0 = performance.now()
    let raf = 0
    const tick = (t: number) => {
      const p = Math.min(1, (t - t0) / 600)
      setShown(score * (1 - Math.pow(1 - p, 3)))
      if (p < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [score])

  const r = (size - 8) / 2
  const c = 2 * Math.PI * r
  const color = score >= 75 ? 'var(--status-good)' : score >= 55 ? 'var(--accent)' : 'var(--status-warn)'

  return (
    <div className="relative shrink-0" style={{ width: size, height: size }} title={`Fit score ${score}/100 — personalized to this traveler's profile`}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="var(--grid)" strokeWidth={5} />
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth={5}
          strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c * (1 - shown / 100)} />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center leading-none">
        <span className="tabular font-bold" style={{ fontSize: size * 0.3, color }}>{Math.round(shown)}</span>
        <span className="muted" style={{ fontSize: size * 0.16 }}>fit</span>
      </div>
    </div>
  )
}
