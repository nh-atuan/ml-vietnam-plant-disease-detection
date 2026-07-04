import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: "#f7f9f6",
          raised: "#ffffff",
        },
        healthy: {
          50: "#f0fdf4",
          500: "#22c55e",
          700: "#15803d",
        },
        warning: {
          50: "#fffbeb",
          500: "#f59e0b",
          700: "#b45309",
        },
        danger: {
          50: "#fef2f2",
          500: "#ef4444",
          700: "#b91c1c",
        },
        info: {
          50: "#eff6ff",
          500: "#3b82f6",
          700: "#1d4ed8",
        },
      },
    },
  },
  plugins: [],
};

export default config;
