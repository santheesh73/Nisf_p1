export const parseBrandTerms = (value) =>
  value
    ? value.split(",").map((term) => term.trim()).filter(Boolean)
    : [];

export const clampGenerateVariantCount = (value) =>
  Math.min(Math.max(Number(value || 5), 1), 5);

export const clampOptimizeVariantCount = (value) =>
  Math.min(Math.max(Number(value || 5), 3), 5);

export const clampVariantCount = clampGenerateVariantCount;

export const getBestVariantText = (result) =>
  result?.best_variant?.text ??
  result?.best_variant?.content ??
  (typeof result?.best_variant === "string" ? result.best_variant : "") ??
  "";

export const getAttentionScore = (result) =>
  result?.scores?.attention_coefficient ??
  result?.best_variant?.attention_coefficient ??
  result?.best_variant?.scores?.attention_coefficient ??
  0;

export const getVariants = (result) =>
  Array.isArray(result?.variants) ? result.variants : [];

export const getCriticDirectives = (result) =>
  Array.isArray(result?.critic_directives) ? result.critic_directives : [];

export const getIterationHistory = (result) =>
  Array.isArray(result?.iteration_history) ? result.iteration_history : [];
