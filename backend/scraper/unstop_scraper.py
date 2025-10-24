from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from typing import List, Dict


class UnstopScraper:
    """
    A class to scrape job/opportunity listings from Unstop (formerly Dare2Compete)
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize the Unstop scraper
        
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
    
    def scrape_jobs(self, keyword: str = "software", category: str = "jobs", max_jobs: int = 20) -> List[Dict[str, str]]:
        """
        Scrape job/opportunity listings from Unstop
        
        Args:
            keyword (str): Search keyword
            category (str): Category - 'jobs', 'internships', 'competitions'
            max_jobs (int): Maximum number of jobs to scrape
        
        Returns:
            List[Dict]: List of job dictionaries
        """
        try:
            self._setup_driver()
            
            # Construct search URL based on category
            if category == "jobs":
                search_url = f"https://unstop.com/jobs?search={keyword}"
            elif category == "internships":
                search_url = f"https://unstop.com/internships?search={keyword}"
            else:
                search_url = f"https://unstop.com/competitions?search={keyword}"
            
            print(f"Scraping from: {search_url}")
            
            self.driver.get(search_url)
            time.sleep(8)  # Wait for page to load
            
            # Scroll to load more content
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Unstop uses different class names, adjust as needed
            job_cards = soup.find_all("div", class_="opportunity_card") or \
                       soup.find_all("div", class_="card") or \
                       soup.find_all("article")
            
            jobs_data = []
            print(f"Found {len(job_cards)} opportunity cards.")
            
            for idx, job in enumerate(job_cards):
                if idx >= max_jobs:
                    break
                
                try:
                    # Try to extract title
                    title_elem = job.find('h3') or job.find('h2') or job.find('h4')
                    title = title_elem.text.strip() if title_elem else "N/A"
                    
                    # Skip if no title found
                    if title == "N/A":
                        continue
                    
                    # Try to extract company/organizer
                    company_elem = job.find('p', class_="company") or \
                                  job.find('div', class_="organizer") or \
                                  job.find('span', class_="company-name")
                    company = company_elem.text.strip() if company_elem else "Unstop"
                    
                    # Try to extract location
                    location_elem = job.find('span', class_="location") or \
                                   job.find('div', class_="location")
                    location = location_elem.text.strip() if location_elem else "Remote/Various"
                    
                    # Try to extract URL
                    link_elem = job.find('a', href=True)
                    job_url = link_elem['href'] if link_elem else "N/A"
                    if job_url != "N/A" and not job_url.startswith('http'):
                        job_url = f"https://unstop.com{job_url}"
                    
                    # Try to extract deadline or posted date
                    deadline_elem = job.find('span', class_="deadline") or \
                                   job.find('div', class_="deadline")
                    deadline = deadline_elem.text.strip() if deadline_elem else "N/A"
                    
                    # Try to extract stipend/salary
                    stipend_elem = job.find('span', class_="stipend") or \
                                  job.find('div', class_="salary")
                    stipend = stipend_elem.text.strip() if stipend_elem else "N/A"
                    
                    job_data = {
                        'title': title,
                        'company': company,
                        'location': location,
                        'experience': "N/A",
                        'salary': stipend,
                        'description': f"Deadline: {deadline}" if deadline != "N/A" else "Check Unstop for details",
                        'url': job_url,
                        'source': 'Unstop'
                    }
                    
                    jobs_data.append(job_data)
                    print(f"Scraped: {title} at {company}")
                    
                except Exception as e:
                    print(f"Error parsing an opportunity: {e}")
                    continue
            
            return jobs_data
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            return []
        
        finally:
            self._close_driver()
    
    def scrape_internships(self, keyword: str = "software", max_jobs: int = 20) -> List[Dict[str, str]]:
        """Convenience method to scrape internships"""
        return self.scrape_jobs(keyword, category="internships", max_jobs=max_jobs)
    
    def scrape_competitions(self, keyword: str = "coding", max_jobs: int = 20) -> List[Dict[str, str]]:
        """Convenience method to scrape competitions"""
        return self.scrape_jobs(keyword, category="competitions", max_jobs=max_jobs)
