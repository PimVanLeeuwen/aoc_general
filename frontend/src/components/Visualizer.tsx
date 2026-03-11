import { useState, useEffect, useRef, useCallback } from 'react'
import { Play, Pause, SkipBack, SkipForward, ChevronsLeft, ChevronsRight } from 'lucide-react'
import type { VisFrame } from '../types'

const DEFAULT_COLORS: Record<string, string> = {
  '#': '#00ff41',
  '.': '#0f0f23',
  O: '#ffff66',
  '@': '#00aaff',
  ' ': '#0a0a1a',
  '*': '#ff5555',
  '+': '#00cc44',
  '-': '#1a1a2e',
  '|': '#1a1a2e',
}

function GridFrame({ frame }: { frame: Extract<VisFrame, { type: 'grid' }> }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const cells = frame.cells
    const rows = cells.length
    const cols = Math.max(...cells.map((r) => r.length), 1)
    if (!rows) return

    const size = Math.max(2, Math.min(Math.floor(640 / cols), Math.floor(400 / rows), 20))
    canvas.width = cols * size
    canvas.height = rows * size

    const colors = frame.colors ?? {}
    cells.forEach((row, y) => {
      row.forEach((cell, x) => {
        ctx.fillStyle = colors[cell] ?? DEFAULT_COLORS[cell] ?? '#444466'
        ctx.fillRect(x * size, y * size, size, size)
      })
    })
  }, [frame])

  return (
    <canvas
      ref={canvasRef}
      className="max-w-full max-h-96"
      style={{ imageRendering: 'pixelated' }}
    />
  )
}

export default function Visualizer({ frames }: { frames: VisFrame[] }) {
  const [current, setCurrent] = useState(0)
  const [playing, setPlaying] = useState(false)
  const timerRef = useRef<number | null>(null)

  const frame = frames[current]

  // Cleanup timer helper
  const clearTimer = useCallback(() => {
    if (timerRef.current !== null) {
      clearTimeout(timerRef.current)
      timerRef.current = null
    }
  }, [])

  const next = useCallback(() => {
    setCurrent((c) => {
      if (c < frames.length - 1) return c + 1
      setPlaying(false)
      return c
    })
  }, [frames.length])

  const prev = () => setCurrent((c) => Math.max(c - 1, 0))

  useEffect(() => {
    if (!playing) {
      clearTimer()
      return
    }
    const delay = (frame as { delay?: number })?.delay ?? 150
    timerRef.current = window.setTimeout(next, delay)
    return clearTimer
  }, [playing, current, frame, next, clearTimer])

  // Reset when frames change
  useEffect(() => {
    clearTimer()
    setCurrent(0)
    setPlaying(false)
  }, [frames, clearTimer])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      clearTimer()
    }
  }, [clearTimer])

  if (!frame) return null

  return (
    <div className="bg-aoc-surface border border-aoc-border rounded-lg overflow-hidden">
      {/* Frame display */}
      <div className="flex items-center justify-center min-h-[160px] bg-aoc-bg p-4 overflow-auto">
        {frame.type === 'grid' ? (
          <GridFrame frame={frame} />
        ) : frame.type === 'text' ? (
          <pre className="text-aoc-green text-sm font-mono whitespace-pre-wrap leading-relaxed">
            {(frame.lines as string[]).join('\n')}
          </pre>
        ) : null}
      </div>

      {/* Controls */}
      <div className="flex items-center justify-between px-4 py-3 border-t border-aoc-border">
        <div className="flex items-center gap-1">
          <button
            onClick={() => setCurrent(0)}
            disabled={current === 0}
            className="p-1.5 rounded text-aoc-muted hover:text-aoc-text disabled:opacity-30 transition-colors"
          >
            <ChevronsLeft size={15} />
          </button>
          <button
            onClick={prev}
            disabled={current === 0}
            className="p-1.5 rounded text-aoc-muted hover:text-aoc-text disabled:opacity-30 transition-colors"
          >
            <SkipBack size={15} />
          </button>
          <button
            onClick={() => setPlaying((p) => !p)}
            className="p-2 mx-1 rounded bg-aoc-elevated text-aoc-gold hover:bg-aoc-border transition-colors"
          >
            {playing ? (
              <Pause size={15} fill="currentColor" />
            ) : (
              <Play size={15} fill="currentColor" />
            )}
          </button>
          <button
            onClick={next}
            disabled={current === frames.length - 1}
            className="p-1.5 rounded text-aoc-muted hover:text-aoc-text disabled:opacity-30 transition-colors"
          >
            <SkipForward size={15} />
          </button>
          <button
            onClick={() => setCurrent(frames.length - 1)}
            disabled={current === frames.length - 1}
            className="p-1.5 rounded text-aoc-muted hover:text-aoc-text disabled:opacity-30 transition-colors"
          >
            <ChevronsRight size={15} />
          </button>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs text-aoc-muted">
            {current + 1} / {frames.length}
          </span>
          <input
            type="range"
            min={0}
            max={frames.length - 1}
            value={current}
            onChange={(e) => {
              setCurrent(parseInt(e.target.value))
              setPlaying(false)
            }}
            className="w-28 accent-aoc-gold"
          />
        </div>
      </div>
    </div>
  )
}
