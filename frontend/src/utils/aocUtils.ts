import type { FetchedSharedFile } from '../types'

// `import aoc_utils` or `from aoc_utils import ...` at the start of a line.
const IMPORTS_AOC_UTILS = /^\s*(import\s+aoc_utils\b|from\s+aoc_utils\s+import\b)/m

export const AOC_UTILS_PATH = 'solutions/aoc_utils.py'

export function importsAocUtils(code: string): boolean {
  return IMPORTS_AOC_UTILS.test(code)
}

export function aocUtilsFile(code: string): FetchedSharedFile {
  return { label: 'Shared helpers', filename: 'aoc_utils.py', code }
}
