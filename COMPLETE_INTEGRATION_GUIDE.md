# Complete Multi-Source Job Scraping Integration Guide

## 🎉 Overview

Your Elevare platform now has **complete multi-source job scraping** integrated with:
- ✅ **3 Job Portals**: Naukri, LinkedIn, Unstop
- ✅ **Database Storage**: Supabase PostgreSQL
- ✅ **Search Functionality**: Full-text search across all jobs
- ✅ **Domain Filtering**: Jobs organized by industry
- ✅ **AI Recommendations**: Resume-based job matching

---

## 📋 What Was Implemented

### 1. Backend Scrapers (3 Sources)

#### **Naukri Scraper** (`backend/scraper/naukri_scraper.py`)
- Scrapes jobs from Naukri.com
- Extracts: title, company, location, experience, salary, description, URL
- Supports location filtering

#### **LinkedIn Scraper** (`backend/scraper/linkedin_scraper.py`)
- Scrapes jobs from LinkedIn
- Extracts: title, company, location, posted date, URL
- Note: LinkedIn has anti-scraping measures; use cautiously

#### **Unstop Scraper** (`backend/scraper/unstop_scraper.py`)
- Scrapes jobs/internships/competitions from Unstop
- Supports multiple categories
- Extracts: title, company, location, deadline, stipend, URL

#### **Unified Manager** (`backend/scraper/job_scraper_manager.py`)
- Manages all scrapers from one place
- Supports parallel scraping for speed
- Domain-based scraping with keyword mapping

### 2. Database Integration

#### **Supabase Schema** (`database/schema.sql`)
Complete database schema with:
- **`jobs`** table - Stores all scraped jobs
- **`profiles`** table - User profiles with preferences
- **`resumes`** table - Uploaded resumes with AI analysis
- **`job_applications`** table - Track applications
- **`saved_jobs`** table - Bookmark jobs
- **`job_recommendations`** table - AI-matched jobs

#### **Database Service** (`backend/utils/job_database.py`)
- Insert jobs from scrapers
- Search jobs with filters
- Get jobs by domain
- Job statistics

### 3. Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scrape-jobs` | POST | Scrape from Naukri only |
| `/api/scrape-all-sources` | POST | Scrape from all 3 sources + save to DB |
| `/api/jobs/search` | GET | Search jobs in database |
| `/api/jobs/domain/<domain>` | GET | Get jobs by domain |
| `/api/jobs/recent` | GET | Get recent jobs |
| `/api/jobs/stats` | GET | Get job statistics |
| `/api/scrape-and-recommend` | POST | Scrape + match with resume |

### 4. Frontend Integration

#### **Jobs Page** (`Frontend/src/pages/Jobs.tsx`)
- **Search Bar**: Search database or scrape fresh jobs
- **Multi-Source Scraping**: Button to scrape from all portals
- **Real-time Updates**: Loading states and toast notifications
- **Job Cards**: Display with source badges and match scores
- **Domain Filtering**: Support for domain-based filtering

#### **Domain Page** (`Frontend/src/pages/Domain.tsx`)
- **Real Counts**: Shows actual job counts from database
- **Domain Cards**: Click to filter jobs by domain
- **Loading States**: Smooth UX while loading

#### **Resume Analyzer** (`Frontend/src/pages/UploadResume.tsx`)
- **AI Analysis**: Upload resume for AI analysis
- **Job Recommendations**: Get matched jobs based on skills
- **Match Scores**: Shows % match with each job
- **Skill Highlighting**: Displays matching skills

---

## 🚀 Setup Instructions

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New dependencies added:**
- `selenium==4.15.2`
- `webdriver-manager==4.0.1`
- `beautifulsoup4==4.12.2`
- `supabase==2.3.0`

### Step 2: Install Chrome/Chromium

