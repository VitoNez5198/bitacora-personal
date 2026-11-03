/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        carbon: {
          950: '#06080a',
          900: '#0a0c10', // Fondo base
          850: '#0f1217', // Fondo secundario / tarjetas
          800: '#151921', // Superficies elevadas y hover
          700: '#212631', // Bordes sutiles
          600: '#30363d', // Bordes interactivos
          500: '#484f58',
        },
        syntax: {
          text: '#e6edf3',       // Texto primario legible
          muted: '#8b949e',      // Metadatos y fechas
          subtle: '#6e7681',     // Bordes tenues y notas menores
          accent: '#3fb950',     // Verde consola / nominal
          warning: '#d29922',    // Ámbar vintage / WIP
          info: '#58a6ff',       // Azul técnico
          danger: '#f85149',     // Alertas
        },
      },
      fontFamily: {
        mono: [
          '"JetBrains Mono"',
          '"Geist Mono"',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Monaco',
          'Consolas',
          'monospace',
        ],
        sans: [
          '"Geist Sans"',
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          'sans-serif',
        ],
      },
    },
  },
  plugins: [],
};

