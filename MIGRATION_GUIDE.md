# Migration Guide - Project Restructuring

This document explains the changes made to restructure your Elevare project and how to work with the new structure.

## 📋 What Changed?

### Before (Old Structure)
```
Codes/
├── Frontend/          # React frontend
└── ResumeParser/      # Flask backend (standalone)
```

### After (New Structure)
```
Codes/
├── frontend/          # React frontend (renamed, integrated)
├── backend/           # Flask backend (restructured)
├── ResumeParser/      # Original (can be archived/deleted)
└── Documentation files
```

## 🔄 Key Changes

### 1. Backend Restructuring

**Old Location**: `ResumeParser/`
**New Location**: `backend/`

#### Changes Made:
- ✅ **RESTful API**: Converted from template-based to JSON API
- ✅ **CORS Support**: Added Flask-CORS for frontend communication
- ✅ **Error Handling**: Comprehensive error responses
- ✅ **File Validation**: Enhanced security with file type/size checks
- ✅ **Environment Config**: Proper `.env` setup with examples

#### File Mapping:
| Old File | New File | Changes |
|----------|----------|---------|
| `ResumeParser/app.py` | `backend/app.py` | Converted to REST API, added CORS |
| `ResumeParser/utils/extract_text.py` | `backend/utils/extract_text.py` | Added error handling |
| `ResumeParser/ai/analyze_resume.py` | `backend/ai/analyze_resume.py` | Improved error handling |
| `ResumeParser/requirements.txt` | `backend/requirements.txt` | Added flask-cors, python-dotenv |
| N/A | `backend/.env.example` | New environment template |
| N/A | `backend/README.md` | New comprehensive documentation |

### 2. Frontend Integration

**Location**: `frontend/` (renamed from `Frontend/`)

#### New Features:
- ✅ **API Client**: New `src/lib/api.ts` for backend communication
- ✅ **Resume Upload**: Integrated with backend API
- ✅ **Analysis Display**: Beautiful dialog showing AI results
- ✅ **Environment Config**: Proper `.env` setup
- ✅ **Error Handling**: User-friendly error messages

#### New Files:
| File | Purpose |
|------|---------|
| `frontend/src/lib/api.ts` | Backend API client |
| `frontend/.env.example` | Environment template |
| Updated `frontend/src/pages/UploadResume.tsx` | Backend integration |

### 3. Documentation

New comprehensive documentation added:

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `SUPABASE_SETUP_GUIDE.md` | Step-by-step Supabase setup |
| `QUICK_START.md` | Quick setup guide |
| `MIGRATION_GUIDE.md` | This file |
| `backend/README.md` | Backend API documentation |
| Updated `frontend/README.md` | Frontend setup guide |

## 🚀 Migration Steps

### If You're Starting Fresh

1. **Use the new structure**:
   - Work in `backend/` for backend code
   - Work in `frontend/` for frontend code

2. **Follow the setup guides**:
   - See `QUICK_START.md` for fastest setup
   - See `README.md` for detailed documentation

### If You Have Existing Work in ResumeParser

1. **Backup your work**:
   ```bash
   # Create a backup of your old code
   xcopy ResumeParser ResumeParser_backup /E /I
   ```

2. **Migrate custom changes**:
   - If you modified `app.py`, merge changes into `backend/app.py`
   - If you added new AI features, update `backend/ai/analyze_resume.py`
   - If you added utilities, add them to `backend/utils/`

3. **Update environment variables**:
   ```bash
   # Copy your .env from ResumeParser to backend
   copy ResumeParser\.env backend\.env
   ```

4. **Test the new backend**:
   ```bash
   cd backend
   python app.py
   ```

5. **Archive the old code** (optional):
   ```bash
   # Rename to indicate it's archived
   rename ResumeParser ResumeParser_OLD
   ```

## 🔧 Configuration Changes

### Backend Environment Variables

**Old** (ResumeParser/.env):
```env
GOOGLE_API_KEY=xxx
```

