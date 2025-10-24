-- Elevare Database Schema
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- PROFILES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  phone TEXT,
  bio TEXT,
  skills TEXT[],
  experience_years INTEGER,
  preferred_location TEXT,
  preferred_domain TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- ============================================
-- JOBS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS jobs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  description TEXT,
  location TEXT,
  experience TEXT,
  salary TEXT,
  url TEXT,
  source TEXT NOT NULL, -- 'Naukri', 'LinkedIn', 'Unstop'
  domain TEXT, -- 'tech', 'design', 'business', etc.
  skills_required TEXT[],
  job_type TEXT, -- 'Full-time', 'Part-time', 'Contract', 'Internship'
  is_active BOOLEAN DEFAULT true,
  keyword TEXT, -- Search keyword used to find this job
  scraped_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location);
CREATE INDEX IF NOT EXISTS idx_jobs_domain ON jobs(domain);
CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_is_active ON jobs(is_active);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at DESC);

-- Enable Row Level Security
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

-- Jobs policies (public read access)
CREATE POLICY "Anyone can view active jobs"
  ON jobs FOR SELECT
  USING (is_active = true);

CREATE POLICY "Service role can insert jobs"
  ON jobs FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Service role can update jobs"
  ON jobs FOR UPDATE
  USING (true);

-- ============================================
-- RESUMES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS resumes (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users ON DELETE CASCADE,
  file_name TEXT NOT NULL,
  file_path TEXT,
  file_url TEXT,
  parsed_text TEXT,
  analysis JSONB, -- AI analysis results
  skills TEXT[],
  experience_years INTEGER,
  education TEXT[],
  certifications TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;

-- Resumes policies
CREATE POLICY "Users can view own resumes"
  ON resumes FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own resumes"
  ON resumes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own resumes"
  ON resumes FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own resumes"
  ON resumes FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================
-- JOB APPLICATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS job_applications (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users ON DELETE CASCADE,
  job_id UUID REFERENCES jobs ON DELETE CASCADE,
  resume_id UUID REFERENCES resumes ON DELETE SET NULL,
  status TEXT DEFAULT 'pending', -- 'pending', 'applied', 'interviewing', 'rejected', 'accepted'
  cover_letter TEXT,
  notes TEXT,
  applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, job_id) -- Prevent duplicate applications
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_applications_user_id ON job_applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_job_id ON job_applications(job_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON job_applications(status);

-- Enable Row Level Security
ALTER TABLE job_applications ENABLE ROW LEVEL SECURITY;

-- Job applications policies
CREATE POLICY "Users can view own applications"
  ON job_applications FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own applications"
  ON job_applications FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own applications"
  ON job_applications FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own applications"
  ON job_applications FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================
-- SAVED JOBS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS saved_jobs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users ON DELETE CASCADE,
  job_id UUID REFERENCES jobs ON DELETE CASCADE,
  notes TEXT,
  saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, job_id) -- Prevent duplicate saves
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_saved_jobs_user_id ON saved_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_saved_jobs_job_id ON saved_jobs(job_id);

-- Enable Row Level Security
ALTER TABLE saved_jobs ENABLE ROW LEVEL SECURITY;

-- Saved jobs policies
CREATE POLICY "Users can view own saved jobs"
  ON saved_jobs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own saved jobs"
  ON saved_jobs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own saved jobs"
  ON saved_jobs FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================
-- JOB RECOMMENDATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS job_recommendations (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users ON DELETE CASCADE,
  job_id UUID REFERENCES jobs ON DELETE CASCADE,
  resume_id UUID REFERENCES resumes ON DELETE CASCADE,
  match_score DECIMAL(5,2), -- 0.00 to 100.00
  matching_skills TEXT[],
  recommendation_reason TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON job_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_match_score ON job_recommendations(match_score DESC);

-- Enable Row Level Security
ALTER TABLE job_recommendations ENABLE ROW LEVEL SECURITY;

-- Job recommendations policies
CREATE POLICY "Users can view own recommendations"
  ON job_recommendations FOR SELECT
  USING (auth.uid() = user_id);

-- ============================================
-- FUNCTIONS
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_resumes_updated_at BEFORE UPDATE ON resumes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON job_applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- VIEWS
-- ============================================

-- View for job listings with application status
CREATE OR REPLACE VIEW jobs_with_user_status AS
SELECT 
    j.*,
    CASE 
        WHEN ja.id IS NOT NULL THEN true 
        ELSE false 
    END as is_applied,
    CASE 
        WHEN sj.id IS NOT NULL THEN true 
        ELSE false 
    END as is_saved,
    ja.status as application_status,
    ja.applied_at
FROM jobs j
LEFT JOIN job_applications ja ON j.id = ja.job_id AND ja.user_id = auth.uid()
LEFT JOIN saved_jobs sj ON j.id = sj.job_id AND sj.user_id = auth.uid()
WHERE j.is_active = true;

-- ============================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================

-- Insert sample domains
-- You can uncomment this to add sample data

/*
INSERT INTO jobs (title, company, description, location, experience, salary, source, domain, is_active) VALUES
('Senior Frontend Developer', 'TechCorp', 'Looking for React expert', 'Bangalore', '3-5 years', '15-25 LPA', 'Manual', 'tech', true),
('UX Designer', 'DesignHub', 'Creative designer needed', 'Mumbai', '2-4 years', '10-18 LPA', 'Manual', 'design', true),
('Product Manager', 'StartupXYZ', 'Drive product strategy', 'Remote', '5+ years', '20-30 LPA', 'Manual', 'business', true);
*/

-- ============================================
-- NOTES
-- ============================================
-- After running this schema:
-- 1. Go to Storage in Supabase and create a bucket named 'resumes'
-- 2. Set appropriate storage policies for the bucket
-- 3. Update your backend to use these tables
-- 4. Update your frontend to query these tables
