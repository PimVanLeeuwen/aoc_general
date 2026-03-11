import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Star, ChevronLeft } from 'lucide-react'
import { useSolutions } from '../context/SolutionsContext'
import CodeViewer from '../components/CodeViewer'
import WriteupView from '../components/WriteupView'
import RunnerPanel from '../components/RunnerPanel'
import { assetUrl } from '../utils/assetUrl'
import type { SolutionDetail } from '../types'

type Tab = 'writeup' | 'code' | 'run'

export default function SolutionPage() {
  const { year, day } = useParams<{ year: string; day: string }>()
  const { manifest } = useSolutions()
  const [tab, setTab] = useState<Tab>('writeup')
  const [solution, setSolution] = useState<SolutionDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Grab summary from manifest (instantly available)
  const daySummary = manifest.years[year!]?.[day!]

  useEffect(() => {
    if (!year || !day) return
    setLoading(true)
    setError(null)
    setSolution(null)

    const pad = day.padStart(2, '0')
    Promise.all([
      fetch(assetUrl(`solutions/${year}/day${pad}/solution.py`)).then((r) =>
        r.ok ? r.text() : '',
      ),
      fetch(assetUrl(`solutions/${year}/day${pad}/meta.json`)).then((r) =>
        r.ok ? r.json() : {},
      ),
    ])
      .then(([code, meta]) => {
        setSolution({
          ...meta,
          code,
          year: parseInt(year),
          day: parseInt(day),
          hasSolution: code.length > 0,
          hasVisualization: code.includes('def visualize('),
        } as SolutionDetail)
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false))
  }, [year, day])

  const stars = (solution?.stars ?? daySummary?.stars) ?? 0
  const title = solution?.title ?? daySummary?.title ?? `Day ${day}`

  const tabs: { id: Tab; label: string }[] = [
    { id: 'writeup', label: 'Write-up' },
    { id: 'code', label: 'Code' },
    { id: 'run', label: 'Run & Visualize' },
  ]

  return (
    <div className="space-y-6">
      <Link
        to="/"
        className="inline-flex items-center gap-1 text-sm text-aoc-muted hover:text-aoc-text transition-colors"
      >
        <ChevronLeft size={15} />
        All solutions
      </Link>

      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="text-aoc-muted text-sm mb-1">
            {year} &mdash; Day {day}
          </div>
          <h1 className="text-3xl font-bold text-aoc-text">{title}</h1>
          {solution?.description && (
            <p className="text-aoc-muted mt-2 max-w-xl leading-relaxed">{solution.description}</p>
          )}
        </div>
        <div className="flex gap-1 mt-1 flex-shrink-0">
          {[0, 1].map((i) => (
            <Star
              key={i}
              size={20}
              className={i < stars ? 'text-aoc-gold' : 'text-aoc-border'}
              fill={i < stars ? 'currentColor' : 'none'}
            />
          ))}
        </div>
      </div>

      {/* Tags */}
      {solution?.tags && solution.tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {solution.tags.map((tag) => (
            <span
              key={tag}
              className="px-2 py-0.5 text-xs rounded bg-aoc-elevated text-aoc-muted border border-aoc-border"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-aoc-border">
        <div className="flex">
          {tabs.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={[
                'px-5 py-3 text-sm font-medium transition-colors relative',
                tab === t.id
                  ? 'text-aoc-gold after:absolute after:bottom-[-1px] after:left-0 after:right-0 after:h-0.5 after:bg-aoc-gold'
                  : 'text-aoc-muted hover:text-aoc-text',
              ].join(' ')}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      {loading && (
        <div className="text-aoc-muted animate-pulse py-8 text-center">Loading…</div>
      )}
      {error && <div className="text-aoc-red py-4">{error}</div>}
      {!loading && solution && (
        <>
          {tab === 'writeup' && <WriteupView content={solution.writeup ?? ''} />}
          {tab === 'code' && <CodeViewer code={solution.code} />}
          {tab === 'run' && (
            <RunnerPanel code={solution.code} hasVisualization={solution.hasVisualization} />
          )}
        </>
      )}
    </div>
  )
}
