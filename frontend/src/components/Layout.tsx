import { Link } from 'react-router-dom'
import { Star } from 'lucide-react'

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-aoc-bg text-aoc-text">
      <header className="sticky top-0 z-50 border-b border-aoc-border bg-aoc-bg/95 backdrop-blur">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
          <Link
            to="/"
            className="flex items-center gap-2 text-aoc-gold hover:text-white transition-colors font-bold text-lg"
          >
            <Star size={18} fill="currentColor" />
            AoC Portfolio
          </Link>
          <span className="text-xs text-aoc-muted hidden sm:block">
            Runs entirely in your browser · no server
          </span>
        </div>
      </header>
      <main className="max-w-5xl mx-auto px-4 py-8">{children}</main>
    </div>
  )
}
