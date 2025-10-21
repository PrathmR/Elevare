from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.extract_text import extract_text_from_resume
from ai.analyze_resume import analyze_resume
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
    Upload and analyze resume endpoint
    Accepts: multipart/form-data with 'file' field
    Returns: JSON with analysis results
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
        
        # Analyze the extracted text using the AI model
        analysis_result = analyze_resume(resume_text)
        print(f"AI Analysis Result: {analysis_result[:200]}...")
        
        # Clean up - optionally delete the file after processing
        # os.remove(filepath)
        
        return jsonify({
            "success": True,
            "filename": file.filename,
            "analysis": analysis_result,
            "extracted_text": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
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
