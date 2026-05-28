import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--color-background)",
        "on-background": "var(--color-on-background)",
        surface: "var(--color-surface)",
        "surface-dim": "var(--color-surface-dim)",
        "surface-bright": "var(--color-surface-bright)",
        "surface-container-lowest": "var(--color-surface-container-lowest)",
        "surface-container-low": "var(--color-surface-container-low)",
        "surface-container": "var(--color-surface-container)",
        "surface-container-high": "var(--color-surface-container-high)",
        "surface-container-highest": "var(--color-surface-container-highest)",
        "on-surface": "var(--color-on-surface)",
        "on-surface-variant": "var(--color-on-surface-variant)",
        outline: "var(--color-outline)",
        "outline-variant": "var(--color-outline-variant)",
        primary: "var(--color-primary)",
        "on-primary": "var(--color-on-primary)",
        "primary-container": "var(--color-primary-container)",
        secondary: "var(--color-secondary)",
        tertiary: "var(--color-tertiary)",
        error: "var(--color-error)"
      },
      fontFamily: {
        sans: ["var(--font-sans)"],
        mono: ["var(--font-mono)"]
      },
      borderRadius: {
        DEFAULT: "0.25rem",
        lg: "0.5rem",
        xl: "0.75rem"
      },
      keyframes: {
        gridMove: {
          "0%": { transform: "rotateX(60deg) translateY(0)" },
          "100%": { transform: "rotateX(60deg) translateY(50px)" }
        },
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        },
        pulseGlow: {
          "0%, 100%": { opacity: "1", transform: "scale(1)" },
          "50%": { opacity: "0.7", transform: "scale(1.05)" }
        },
        dashFlow: {
          "0%": { strokeDashoffset: "0" },
          "100%": { strokeDashoffset: "-16" }
        }
      },
      animation: {
        "grid-move": "gridMove 20s linear infinite",
        "fade-up": "fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards",
        "pulse-glow": "pulseGlow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "dash-flow": "dashFlow 2s linear infinite"
      }
    }
  },
  plugins: [require("@tailwindcss/forms")]
};

export default config;
