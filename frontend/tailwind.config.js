/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        aoc: {
          bg: '#0f0f23',
          surface: '#1a1a2e',
          elevated: '#222244',
          border: '#2a2a4a',
          text: '#cccccc',
          muted: '#666699',
          gold: '#ffff66',
          green: '#00cc44',
          blue: '#00aaff',
          red: '#ff5555',
        },
      },
    },
  },
  plugins: [],
}
