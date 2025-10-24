from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from typing import List, Dict, Optional


class NaukriScraper:
    """
    A class to scrape job listings from Naukri.com
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize the Naukri scraper
        
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
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    
    def _close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_jobs(self, keyword: str = "python-developer", max_jobs: int = 20) -> List[Dict[str, str]]:
        """
        Scrape job listings from Naukri.com
        
        Args:
            keyword (str): Job search keyword (e.g., 'python-developer', 'java-developer')
            max_jobs (int): Maximum number of jobs to scrape
        
        Returns:
            List[Dict]: List of job dictionaries with title, company, and location
        """
        try:
            self._setup_driver()
            
            # Construct search URL
            search_url = f"https://www.naukri.com/{keyword}-jobs"
            print(f"Scraping jobs from: {search_url}")
            
            self.driver.get(search_url)
            
            # Wait for page to load
            time.sleep(10)
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")
            
            jobs_data = []
            print(f"Found {len(job_cards)} job cards.")
            
            for idx, job in enumerate(job_cards):
                if idx >= max_jobs:
                    break
                
                try:
                    # Job Title
                    row1 = job.find('div', class_="row1")
                    title = row1.a.text.strip() if row1 and row1.a else "N/A"
                    
                    # Job URL
                    job_url = row1.a['href'] if row1 and row1.a and row1.a.has_attr('href') else "N/A"
                    
                    # Company Name
                    row2 = job.find('div', class_="row2")
                    company = row2.span.a.text.strip() if row2 and row2.span and row2.span.a else "N/A"
                    
                    # Location
                    row3 = job.find('div', class_="row3")
                    location = "N/A"
                    if row3:
                        job_details = row3.find('div', class_="job-details")
                        if job_details:
                            location_elem = job_details.find('span', class_="loc-wrap ver-line")
                            if location_elem and location_elem.span and location_elem.span.span:
                                location = location_elem.span.span.text.strip()
                    
                    # Experience
                    experience = "N/A"
                    if row3:
                        job_details = row3.find('div', class_="job-details")
                        if job_details:
                            exp_elem = job_details.find('span', class_="exp-wrap ver-line")
                            if exp_elem and exp_elem.span:
                                experience = exp_elem.span.text.strip()
                    
                    # Salary
                    salary = "N/A"
                    if row3:
                        job_details = row3.find('div', class_="job-details")
                        if job_details:
                            salary_elem = job_details.find('span', class_="sal-wrap ver-line")
                            if salary_elem and salary_elem.span:
                                salary = salary_elem.span.text.strip()
                    
                    # Job Description (snippet)
                    description = "N/A"
                    desc_elem = job.find('div', class_="job-desc")
                    if desc_elem:
                        description = desc_elem.text.strip()
                    
                    job_data = {
                        'title': title,
                        'company': company,
                        'location': location,
                        'experience': experience,
                        'salary': salary,
                        'description': description,
                        'url': job_url
                    }
                    
                    jobs_data.append(job_data)
                    print(f"Scraped: {title} at {company}")
                    
                except Exception as e:
                    print(f"Error parsing a job: {e}")
                    continue
            
            return jobs_data
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            raise
        
        finally:
            self._close_driver()
    
    def scrape_jobs_by_location(self, keyword: str, location: str, max_jobs: int = 20) -> List[Dict[str, str]]:
        """
        Scrape job listings from Naukri.com filtered by location
        
        Args:
            keyword (str): Job search keyword
            location (str): Location filter (e.g., 'bangalore', 'mumbai')
            max_jobs (int): Maximum number of jobs to scrape
        
        Returns:
            List[Dict]: List of job dictionaries
        """
        try:
            self._setup_driver()
            
            # Construct search URL with location
            search_url = f"https://www.naukri.com/{keyword}-jobs-in-{location}"
            print(f"Scraping jobs from: {search_url}")
            
            self.driver.get(search_url)
            time.sleep(10)
            
            # Use the same parsing logic
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")
            
            jobs_data = []
            
            for idx, job in enumerate(job_cards):
                if idx >= max_jobs:
                    break
                
                try:
                    row1 = job.find('div', class_="row1")
                    title = row1.a.text.strip() if row1 and row1.a else "N/A"
                    job_url = row1.a['href'] if row1 and row1.a and row1.a.has_attr('href') else "N/A"
                    
                    row2 = job.find('div', class_="row2")
                    company = row2.span.a.text.strip() if row2 and row2.span and row2.span.a else "N/A"
                    
                    row3 = job.find('div', class_="row3")
                    loc = "N/A"
                    experience = "N/A"
                    salary = "N/A"
                    
                    if row3:
                        job_details = row3.find('div', class_="job-details")
                        if job_details:
                            location_elem = job_details.find('span', class_="loc-wrap ver-line")
                            if location_elem and location_elem.span and location_elem.span.span:
                                loc = location_elem.span.span.text.strip()
                            
                            exp_elem = job_details.find('span', class_="exp-wrap ver-line")
                            if exp_elem and exp_elem.span:
                                experience = exp_elem.span.text.strip()
                            
                            salary_elem = job_details.find('span', class_="sal-wrap ver-line")
                            if salary_elem and salary_elem.span:
                                salary = salary_elem.span.text.strip()
                    
                    description = "N/A"
                    desc_elem = job.find('div', class_="job-desc")
                    if desc_elem:
                        description = desc_elem.text.strip()
                    
                    job_data = {
                        'title': title,
                        'company': company,
                        'location': loc,
                        'experience': experience,
                        'salary': salary,
                        'description': description,
                        'url': job_url
                    }
                    
                    jobs_data.append(job_data)
                    
                except Exception as e:
                    print(f"Error parsing a job: {e}")
                    continue
            
            return jobs_data
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            raise
        
        finally:
            self._close_driver()
