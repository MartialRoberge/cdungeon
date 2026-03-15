/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dg: {
          bg:      "#080810",
          surface: "#0f0f1a",
          surface2:"#161625",
          border:  "#1e1e35",
          accent:  "#00ff88",
          danger:  "#ff3355",
          warning: "#ffb800",
          muted:   "#3a3a5c",
          code:    "#0d0d1a",
          glow:    "#00ff8820",
        },
      },
      fontFamily: {
        sans: ["'Space Grotesk'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      animation: {
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "slide-up": "slide-up 0.3s ease-out",
        "flash-green": "flash-green 0.4s ease-out",
        "flash-red": "flash-red 0.4s ease-out",
        "badge-pop": "badge-pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
        scanline: "scanline 8s linear infinite",
        "type-in": "type-in 0.5s steps(20) forwards",
      },
      keyframes: {
        "pulse-glow": {
          "0%,100%": { boxShadow: "0 0 5px #00ff8840" },
          "50%": { boxShadow: "0 0 20px #00ff8880, 0 0 40px #00ff8840" },
        },
        "slide-up": {
          from: { opacity: "0", transform: "translateY(20px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "flash-green": {
          "0%": { backgroundColor: "#00ff8830" },
          "100%": { backgroundColor: "transparent" },
        },
        "flash-red": {
          "0%": { backgroundColor: "#ff335530" },
          "100%": { backgroundColor: "transparent" },
        },
        "badge-pop": {
          "0%": { opacity: "0", transform: "scale(0.5)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        scanline: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100vh)" },
        },
        "type-in": {
          from: { width: "0" },
          to: { width: "100%" },
        },
      },
      boxShadow: {
        neon: "0 0 10px #00ff88, 0 0 20px #00ff8840",
        "neon-red": "0 0 10px #ff3355, 0 0 20px #ff335540",
        "neon-warn": "0 0 10px #ffaa00, 0 0 20px #ffaa0040",
      },
    },
  },
  plugins: [],
};

