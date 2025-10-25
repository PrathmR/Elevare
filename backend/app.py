from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.extract_text import extract_text_from_resume
from ai.analyze_resume import analyze_resume
from ai.extract_candidate_info import extract_candidate_info
from scraper.naukri_scraper import NaukriScraper
from scraper.job_scraper_manager import JobScraperManager
from utils.job_database import JobDatabase
from utils.background_scraper import BackgroundJobScraper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow requests from the frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure upload folder
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB max file size
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Backend is running"}), 200

@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    """
    Upload and analyze resume endpoint - NOW RETURNS SIMPLIFIED CANDIDATE INFO
    Accepts: multipart/form-data with 'file' field
    Returns: JSON with basic candidate information
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only PDF, DOC, and DOCX are allowed"}), 400
        
        # Save file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        print(f"File saved at: {filepath}")
        
        # Extract text from the uploaded resume
        resume_text = extract_text_from_resume(filepath)
        print(f"Extracted Text: {resume_text[:200]}...")
        
        if resume_text == "Unsupported file format.":
            return jsonify({"error": "Unsupported file format"}), 400
        
        # Extract basic candidate information using AI
        candidate_info = extract_candidate_info(resume_text)
        print(f"Candidate Info: {candidate_info}")
        
        # Clean up - optionally delete the file after processing
        # os.remove(filepath)
        
        return jsonify({
            "success": True,
            "filename": file.filename,
            "candidate_info": candidate_info,
            "resume_text": resume_text  # Full text for matching
        }), 200
        
    except Exception as e:
        print(f"Error processing resume: {str(e)}")
        return jsonify({"error": f"Error processing resume: {str(e)}"}), 500

@app.route("/api/analyze-text", methods=["POST"])
def analyze_text():
    """
    Analyze resume text directly without file upload
    Accepts: JSON with 'text' field
    Returns: JSON with analysis results
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
        
        resume_text = data['text']
        
        if not resume_text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        # Analyze the text using the AI model
        analysis_result = analyze_resume(resume_text)
        
        return jsonify({
            "success": True,
            "analysis": analysis_result
        }), 200
        
    except Exception as e:
        print(f"Error analyzing text: {str(e)}")
        return jsonify({"error": f"Error analyzing text: {str(e)}"}), 500

@app.route("/api/scrape-jobs", methods=["POST"])
def scrape_jobs():
    """
    Scrape job listings from Naukri.com
    Accepts: JSON with 'keyword', optional 'location', and optional 'max_jobs'
    Returns: JSON with scraped job listings
    """
    try:
        data = request.get_json()
        
        if not data or 'keyword' not in data:
            return jsonify({"error": "No keyword provided"}), 400
        
        keyword = data['keyword']
        location = data.get('location', None)
        max_jobs = data.get('max_jobs', 20)
        
        # Validate max_jobs
        if not isinstance(max_jobs, int) or max_jobs < 1 or max_jobs > 100:
            return jsonify({"error": "max_jobs must be between 1 and 100"}), 400
        
        # Initialize scraper
        scraper = NaukriScraper(headless=True)
        
        # Scrape jobs
        if location:
            jobs = scraper.scrape_jobs_by_location(keyword, location, max_jobs)
        else:
            jobs = scraper.scrape_jobs(keyword, max_jobs)
        
        return jsonify({
            "success": True,
            "keyword": keyword,
            "location": location,
            "jobs_count": len(jobs),
            "jobs": jobs
        }), 200
        
    except Exception as e:
        print(f"Error scraping jobs: {str(e)}")
        return jsonify({"error": f"Error scraping jobs: {str(e)}"}), 500

@app.route("/api/scrape-all-sources", methods=["POST"])
def scrape_all_sources():
    """
    Scrape jobs from all sources (Naukri, LinkedIn, Unstop) and store in database
    Accepts: JSON with 'keyword', optional 'location', 'max_jobs_per_source', 'sources', 'save_to_db'
    Returns: JSON with scraped job listings
    """
    try:
        data = request.get_json()
        
        if not data or 'keyword' not in data:
            return jsonify({"error": "No keyword provided"}), 400
        
        keyword = data['keyword']
        location = data.get('location', None)
        max_jobs_per_source = data.get('max_jobs_per_source', 10)
        sources = data.get('sources', ['naukri', 'linkedin', 'unstop'])
        save_to_db = data.get('save_to_db', True)
        
        # Validate max_jobs_per_source
        if not isinstance(max_jobs_per_source, int) or max_jobs_per_source < 1 or max_jobs_per_source > 50:
            return jsonify({"error": "max_jobs_per_source must be between 1 and 50"}), 400
        
        # Initialize scraper manager
        scraper_manager = JobScraperManager(headless=True)
        
        # Scrape jobs from all sources
        result = scraper_manager.scrape_all_sources(
            keyword=keyword,
            location=location,
            max_jobs_per_source=max_jobs_per_source,
            sources=sources
        )
        
        # Save to database if requested
        if save_to_db and result['jobs']:
            try:
                db = JobDatabase()
                db_result = db.insert_jobs(result['jobs'])
                result['database'] = db_result
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
                result['database'] = {"success": False, "message": "Database not configured"}
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error scraping jobs: {str(e)}")
        return jsonify({"error": f"Error scraping jobs: {str(e)}"}), 500

