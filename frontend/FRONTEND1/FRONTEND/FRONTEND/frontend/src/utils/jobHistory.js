const HISTORY_KEY = "nisf_job_history";

export const getJobHistory = () => {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

export const saveJobHistory = (jobs) => {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(jobs));
};

export const addJobToHistory = (job) => {
  const jobs = getJobHistory();
  const exists = jobs.some((item) => item.job_id === job.job_id);
  if (exists) return;
  const next = [job, ...jobs].slice(0, 50);
  saveJobHistory(next);
};

export const updateJobInHistory = (jobId, updates) => {
  const jobs = getJobHistory();
  const next = jobs.map((job) =>
    job.job_id === jobId ? { ...job, ...updates, updated_at: new Date().toISOString() } : job
  );
  saveJobHistory(next);
};

export const clearJobHistory = () => {
  localStorage.removeItem(HISTORY_KEY);
};
