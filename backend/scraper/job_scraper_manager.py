"""
Unified Job Scraper Manager
Manages scraping from multiple job portals (Naukri, LinkedIn, Unstop)
"""

from typing import List, Dict, Optional
from .naukri_scraper import NaukriScraper
from .linkedin_scraper import LinkedInScraper
from .unstop_scraper import UnstopScraper
import concurrent.futures
from datetime import datetime


class JobScraperManager:
    """
    Manages job scraping from multiple sources
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize the scraper manager
        
        Args:
            headless (bool): Whether to run browsers in headless mode
        """
        self.headless = headless
    
    def scrape_all_sources(
        self,
        keyword: str,
        location: Optional[str] = None,
        max_jobs_per_source: int = 10,
        sources: List[str] = None
    ) -> Dict[str, any]:
        """
        Scrape jobs from all enabled sources
        
        Args:
            keyword (str): Job search keyword
            location (str): Optional location filter
            max_jobs_per_source (int): Max jobs to scrape from each source
            sources (List[str]): List of sources to scrape from. 
                                Options: ['naukri', 'linkedin', 'unstop']
                                If None, scrapes from all sources
        
        Returns:
            Dict with jobs from all sources and metadata
        """
        if sources is None:
            sources = ['naukri', 'linkedin', 'unstop']
        
        all_jobs = []
        source_stats = {}
        errors = {}
        
        # Scrape from each source
        for source in sources:
            try:
                print(f"\n{'='*60}")
                print(f"Scraping from {source.upper()}...")
                print(f"{'='*60}")
                
                jobs = []
                
                if source.lower() == 'naukri':
                    scraper = NaukriScraper(headless=self.headless)
                    if location:
                        jobs = scraper.scrape_jobs_by_location(keyword, location, max_jobs_per_source)
                    else:
                        jobs = scraper.scrape_jobs(keyword, max_jobs_per_source)
                
                elif source.lower() == 'linkedin':
                    scraper = LinkedInScraper(headless=self.headless)
                    jobs = scraper.scrape_jobs(keyword, location or "", max_jobs_per_source)
                
                elif source.lower() == 'unstop':
                    scraper = UnstopScraper(headless=self.headless)
                    jobs = scraper.scrape_jobs(keyword, category="jobs", max_jobs=max_jobs_per_source)
                
                # Add scraped timestamp to each job
                for job in jobs:
                    job['scraped_at'] = datetime.now().isoformat()
                    job['keyword'] = keyword
                
                all_jobs.extend(jobs)
                source_stats[source] = len(jobs)
                print(f"✅ Successfully scraped {len(jobs)} jobs from {source}")
                
            except Exception as e:
                print(f"❌ Error scraping from {source}: {str(e)}")
                errors[source] = str(e)
                source_stats[source] = 0
        
        return {
            'success': True,
            'keyword': keyword,
            'location': location,
            'total_jobs': len(all_jobs),
            'jobs': all_jobs,
            'source_stats': source_stats,
            'errors': errors if errors else None,
            'scraped_at': datetime.now().isoformat()
        }
    
    def scrape_parallel(
        self,
        keyword: str,
        location: Optional[str] = None,
        max_jobs_per_source: int = 10,
        sources: List[str] = None
    ) -> Dict[str, any]:
        """
        Scrape jobs from multiple sources in parallel (faster but more resource-intensive)
        
        Args:
            keyword (str): Job search keyword
            location (str): Optional location filter
            max_jobs_per_source (int): Max jobs to scrape from each source
            sources (List[str]): List of sources to scrape from
        
        Returns:
            Dict with jobs from all sources and metadata
        """
        if sources is None:
            sources = ['naukri', 'linkedin', 'unstop']
        
        all_jobs = []
        source_stats = {}
        errors = {}
        
        def scrape_source(source: str) -> tuple:
            """Helper function to scrape from a single source"""
            try:
                print(f"Starting {source} scraper...")
                jobs = []
                
                if source.lower() == 'naukri':
                    scraper = NaukriScraper(headless=self.headless)
                    if location:
                        jobs = scraper.scrape_jobs_by_location(keyword, location, max_jobs_per_source)
                    else:
                        jobs = scraper.scrape_jobs(keyword, max_jobs_per_source)
                
                elif source.lower() == 'linkedin':
                    scraper = LinkedInScraper(headless=self.headless)
                    jobs = scraper.scrape_jobs(keyword, location or "", max_jobs_per_source)
                
                elif source.lower() == 'unstop':
                    scraper = UnstopScraper(headless=self.headless)
                    jobs = scraper.scrape_jobs(keyword, category="jobs", max_jobs=max_jobs_per_source)
                
                # Add metadata
                for job in jobs:
                    job['scraped_at'] = datetime.now().isoformat()
                    job['keyword'] = keyword
                
                return (source, jobs, None)
                
            except Exception as e:
                return (source, [], str(e))
        
        # Use ThreadPoolExecutor for parallel scraping
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(sources)) as executor:
            future_to_source = {executor.submit(scrape_source, source): source for source in sources}
            
            for future in concurrent.futures.as_completed(future_to_source):
                source, jobs, error = future.result()
                
                if error:
                    errors[source] = error
                    source_stats[source] = 0
                    print(f"❌ Error scraping from {source}: {error}")
                else:
                    all_jobs.extend(jobs)
                    source_stats[source] = len(jobs)
                    print(f"✅ Successfully scraped {len(jobs)} jobs from {source}")
        
        return {
            'success': True,
            'keyword': keyword,
            'location': location,
            'total_jobs': len(all_jobs),
            'jobs': all_jobs,
            'source_stats': source_stats,
            'errors': errors if errors else None,
            'scraped_at': datetime.now().isoformat()
        }
    
    def scrape_by_domain(
        self,
        domain: str,
        location: Optional[str] = None,
        max_jobs_per_source: int = 10
    ) -> Dict[str, any]:
        """
        Scrape jobs for a specific domain/industry
        
        Args:
            domain (str): Domain/industry (e.g., 'tech', 'design', 'business')
            location (str): Optional location filter
            max_jobs_per_source (int): Max jobs to scrape from each source
        
        Returns:
            Dict with jobs from all sources
        """
        # Map domains to search keywords
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
        
        keyword = domain_keywords.get(domain.lower(), domain)
        
        return self.scrape_all_sources(
            keyword=keyword,
            location=location,
            max_jobs_per_source=max_jobs_per_source
        )
