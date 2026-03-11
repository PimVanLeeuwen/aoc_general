import { getPyodide } from '../context/PyodideContext'
import type { RunResult, VisFrame } from '../types'

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

export async function runSolution(code: string, puzzleInput: string): Promise<RunResult> {
  const py = getPyodide()
  if (!py) throw new Error('Pyodide not initialized — click Run to load it first')

  const start = Date.now()
  py.globals.set('_solution_code', code)
  py.globals.set('_puzzle_input', puzzleInput)

  const resultJson: string = await py.runPythonAsync(RUNNER_CODE)
  const result = JSON.parse(resultJson)
  return { ...result, timeMs: Date.now() - start }
}

export async function runVisualization(code: string, puzzleInput: string): Promise<VisFrame[]> {
  const py = getPyodide()
  if (!py) throw new Error('Pyodide not initialized')

  py.globals.set('_solution_code', code)
  py.globals.set('_puzzle_input', puzzleInput)

  const framesJson: string = await py.runPythonAsync(VIZ_CODE)
  return JSON.parse(framesJson) as VisFrame[]
}