@app.route("/api/jobs/search", methods=["GET"])
def search_jobs():
    """
    Search jobs in the database
    Query params: keyword, location, domain, source, limit
    Returns: JSON with job listings from database
    """
    try:
        keyword = request.args.get('keyword')
        location = request.args.get('location')
        domain = request.args.get('domain')
        source = request.args.get('source')
        limit = int(request.args.get('limit', 50))
        
        db = JobDatabase()
        jobs = db.search_jobs(
            keyword=keyword,
            location=location,
            domain=domain,
            source=source,
            limit=limit
        )
        
        return jsonify({
            "success": True,
            "count": len(jobs),
            "jobs": jobs
        }), 200
        
    except Exception as e:
        print(f"Error searching jobs: {str(e)}")
        return jsonify({"error": f"Error searching jobs: {str(e)}"}), 500

@app.route("/api/jobs/domain/<domain>", methods=["GET"])
def get_jobs_by_domain(domain):
    """
    Get jobs filtered by domain
    Returns: JSON with job listings for the specified domain
    """
    try:
        limit = int(request.args.get('limit', 50))
        
        db = JobDatabase()
        jobs = db.get_jobs_by_domain(domain, limit=limit)
        
        return jsonify({
            "success": True,
            "domain": domain,
            "count": len(jobs),
            "jobs": jobs
        }), 200
        
    except Exception as e:
        print(f"Error getting jobs by domain: {str(e)}")
        return jsonify({"error": f"Error getting jobs by domain: {str(e)}"}), 500

@app.route("/api/jobs/recent", methods=["GET"])
def get_recent_jobs():
    """
    Get most recent jobs
    Returns: JSON with recent job listings
    """
    try:
        limit = int(request.args.get('limit', 20))
        
        db = JobDatabase()
        jobs = db.get_recent_jobs(limit=limit)
        
        return jsonify({
            "success": True,
            "count": len(jobs),
            "jobs": jobs
        }), 200
        
    except Exception as e:
        print(f"Error getting recent jobs: {str(e)}")
        return jsonify({"error": f"Error getting recent jobs: {str(e)}"}), 500

@app.route("/api/jobs/stats", methods=["GET"])
def get_job_stats():
    """
    Get job statistics
    Returns: JSON with job statistics
    """
    try:
        db = JobDatabase()
        stats = db.get_job_stats()
        
        return jsonify({
            "success": True,
            "stats": stats
        }), 200
        
    except Exception as e:
        print(f"Error getting job stats: {str(e)}")
        return jsonify({"error": f"Error getting job stats: {str(e)}"}), 500

@app.route("/api/scrape-and-recommend", methods=["POST"])
def scrape_and_recommend():
    """
    Get job recommendations from DATABASE based on resume analysis
    NO LONGER SCRAPES - uses pre-populated database
    Accepts: JSON with 'resume_skills', 'domain', optional 'location'
    Returns: JSON with matched jobs from database
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        resume_skills = data.get('resume_skills', [])
        domain = data.get('domain', None)
        location = data.get('location', None)
        
        # Get jobs from database (no scraping)
        db = JobDatabase()
        
        # Search with domain as keyword if available
        keyword = domain if domain and domain != "Not Found" else None
        
        jobs = db.search_jobs(
            keyword=keyword,
            location=location,
            limit=100  # Get more jobs for better matching
        )
        
        # Calculate match scores based on skills
        if resume_skills:
            for job in jobs:
                # Calculate match score based on skills in job description
                job_text = f"{job.get('title', '')} {job.get('description', '')}".lower()
                matching_skills = [skill for skill in resume_skills if skill.lower() in job_text]
                match_score = (len(matching_skills) / len(resume_skills)) * 100 if resume_skills else 0
                job['match_score'] = round(match_score, 2)
                job['matching_skills'] = matching_skills
            
            # Sort by match score and filter jobs with at least some match
            jobs = [job for job in jobs if job.get('match_score', 0) > 0]
            jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
            
            # Limit to top 50 matches
            jobs = jobs[:50]
        
        return jsonify({
            "success": True,
            "total_jobs": len(jobs),
            "jobs": jobs,
            "source": "database"
        }), 200
        
    except Exception as e:
        print(f"Error in scrape and recommend: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route("/api/scrape-background", methods=["POST"])
def scrape_background():
    """
    Start background job scraping to populate database
    Accepts: JSON with optional 'keywords' list and 'max_jobs_per_source'
    Returns: JSON with scraping status
    """
    try:
        data = request.get_json() or {}
        
        keywords = data.get('keywords', None)  # None = use popular keywords
        max_jobs_per_source = data.get('max_jobs_per_source', 5)
        run_async = data.get('async', False)  # Run in background thread
        
        scraper = BackgroundJobScraper(headless=True)
        
        if run_async:
            # Start scraping in background
            scraper.scrape_async(keywords=keywords, max_jobs_per_source=max_jobs_per_source)
            return jsonify({
                "success": True,
                "message": "Background scraping started",
                "keywords_count": len(keywords) if keywords else len(scraper.POPULAR_KEYWORDS)
            }), 202  # 202 Accepted
        else:
            # Run synchronously (will block)
            if keywords:
                results = []
                for keyword in keywords:
                    result = scraper.scrape_keyword(keyword, max_jobs_per_source)
                    results.append(result)
                
                total_jobs = sum(r.get('total_jobs', 0) for r in results if r.get('success'))
                total_saved = sum(r.get('database', {}).get('inserted_count', 0) for r in results)
                
                return jsonify({
                    "success": True,
                    "total_jobs_scraped": total_jobs,
                    "total_jobs_saved": total_saved,
                    "results": results
                }), 200
            else:
                # Scrape all popular keywords
                result = scraper.scrape_all_popular_keywords(max_jobs_per_source)
                return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in background scraping: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"error": "File too large. Maximum size is 10MB"}), 413

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
