export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        df: {
          bg: "#081B16",
          section: "#0C1F26",
          card: "#10252A",
          cardhover: "#16333A",
          border: "#243B42",
          text: "#F8FAFC",
          textsec: "#94A3B8",
          textmuted: "#64748B",
          accent: "#FF5A5F",
          accenthover: "#FF7A7F",
          gold: "#FFC857",
          success: "#2ECC71",
          warning: "#F4A261",
          error: "#EF4444"
        },
        forest: "#0f3d2e",
        emeraldx: "#10b981",
        gold: "#f6c453",
        slatex: "#0f172a"
      },
      boxShadow: {
        glow: "0 0 40px rgba(255, 90, 95, 0.18)",
        gold: "0 0 30px rgba(246, 196, 83, 0.18)"
      }
    }
  },
  plugins: []
};
