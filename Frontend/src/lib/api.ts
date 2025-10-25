/**
 * API client for backend communication
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

export interface CandidateInfo {
  name: string;
  email: string;
  mobile: string;
  experience: number;
  domain: string;
  skills: string[];
  error?: string;
}

export interface UploadResumeResponse {
  success: boolean;
  filename: string;
  candidate_info: CandidateInfo;
  resume_text: string;
}

export interface AnalyzeTextResponse {
  success: boolean;
  analysis: string;
}

export interface ApiError {
  error: string;
}

export interface Job {
  id?: string;
  title: string;
  company: string;
  location: string;
  experience: string;
  salary: string;
  description: string;
  url: string;
  source?: string;
  domain?: string;
  keyword?: string;
  scraped_at?: string;
  created_at?: string;
  match_score?: number;
  matching_skills?: string[];
}

export interface ScrapeJobsResponse {
  success: boolean;
  keyword: string;
  location: string | null;
  jobs_count: number;
  jobs: Job[];
}

export interface ScrapeAllSourcesResponse {
  success: boolean;
  keyword: string;
  location: string | null;
  total_jobs: number;
  jobs: Job[];
  source_stats: Record<string, number>;
  errors?: Record<string, string>;
  scraped_at: string;
  database?: {
    success: boolean;
    inserted_count?: number;
    message: string;
  };
}

export interface JobSearchResponse {
  success: boolean;
  count: number;
  jobs: Job[];
}

export interface JobStatsResponse {
  success: boolean;
  stats: {
    total_jobs: number;
    jobs_by_source: Record<string, number>;
  };
}

export interface BackgroundScrapeResponse {
  success: boolean;
  message?: string;
  keywords_count?: number;
  total_jobs_scraped?: number;
  total_jobs_saved?: number;
  duration_seconds?: number;
}

/**
 * Upload and analyze a resume file
 */
export async function uploadResume(file: File): Promise<UploadResumeResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload-resume`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to upload resume');
  }

  return response.json();
}

/**
 * Analyze resume text directly
 */
export async function analyzeText(text: string): Promise<AnalyzeTextResponse> {
  const response = await fetch(`${API_BASE_URL}/analyze-text`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to analyze text');
  }

  return response.json();
}

/**
 * Check backend health
 */
export async function checkHealth(): Promise<{ status: string; message: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error('Backend is not responding');
  }

  return response.json();
}

/**
 * Scrape job listings from Naukri.com
 */
export async function scrapeJobs(
  keyword: string,
  location?: string,
  maxJobs: number = 20
): Promise<ScrapeJobsResponse> {
  const response = await fetch(`${API_BASE_URL}/scrape-jobs`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      keyword,
      location: location || null,
      max_jobs: maxJobs,
    }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to scrape jobs');
  }

  return response.json();
}

/**
 * Scrape jobs from all sources (Naukri, LinkedIn, Unstop) and save to database
 */
export async function scrapeAllSources(
  keyword: string,
  location?: string,
  maxJobsPerSource: number = 10,
  sources: string[] = ['naukri', 'linkedin', 'unstop'],
  saveToDb: boolean = true
): Promise<ScrapeAllSourcesResponse> {
  const response = await fetch(`${API_BASE_URL}/scrape-all-sources`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      keyword,
      location: location || null,
      max_jobs_per_source: maxJobsPerSource,
      sources,
      save_to_db: saveToDb,
    }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to scrape jobs from all sources');
  }

  return response.json();
}

/**
 * Search jobs in the database
 */
export async function searchJobs(
  keyword?: string,
  location?: string,
  domain?: string,
  source?: string,
  limit: number = 50
): Promise<JobSearchResponse> {
  const params = new URLSearchParams();
  if (keyword) params.append('keyword', keyword);
  if (location) params.append('location', location);
  if (domain) params.append('domain', domain);
  if (source) params.append('source', source);
  params.append('limit', limit.toString());

  const response = await fetch(`${API_BASE_URL}/jobs/search?${params.toString()}`);

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to search jobs');
  }

  return response.json();
}

/**
 * Get jobs by domain
 */
export async function getJobsByDomain(
  domain: string,
  limit: number = 50
): Promise<JobSearchResponse> {
  const response = await fetch(`${API_BASE_URL}/jobs/domain/${domain}?limit=${limit}`);

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to get jobs by domain');
  }

  return response.json();
}

/**
 * Get recent jobs
 */
export async function getRecentJobs(limit: number = 20): Promise<JobSearchResponse> {
  const response = await fetch(`${API_BASE_URL}/jobs/recent?limit=${limit}`);

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to get recent jobs');
  }

  return response.json();
}

/**
 * Get job statistics
 */
export async function getJobStats(): Promise<JobStatsResponse> {
  const response = await fetch(`${API_BASE_URL}/jobs/stats`);

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to get job stats');
  }

  return response.json();
}

/**
 * Get job recommendations from database based on resume (NO SCRAPING)
 */
export async function scrapeAndRecommend(
  resumeSkills: string[],
  domain?: string,
  location?: string
): Promise<JobSearchResponse> {
  const response = await fetch(`${API_BASE_URL}/scrape-and-recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      resume_skills: resumeSkills,
      domain: domain || null,
      location: location || null,
    }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to get recommendations');
  }

  return response.json();
}

/**
 * Start background job scraping to populate database
 */
export async function startBackgroundScraping(
  keywords?: string[],
  maxJobsPerSource: number = 5,
  runAsync: boolean = true
): Promise<BackgroundScrapeResponse> {
  const response = await fetch(`${API_BASE_URL}/scrape-background`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      keywords: keywords || null,
      max_jobs_per_source: maxJobsPerSource,
      async: runAsync,
    }),
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to start background scraping');
  }

  return response.json();
}
