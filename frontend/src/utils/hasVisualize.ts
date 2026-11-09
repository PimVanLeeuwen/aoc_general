// A real top-level visualize(), not the commented-out example from the solution template.
const VISUALIZE_DEF = /^def visualize\(/m

export function hasVisualize(code: string): boolean {
  return VISUALIZE_DEF.test(code)
}
