/**
 * String normalization parser — intercepts raw preference values (arrays,
 * JSON-shaped objects, booleans, coded enums) before they reach the screen
 * and turns them into elegant, human-readable traveler tags.
 *
 * Backend contract (see backend/app/data/models.py Preference + profile/*):
 * a Preference.value can be a string, number, boolean, string[], or a small
 * plain object (currently only the `baggage` key: {carryon_only, checked_bags,
 * stroller}). This module knows the specific shapes WayFinder's fusion engine
 * produces — it is NOT a generic JSON formatter, it's a targeted translator.
 */

const AIRLINE_NAMES: Record<string, string> = {
  AA: 'American Airlines', AF: 'Air France', AI: 'Air India', BA: 'British Airways',
  CX: 'Cathay Pacific', DL: 'Delta', EK: 'Emirates', JL: 'Japan Airlines',
  KE: 'Korean Air', KL: 'KLM', LH: 'Lufthansa', NH: 'ANA', QF: 'Qantas',
  QR: 'Qatar Airways', SQ: 'Singapore Airlines', TG: 'Thai Airways',
  TK: 'Turkish Airlines', UA: 'United',
}

const MONTH_SEASON: Record<number, 'Winter' | 'Spring' | 'Summer' | 'Autumn'> = {
  12: 'Winter', 1: 'Winter', 2: 'Winter',
  3: 'Spring', 4: 'Spring', 5: 'Spring',
  6: 'Summer', 7: 'Summer', 8: 'Summer',
  9: 'Autumn', 10: 'Autumn', 11: 'Autumn',
}
const SEASON_ICON: Record<string, string> = { Winter: '❄️', Spring: '🌸', Summer: '☀️', Autumn: '🍂' }

function airlineNames(codes: string[]): string {
  return codes.map(c => AIRLINE_NAMES[c] ?? c).join(', ')
}

function seasonLabel(months: number[]): string {
  const seasons = Array.from(new Set(months.map(m => MONTH_SEASON[m]).filter(Boolean)))
  if (seasons.length === 0) return '📅 Seasonal Window Set'
  if (seasons.length >= 3) return '📅 Travels Nearly Year-Round'
  const icons = seasons.map(s => SEASON_ICON[s]).join('')
  return `${icons} ${seasons.join(' & ')} Travel Preferred`
}

function baggageLabel(v: { carryon_only?: boolean; checked_bags?: number; stroller?: boolean }): string {
  const parts: string[] = []
  if (v.carryon_only) parts.push('🎒 Carry-On Only Traveler')
  else if ((v.checked_bags ?? 0) > 0) parts.push(`🧳 ${v.checked_bags} Checked Bag${v.checked_bags === 1 ? '' : 's'} Required`)
  else parts.push('🧳 Checked Bags Required')
  if (v.stroller) parts.push('👶 Traveling with a Stroller')
  return parts.join(' · ')
}

/** Human phrasing for boolean flags, keyed by the backend preference key. */
const BOOLEAN_LABELS: Record<string, string> = {
  dates_very_flexible: '📅 Highly Flexible Travel Dates',
  dates_school_breaks_only: '🏫 Locked to School Holiday Windows',
  avoid_redeye: '🌙 Avoids Red-Eye Flights',
  redeye_ok_if_cheaper: '💤 Will Take a Red-Eye to Save Money',
  avoid_night_departure: '🌃 Avoids Night Departures',
  avoid_holiday_season: '🎉 Avoids Peak Holiday Travel',
  peak_season_ok: '🎊 Comfortable Flying Peak Season',
  carryon_only: '🎒 Carry-On Only Traveler',
  stroller: '👶 Traveling with a Stroller',
  layover_tolerance_high: '🔁 High Tolerance for Long Layovers',
}

/** Human phrasing for enum-style string values, keyed by "prefKey:value". */
const ENUM_LABELS: Record<string, string> = {
  'direct_preference:strong': '➡️ Direct Flights Only',
  'direct_preference:moderate': '➡️ Prefers Direct, Flexible if Needed',
  'direct_preference:none': '🔀 Connections Are Fine',
  'budget_priority:high': '💸 Budget-First Traveler',
  'budget_priority:none': '💎 Comfort Over Cost',
  'budget_priority:balanced': '⚖️ Balances Price & Comfort',
  'airline_loyalty:none': '🚫 No Airline Loyalty',
  'preferred_departure:morning': '🌅 Morning Departures Preferred',
  'preferred_departure:afternoon': '🌤️ Afternoon Departures Preferred',
  'preferred_departure:evening': '🌆 Evening Departures Preferred',
  'price_sensitivity:high': '💸 Highly Price-Sensitive',
  'price_sensitivity:none': '💎 Price Is No Object',
}

export interface HumanizedPref {
  icon: string
  text: string
}

/** Main entry point: given a preference key + its raw backend value, return
 * a clean display string (icon baked in). Falls back to a readable — never
 * raw-JSON — rendering for anything not explicitly mapped. */
export function humanizeValue(key: string, value: unknown): string {
  if (key === 'seasonal_months' && Array.isArray(value)) {
    return seasonLabel(value as number[])
  }
  if (key === 'baggage' && value && typeof value === 'object') {
    return baggageLabel(value as { carryon_only?: boolean; checked_bags?: number; stroller?: boolean })
  }
  if (key === 'preferred_airlines' && Array.isArray(value)) {
    const codes = value as string[]
    if (codes.length === 0) return ''
    return `✨ Loyalist: ${airlineNames(codes)}`
  }
  if (key === 'airline_liked' && typeof value === 'string') {
    return `✨ Loyalist: ${AIRLINE_NAMES[value] ?? value}`
  }
  if (key === 'checked_bags' && typeof value === 'number') {
    return value > 0 ? `🧳 ${value} Checked Bag${value === 1 ? '' : 's'} Required` : ''
  }
  if (typeof value === 'boolean') {
    if (BOOLEAN_LABELS[key]) return value ? BOOLEAN_LABELS[key] : ''
    return `${value ? '✅' : '—'} ${titleCase(key)}`
  }
  const enumKey = `${key}:${String(value)}`
  if (ENUM_LABELS[enumKey]) return ENUM_LABELS[enumKey]

  if (Array.isArray(value)) {
    if (value.length === 0) return `${titleCase(key)}: none`
    return `${titleCase(key)}: ${value.join(', ')}`
  }
  if (value && typeof value === 'object') {
    // last-resort object fallback — describe truthy fields in plain English,
    // never dump raw JSON to the screen
    const truthy = Object.entries(value as Record<string, unknown>)
      .filter(([, v]) => v && v !== 0)
      .map(([k]) => titleCase(k))
    return truthy.length ? `${titleCase(key)}: ${truthy.join(', ')}` : titleCase(key)
  }
  if (typeof value === 'number') {
    if (key.endsWith('_minutes')) return `${titleCase(key.replace('_minutes', ''))}: ${value} min`
    return `${titleCase(key)}: ${value}`
  }
  return `${titleCase(key)}: ${String(value)}`
}

function titleCase(s: string): string {
  return s.replaceAll('_', ' ').replace(/\b\w/g, c => c.toUpperCase())
}
