// Static mirror of backend/app/data/airports.py (35 airports): [lon, lat], city
export const AIRPORTS: Record<string, { lon: number; lat: number; city: string }> = {
  AKL: { lon: 174.79, lat: -37.01, city: 'Auckland' },
  AMS: { lon: 4.76, lat: 52.31, city: 'Amsterdam' },
  BCN: { lon: 2.08, lat: 41.3, city: 'Barcelona' },
  BKK: { lon: 100.75, lat: 13.69, city: 'Bangkok' },
  BOM: { lon: 72.87, lat: 19.09, city: 'Mumbai' },
  CDG: { lon: 2.55, lat: 49.01, city: 'Paris' },
  CPT: { lon: 18.6, lat: -33.97, city: 'Cape Town' },
  DEL: { lon: 77.1, lat: 28.57, city: 'Delhi' },
  DOH: { lon: 51.61, lat: 25.27, city: 'Doha' },
  DPS: { lon: 115.17, lat: -8.75, city: 'Denpasar' },
  DXB: { lon: 55.36, lat: 25.25, city: 'Dubai' },
  FCO: { lon: 12.24, lat: 41.8, city: 'Rome' },
  FRA: { lon: 8.56, lat: 50.03, city: 'Frankfurt' },
  GIG: { lon: -43.25, lat: -22.81, city: 'Rio de Janeiro' },
  GRU: { lon: -46.47, lat: -23.43, city: 'Sao Paulo' },
  HKG: { lon: 113.91, lat: 22.31, city: 'Hong Kong' },
  ICN: { lon: 126.44, lat: 37.46, city: 'Seoul' },
  IST: { lon: 28.75, lat: 41.28, city: 'Istanbul' },
  JFK: { lon: -73.78, lat: 40.64, city: 'New York' },
  KUL: { lon: 101.71, lat: 2.75, city: 'Kuala Lumpur' },
  LAX: { lon: -118.41, lat: 33.94, city: 'Los Angeles' },
  LHR: { lon: -0.45, lat: 51.47, city: 'London' },
  LIS: { lon: -9.13, lat: 38.77, city: 'Lisbon' },
  MAA: { lon: 80.17, lat: 12.99, city: 'Chennai' },
  MEL: { lon: 144.84, lat: -37.67, city: 'Melbourne' },
  MEX: { lon: -99.07, lat: 19.44, city: 'Mexico City' },
  NRT: { lon: 140.39, lat: 35.77, city: 'Tokyo' },
  ORD: { lon: -87.91, lat: 41.97, city: 'Chicago' },
  PEK: { lon: 116.58, lat: 40.08, city: 'Beijing' },
  PVG: { lon: 121.81, lat: 31.14, city: 'Shanghai' },
  SFO: { lon: -122.38, lat: 37.62, city: 'San Francisco' },
  SIN: { lon: 103.99, lat: 1.36, city: 'Singapore' },
  SVO: { lon: 37.41, lat: 55.97, city: 'Moscow' },
  SYD: { lon: 151.18, lat: -33.95, city: 'Sydney' },
  YYZ: { lon: -79.61, lat: 43.68, city: 'Toronto' },
}

export function fmtDuration(minutes: number): string {
  const h = Math.floor(minutes / 60), m = Math.round(minutes % 60)
  return h ? `${h}h${String(m).padStart(2, '0')}m` : `${m}m`
}

export function fmtMoney(x: number): string {
  return '$' + x.toLocaleString('en-US', { maximumFractionDigits: 0 })
}
