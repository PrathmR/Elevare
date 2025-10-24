/**
 * API client for backend communication
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

export interface UploadResumeResponse {
  success: boolean;
  filename: string;
  analysis: string;
  extracted_text: string;
}

export interface AnalyzeTextResponse {
  success: boolean;
  analysis: string;
}

export interface ApiError {
  error: string;
}

export interface Job {
  title: string;
  company: string;
  location: string;
  experience: string;
  salary: string;
  description: string;
  url: string;
}

export interface ScrapeJobsResponse {
  success: boolean;
  keyword: string;
  location: string | null;
  jobs_count: number;
  jobs: Job[];
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
