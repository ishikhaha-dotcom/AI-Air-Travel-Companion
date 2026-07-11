export interface Meta {
  sim_today: string; llm_mode: string; flights: number; users: number;
  routes: number; benchmarks: number; qa: string;
}

export interface UserSummary {
  user_id: string; age: number; home_airport: string; home_city: string;
  trip_purpose: string; price_sensitivity: string; direct_preference: string;
  preferred_cabin: string; summary: string;
}

export interface Preference {
  key: string; value: unknown; strength: string; source: string;
  evidence: string; confidence: number; note: string;
}

export interface UserProfile {
  user_id: string; home_city: string; home_airport: string; age: number;
  raw_history: string[]; party_size: number; contradictions: string[];
  preferences: Preference[]; highlights: Preference[];
}

export interface FlightJson {
  flight_id: string; airline: string; airline_name: string; numbers: string[];
  origin: string; destination: string; dep_utc: string; arr_utc: string;
  dep_local: string; arr_local: string; daypart: string; redeye: boolean;
  duration_minutes: number; stops: number; layover_airports: string[];
  layover_minutes: number; cabin: string; price: number; seats: number;
  otp: number; baggage_included: boolean; refundable: boolean;
  demand: string; season: string; holiday: boolean; aircraft: string;
}

export interface LegJson {
  origin: string; destination: string; origin_city: string; destination_city: string;
  flights: FlightJson[]; self_transfer: boolean; transfer_airport: string;
  transfer_minutes: number; price: number; duration_minutes: number;
  stops: number; layover_total: number; in_ticket_layover: number; seats_min: number;
}

export interface OptionJson {
  key: string; fit_score: number; breakdown: Record<string, number>;
  goodness: Record<string, number>; badges: string[];
  why: { reason: string; evidence: string; source: string }[];
  legs: LegJson[]; total_price_pp: number; total_price_party: number;
  total_duration_minutes: number; total_stops: number; seats_min: number;
  self_transfer: boolean; cities: string[]; summary: string; dep_date: string;
}

export interface TradeoffBrief {
  label: string; key: string; fit_score: number; price_pp: number;
  price_party: number; duration_minutes: number; duration: string; stops: number;
}

export interface RecommendResponse {
  user_id: string; query: string; sim_today: string;
  intent: {
    origin: string; destinations: string[]; trip_type: string;
    window_start: string; window_end: string; party_size: number;
    purpose: string; emphasis: string; region: string;
    fixed_pattern: Record<string, number>; trip_length_days: number; notes: string[];
  };
  profile_highlights: Preference[]; contradictions: string[];
  weights: Record<string, number>; weight_notes: string[];
  recommendations: OptionJson[];
  anchors: { cheapest: OptionJson | null; fastest: OptionJson | null };
  tradeoffs: { recommended?: TradeoffBrief; cheapest?: TradeoffBrief; fastest?: TradeoffBrief; statements?: string[] };
  insights: string[];
  price_by_date: { date: string; price: number; fit_score: number; stops: number }[];
  flex_insight: string | null;
  relaxations: { name: string; detail: string; count: number }[];
  route_facts: string[]; filtered_counts: Record<string, number>;
  narrative: string; elapsed_ms: number; total_candidates: number;
}

export interface Benchmark {
  prompt_id: string; user_id: string; request: string;
  expected_behavior: string[]; notes: string;
}

export interface BenchmarkRun {
  benchmark: Benchmark;
  checks: { behavior: string; passed: boolean; evidence: string }[];
  passed: number; total: number; response: RecommendResponse;
}
