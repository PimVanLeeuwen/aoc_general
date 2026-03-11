export interface DaySummary {
  year: number
  day: number
  title?: string
  description?: string
  /** 0 = not started, 1 = part 1, 2 = both */
  stars?: 0 | 1 | 2
  tags?: string[]
  hasSolution: boolean
  hasVisualization: boolean
}

export interface SolutionDetail extends DaySummary {
  code: string
  writeup?: string
}

export interface SolutionsManifest {
  years: {
    /** year string e.g. "2024" */
    [year: string]: {
      /** day number as string e.g. "1" */
      [day: string]: DaySummary
    }
  }
}

export interface RunResult {
  part1: string
  part2: string
  stdout: string
  error: string | null
  timeMs: number
}

export type VisFrame =
  | { type: 'grid'; cells: string[][]; colors?: Record<string, string>; delay?: number }
  | { type: 'text'; lines: string[]; delay?: number }
