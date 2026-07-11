import { useMemo } from 'react'
import { geoNaturalEarth1, geoPath } from 'd3-geo'
import { feature } from 'topojson-client'
import type { Topology, GeometryCollection } from 'topojson-specification'
import landTopo from 'world-atlas/land-110m.json'
import { AIRPORTS } from '../airports'
import type { OptionJson } from '../types'

const LEG_COLORS = ['var(--series-1)', 'var(--series-2)', 'var(--series-3)',
                    'var(--series-5)', 'var(--series-4)']

/** Offline SVG route map: bundled world-atlas coastlines (no tile servers),
 *  great-circle arcs per leg — always works in a demo, even with no internet. */
export default function RouteMap({ option }: { option: OptionJson }) {
  const W = 460, H = 260

  const { landPath, projection } = useMemo(() => {
    const topo = landTopo as unknown as Topology<{ land: GeometryCollection }>
    const land = feature(topo, topo.objects.land)
    const proj = geoNaturalEarth1().fitExtent([[6, 6], [W - 6, H - 6]], { type: 'Sphere' })
    return { landPath: geoPath(proj)(land) ?? '', projection: proj }
  }, [])

  const path = geoPath(projection)
  const stations: { code: string; x: number; y: number }[] = []
  const seen = new Set<string>()
  const segs: { d: string; color: string; dashed: boolean }[] = []

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
      if (d) segs.push({ d, color, dashed: leg.self_transfer })
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
    <div className="card p-3">
      <div className="text-xs muted mb-1">
        Recommended routing — {option.cities.join(' → ')}
        {option.self_transfer && <span style={{ color: 'var(--status-warn)' }}> (dashed = self-transfer)</span>}
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Route map">
        <path d={landPath} fill="var(--surface-2)" stroke="var(--grid)" strokeWidth={0.5} />
        {segs.map((s, i) => (
          <path key={i} d={s.d} fill="none" stroke={s.color} strokeWidth={2}
            strokeDasharray={s.dashed ? '5 4' : undefined} strokeLinecap="round" opacity={0.9} />
        ))}
        {stations.map(s => (
          <g key={s.code}>
            <circle cx={s.x} cy={s.y} r={4.5} fill="var(--ink)" stroke="var(--surface)" strokeWidth={2} />
            <text x={s.x + 7} y={s.y + 4} fontSize={10} fontWeight={600} fill="var(--ink)"
              stroke="var(--surface)" strokeWidth={3} paintOrder="stroke">
              {s.code}
            </text>
          </g>
        ))}
      </svg>
    </div>
  )
}
