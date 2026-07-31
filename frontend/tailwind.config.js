/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#070A12",
          900: "#0B1020",
          800: "#111830",
          700: "#1A2340",
          600: "#26325A",
          500: "#3A4A7A",
        },
        signal: {
          amber: "#F5A623",
          amberDark: "#C97F0E",
        },
        teal: {
          glow: "#2DD4BF",
        },
        alert: {
          low: "#3FA9F5",
          medium: "#F5A623",
          high: "#FF6B4A",
          critical: "#FF3B5C",
        },
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        sans: ["Inter", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(45,212,191,0.25), 0 0 24px rgba(45,212,191,0.12)",
        amberglow: "0 0 0 1px rgba(245,166,35,0.3), 0 0 24px rgba(245,166,35,0.15)",
      },
      keyframes: {
        pulseLine: {
          "0%, 100%": { opacity: 0.35 },
          "50%": { opacity: 1 },
        },
        scan: {
          "0%": { transform: "translateX(-100%)" },
          "100%": { transform: "translateX(100%)" },
        },
      },
      animation: {
        pulseLine: "pulseLine 2s ease-in-out infinite",
        scan: "scan 2.4s linear infinite",
      },
    },
  },
  plugins: [],
}

