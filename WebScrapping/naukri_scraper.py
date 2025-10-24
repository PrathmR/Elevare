from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import csv
import os

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (comment out to see browser)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Anti-detection

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open Naukri search page (change 'python-developer' to your keyword, e.g., 'java-developer')
search_url = "https://www.naukri.com/python-developer-jobs"
driver.get(search_url)

# Wait for page to load (Naukri uses JS, so longer wait)
time.sleep(10)

# Parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

data = []
print(f"Found {len(job_cards)} job cards.")

for job in job_cards:
    try:
        # Job Title
        row1 = job.find('div', class_="row1")
        title = row1.a.text.strip() if row1 and row1.a else "N/A"
        
        # Company Name
        row2 = job.find('div', class_="row2")
        company = row2.span.a.text.strip() if row2 and row2.span and row2.span.a else "N/A"
        
        # Location
        row3 = job.find('div', class_="row3")
        if row3:
            job_details = row3.find('div', class_="job-details")
            if job_details:
                location_elem = job_details.find('span', class_="loc-wrap ver-line")
                location = location_elem.span.span.text.strip() if location_elem and location_elem.span and location_elem.span.span else "N/A"
            else:
                location = "N/A"
        else:
            location = "N/A"
        
        job_data = {'Title': title, 'Company': company, 'Location': location}
        data.append(job_data)
        print(f"Title: {title}, Company: {company}, Location: {location}")
    except Exception as e:
        print(f"Error parsing a job: {e}")
        continue

# Save to CSV (overwrites if exists; change to 'a' mode to append)
csv_filename = 'naukri jobs.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
    if data:
        writer = csv.DictWriter(f, fieldnames=['Title', 'Company', 'Location'])
        writer.writeheader()
        writer.writerows(data)
        print(f"\nData saved to {csv_filename} ({len(data)} jobs).")
    else:
        print("No data found—check URL or selectors.")

# Close the browser
driver.quit()