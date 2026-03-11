import { useNavigate } from 'react-router-dom'
import { Star } from 'lucide-react'
import { useSolutions } from '../context/SolutionsContext'
import type { DaySummary } from '../types'

export default function HomePage() {
  const { manifest, loading, error } = useSolutions()
  const navigate = useNavigate()

  if (loading) {
    return (
      <div className="text-aoc-muted animate-pulse text-center py-20">
        Loading solutions…
      </div>
    )
  }
  if (error) {
    return <div className="text-aoc-red text-center py-20">{error}</div>
  }

  const years = Object.keys(manifest.years).sort((a, b) => parseInt(b) - parseInt(a))

  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="text-center py-10">
        <h1 className="text-4xl font-bold text-aoc-gold mb-3">Advent of Code Portfolio</h1>
        <p className="text-aoc-muted max-w-lg mx-auto leading-relaxed">
          Solutions with write-ups, code, and step-by-step visualizations. Paste your own
          puzzle input to run them directly in the browser — no server required.
        </p>
      </section>

      {years.length === 0 ? (
        <div className="text-center text-aoc-muted border border-dashed border-aoc-border rounded-xl p-16">
          <p className="text-lg mb-2">No solutions yet.</p>
          <p className="text-sm">
            Add one to{' '}
            <code className="text-aoc-gold bg-aoc-elevated px-1.5 py-0.5 rounded">
              solutions/YEAR/dayDD/
            </code>
          </p>
        </div>
      ) : (
        years.map((year) => {
          const days = manifest.years[year]
          const solved = Object.values(days).filter((d) => (d as DaySummary).stars ?? 0 > 0)
            .length

          return (
            <section key={year}>
              <div className="flex items-baseline gap-3 mb-5">
                <h2 className="text-2xl font-bold text-aoc-gold">{year}</h2>
                <span className="text-sm text-aoc-muted">
                  {solved} / {Object.keys(days).length} solved
                </span>
              </div>

              <div className="grid grid-cols-5 sm:grid-cols-7 md:grid-cols-5 lg:grid-cols-7 xl:grid-cols-5 gap-2.5">
                {Array.from({ length: 25 }, (_, i) => i + 1).map((day) => {
                  const meta = days[String(day)] as DaySummary | undefined
                  const stars = meta?.stars ?? 0

                  return (
                    <button
                      key={day}
                      onClick={() => meta && navigate(`/${year}/${day}`)}
                      disabled={!meta}
                      className={[
                        'relative p-3 rounded-lg border text-left transition-all duration-150',
                        meta
                          ? 'border-aoc-border bg-aoc-surface hover:border-aoc-gold hover:bg-aoc-elevated cursor-pointer group'
                          : 'border-aoc-border/20 bg-aoc-bg/50 cursor-not-allowed opacity-30',
                      ].join(' ')}
                    >
                      <div className="text-[10px] text-aoc-muted leading-none mb-1">Day</div>
                      <div className="text-xl font-bold text-aoc-text group-hover:text-white transition-colors">
                        {day}
                      </div>
                      {meta && (
                        <>
                          {meta.title && (
                            <div className="text-[10px] text-aoc-muted mt-1 truncate leading-tight">
                              {meta.title}
                            </div>
                          )}
                          {stars > 0 && (
                            <div className="absolute top-2 right-2 flex gap-0.5">
                              {Array.from({ length: stars }).map((_, i) => (
                                <Star key={i} size={9} className="text-aoc-gold" fill="currentColor" />
                              ))}
                            </div>
                          )}
                        </>
                      )}
                    </button>
                  )
                })}
              </div>
            </section>
          )
        })
      )}
    </div>
  )
}
