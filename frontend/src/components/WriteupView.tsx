import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

export default function WriteupView({ content }: { content: string }) {
  if (!content) {
    return (
      <div className="border border-dashed border-aoc-border rounded-lg p-12 text-center text-aoc-muted">
        No write-up yet. Add a{' '}
        <code className="text-aoc-gold bg-aoc-elevated px-1 rounded">writeup</code> field to{' '}
        <code className="text-aoc-gold bg-aoc-elevated px-1 rounded">meta.json</code>.
      </div>
    )
  }

  return (
    <div className="max-w-3xl space-y-1">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h1 className="text-2xl font-bold text-aoc-gold mt-8 mb-4 first:mt-0">{children}</h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-xl font-bold text-aoc-text mt-8 mb-3 border-b border-aoc-border pb-2">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-base font-bold text-aoc-text mt-6 mb-2">{children}</h3>
          ),
          p: ({ children }) => (
            <p className="text-aoc-text mb-4 leading-relaxed">{children}</p>
          ),
          ul: ({ children }) => (
            <ul className="list-disc list-inside mb-4 space-y-1 text-aoc-text">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside mb-4 space-y-1 text-aoc-text">{children}</ol>
          ),
          li: ({ children }) => <li className="text-aoc-text">{children}</li>,
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-aoc-gold pl-4 my-4 text-aoc-muted italic">
              {children}
            </blockquote>
          ),
          a: ({ href, children }) => (
            <a
              href={href}
              className="text-aoc-blue hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              {children}
            </a>
          ),
          strong: ({ children }) => (
            <strong className="text-white font-bold">{children}</strong>
          ),
          pre: ({ children }) => (
            <pre className="my-4 rounded-lg overflow-hidden">{children}</pre>
          ),
          code: ({ className, children }) => {
            const match = /language-(\w+)/.exec(className || '')
            if (match) {
              return (
                <SyntaxHighlighter
                  language={match[1]}
                  style={oneDark}
                  customStyle={{ borderRadius: '0.375rem', fontSize: '0.875rem', margin: 0 }}
                >
                  {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
              )
            }
            return (
              <code className="bg-aoc-elevated px-1.5 py-0.5 rounded text-sm text-aoc-gold font-mono">
                {children}
              </code>
            )
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}