The scrapers use Chrome for web automation:
- **Windows**: Download from [google.com/chrome](https://www.google.com/chrome/)
- **Linux**: `sudo apt-get install chromium-browser`
- **Mac**: Download from Chrome website

### Step 3: Set Up Supabase Database

1. **Go to Supabase Dashboard**: [supabase.com](https://supabase.com)
2. **Create/Open Your Project**
3. **Run the Schema**:
   - Go to SQL Editor
   - Copy contents from `database/schema.sql`
   - Click "Run"
4. **Get Credentials**:
   - Go to Settings → API
   - Copy Project URL and Service Role Key

### Step 4: Configure Environment Variables

#### Backend `.env` file:
```env
# Existing
GOOGLE_API_KEY=your_gemini_api_key

# Add these new variables
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_service_role_key_here
```

#### Frontend `.env` file (already configured):
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=your_anon_key_here
VITE_API_BASE_URL=http://localhost:5000/api
```

### Step 5: Start the Backend

```bash
cd backend
python app.py
```

Server starts on `http://localhost:5000`

### Step 6: Start the Frontend

```bash
cd Frontend
npm install
npm run dev
```

Frontend starts on `http://localhost:5173`

---

## 💻 Usage Guide

### 1. Search for Jobs

**In the Jobs Page:**
1. Enter a keyword (e.g., "python developer")
2. Click **Search** to search the database
3. Click **Scrape Fresh Jobs** to get new jobs from all sources
4. Jobs are automatically saved to the database

### 2. Browse by Domain

**In the Domains Page:**
1. Click on any domain card (Tech, Design, Business, etc.)
2. View jobs specific to that domain
3. Real counts are loaded from the database

### 3. Get AI Recommendations

**In the Upload Resume Page:**
1. Upload your resume (PDF, DOC, DOCX)
2. Wait for AI analysis
3. Click **Get Job Recommendations**
4. System scrapes jobs and matches them with your skills
5. View jobs sorted by match score

### 4. Direct API Usage

#### Scrape from all sources:
```bash
curl -X POST http://localhost:5000/api/scrape-all-sources \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "react developer",
    "location": "bangalore",
    "max_jobs_per_source": 10,
    "sources": ["naukri", "linkedin", "unstop"],
    "save_to_db": true
  }'
```

#### Search jobs:
```bash
curl "http://localhost:5000/api/jobs/search?keyword=python&location=mumbai&limit=20"
```

#### Get domain jobs:
```bash
curl "http://localhost:5000/api/jobs/domain/tech?limit=50"
```

---

## 📊 Features Breakdown

### Multi-Source Scraping
- **Parallel Processing**: Scrape from multiple sources simultaneously
- **Error Handling**: Continues even if one source fails
- **Source Statistics**: Shows count from each source
- **Auto-Save**: Automatically saves to database

### Database Features
- **Full-Text Search**: Search across title, company, description
- **Filtering**: By keyword, location, domain, source
- **Pagination**: Limit results for performance
- **Deduplication**: Prevents duplicate job entries
- **Statistics**: Track jobs by source and domain

### AI Matching
- **Skill Extraction**: Extracts skills from resume
- **Match Scoring**: Calculates % match with each job
- **Skill Highlighting**: Shows which skills match
- **Smart Sorting**: Jobs sorted by relevance

### User Experience
- **Loading States**: Clear feedback during operations
- **Toast Notifications**: Success/error messages
- **Real-time Updates**: Immediate UI updates
- **Responsive Design**: Works on all devices

---

## 🔧 Configuration Options

### Scraping Configuration

```python
# In backend/scraper/job_scraper_manager.py

# Domain to keyword mapping
domain_keywords = {
    'tech': 'software developer',
    'design': 'designer',
    'business': 'business analyst',
    'hr': 'human resources',
    'security': 'cybersecurity',
    'healthcare': 'healthcare',
    'data': 'data scientist',
    'marketing': 'marketing manager',
    'sales': 'sales executive'
}
```

### Database Configuration

```sql
-- Adjust job retention period
-- In database/schema.sql, modify the delete_old_jobs function
-- Default: 30 days
```

### Frontend Configuration

```typescript
// In Frontend/src/lib/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

// Adjust default limits
const DEFAULT_LIMIT = 50;
const MAX_JOBS_PER_SOURCE = 10;
```

---

## 🐛 Troubleshooting

### Issue: ChromeDriver not found
**Solution**: ChromeDriver auto-downloads on first run. Ensure internet connection.

### Issue: No jobs scraped
**Solutions**:
- Check keyword format (use hyphens: `python-developer`)
- Verify internet connection
- Check if websites are accessible
- Try with headless=False to see browser

### Issue: Database connection failed
**Solutions**:
- Verify Supabase credentials in `.env`
- Check if Supabase project is active
- Ensure service role key (not anon key) is used in backend

### Issue: CORS errors
**Solutions**:
- Ensure backend is running on port 5000
- Check CORS configuration in `backend/app.py`
- Verify frontend URL in CORS origins

### Issue: Scraping takes too long
**Solutions**:
- Reduce `max_jobs_per_source` (default: 10)
- Use fewer sources
- Enable parallel scraping (already implemented)

---

## 📈 Performance Tips

1. **Initial Setup**: Run a bulk scrape to populate database
   ```bash
   # Scrape multiple domains
   curl -X POST http://localhost:5000/api/scrape-all-sources \
     -d '{"keyword":"software developer","max_jobs_per_source":20}'
   ```

2. **Scheduled Scraping**: Set up cron job for daily updates
   ```bash
   # Add to crontab
   0 2 * * * curl -X POST http://localhost:5000/api/scrape-all-sources ...
   ```

3. **Database Maintenance**: Clean old jobs periodically
   ```sql
   -- Run in Supabase SQL Editor
   UPDATE jobs SET is_active = false 
   WHERE created_at < NOW() - INTERVAL '30 days';
   ```

4. **Caching**: Jobs are cached in database, reducing scraping frequency

---

## 🔒 Security Considerations

1. **API Keys**: Never commit `.env` files
2. **Rate Limiting**: Be respectful of job portal servers
3. **User Data**: Resume data is encrypted in Supabase
4. **Authentication**: Use Supabase RLS policies
5. **CORS**: Restrict to known origins in production

---

## 🚀 Future Enhancements

Potential improvements:
- [ ] Add more job portals (Indeed, Glassdoor)
- [ ] Implement job alerts via email
- [ ] Add advanced filters (salary range, company size)
- [ ] Create job comparison feature
- [ ] Add application tracking
- [ ] Implement job analytics dashboard
- [ ] Add social sharing features
- [ ] Create mobile app

---

## 📚 File Structure

```
Codes/
├── backend/
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── naukri_scraper.py          ✅ NEW
│   │   ├── linkedin_scraper.py        ✅ NEW
│   │   ├── unstop_scraper.py          ✅ NEW
│   │   └── job_scraper_manager.py     ✅ NEW
│   ├── utils/
│   │   ├── supabase_client.py         ✅ NEW
│   │   └── job_database.py            ✅ NEW
│   ├── app.py                         ✅ UPDATED
│   └── requirements.txt               ✅ UPDATED
│
├── Frontend/src/
│   ├── lib/
│   │   └── api.ts                     ✅ UPDATED
│   ├── pages/
│   │   ├── Jobs.tsx                   ✅ UPDATED
│   │   ├── Domain.tsx                 ✅ UPDATED
│   │   └── UploadResume.tsx           ✅ UPDATED
│
├── database/
│   └── schema.sql                     ✅ NEW
│
└── Documentation/
    ├── WEB_SCRAPING_INTEGRATION.md
    ├── INTEGRATION_SUMMARY.md
    ├── QUICK_REFERENCE_SCRAPING.md
    └── COMPLETE_INTEGRATION_GUIDE.md  ✅ THIS FILE
```

---

## 🎯 Quick Start Checklist

- [ ] Install Python dependencies (`pip install -r requirements.txt`)
- [ ] Install Chrome/Chromium browser
- [ ] Set up Supabase project
- [ ] Run database schema (`database/schema.sql`)
- [ ] Configure backend `.env` (add Supabase credentials)
- [ ] Configure frontend `.env` (already done)
- [ ] Start backend (`python app.py`)
- [ ] Start frontend (`npm run dev`)
- [ ] Test scraping from Jobs page
- [ ] Upload resume and get recommendations
- [ ] Browse jobs by domain

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review console logs (backend and frontend)
3. Verify all environment variables are set
4. Ensure all services are running

---

**🎉 Congratulations! Your multi-source job scraping platform is ready!**

The system now scrapes jobs from Naukri, LinkedIn, and Unstop, stores them in a database, provides intelligent search, domain filtering, and AI-powered job recommendations based on resume analysis.
