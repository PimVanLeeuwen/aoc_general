import { useState, useEffect } from 'react'
import { Play, Loader, AlertCircle, CheckCircle } from 'lucide-react'
import { usePyodide } from '../context/PyodideContext'
import { runSolution, runVisualization } from '../utils/pyodide-runner'
import Visualizer from './Visualizer'
import type { RunResult, VisFrame } from '../types'

export default function RunnerPanel({
  code,
  hasVisualization,
}: {
  code: string
  hasVisualization: boolean
}) {
  const { isReady, isLoading: pyLoading, load } = usePyodide()
  const [input, setInput] = useState('')
  const [running, setRunning] = useState(false)
  const [result, setResult] = useState<RunResult | null>(null)
  const [frames, setFrames] = useState<VisFrame[] | null>(null)
  const [runError, setRunError] = useState<string | null>(null)

  // Clear state when switching between solutions
  useEffect(() => {
    setResult(null)
    setFrames(null)
    setRunError(null)
  }, [code])

  const handleRun = async () => {
    if (!isReady) {
      await load()
      // load() sets isReady async — re-trigger on next click if needed
      return
    }
    setRunning(true)
    setResult(null)
    setFrames(null)
    setRunError(null)
    try {
      const res = await runSolution(code, input)
      setResult(res)
      if (hasVisualization && !res.error) {
        const vizFrames = await runVisualization(code, input)
        if (vizFrames.length > 0) setFrames(vizFrames)
      }
    } catch (e) {
      setRunError(String(e))
    } finally {
      setRunning(false)
    }
  }

  const busy = running || pyLoading
  const buttonLabel = pyLoading
    ? 'Loading Python (~10 MB)…'
    : running
      ? 'Running…'
      : isReady
        ? 'Run'
        : 'Load Python & Run'

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Input */}
        <div className="space-y-2">
          <label className="text-sm text-aoc-muted">Puzzle Input</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste your puzzle input here…"
            className="w-full h-48 bg-aoc-surface border border-aoc-border rounded-lg p-3 text-sm text-aoc-text font-mono resize-y focus:outline-none focus:border-aoc-gold placeholder:text-aoc-border"
            spellCheck={false}
          />
          <button
            onClick={handleRun}
            disabled={busy}
            className="w-full py-2.5 px-4 rounded-lg font-medium text-sm transition-colors flex items-center justify-center gap-2 bg-aoc-gold text-aoc-bg hover:brightness-110 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {busy ? (
              <Loader size={15} className="animate-spin" />
            ) : (
              <Play size={15} fill="currentColor" />
            )}
            {buttonLabel}
          </button>
        </div>

        {/* Output */}
        <div className="space-y-2">
          <label className="text-sm text-aoc-muted">Output</label>
          <div className="h-48 bg-aoc-surface border border-aoc-border rounded-lg p-3 overflow-y-auto text-sm font-mono">
            {(runError || result?.error) && (
              <div className="text-aoc-red flex items-start gap-2">
                <AlertCircle size={14} className="mt-0.5 flex-shrink-0" />
                <pre className="whitespace-pre-wrap text-xs">
                  {runError ?? result?.error}
                </pre>
              </div>
            )}
            {result && !result.error && (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <CheckCircle size={14} className="text-aoc-green" />
                  <span className="text-aoc-muted text-xs">{result.timeMs} ms</span>
                </div>
                {result.part1 && (
                  <div>
                    <span className="text-aoc-muted">Part 1: </span>
                    <span className="text-aoc-gold font-bold">{result.part1}</span>
                  </div>
                )}
                {result.part2 && (
                  <div>
                    <span className="text-aoc-muted">Part 2: </span>
                    <span className="text-aoc-gold font-bold">{result.part2}</span>
                  </div>
                )}
                {result.stdout && (
                  <div className="mt-2 pt-2 border-t border-aoc-border">
                    <div className="text-aoc-muted text-xs mb-1">stdout</div>
                    <pre className="text-aoc-text whitespace-pre-wrap text-xs">{result.stdout}</pre>
                  </div>
                )}
              </div>
            )}
            {!result && !runError && (
              <div className="h-full flex items-center justify-center text-aoc-border">
                Results will appear here
              </div>
            )}
          </div>
        </div>
      </div>

      {frames && frames.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm text-aoc-muted">
            Visualization &mdash; {frames.length} frame{frames.length !== 1 ? 's' : ''}
          </p>
          <Visualizer frames={frames} />
        </div>
      )}
    </div>
  )
}
