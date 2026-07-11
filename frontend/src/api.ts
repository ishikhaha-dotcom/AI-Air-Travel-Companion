import type { Benchmark, BenchmarkRun, Meta, RecommendResponse, UserProfile, UserSummary } from './types'

async function get<T>(url: string): Promise<T> {
  const r = await fetch(url)
  if (!r.ok) throw new Error(`${url}: ${r.status}`)
  return r.json()
}

export const fetchMeta = () => get<Meta>('/api/meta')
export const fetchUsers = () => get<UserSummary[]>('/api/users')
export const fetchProfile = (id: string) => get<UserProfile>(`/api/users/${id}/profile`)
export const fetchBenchmarks = () => get<Benchmark[]>('/api/benchmarks')

export async function postRecommend(user_id: string, query: string): Promise<RecommendResponse> {
  const r = await fetch('/api/recommend', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id, query }),
  })
  if (!r.ok) throw new Error(`recommend: ${r.status}`)
  return r.json()
}

export async function postRefine(user_id: string, query: string, followup: string): Promise<RecommendResponse> {
  const r = await fetch('/api/refine', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id, query, followup }),
  })
  if (!r.ok) throw new Error(`refine: ${r.status}`)
  return r.json()
}

export async function runBenchmark(id: string): Promise<BenchmarkRun> {
  const r = await fetch(`/api/benchmarks/${id}/run`, { method: 'POST' })
  if (!r.ok) throw new Error(`benchmark ${id}: ${r.status}`)
  return r.json()
}
