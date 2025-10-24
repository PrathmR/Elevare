from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from typing import List, Dict


class LinkedInScraper:
    """
    A class to scrape job listings from LinkedIn
    Note: LinkedIn has strict anti-scraping measures. This is a basic implementation.
    For production, consider using LinkedIn's official API.
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize the LinkedIn scraper
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        self.headless = headless
        self.driver = None
    
    def _setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    
    def _close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_jobs(self, keyword: str = "software developer", location: str = "", max_jobs: int = 20) -> List[Dict[str, str]]:
        """
        Scrape job listings from LinkedIn
        
        Args:
            keyword (str): Job search keyword
            location (str): Location filter
            max_jobs (int): Maximum number of jobs to scrape
        
        Returns:
            List[Dict]: List of job dictionaries
        """
        try:
            self._setup_driver()
            
            # Construct search URL
            keyword_encoded = keyword.replace(' ', '%20')
            location_encoded = location.replace(' ', '%20') if location else ""
            
            if location:
                search_url = f"https://www.linkedin.com/jobs/search?keywords={keyword_encoded}&location={location_encoded}&f_TPR=r86400"
            else:
                search_url = f"https://www.linkedin.com/jobs/search?keywords={keyword_encoded}&f_TPR=r86400"
            
            print(f"Scraping jobs from: {search_url}")
            
            self.driver.get(search_url)
            time.sleep(5)  # Wait for page to load
            
            # Scroll to load more jobs
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            job_cards = soup.find_all("div", class_="base-card")
            
            jobs_data = []
            print(f"Found {len(job_cards)} job cards.")
            
            for idx, job in enumerate(job_cards):
                if idx >= max_jobs:
                    break
                
                try:
                    # Job Title
                    title_elem = job.find('h3', class_="base-search-card__title")
                    title = title_elem.text.strip() if title_elem else "N/A"
                    
                    # Company Name
                    company_elem = job.find('h4', class_="base-search-card__subtitle")
                    company = company_elem.text.strip() if company_elem else "N/A"
                    
                    # Location
                    location_elem = job.find('span', class_="job-search-card__location")
                    loc = location_elem.text.strip() if location_elem else "N/A"
                    
                    # Job URL
                    link_elem = job.find('a', class_="base-card__full-link")
                    job_url = link_elem['href'] if link_elem and link_elem.has_attr('href') else "N/A"
                    
                    # Posted date
                    time_elem = job.find('time')
                    posted_date = time_elem.text.strip() if time_elem else "N/A"
                    
                    job_data = {
                        'title': title,
                        'company': company,
                        'location': loc,
                        'experience': "N/A",  # LinkedIn doesn't show this in search results
                        'salary': "N/A",  # LinkedIn doesn't show this in search results
                        'description': f"Job posted {posted_date}",
                        'url': job_url,
                        'source': 'LinkedIn'
                    }
                    
                    jobs_data.append(job_data)
                    print(f"Scraped: {title} at {company}")
                    
                except Exception as e:
                    print(f"Error parsing a job: {e}")
                    continue
            
            return jobs_data
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            return []
        
        finally:
            self._close_driver()
