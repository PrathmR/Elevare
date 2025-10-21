# Setup Checklist - Elevare Platform

Use this checklist to ensure your Elevare platform is properly configured and running.

## 📋 Pre-Setup Requirements

### System Requirements
- [ ] **Node.js** installed (v16+)
  - Check: `node --version`
  - Download: https://nodejs.org/
  
- [ ] **Python** installed (v3.8+)
  - Check: `python --version`
  - Download: https://python.org/
  
- [ ] **Git** installed (optional, for version control)
  - Check: `git --version`

### Account Setup
- [ ] **Supabase Account** created
  - Sign up: https://supabase.com
  
- [ ] **Google Gemini API Key** obtained
  - Get key: https://makersuite.google.com/app/apikey

---

## 🔧 Backend Setup

### 1. Environment Setup
- [ ] Navigate to `backend/` directory
- [ ] Create Python virtual environment
  ```bash
  python -m venv venv
  ```
- [ ] Activate virtual environment
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- [ ] Verify activation (should see `(venv)` in terminal)

### 2. Dependencies
- [ ] Install Python packages
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Verify installation completed without errors

### 3. Environment Variables
- [ ] Copy `.env.example` to `.env`
  ```bash
  copy .env.example .env
  ```
- [ ] Open `backend/.env` in text editor
- [ ] Add Google Gemini API key:
  ```env
  GOOGLE_API_KEY=your_actual_api_key_here
  ```
- [ ] Save the file

### 4. Test Backend
- [ ] Start the Flask server
  ```bash
  python app.py
  ```
- [ ] Verify server starts without errors
- [ ] Check console shows: `Running on http://127.0.0.1:5000`
- [ ] Test health endpoint in browser: http://localhost:5000/api/health
- [ ] Should see: `{"status":"healthy","message":"Backend is running"}`

### 5. Backend Verification
- [ ] No error messages in console
- [ ] Can access http://localhost:5000/api/health
- [ ] `uploads/` directory created automatically
- [ ] Keep this terminal window open

---

## 🎨 Frontend Setup

### 1. Environment Setup
- [ ] Open a **NEW terminal window**
- [ ] Navigate to `frontend/` directory
- [ ] Verify `package.json` exists

### 2. Dependencies
- [ ] Install npm packages
  ```bash
  npm install
  ```
- [ ] Wait for installation to complete (may take 2-3 minutes)
- [ ] Verify no critical errors

### 3. Environment Variables
- [ ] Copy `.env.example` to `.env`
  ```bash
  copy .env.example .env
  ```
- [ ] Open `frontend/.env` in text editor
- [ ] Add Supabase credentials:
  ```env
  VITE_SUPABASE_URL=https://your-project-id.supabase.co
  VITE_SUPABASE_PUBLISHABLE_KEY=your_anon_public_key_here
  VITE_API_BASE_URL=http://localhost:5000/api
  ```
- [ ] Save the file

### 4. Test Frontend
- [ ] Start the development server
  ```bash
  npm run dev
  ```
- [ ] Verify server starts without errors
- [ ] Check console shows: `Local: http://localhost:5173/`
- [ ] Open browser to http://localhost:5173
- [ ] Should see Elevare landing page

### 5. Frontend Verification
- [ ] No error messages in console
- [ ] Landing page loads correctly
- [ ] Can navigate to different pages
- [ ] UI elements render properly
- [ ] Keep this terminal window open

---

## 🔗 Supabase Configuration

### 1. Project Setup
- [ ] Log in to Supabase dashboard
- [ ] Create new project (if not already created)
- [ ] Wait for project provisioning (2-3 minutes)
- [ ] Project status shows "Active"

### 2. Get API Credentials
- [ ] Go to Project Settings → API
- [ ] Copy **Project URL**
- [ ] Copy **anon public** key
- [ ] Add both to `frontend/.env`

### 3. Authentication Setup
- [ ] Go to Authentication → Providers
- [ ] Verify Email provider is enabled
- [ ] (Optional) Enable additional providers (Google, GitHub)
- [ ] Go to Authentication → URL Configuration
- [ ] Add redirect URL: `http://localhost:5173`

### 4. Database Setup (Optional but Recommended)
- [ ] Go to Table Editor
- [ ] Create `profiles` table (see SUPABASE_SETUP_GUIDE.md)
- [ ] Create `resumes` table
- [ ] Create `jobs` table
- [ ] Create `job_applications` table
- [ ] Enable Row Level Security (RLS) on tables

### 5. Storage Setup (Optional)
- [ ] Go to Storage
- [ ] Create new bucket named `resumes`
- [ ] Set bucket to Private
- [ ] Add storage policies (see SUPABASE_SETUP_GUIDE.md)

---

## ✅ Functionality Testing

### 1. Authentication
- [ ] Open http://localhost:5173
- [ ] Click "Sign Up"
- [ ] Create a test account
- [ ] Verify email sent (check spam folder)
- [ ] Confirm email (if required)
- [ ] Log in with test account
- [ ] Redirected to Dashboard

### 2. Navigation
- [ ] Click "Dashboard" - loads correctly
- [ ] Click "Jobs" - loads correctly
- [ ] Click "My Jobs" - loads correctly
- [ ] Click "Domains" - loads correctly
- [ ] Click "Upload Resume" - loads correctly
- [ ] All navigation links work

