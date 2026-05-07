export const CONTENT_TYPES = ["ad_copy", "social_media", "email", "product_description", "blog_intro", "landing_page_headline", "cta", "microcopy"];
export const TONES = ["professional", "friendly", "persuasive", "bold", "luxury", "playful", "urgent", "educational"];
export const PLATFORMS = ["website", "instagram", "linkedin", "youtube", "email", "google_ads", "facebook_ads", "x_twitter"];
export const SCORE_DIMENSIONS = ["clarity", "engagement", "emotional_resonance", "readability", "originality", "brand_fit", "safety", "attention_coefficient"];
export const JOB_STATUSES = ["queued", "running", "generating", "simulating", "scoring", "criticizing", "optimizing", "safety_checking", "completed", "failed", "cancelled"];
export const TERMINAL_STATUSES = ["completed", "failed", "cancelled"];
export const DEFAULT_TEMPLATES = [
  { id: "ad_copy", name: "Ad Copy", content_type: "ad_copy", prompt: "Write conversion-focused ad copy for..." },
  { id: "social_media", name: "Social Media Caption", content_type: "social_media", prompt: "Create a platform-native caption for..." },
  { id: "email", name: "Email Campaign", content_type: "email", prompt: "Draft an email campaign message for..." },
  { id: "product_description", name: "Product Description", content_type: "product_description", prompt: "Describe this product with benefits and proof..." },
  { id: "blog_intro", name: "Blog Intro", content_type: "blog_intro", prompt: "Write a compelling blog introduction about..." },
  { id: "landing_page_headline", name: "Landing Page Headline", content_type: "landing_page_headline", prompt: "Create a sharp landing page headline for..." },
  { id: "cta", name: "CTA", content_type: "cta", prompt: "Generate a clear call to action for..." },
  { id: "microcopy", name: "Microcopy", content_type: "microcopy", prompt: "Improve this interface microcopy..." }
];
