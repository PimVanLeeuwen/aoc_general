/** Resolved at build time by Vite — '/' in dev, '/repo-name/' on GitHub Pages */
const BASE = import.meta.env.BASE_URL

/** Resolve a path relative to the site root, respecting the Vite base URL. */
export function assetUrl(path: string): string {
  return `${BASE}${path.replace(/^\//, '')}`
}
