import React, { createContext, useContext, useState, useEffect } from 'react'
import type { SolutionsManifest } from '../types'
import { assetUrl } from '../lib/assetUrl'

interface SolutionsContextValue {
  manifest: SolutionsManifest
  loading: boolean
  error: string | null
}

const SolutionsContext = createContext<SolutionsContextValue | null>(null)

const emptyManifest: SolutionsManifest = { years: {} }

export function SolutionsProvider({ children }: { children: React.ReactNode }) {
  const [manifest, setManifest] = useState<SolutionsManifest>(emptyManifest)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch(assetUrl('solutions-manifest.json'))
      .then((r) => r.json())
      .then(setManifest)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false))
  }, [])

  return (
    <SolutionsContext.Provider value={{ manifest, loading, error }}>
      {children}
    </SolutionsContext.Provider>
  )
}

export function useSolutions() {
  const ctx = useContext(SolutionsContext)
  if (!ctx) throw new Error('useSolutions must be used within SolutionsProvider')
  return ctx
}
