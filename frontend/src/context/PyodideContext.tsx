import React, { createContext, useContext, useState, useCallback } from 'react'

interface PyodideContextValue {
  isLoading: boolean
  isReady: boolean
  error: string | null
  load: () => Promise<void>
}

const PyodideContext = createContext<PyodideContextValue | null>(null)

// Singleton state — survives React re-renders
let _pyodide: unknown = null
let _loadPromise: Promise<void> | null = null

/** Access the raw Pyodide instance from outside React (e.g. in pyodide-runner.ts). */
export function getPyodide(): unknown {
  return _pyodide
}

export function PyodideProvider({ children }: { children: React.ReactNode }) {
  const [isLoading, setIsLoading] = useState(false)
  const [isReady, setIsReady] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    if (_pyodide) return
    if (_loadPromise) {
      await _loadPromise
      setIsReady(true)
      return
    }

    setIsLoading(true)
    _loadPromise = (async () => {
      if (!(window as { loadPyodide?: unknown }).loadPyodide) {
        await new Promise<void>((resolve, reject) => {
          const s = document.createElement('script')
          s.src = 'https://cdn.jsdelivr.net/pyodide/v0.27.3/full/pyodide.js'
          s.onload = () => resolve()
          s.onerror = () => reject(new Error('Failed to load Pyodide script'))
          document.head.appendChild(s)
        })
      }
      _pyodide = await (window as { loadPyodide: (opts: object) => Promise<unknown> }).loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.3/full/',
      })
    })()

    try {
      await _loadPromise
      setIsReady(true)
    } catch (e) {
      _loadPromise = null
      setError(String(e))
    } finally {
      setIsLoading(false)
    }
  }, [])

  return (
    <PyodideContext.Provider value={{ isLoading, isReady, error, load }}>
      {children}
    </PyodideContext.Provider>
  )
}

export function usePyodide() {
  const ctx = useContext(PyodideContext)
  if (!ctx) throw new Error('usePyodide must be used within PyodideProvider')
  return ctx
}
