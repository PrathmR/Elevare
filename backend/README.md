# Elevare Backend API

Backend service for the Elevare AI-driven job matching platform. This service handles resume parsing, AI analysis, and provides RESTful APIs for the frontend.

## Features

- 📄 **Resume Parsing**: Extract text from PDF and DOCX files
- 🤖 **AI Analysis**: Analyze resumes using Google's Gemini AI
- 🔒 **Secure**: Environment-based configuration
- 🚀 **RESTful API**: Clean API endpoints for frontend integration
- ⚡ **Fast**: Optimized for quick response times

## Tech Stack

- **Framework**: Flask 3.0
- **AI Model**: Google Gemini 2.5 Flash
- **Document Processing**: PyMuPDF, python-docx
- **CORS**: Flask-CORS for cross-origin requests

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and add your Google API key:
     ```env
     GOOGLE_API_KEY=your_actual_api_key_here
     ```

## Running the Server

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. The server will start on `http://localhost:5000`

3. Test the health endpoint:
   ```bash
   curl http://localhost:5000/api/health
   ```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns the health status of the API.

**Response**:
```json
{
  "status": "healthy",
  "message": "Backend is running"
}
```

### Upload Resume
```
POST /api/upload-resume
```
Upload and analyze a resume file.

**Request**:
- Content-Type: `multipart/form-data`
- Body: `file` (PDF, DOC, or DOCX)

**Response**:
```json
{
  "success": true,
  "filename": "resume.pdf",
  "analysis": "Detailed AI analysis...",
  "extracted_text": "Extracted resume text..."
}
```

### Analyze Text
```
POST /api/analyze-text
```
Analyze resume text directly without file upload.

**Request**:
```json
{
  "text": "Resume text content..."
}
```

**Response**:
```json
{
  "success": true,
  "analysis": "Detailed AI analysis..."
}
```

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── utils/                # Utility modules
│   ├── __init__.py
│   └── extract_text.py   # Text extraction from documents
├── ai/                   # AI modules
│   ├── __init__.py
│   └── analyze_resume.py # Resume analysis using Gemini AI
└── uploads/              # Temporary file uploads (gitignored)
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input or missing parameters
- **413 Payload Too Large**: File exceeds 10MB limit
- **404 Not Found**: Endpoint doesn't exist
- **500 Internal Server Error**: Server-side errors

## Security Considerations

1. **File Size Limit**: Maximum 10MB per upload
2. **File Type Validation**: Only PDF, DOC, and DOCX allowed
3. **CORS**: Configured for specific frontend origins
4. **Environment Variables**: Sensitive data in `.env` file
5. **Input Validation**: All inputs are validated before processing

## Development

### Adding New Endpoints

1. Create a new route in `app.py`:
   ```python
   @app.route("/api/your-endpoint", methods=["POST"])
   def your_function():
       # Your logic here
       return jsonify({"result": "data"}), 200
   ```

2. Update CORS settings if needed

3. Document the endpoint in this README

### Testing

Test endpoints using curl or Postman:

```bash
# Upload a resume
curl -X POST -F "file=@path/to/resume.pdf" http://localhost:5000/api/upload-resume

# Analyze text
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Your resume text"}' \
  http://localhost:5000/api/analyze-text
```

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY not set"**
   - Ensure `.env` file exists with valid API key
   - Restart the server after adding the key

2. **CORS errors**
   - Check frontend URL in CORS configuration
   - Ensure frontend is running on allowed origin

3. **File upload fails**
   - Check file size (max 10MB)
   - Verify file format (PDF, DOC, DOCX only)
   - Ensure `uploads/` directory exists

4. **Import errors**
   - Activate virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the Elevare platform.

## Support

For issues or questions, please contact the development team.
