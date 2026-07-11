/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#05080a',
        panel: '#0b1116',
        line: '#182226',
        cyan: {
          DEFAULT: '#00e5ff',
          dim: '#0891a8',
        },
      },
      fontFamily: {
        display: ['Orbitron', 'sans-serif'],
        mono: ['"Share Tech Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
