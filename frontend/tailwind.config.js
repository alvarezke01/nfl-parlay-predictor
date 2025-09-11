/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          bg: "#0f172a",        // slate-900
          fg: "#111827",        // gray-900
          accent: "#10b981",    // emerald-500
          accentDark: "#059669" // emerald-600
        }
      },
      borderRadius: { xl2: "1rem" },
      boxShadow: { soft: "0 4px 24px rgba(15,23,42,.08)" },
      fontFamily: {
        sans: ["Inter","system-ui","Avenir","Helvetica","Arial","sans-serif"]
      }
    }
  },
  plugins: []
};
