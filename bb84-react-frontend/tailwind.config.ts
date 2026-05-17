import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cyan-accent': '#0284C7',
        'green-secure': '#16A34A',
        'purple-key': '#7C3AED',
        'red-attack': '#EF4444',
        'amber-warn': '#F59E0B',
      },
    },
  },
  plugins: [],
}
export default config
