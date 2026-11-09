import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronDown, ChevronRight, Search } from 'lucide-react'
import { useSolutions } from '../context/SolutionsContext'
import { CodeBlock } from '../components/CodeViewer'
import data from '../data/techniques.json'
import type { DaySummary } from '../types'

interface Technique {
  id: string
  category: string
  name: string
  tags: string[]
  recognise: string[]
  example: { year: number; day: number }
}

// Snippets live next to the data as real .py files so they can be tested from Python.
const snippets = import.meta.glob('../data/snippets/*.py', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>

function snippetFor(id: string): string {
  return snippets[`../data/snippets/${id}.py`] ?? ''
}

function matches(technique: Technique, query: string): boolean {
  if (!query) return true
  const haystack = [technique.name, ...technique.tags, ...technique.recognise].join(' ').toLowerCase()
  return query
    .toLowerCase()
    .split(/\s+/)
    .every((word) => haystack.includes(word))
}

function TechniqueCard({ technique, days }: { technique: Technique; days: DaySummary[] }) {
  const [showSnippet, setShowSnippet] = useState(false)
  const example = days.find(
    (d) => d.year === technique.example.year && d.day === technique.example.day,
  )

  return (
    <article
      id={technique.id}
      className={`rounded-lg border border-aoc-border bg-aoc-surface p-5 space-y-4 ${showSnippet ? 'lg:col-span-2' : ''}`}
    >
      <div className="flex items-baseline justify-between gap-3">
        <h3 className="text-lg font-bold text-aoc-text">{technique.name}</h3>
        <span className="text-xs text-aoc-muted whitespace-nowrap">
          {days.length} {days.length === 1 ? 'solution' : 'solutions'}
        </span>
      </div>

      <ul className="space-y-1.5 text-sm leading-relaxed text-aoc-text">
        {technique.recognise.map((line) => (
          <li key={line} className="flex gap-2">
            <span className="text-aoc-gold select-none">›</span>
            <span>{line}</span>
          </li>
        ))}
      </ul>

      {example && (
        <p className="text-sm">
          <span className="text-aoc-muted">Best example to reread: </span>
          <Link
            to={`/${example.year}/${example.day}`}
            className="text-aoc-gold hover:text-white transition-colors"
          >
            {example.year} day {example.day}: {example.title}
          </Link>
        </p>
      )}

      <div className="flex flex-wrap gap-1.5">
        {days.map((d) => (
          <Link
            key={`${d.year}-${d.day}`}
            to={`/${d.year}/${d.day}`}
            title={d.title}
            className="text-[11px] px-1.5 py-0.5 rounded border border-aoc-border bg-aoc-bg text-aoc-muted hover:border-aoc-gold hover:text-aoc-gold transition-colors"
          >
            {d.year}/{d.day}
          </Link>
        ))}
      </div>

      <div>
        <button
          onClick={() => setShowSnippet((shown) => !shown)}
          aria-expanded={showSnippet}
          className="flex items-center gap-1 text-sm text-aoc-blue hover:text-white transition-colors"
        >
          {showSnippet ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          {showSnippet ? 'Hide snippet' : 'Show snippet'}
        </button>
        {showSnippet && (
          <div className="mt-3">
            <CodeBlock label={`${technique.id}.py`} code={snippetFor(technique.id).trimEnd()} />
          </div>
        )}
      </div>
    </article>
  )
}

export default function TechniquesPage() {
  const { manifest, loading, error } = useSolutions()
  const [query, setQuery] = useState('')

  // Every solved day per technique, newest first.
  const daysByTechnique = useMemo(() => {
    const allDays = Object.values(manifest.years)
      .flatMap((days) => Object.values(days))
      .sort((a, b) => b.year - a.year || b.day - a.day)
    const result = new Map<string, DaySummary[]>()
    for (const technique of data.techniques as Technique[]) {
      const tags = new Set(technique.tags)
      result.set(
        technique.id,
        allDays.filter((d) => d.tags?.some((tag) => tags.has(tag))),
      )
    }
    return result
  }, [manifest])

  if (loading) {
    return <div className="text-aoc-muted animate-pulse text-center py-20">Loading solutions…</div>
  }
  if (error) {
    return <div className="text-aoc-red text-center py-20">{error}</div>
  }

  const visible = (data.techniques as Technique[]).filter((t) => matches(t, query.trim()))

  return (
    <div className="space-y-10">
      <section className="space-y-4">
        <h1 className="text-3xl font-bold text-aoc-gold">Techniques</h1>
        <p className="text-aoc-muted max-w-2xl leading-relaxed">
          The algorithms that keep coming back, how to recognise them in a puzzle, the best past
          solution to reread, and a short Python snippet for each.
        </p>
        <label className="flex items-center gap-2 max-w-md rounded-lg border border-aoc-border bg-aoc-surface px-3 py-2 focus-within:border-aoc-gold">
          <Search size={16} className="text-aoc-muted" />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Filter: shortest path, cycle, intervals…"
            className="w-full bg-transparent text-sm text-aoc-text placeholder:text-aoc-muted outline-none"
          />
        </label>
        <nav className="flex flex-wrap gap-2">
          {data.categories.map((category) => (
            <button
              key={category.id}
              onClick={() =>
                document.getElementById(`category-${category.id}`)?.scrollIntoView({ behavior: 'smooth' })
              }
              className="text-xs px-2.5 py-1 rounded-full border border-aoc-border text-aoc-muted hover:border-aoc-gold hover:text-aoc-gold transition-colors"
            >
              {category.name}
            </button>
          ))}
        </nav>
      </section>

      {visible.length === 0 && (
        <p className="text-aoc-muted text-center py-10">No technique matches “{query}”.</p>
      )}

      {data.categories.map((category) => {
        const techniques = visible.filter((t) => t.category === category.id)
        if (techniques.length === 0) return null
        return (
          <section key={category.id} id={`category-${category.id}`} className="space-y-4 scroll-mt-20">
            <h2 className="text-xl font-bold text-aoc-text border-b border-aoc-border pb-2">
              {category.name}
            </h2>
            <div className="grid gap-4 lg:grid-cols-2 items-start">
              {techniques.map((technique) => (
                <TechniqueCard
                  key={technique.id}
                  technique={technique}
                  days={daysByTechnique.get(technique.id) ?? []}
                />
              ))}
            </div>
          </section>
        )
      })}
    </div>
  )
}
