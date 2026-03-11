import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import { readdirSync, readFileSync, existsSync, statSync, cpSync } from 'node:fs'
import { resolve, join } from 'node:path'
import type { IncomingMessage, ServerResponse } from 'node:http'

const SOLUTIONS_ROOT = resolve(__dirname, '../solutions')

function buildManifest() {
  const years: Record<string, Record<string, object>> = {}
  if (!existsSync(SOLUTIONS_ROOT)) return { years }

  for (const year of readdirSync(SOLUTIONS_ROOT).sort()) {
    const yearPath = join(SOLUTIONS_ROOT, year)
    if (!statSync(yearPath).isDirectory() || !/^\d{4}$/.test(year)) continue
    years[year] = {}

    for (const dayDir of readdirSync(yearPath).sort()) {
      const dayPath = join(yearPath, dayDir)
      if (!statSync(dayPath).isDirectory() || !/^day\d{2}$/.test(dayDir)) continue

      const metaPath = join(dayPath, 'meta.json')
      const solPath = join(dayPath, 'solution.py')
      const dayNum = parseInt(dayDir.replace('day', ''), 10)
      const meta = existsSync(metaPath) ? JSON.parse(readFileSync(metaPath, 'utf-8')) : {}

      years[year][dayNum] = {
        ...meta,
        year: parseInt(year),
        day: dayNum,
        hasSolution: existsSync(solPath),
        hasVisualization:
          existsSync(solPath) && readFileSync(solPath, 'utf-8').includes('def visualize('),
      }
    }
  }
  return { years }
}

function solutionsPlugin(): Plugin {
  let outDir = 'dist'
  return {
    name: 'solutions',
    configResolved(config) {
      outDir = resolve(config.root, config.build.outDir)
    },
    configureServer(server) {
      // Serve manifest in dev
      server.middlewares.use(
        '/solutions-manifest.json',
        (_req: IncomingMessage, res: ServerResponse) => {
          res.setHeader('Content-Type', 'application/json; charset=utf-8')
          res.end(JSON.stringify(buildManifest()))
        },
      )
      // Serve solution files in dev
      server.middlewares.use(
        '/solutions',
        (req: IncomingMessage, res: ServerResponse, next: () => void) => {
          const url = decodeURIComponent((req.url ?? '').split('?')[0])
          const filePath = join(SOLUTIONS_ROOT, url)
          try {
            if (existsSync(filePath) && statSync(filePath).isFile()) {
              const ext = filePath.split('.').pop() ?? ''
              const ctypes: Record<string, string> = {
                py: 'text/plain',
                json: 'application/json',
                md: 'text/markdown',
              }
              res.setHeader('Content-Type', `${ctypes[ext] ?? 'text/plain'}; charset=utf-8`)
              res.end(readFileSync(filePath))
              return
            }
          } catch {
            /* fall through */
          }
          next()
        },
      )
    },
    generateBundle() {
      // Emit manifest into build output
      this.emitFile({
        type: 'asset',
        fileName: 'solutions-manifest.json',
        source: JSON.stringify(buildManifest()),
      })
    },
    closeBundle() {
      // Copy solutions directory into dist
      if (existsSync(SOLUTIONS_ROOT)) {
        cpSync(SOLUTIONS_ROOT, join(outDir, 'solutions'), { recursive: true })
      }
    },
  }
}

export default defineConfig({
  base: process.env.VITE_BASE_URL ?? '/',
  plugins: [react(), solutionsPlugin()],
})
