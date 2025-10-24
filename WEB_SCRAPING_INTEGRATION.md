# Web Scraping Integration Guide

## 📋 Overview

The Naukri.com web scraping functionality has been successfully integrated into the Elevare platform. This allows you to scrape job listings directly from Naukri.com through a REST API endpoint.

## 🏗️ Architecture

```
Frontend (React)
    ↓
    └─→ API Client (src/lib/api.ts)
            ↓
            └─→ POST /api/scrape-jobs
                    ↓
                    └─→ Backend (Flask)
                            ↓
                            └─→ NaukriScraper (scraper/naukri_scraper.py)
                                    ↓
                                    └─→ Naukri.com (Selenium + BeautifulSoup)
```

## 📁 New Files Created

### Backend
- **`backend/scraper/__init__.py`** - Package initializer
- **`backend/scraper/naukri_scraper.py`** - Main scraper class with enhanced features

### Documentation
- **`WEB_SCRAPING_INTEGRATION.md`** - This file

## 🔧 Setup Instructions

### 1. Install Backend Dependencies

Navigate to the backend directory and install the new dependencies:

```bash
cd backend
pip install -r requirements.txt
```

New dependencies added:
- `selenium==4.15.2` - Browser automation
- `webdriver-manager==4.0.1` - Automatic ChromeDriver management
- `beautifulsoup4==4.12.2` - HTML parsing

### 2. Verify Chrome Installation

The scraper uses Chrome/Chromium. Ensure you have Chrome installed on your system:
- **Windows**: Chrome should be installed in the default location
- **Linux**: Install with `sudo apt-get install chromium-browser`
- **Mac**: Install Chrome from the official website

## 🚀 API Usage

### Endpoint: `/api/scrape-jobs`

**Method:** `POST`

**Request Body:**
```json
{
  "keyword": "python-developer",
  "location": "bangalore",  // Optional
  "max_jobs": 20            // Optional, default: 20, max: 100
}
```

**Response:**
```json
{
  "success": true,
  "keyword": "python-developer",
  "location": "bangalore",
  "jobs_count": 20,
  "jobs": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "Bangalore",
      "experience": "3-5 years",
      "salary": "10-15 LPA",
      "description": "Looking for experienced Python developer...",
      "url": "https://www.naukri.com/job-listings/..."
    }
    // ... more jobs
  ]
}
```

## 💻 Frontend Usage

### Using the API Client

```typescript
import { scrapeJobs } from '@/lib/api';

// Basic usage - scrape by keyword only
const result = await scrapeJobs('python-developer');

// With location filter
const result = await scrapeJobs('java-developer', 'mumbai');

// With custom max jobs
const result = await scrapeJobs('react-developer', 'pune', 30);

// Access the jobs
console.log(result.jobs);
```

### Example React Component

```tsx
import { useState } from 'react';
import { scrapeJobs, Job } from '@/lib/api';
import { Button } from '@/components/ui/button';

function JobScraper() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [keyword, setKeyword] = useState('');

  const handleScrape = async () => {
    setLoading(true);
    try {
      const result = await scrapeJobs(keyword);
      setJobs(result.jobs);
    } catch (error) {
      console.error('Error scraping jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        placeholder="Enter job keyword"
      />
      <Button onClick={handleScrape} disabled={loading}>
        {loading ? 'Scraping...' : 'Scrape Jobs'}
      </Button>
      
      <div>
        {jobs.map((job, index) => (
          <div key={index}>
            <h3>{job.title}</h3>
            <p>{job.company} - {job.location}</p>
            <p>Experience: {job.experience}</p>
            <p>Salary: {job.salary}</p>
            <a href={job.url} target="_blank">View Job</a>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## 🔍 Scraper Features

### NaukriScraper Class

The `NaukriScraper` class provides two main methods:

#### 1. `scrape_jobs(keyword, max_jobs)`
Scrapes jobs based on keyword only.

```python
from scraper.naukri_scraper import NaukriScraper

scraper = NaukriScraper(headless=True)
jobs = scraper.scrape_jobs('python-developer', max_jobs=20)
```

#### 2. `scrape_jobs_by_location(keyword, location, max_jobs)`
Scrapes jobs filtered by both keyword and location.

```python
scraper = NaukriScraper(headless=True)
jobs = scraper.scrape_jobs_by_location('java-developer', 'bangalore', max_jobs=30)
```

### Extracted Job Data

Each job object contains:
- **title**: Job title
- **company**: Company name
- **location**: Job location(s)
- **experience**: Required experience
- **salary**: Salary range
- **description**: Job description snippet
- **url**: Direct link to the job posting

## ⚙️ Configuration

### Headless Mode

By default, the scraper runs in headless mode (no browser window). To see the browser:

```python
scraper = NaukriScraper(headless=False)
```

### Timeout Settings

The scraper waits 10 seconds for pages to load. Adjust in `naukri_scraper.py`:

```python
time.sleep(10)  # Change this value if needed
```

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver not found**
   - The `webdriver-manager` package automatically downloads ChromeDriver
   - Ensure you have internet connection on first run

2. **Timeout errors**
   - Increase the `time.sleep()` duration in the scraper
   - Check your internet connection

3. **No jobs found**
   - Verify the keyword format (use hyphens: `python-developer`)
   - Check if Naukri.com is accessible
   - The website structure may have changed (update selectors)

4. **Selenium errors**
   - Ensure Chrome/Chromium is installed
   - Update Chrome to the latest version
   - Clear browser cache

### Debug Mode

To see detailed logs, check the Flask console output when running the backend.

## 📊 Performance Considerations

- **Scraping Time**: Approximately 10-15 seconds for 20 jobs
- **Rate Limiting**: Be respectful of Naukri.com's servers
- **Caching**: Consider caching results to avoid repeated scraping
- **Max Jobs**: Limited to 100 jobs per request to prevent timeouts

## 🔒 Best Practices

1. **Don't abuse the scraper** - Use reasonable intervals between requests
2. **Cache results** - Store scraped data to reduce API calls
3. **Handle errors gracefully** - Always wrap API calls in try-catch blocks
4. **Respect robots.txt** - Be aware of Naukri.com's scraping policies
5. **Monitor performance** - Track scraping times and success rates

## 🚀 Future Enhancements

Potential improvements:
- [ ] Add support for more job portals (LinkedIn, Indeed, etc.)
- [ ] Implement pagination for more than 100 jobs
- [ ] Add filters for salary range, company type, etc.
- [ ] Cache scraped jobs in database
- [ ] Add job deduplication logic
- [ ] Implement background job scraping with Celery
- [ ] Add rate limiting to prevent abuse

## 📝 Example Use Cases

### 1. Job Search Page
Create a job search page where users can:
- Enter keywords and location
- View scraped jobs in real-time
- Save jobs to their profile
- Apply filters

### 2. Automated Job Alerts
- Scrape jobs periodically
- Match with user preferences
- Send email notifications

### 3. Job Market Analysis
- Scrape jobs for different keywords
- Analyze salary trends
- Identify in-demand skills

## 🔗 Related Files

- **Backend API**: `backend/app.py` (lines 121-161)
- **Scraper Module**: `backend/scraper/naukri_scraper.py`
- **Frontend API Client**: `Frontend/src/lib/api.ts` (lines 94-120)
- **Dependencies**: `backend/requirements.txt`

## 📞 Support

If you encounter issues:
1. Check the Flask console for error messages
2. Verify all dependencies are installed
3. Ensure Chrome is up to date
4. Review this documentation

---

**Integration completed successfully! 🎉**
