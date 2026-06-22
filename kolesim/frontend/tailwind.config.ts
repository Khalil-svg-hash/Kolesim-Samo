import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#0F62FE",
        "primary-dark": "#0043CE",
        "primary-light": "#4589FF",
        surface: "#F5F7FA",
        text: "#1A1A1A",
        "text-secondary": "#6B7280",
        border: "#E0E6ED",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      fontSize: {
        "display": ["48px", { lineHeight: "1.15", fontWeight: "700" }],
        "h2": ["32px", { lineHeight: "1.25", fontWeight: "700" }],
        "h3": ["24px", { lineHeight: "1.3", fontWeight: "600" }],
        "h4": ["20px", { lineHeight: "1.4", fontWeight: "600" }],
        "body-lg": ["18px", { lineHeight: "1.6", fontWeight: "400" }],
        "body": ["16px", { lineHeight: "1.6", fontWeight: "400" }],
        "body-sm": ["14px", { lineHeight: "1.5", fontWeight: "400" }],
      },
      maxWidth: {
        "container": "1280px",
      },
    },
  },
  plugins: [],
};

export default config;