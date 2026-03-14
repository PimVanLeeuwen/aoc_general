import { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Copy, Check } from 'lucide-react'

// Strip the optional visualizer section — it's not part of the solve logic
function stripVisualizer(code: string): string {
  const sepIdx = code.indexOf('\n# ── Optional visualizer')
  const fnIdx = code.indexOf('\ndef visualize(')
  const cutAt = [sepIdx, fnIdx].filter((i) => i !== -1)
  if (cutAt.length === 0) return code
  return code.slice(0, Math.min(...cutAt)).trimEnd()
}

export default function CodeViewer({ code }: { code: string }) {
  const [copied, setCopied] = useState(false)
  const displayCode = stripVisualizer(code)

  const copy = () => {
    navigator.clipboard.writeText(displayCode)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const BG = '#1a1a2e'

  return (
    <div className="rounded-lg overflow-hidden border border-aoc-border">
      <div className="flex items-center justify-between px-4 py-2 bg-aoc-elevated border-b border-aoc-border">
        <span className="text-xs text-aoc-muted">solution.py</span>
        <button
          onClick={copy}
          className="flex items-center gap-1.5 text-xs text-aoc-muted hover:text-aoc-text transition-colors"
        >
          {copied ? (
            <Check size={13} className="text-aoc-green" />
          ) : (
            <Copy size={13} />
          )}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>
      <SyntaxHighlighter
        language="python"
        style={oneDark}
        customStyle={{
          margin: 0,
          borderRadius: 0,
          background: BG,
          fontSize: '0.875rem',
          lineHeight: '1.6',
        }}
        codeTagProps={{ style: { background: BG } }}
        showLineNumbers
        lineNumberStyle={{ color: '#555577', minWidth: '2.5em', background: BG }}
      >
        {displayCode}
      </SyntaxHighlighter>
    </div>
  )
}
