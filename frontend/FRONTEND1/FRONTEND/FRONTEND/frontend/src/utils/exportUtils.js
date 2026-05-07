export const copyBestText = async (text) => {
  if (!text) throw new Error("No text available to copy.");
  await navigator.clipboard.writeText(text);
};

const downloadFile = (filename, content, type) => {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
};

export const downloadResultJson = (result) => downloadFile(`nisf-result-${result?.job_id || "export"}.json`, JSON.stringify(result, null, 2), "application/json");
export const downloadBestTextTxt = (result) => downloadFile(`nisf-best-text-${result?.job_id || "export"}.txt`, result?.best_variant?.text || "", "text/plain");
export const downloadResultMarkdown = (result) => {
  const best = result?.best_variant;
  const lines = [
    `# NISF Result ${result?.job_id || ""}`,
    "",
    `## Best Variant`,
    "",
    best?.text || "No best variant text available.",
    "",
    `Attention Coefficient: ${best?.attention_coefficient ?? "n/a"}`,
    "",
    `Status: ${result?.status || "unknown"}`
  ];
  downloadFile(`nisf-summary-${result?.job_id || "export"}.md`, lines.join("\n"), "text/markdown");
};