### 3. Resume Upload
- [ ] Go to "Upload Resume" page
- [ ] Click upload area or drag a resume file
- [ ] File should be PDF, DOC, or DOCX
- [ ] File size under 10MB
- [ ] Click "Upload & Analyze Resume"
- [ ] See loading spinner
- [ ] Wait for analysis (10-30 seconds)
- [ ] Analysis dialog appears with results

### 4. Resume Analysis Results
- [ ] Analysis contains multiple sections:
  - [ ] Summary of Candidate
  - [ ] Strengths
  - [ ] Weaknesses & Gaps
  - [ ] ATS Score
  - [ ] Suggested Improvements
  - [ ] Interview Questions
  - [ ] Course Recommendations
- [ ] Can scroll through results
- [ ] "Close" button works
- [ ] "View Recommended Jobs" button works

### 5. Backend API
- [ ] Test health endpoint: http://localhost:5000/api/health
- [ ] Returns JSON response
- [ ] No CORS errors in browser console
- [ ] Backend logs show requests

---

## 🐛 Troubleshooting Checklist

### Backend Issues
- [ ] Virtual environment is activated
- [ ] All dependencies installed successfully
- [ ] `.env` file exists in `backend/` directory
- [ ] `GOOGLE_API_KEY` is set correctly
- [ ] No syntax errors in Python files
- [ ] Port 5000 is not in use by another application
- [ ] Firewall allows localhost connections

### Frontend Issues
- [ ] All npm packages installed successfully
- [ ] `.env` file exists in `frontend/` directory
- [ ] Supabase credentials are correct
- [ ] No extra spaces in `.env` values
- [ ] Backend is running on port 5000
- [ ] `VITE_API_BASE_URL` points to correct backend
- [ ] Browser console shows no errors
- [ ] Restarted dev server after changing `.env`

### Supabase Issues
- [ ] Project is active and provisioned
- [ ] API credentials copied correctly
- [ ] Email authentication is enabled
- [ ] Redirect URLs configured
- [ ] No typos in environment variables
- [ ] Supabase dashboard shows no errors

### Resume Upload Issues
- [ ] File is correct format (PDF, DOC, DOCX)
- [ ] File size is under 10MB
- [ ] Backend is running and accessible
- [ ] Google API key is valid and has quota
- [ ] No errors in backend console
- [ ] Network tab shows successful API calls

---

## 📊 Performance Checklist

### Backend Performance
- [ ] Server starts in under 5 seconds
- [ ] Health endpoint responds instantly
- [ ] Resume upload completes in under 30 seconds
- [ ] No memory leaks or warnings
- [ ] Logs are clear and informative

### Frontend Performance
- [ ] Page loads in under 3 seconds
- [ ] Navigation is smooth
- [ ] No layout shifts
- [ ] Images load properly
- [ ] Responsive on different screen sizes

---

## 🔒 Security Checklist

### Environment Security
- [ ] `.env` files are in `.gitignore`
- [ ] No credentials committed to Git
- [ ] API keys are valid and active
- [ ] Using environment variables for all secrets

### Application Security
- [ ] File upload validates file types
- [ ] File size limits enforced (10MB)
- [ ] CORS configured properly
- [ ] Supabase RLS enabled (if using database)
- [ ] Authentication working correctly

---

## 📚 Documentation Review

- [ ] Read `README.md` - Main documentation
- [ ] Read `QUICK_START.md` - Quick setup guide
- [ ] Read `SUPABASE_SETUP_GUIDE.md` - Supabase details
- [ ] Read `backend/README.md` - Backend API docs
- [ ] Read `frontend/README.md` - Frontend details
- [ ] Read `MIGRATION_GUIDE.md` - If migrating from old structure

---

## 🎯 Final Verification

### Both Servers Running
- [ ] Backend terminal shows no errors
- [ ] Frontend terminal shows no errors
- [ ] Backend accessible at http://localhost:5000
- [ ] Frontend accessible at http://localhost:5173

### Core Features Working
- [ ] Can create an account
- [ ] Can log in
- [ ] Can navigate all pages
- [ ] Can upload a resume
- [ ] AI analysis works
- [ ] Results display correctly

### Ready for Development
- [ ] Both servers auto-reload on changes
- [ ] Can make code changes and see updates
- [ ] Git repository initialized (optional)
- [ ] Project structure understood

---

## 🎉 Success Criteria

**Your setup is complete when:**

✅ Backend running without errors on port 5000  
✅ Frontend running without errors on port 5173  
✅ Can create account and log in  
✅ Can upload resume and get AI analysis  
✅ All navigation links work  
✅ No console errors in browser or terminals  

---

## 📝 Next Steps After Setup

1. **Explore the codebase**:
   - Review `backend/app.py` for API endpoints
   - Check `frontend/src/pages/` for page components
   - Understand `frontend/src/lib/api.ts` for API calls

2. **Customize the platform**:
   - Modify AI prompts in `backend/ai/analyze_resume.py`
   - Update UI components in `frontend/src/components/`
   - Add new features as needed

3. **Add more features**:
   - Job listing management
   - Application tracking
   - Messaging system
   - Notifications

4. **Prepare for deployment**:
   - Review deployment options
   - Set up production environment variables
   - Test in production-like environment

---

## 🆘 Still Having Issues?

If you've gone through this checklist and still have problems:

1. **Check the logs**: Read error messages carefully
2. **Review documentation**: See specific guides for detailed help
3. **Verify environment**: Double-check all `.env` values
4. **Restart everything**: Sometimes a fresh start helps
5. **Check versions**: Ensure Node.js and Python versions are correct

---

**Setup Complete? Start building amazing features! 🚀**

*Last updated: Project restructuring complete*
