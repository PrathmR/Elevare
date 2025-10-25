"""
Background Job Scraper
Scrapes jobs from multiple sources for common keywords and stores in database
"""

from scraper.job_scraper_manager import JobScraperManager
from utils.job_database import JobDatabase
from datetime import datetime
import threading


class BackgroundJobScraper:
    """
    Manages background job scraping for popular keywords
    """
    
    # Popular job keywords to scrape
    POPULAR_KEYWORDS = [
        "software developer",
        "data scientist",
        "python developer",
        "full stack developer",
        "frontend developer",
        "backend developer",
        "machine learning engineer",
        "data analyst",
        "devops engineer",
        "ui ux designer",
        "product manager",
        "business analyst",
        "cybersecurity engineer",
        "cloud engineer",
        "mobile app developer"
    ]
    
    def __init__(self, headless: bool = True):
        """
        Initialize background scraper
        
        Args:
            headless (bool): Run scrapers in headless mode
        """
        self.headless = headless
        self.scraper_manager = JobScraperManager(headless=headless)
        self.db = JobDatabase()
    
    def scrape_keyword(self, keyword: str, max_jobs_per_source: int = 5) -> dict:
        """
        Scrape jobs for a single keyword and save to database
        
        Args:
            keyword (str): Job search keyword
            max_jobs_per_source (int): Max jobs to scrape per source
            
        Returns:
            dict: Scraping results
        """
        try:
            print(f"\n🔍 Scraping jobs for: {keyword}")
            
            # Scrape from all sources
            result = self.scraper_manager.scrape_all_sources(
                keyword=keyword,
                location=None,
                max_jobs_per_source=max_jobs_per_source,
                sources=['naukri', 'linkedin', 'unstop']
            )
            
            # Save to database
            if result['jobs']:
                db_result = self.db.insert_jobs(result['jobs'])
                result['database'] = db_result
                print(f"✅ Saved {db_result.get('inserted_count', 0)} jobs for '{keyword}'")
            
            return result
            
        except Exception as e:
            print(f"❌ Error scraping '{keyword}': {str(e)}")
            return {
                "success": False,
                "keyword": keyword,
                "error": str(e)
            }
    
    def scrape_all_popular_keywords(self, max_jobs_per_source: int = 5) -> dict:
        """
        Scrape jobs for all popular keywords
        
        Args:
            max_jobs_per_source (int): Max jobs to scrape per source per keyword
            
        Returns:
            dict: Overall scraping results
        """
        print(f"\n{'='*60}")
        print("🚀 Starting background job scraping")
        print(f"Keywords: {len(self.POPULAR_KEYWORDS)}")
        print(f"{'='*60}")
        
        start_time = datetime.now()
        results = []
        total_jobs_scraped = 0
        total_jobs_saved = 0
        
        for keyword in self.POPULAR_KEYWORDS:
            result = self.scrape_keyword(keyword, max_jobs_per_source)
            results.append(result)
            
            if result.get('success'):
                total_jobs_scraped += result.get('total_jobs', 0)
                total_jobs_saved += result.get('database', {}).get('inserted_count', 0)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        summary = {
            "success": True,
            "total_keywords": len(self.POPULAR_KEYWORDS),
            "total_jobs_scraped": total_jobs_scraped,
            "total_jobs_saved": total_jobs_saved,
            "duration_seconds": duration,
            "started_at": start_time.isoformat(),
            "completed_at": end_time.isoformat(),
            "results": results
        }
        
        print(f"\n{'='*60}")
        print("✅ Background scraping completed!")
        print(f"Total jobs scraped: {total_jobs_scraped}")
        print(f"Total jobs saved to DB: {total_jobs_saved}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"{'='*60}\n")
        
        return summary
    
    def scrape_async(self, keywords: list = None, max_jobs_per_source: int = 5) -> None:
        """
        Start background scraping in a separate thread (non-blocking)
        
        Args:
            keywords (list): List of keywords to scrape (None = use popular keywords)
            max_jobs_per_source (int): Max jobs per source per keyword
        """
        if keywords is None:
            keywords = self.POPULAR_KEYWORDS
        
        def scrape_task():
            for keyword in keywords:
                self.scrape_keyword(keyword, max_jobs_per_source)
        
        thread = threading.Thread(target=scrape_task, daemon=True)
        thread.start()
        print(f"🚀 Started background scraping for {len(keywords)} keywords")
