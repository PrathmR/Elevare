# Web Scraping Quick Reference

## 🚀 Quick Commands

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Test Scraper
```bash
cd backend
python test_scraper.py
```

### Start Backend
```bash
cd backend
python app.py
```

## 📡 API Endpoint

```
POST http://localhost:5000/api/scrape-jobs
```

### Request
```json
{
  "keyword": "python-developer",
  "location": "bangalore",
  "max_jobs": 20
}
```

### cURL Example
```bash
curl -X POST http://localhost:5000/api/scrape-jobs \
  -H "Content-Type: application/json" \
  -d '{"keyword":"python-developer","max_jobs":10}'
```

## 💻 Frontend Usage

### Import
```typescript
import { scrapeJobs } from '@/lib/api';
```

### Basic Usage
```typescript
const result = await scrapeJobs('python-developer');
```

### With Location
```typescript
const result = await scrapeJobs('java-developer', 'bangalore');
```

### With Max Jobs
```typescript
const result = await scrapeJobs('react-developer', 'pune', 30);
```

## 🔧 Python Usage

```python
from scraper.naukri_scraper import NaukriScraper

scraper = NaukriScraper(headless=True)
jobs = scraper.scrape_jobs('python-developer', max_jobs=20)
```

## 📊 Response Structure

```typescript
{
  success: boolean;
  keyword: string;
  location: string | null;
  jobs_count: number;
  jobs: [
    {
      title: string;
      company: string;
      location: string;
      experience: string;
      salary: string;
      description: string;
      url: string;
    }
  ]
}
```

## 🎯 Common Keywords

- `python-developer`
- `java-developer`
- `react-developer`
- `full-stack-developer`
- `data-scientist`
- `machine-learning-engineer`
- `devops-engineer`
- `frontend-developer`
- `backend-developer`

## 🏙️ Common Locations

- `bangalore`
- `mumbai`
- `pune`
- `hyderabad`
- `delhi`
- `chennai`
- `noida`
- `gurgaon`

## ⚡ Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| ChromeDriver not found | Auto-downloads on first run, ensure internet |
| No jobs found | Check keyword format (use hyphens) |
| Timeout error | Increase sleep duration in scraper |
| Import error | Activate venv: `venv\Scripts\activate` |
| Chrome not found | Install Chrome/Chromium |

## 📚 Documentation

- **Full Guide**: `WEB_SCRAPING_INTEGRATION.md`
- **Summary**: `INTEGRATION_SUMMARY.md`
- **Backend README**: `backend/README.md`

---

**Ready to scrape! 🎉**
