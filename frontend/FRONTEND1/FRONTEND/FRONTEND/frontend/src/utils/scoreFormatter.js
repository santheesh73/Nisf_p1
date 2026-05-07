export const formatScore = (value) => (Number.isFinite(Number(value)) ? Number(value).toFixed(1) : "0.0");
export const scoreToneClass = (score) => {
  const value = Number(score);
  if (value >= 85) return "text-slate-700 bg-slate-100/70 border-slate-300";
  if (value >= 70) return "text-cyan-800 bg-cyan-100/70 border-cyan-300";
  if (value >= 50) return "text-amber-700 bg-amber-100/70 border-amber-300";
  return "text-rose-700 bg-rose-100/70 border-rose-300";
};
export const labelize = (value = "") => value.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
