import { getPyodide } from '../context/PyodideContext'
import type { RunResult, VisFrame, FetchedSharedFile } from '../types'

/**
 * Python wrapper that executes the solution in a fresh namespace,
 * captures stdout, and returns a JSON-encoded result dict.
 * _solution_code and _puzzle_input must be set on pyodide.globals before calling.
 */
const RUNNER_CODE = `
import sys, io, json, traceback as _tb

_capture = io.StringIO()
_orig_out, _orig_err = sys.stdout, sys.stderr
sys.stdout = sys.stderr = _capture

_part1, _part2, _error = '', '', None
try:
    _ns = {'__builtins__': __builtins__}
    exec(_solution_code, _ns)
    if 'solve' in _ns:
        _r = _ns['solve'](_puzzle_input)
        if isinstance(_r, (tuple, list)) and len(_r) >= 2:
            _part1, _part2 = str(_r[0]), str(_r[1])
        elif _r is not None:
            _part1 = str(_r)
except Exception:
    _error = _tb.format_exc()
finally:
    sys.stdout, sys.stderr = _orig_out, _orig_err

json.dumps({'part1': _part1, 'part2': _part2, 'stdout': _capture.getvalue(), 'error': _error})
`

/**
 * Python wrapper that runs the optional visualize() generator and collects
 * up to 500 frames, returned as a JSON array.
 */
const VIZ_CODE = `
import json, traceback as _tb

_frames = []
try:
    _ns = {'__builtins__': __builtins__}
    exec(_solution_code, _ns)
    if 'visualize' in _ns:
        for _f in _ns['visualize'](_puzzle_input):
            _frames.append(dict(_f))
            if len(_frames) >= 500:
                break
except Exception:
    pass

json.dumps(_frames)
`

/**
 * Cleanup code to remove temporary globals and run garbage collection
 */
const CLEANUP_CODE = `
import gc
# Clear the temporary namespace variables
for _var in ['_solution_code', '_puzzle_input', '_ns', '_capture', '_r', '_f', '_frames', '_part1', '_part2', '_error']:
    if _var in dir():
        try:
            del globals()[_var]
        except:
            pass
gc.collect()
None
`

/**
 * Register shared code files as importable Python modules.
 * This allows solution.py to use `from intcode import IntcodeComputer` etc.
 */
function preloadSharedModules(py: any, sharedCode?: FetchedSharedFile[]): void {
  if (!sharedCode?.length) return

  for (const sf of sharedCode) {
    const moduleName = sf.filename.replace(/\.py$/, '')
    py.globals.set('_shared_module_name', moduleName)
    py.globals.set('_shared_module_code', sf.code)
    py.runPython(`
import types, sys
_mod = types.ModuleType(_shared_module_name)
exec(_shared_module_code, _mod.__dict__)
sys.modules[_shared_module_name] = _mod
del _mod
`)
    py.globals.delete('_shared_module_name')
    py.globals.delete('_shared_module_code')
  }
}

/**
 * Clean up Pyodide globals to free memory after running solutions
 */
function cleanupPyodide(py: any): void {
  try {
    // Delete globals from JavaScript side
    py.globals.delete('_solution_code')
    py.globals.delete('_puzzle_input')
    // Run Python-side cleanup
    py.runPython(CLEANUP_CODE)
  } catch {
    // Ignore cleanup errors
  }
}

export async function runSolution(code: string, puzzleInput: string, sharedCode?: FetchedSharedFile[]): Promise<RunResult> {
  const py = getPyodide() as any
  if (!py) throw new Error('Pyodide not initialized — click Run to load it first')

  const start = Date.now()
  preloadSharedModules(py, sharedCode)
  py.globals.set('_solution_code', code)
  py.globals.set('_puzzle_input', puzzleInput)

  try {
    const resultJson: string = await py.runPythonAsync(RUNNER_CODE)
    const result = JSON.parse(resultJson)
    return { ...result, timeMs: Date.now() - start }
  } finally {
    cleanupPyodide(py)
  }
}

export async function runVisualization(code: string, puzzleInput: string, sharedCode?: FetchedSharedFile[]): Promise<VisFrame[]> {
  const py = getPyodide() as any
  if (!py) throw new Error('Pyodide not initialized')

  preloadSharedModules(py, sharedCode)
  py.globals.set('_solution_code', code)
  py.globals.set('_puzzle_input', puzzleInput)

  try {
    const framesJson: string = await py.runPythonAsync(VIZ_CODE)
    return JSON.parse(framesJson) as VisFrame[]
  } finally {
    cleanupPyodide(py)
  }
}
