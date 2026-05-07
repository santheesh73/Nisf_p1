export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#111827",
        sidebar: "#020617",
        brand: "#4f46e5",
        accent: "#059669",
        warning: "#d97706"
      },
      boxShadow: {
        soft: "0 16px 40px rgba(15, 23, 42, 0.08)",
        glow: "0 20px 60px rgba(79, 70, 229, 0.22)",
        panel: "0 1px 2px rgba(15, 23, 42, 0.06), 0 24px 70px rgba(15, 23, 42, 0.08)"
      }
    }
  },
  plugins: []
};
