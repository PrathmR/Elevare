"""
Test script for the Naukri scraper integration
Run this to verify the scraper is working correctly
"""

from scraper.naukri_scraper import NaukriScraper
import json


def test_basic_scraping():
    """Test basic job scraping"""
    print("=" * 60)
    print("Testing Basic Job Scraping")
    print("=" * 60)
    
    scraper = NaukriScraper(headless=True)
    
    try:
        print("\n🔍 Scraping Python Developer jobs...")
        jobs = scraper.scrape_jobs('python-developer', max_jobs=5)
        
        print(f"\n✅ Successfully scraped {len(jobs)} jobs!")
        
        if jobs:
            print("\n📋 Sample Job:")
            print(json.dumps(jobs[0], indent=2))
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def test_location_scraping():
    """Test job scraping with location filter"""
    print("\n" + "=" * 60)
    print("Testing Location-Based Job Scraping")
    print("=" * 60)
    
    scraper = NaukriScraper(headless=True)
    
    try:
        print("\n🔍 Scraping Java Developer jobs in Bangalore...")
        jobs = scraper.scrape_jobs_by_location('java-developer', 'bangalore', max_jobs=5)
        
        print(f"\n✅ Successfully scraped {len(jobs)} jobs!")
        
        if jobs:
            print("\n📋 Sample Job:")
            print(json.dumps(jobs[0], indent=2))
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n🚀 Starting Naukri Scraper Tests\n")
    
    # Test 1: Basic scraping
    test1_passed = test_basic_scraping()
    
    # Test 2: Location-based scraping
    test2_passed = test_location_scraping()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Basic Scraping: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Location Scraping: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The scraper is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
