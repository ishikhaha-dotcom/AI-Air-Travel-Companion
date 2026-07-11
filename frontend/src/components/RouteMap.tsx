import { useMemo } from 'react'
import { geoGraticule10, geoNaturalEarth1, geoPath } from 'd3-geo'
import { feature } from 'topojson-client'
import type { Topology, GeometryCollection } from 'topojson-specification'
import landTopo from 'world-atlas/land-110m.json'
import { AIRPORTS } from '../airports'
import type { OptionJson } from '../types'

const LEG_COLORS = ['#4f8ff7', '#2db98c', '#e0a63a', '#a78bfa', '#34a853']

/** Offline SVG route map: bundled world-atlas coastlines (no tile servers),
 *  great-circle arcs per leg with a draw-in animation — works with zero internet. */
export default function RouteMap({ option }: { option: OptionJson }) {
  const W = 460, H = 260

  const { landPath, gratPath, projection } = useMemo(() => {
    const topo = landTopo as unknown as Topology<{ land: GeometryCollection }>
    const land = feature(topo, topo.objects.land)
    const proj = geoNaturalEarth1().fitExtent([[6, 6], [W - 6, H - 6]], { type: 'Sphere' })
    const p = geoPath(proj)
    return { landPath: p(land) ?? '', gratPath: p(geoGraticule10()) ?? '', projection: proj }
  }, [])

  const path = geoPath(projection)
  const stations: { code: string; x: number; y: number }[] = []
  const seen = new Set<string>()
  const segs: { d: string; color: string; dashed: boolean; len: number }[] = []

  option.legs.forEach((leg, li) => {
    const color = LEG_COLORS[li % LEG_COLORS.length]
    const points = [leg.origin,
      ...leg.flights.flatMap(f => f.layover_airports),
      ...(leg.self_transfer ? [leg.transfer_airport] : []),
      leg.destination]
    const uniq = points.filter((p, i) => p && points.indexOf(p) === i && AIRPORTS[p])
    for (let i = 0; i < uniq.length - 1; i++) {
      const a = AIRPORTS[uniq[i]], b = AIRPORTS[uniq[i + 1]]
      const d = path({ type: 'LineString', coordinates: [[a.lon, a.lat], [b.lon, b.lat]] })
      if (d) {
        const approxLen = Math.hypot(
          (projection([b.lon, b.lat])?.[0] ?? 0) - (projection([a.lon, a.lat])?.[0] ?? 0),
          (projection([b.lon, b.lat])?.[1] ?? 0) - (projection([a.lon, a.lat])?.[1] ?? 0),
        ) * 1.6 + 40
        segs.push({ d, color, dashed: leg.self_transfer, len: approxLen })
      }
    }
    for (const code of uniq) {
      if (!seen.has(code)) {
        seen.add(code)
        const [x, y] = projection([AIRPORTS[code].lon, AIRPORTS[code].lat]) ?? [0, 0]
        stations.push({ code, x, y })
      }
    }
  })

  return (
    <div className="card p-4">
      <div className="text-[10.5px] font-semibold uppercase tracking-wider muted mb-2">
        Recommended routing — {option.cities.join(' → ')}
        {option.self_transfer && <span style={{ color: 'var(--status-warn)', textTransform: 'none' }}> · dashed = self-transfer</span>}
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Route map">
        <path d={gratPath} fill="none" stroke="var(--grid)" strokeWidth={0.3} opacity={0.6} />
        <path d={landPath} fill="#242a34" stroke="#39414f" strokeWidth={0.6} />
        {segs.map((s, i) => (
          <g key={i}>
            {/* soft glow under the arc */}
            <path d={s.d} fill="none" stroke={s.color} strokeWidth={5} opacity={0.18} strokeLinecap="round" />
            <path d={s.d} fill="none" stroke={s.color} strokeWidth={2}
              className={s.dashed ? 'route-arc-dashed' : 'route-arc'}
              style={{ ['--dash-len' as string]: s.len }}
              strokeDasharray={s.dashed ? '5 4' : undefined} strokeLinecap="round" />
          </g>
        ))}
        {stations.map(s => (
          <g key={s.code}>
            <circle cx={s.x} cy={s.y} r={6.5} fill="var(--accent)" opacity={0.25} />
            <circle cx={s.x} cy={s.y} r={3.5} fill="#fff" stroke="var(--accent)" strokeWidth={2} />
            <text x={s.x + 8} y={s.y + 4} fontSize={10.5} fontWeight={700} fill="var(--ink)"
              stroke="var(--page)" strokeWidth={3.5} paintOrder="stroke">
              {s.code}
            </text>
          </g>
        ))}
      </svg>
    </div>
  )
}