**New** (backend/.env):
```env
GOOGLE_API_KEY=xxx
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend Environment Variables

**Old** (Frontend/.env) - if existed:
```env
VITE_SUPABASE_URL=xxx
VITE_SUPABASE_PUBLISHABLE_KEY=xxx
```

**New** (frontend/.env):
```env
VITE_SUPABASE_URL=xxx
VITE_SUPABASE_PUBLISHABLE_KEY=xxx
VITE_API_BASE_URL=http://localhost:5000/api
```

## 📡 API Changes

### Old Endpoint (Template-based)
```python
@app.route("/", methods=["GET", "POST"])
def index():
    # Returns HTML template
    return render_template("index.html", result=result)
```

### New Endpoints (REST API)

```python
# Health check
GET /api/health
Response: {"status": "healthy", "message": "Backend is running"}

# Upload resume
POST /api/upload-resume
Content-Type: multipart/form-data
Response: {
  "success": true,
  "filename": "resume.pdf",
  "analysis": "...",
  "extracted_text": "..."
}

# Analyze text
POST /api/analyze-text
Content-Type: application/json
Body: {"text": "..."}
Response: {
  "success": true,
  "analysis": "..."
}
```

## 🎯 Benefits of New Structure

### 1. Separation of Concerns
- **Backend**: Pure API, no HTML templates
- **Frontend**: Modern React SPA
- **Clear boundaries**: Easy to maintain and scale

### 2. Better Development Experience
- **Hot Reload**: Both frontend and backend support live reloading
- **Type Safety**: TypeScript in frontend
- **API Client**: Centralized API calls in `frontend/src/lib/api.ts`

### 3. Deployment Ready
- **Backend**: Can deploy to any Python hosting (Heroku, Railway, Render)
- **Frontend**: Can deploy to any static hosting (Vercel, Netlify)
- **Separate scaling**: Scale frontend and backend independently

### 4. Enhanced Security
- **Environment Variables**: Proper separation of secrets
- **CORS**: Controlled cross-origin access
- **File Validation**: Enhanced upload security
- **Input Validation**: All inputs validated

### 5. Better Documentation
- **Comprehensive guides**: Multiple documentation files
- **API documentation**: Clear endpoint specifications
- **Setup guides**: Step-by-step instructions

## 🔍 Code Comparison

### Resume Upload - Before vs After

**Before** (ResumeParser/app.py):
```python
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            resume_text = extract_text_from_resume(filepath)
            result = analyze_resume(resume_text)
    return render_template("index.html", result=result)
```

**After** (backend/app.py):
```python
@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400
        
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        
        resume_text = extract_text_from_resume(filepath)
        analysis_result = analyze_resume(resume_text)
        
        return jsonify({
            "success": True,
            "filename": file.filename,
            "analysis": analysis_result,
            "extracted_text": resume_text[:500] + "..."
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Frontend Integration - New

**New** (frontend/src/lib/api.ts):
```typescript
export async function uploadResume(file: File): Promise<UploadResumeResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload-resume`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.error || 'Failed to upload resume');
  }

  return response.json();
}
```

## 📝 What to Keep from Old Structure

You can safely **archive or delete** the `ResumeParser/` directory after migration, but keep:

- ✅ Your `.env` file (migrate to `backend/.env`)
- ✅ Any custom modifications you made
- ✅ Uploaded resumes in `Uploaded_Resumes/` (if needed)

## ✅ Migration Checklist

- [ ] Backed up old `ResumeParser/` directory
- [ ] Set up `backend/.env` with Google API key
- [ ] Set up `frontend/.env` with Supabase credentials
- [ ] Installed backend dependencies (`pip install -r requirements.txt`)
- [ ] Installed frontend dependencies (`npm install`)
- [ ] Tested backend API (http://localhost:5000/api/health)
- [ ] Tested frontend (http://localhost:5173)
- [ ] Tested resume upload functionality
- [ ] Verified AI analysis works
- [ ] Archived old `ResumeParser/` directory

## 🆘 Need Help?

If you encounter issues during migration:

1. **Check the logs**: Both terminals show detailed error messages
2. **Verify environment variables**: Most issues come from missing `.env` values
3. **Review documentation**: See `README.md` and `QUICK_START.md`
4. **Check file paths**: Ensure you're in the correct directory

## 📞 Support

For migration-specific questions:
- Review this guide thoroughly
- Check the `README.md` for general setup
- See `QUICK_START.md` for quick troubleshooting

---

**Migration completed successfully? You're ready to build amazing features! 🎉**
