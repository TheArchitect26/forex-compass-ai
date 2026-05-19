/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0a0e17",
        panel: "#0f1521",
        panel2: "#141b2a",
        border: "#1f2937",
        text: "#e5e7eb",
        muted: "#94a3b8",
        accent: "#22d3ee",
        bull: "#10b981",
        bear: "#ef4444",
      },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"], mono: ["JetBrains Mono", "monospace"] },
    },
  },
  plugins: [],
};
