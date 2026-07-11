// Display names for backend scoring keys — never leak raw keys into the UI.
export const FEATURE_LABELS: Record<string, string> = {
  price: 'Price',
  time: 'Time',
  convenience: 'Convenience',
  reliability: 'Reliability',
  preffit: 'Preference fit',
}

export const FEATURE_COLORS: Record<string, string> = {
  price: 'var(--series-1)',
  time: 'var(--series-2)',
  convenience: 'var(--series-3)',
  reliability: 'var(--series-4)',
  preffit: 'var(--series-5)',
}

export const featureLabel = (key: string) =>
  FEATURE_LABELS[key] ?? key.replaceAll('_', ' ')
