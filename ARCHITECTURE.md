# Elevare Platform Architecture

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                    http://localhost:5173                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/HTTPS
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    FRONTEND (React + TS)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Components: UI, Pages, Forms, Dialogs                 │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  API Client (src/lib/api.ts)                           │ │
│  │  - uploadResume()                                      │ │
│  │  - analyzeText()                                       │ │
│  │  - checkHealth()                                       │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Supabase Client                                       │ │
│  │  - Authentication                                      │ │
│  │  - Database queries                                    │ │
│  │  - Storage operations                                  │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────┬─────────────────────────────┬────────────────┘
               │                             │
               │ REST API                    │ SDK
               │                             │
┌──────────────▼──────────────┐  ┌──────────▼────────────────┐
│   BACKEND (Flask API)       │  │   SUPABASE PLATFORM       │
│   http://localhost:5000     │  │                           │
│                             │  │  ┌─────────────────────┐  │
│  ┌───────────────────────┐  │  │  │  Authentication     │  │
│  │  API Endpoints        │  │  │  │  - Email/Password   │  │
│  │  - /api/health        │  │  │  │  - OAuth providers  │  │
│  │  - /api/upload-resume │  │  │  └─────────────────────┘  │
│  │  - /api/analyze-text  │  │  │                           │
│  └───────────────────────┘  │  │  ┌─────────────────────┐  │
│                             │  │  │  PostgreSQL DB      │  │
│  ┌───────────────────────┐  │  │  │  - profiles         │  │
│  │  Utils Module         │  │  │  │  - resumes          │  │
│  │  - extract_text.py    │  │  │  │  - jobs             │  │
│  │    • PDF parsing      │  │  │  │  - applications     │  │
│  │    • DOCX parsing     │  │  │  └─────────────────────┘  │
│  └───────────────────────┘  │  │                           │
│                             │  │  ┌─────────────────────┐  │
│  ┌───────────────────────┐  │  │  │  Storage Buckets    │  │
│  │  AI Module            │  │  │  │  - resumes/         │  │
│  │  - analyze_resume.py  │  │  │  └─────────────────────┘  │
│  └──────────┬────────────┘  │  │                           │
│             │               │  └───────────────────────────┘
│             │ API Call      │
│  ┌──────────▼────────────┐  │
│  │  Google Gemini AI     │  │
│  │  - Resume Analysis    │  │
│  │  - Skill Extraction   │  │
│  │  - Recommendations    │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

## 📁 Directory Structure

```
Codes/
│
├── frontend/                          # React Frontend Application
│   ├── src/
│   │   ├── components/               # Reusable UI Components
│   │   │   └── ui/                   # shadcn/ui components
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       ├── dialog.tsx
│   │   │       └── ...
│   │   │
│   │   ├── pages/                    # Page Components (Routes)
│   │   │   ├── Index.tsx            # Landing page
│   │   │   ├── Auth.tsx             # Login/Signup
│   │   │   ├── Dashboard.tsx        # User dashboard
│   │   │   ├── Jobs.tsx             # Job listings
│   │   │   ├── MyJobs.tsx           # Applied jobs
│   │   │   ├── Domain.tsx           # Domain filtering
│   │   │   └── UploadResume.tsx     # Resume upload & analysis
│   │   │
│   │   ├── lib/                      # Utility Functions
│   │   │   ├── api.ts               # Backend API client ⭐
│   │   │   └── utils.ts             # Helper functions
│   │   │
│   │   ├── integrations/             # Third-party Integrations
│   │   │   └── supabase/
│   │   │       ├── client.ts        # Supabase client
│   │   │       └── types.ts         # Database types
│   │   │
│   │   ├── hooks/                    # Custom React Hooks
│   │   │   └── use-mobile.tsx
│   │   │
│   │   ├── App.tsx                   # Main app component
│   │   └── main.tsx                  # Entry point
│   │
│   ├── public/                       # Static Assets
│   ├── .env                          # Environment variables (gitignored)
│   ├── .env.example                  # Environment template ⭐
│   ├── package.json                  # Dependencies
│   ├── vite.config.ts               # Vite configuration
│   └── README.md                     # Frontend documentation
│
├── backend/                           # Flask Backend API
│   ├── ai/                           # AI Processing Module
│   │   ├── __init__.py
│   │   └── analyze_resume.py        # Gemini AI integration ⭐
│   │
│   ├── utils/                        # Utility Functions
│   │   ├── __init__.py
│   │   └── extract_text.py          # Document text extraction ⭐
│   │
│   ├── uploads/                      # Temporary file storage (gitignored)
│   │
│   ├── app.py                        # Main Flask application ⭐
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Environment variables (gitignored)
│   ├── .env.example                  # Environment template ⭐
│   ├── .gitignore                    # Git ignore rules
│   └── README.md                     # Backend documentation
│
├── ResumeParser/                      # Original code (can be archived)
│
├── README.md                          # Main project documentation ⭐
├── SUPABASE_SETUP_GUIDE.md           # Supabase setup guide ⭐
├── QUICK_START.md                    # Quick setup guide ⭐
├── MIGRATION_GUIDE.md                # Migration instructions ⭐
├── SETUP_CHECKLIST.md                # Setup verification ⭐
├── PROJECT_SUMMARY.md                # Project summary ⭐
└── ARCHITECTURE.md                   # This file ⭐

⭐ = Newly created or significantly updated
```

## 🔄 Data Flow

### 1. Resume Upload Flow

```
┌─────────────┐
│   User      │
│ Selects     │
│ Resume File │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Frontend: UploadResume.tsx             │
│  - Validates file type (PDF/DOC/DOCX)   │
│  - Checks file size (< 10MB)            │
│  - Shows loading state                  │
└──────┬──────────────────────────────────┘
       │
       │ POST /api/upload-resume
       │ (multipart/form-data)
       ▼
┌─────────────────────────────────────────┐
│  Backend: app.py                        │
│  - Receives file                        │
│  - Validates file type & size           │
│  - Saves to uploads/ directory          │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Backend: utils/extract_text.py         │
│  - Detects file format                  │
│  - Extracts text from PDF/DOCX          │
│  - Returns plain text                   │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Backend: ai/analyze_resume.py          │
│  - Constructs AI prompt                 │
│  - Calls Google Gemini API              │
│  - Receives structured analysis         │
└──────┬──────────────────────────────────┘
       │
       │ JSON Response
       │ {success, filename, analysis, text}
       ▼
┌─────────────────────────────────────────┐
│  Frontend: UploadResume.tsx             │
│  - Receives analysis results            │
│  - Stores in localStorage               │
│  - Displays in dialog                   │
│  - Formats markdown content             │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   User      │
│ Views       │
│ Analysis    │
└─────────────┘
```

### 2. Authentication Flow

```
┌─────────────┐
│   User      │
│ Clicks      │
│ Sign Up     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Frontend: Auth.tsx                     │
│  - Collects email & password            │
│  - Validates input                      │
└──────┬──────────────────────────────────┘
       │
       │ supabase.auth.signUp()
       ▼
┌─────────────────────────────────────────┐
│  Supabase Authentication                │
│  - Creates user account                 │
│  - Sends verification email             │
│  - Returns session token                │
└──────┬──────────────────────────────────┘
       │
       │ Session data
       ▼
┌─────────────────────────────────────────┐
│  Frontend: Protected Routes             │
│  - Stores session in localStorage       │
│  - Redirects to Dashboard               │
│  - Enables authenticated features       │
└──────┬──────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   User      │
│ Accesses    │
│ Dashboard   │
└─────────────┘
```

## 🔌 API Integration Points

### Frontend → Backend

**API Client**: `frontend/src/lib/api.ts`

```typescript
// Upload resume
uploadResume(file: File) → Promise<UploadResumeResponse>

// Analyze text
analyzeText(text: string) → Promise<AnalyzeTextResponse>

// Health check
checkHealth() → Promise<{status, message}>
```

### Frontend → Supabase

**Supabase Client**: `frontend/src/integrations/supabase/client.ts`

```typescript
// Authentication
supabase.auth.signUp({email, password})
supabase.auth.signIn({email, password})
supabase.auth.signOut()

// Database (when tables are set up)
supabase.from('profiles').select()
supabase.from('jobs').select()
supabase.from('resumes').insert()

// Storage (when bucket is set up)
supabase.storage.from('resumes').upload()
```

### Backend → Google Gemini

**AI Module**: `backend/ai/analyze_resume.py`

```python
# Generate resume analysis
model.generate_content(prompt) → analysis_text
```

## 🌐 Network Communication

### Development Environment

```
Frontend (Port 5173)
    ↓
    ├─→ Backend API (Port 5000)
    │       ↓
    │       └─→ Google Gemini API
    │
    └─→ Supabase (Cloud)
            ├─→ Authentication
            ├─→ Database
            └─→ Storage
```

### CORS Configuration

```python
# Backend allows requests from:
- http://localhost:5173  (Frontend dev server)
- http://localhost:3000  (Alternative frontend port)
```

## 📦 Technology Stack Details

### Frontend Stack

```
React 18.3.1
    ├─→ TypeScript 5.8.3 (Type safety)
    ├─→ Vite 5.4.19 (Build tool)
    ├─→ React Router 6.30.1 (Routing)
    ├─→ TanStack Query 5.83.0 (Data fetching)
    ├─→ Tailwind CSS 3.4.17 (Styling)
    ├─→ shadcn/ui (UI components)
    │       ├─→ Radix UI (Primitives)
    │       └─→ Lucide React (Icons)
    └─→ Supabase JS 2.58.0 (Backend SDK)
```

### Backend Stack

```
Flask 3.0.0
    ├─→ Flask-CORS 4.0.0 (Cross-origin support)
    ├─→ PyMuPDF 1.23.8 (PDF parsing)
    ├─→ python-docx 1.1.0 (DOCX parsing)
    ├─→ google-generativeai 0.3.2 (AI integration)
    └─→ python-dotenv 1.0.0 (Environment variables)
```

## 🔐 Security Architecture

### Environment Variables

```
Frontend (.env)
    ├─→ VITE_SUPABASE_URL (Public)
    ├─→ VITE_SUPABASE_PUBLISHABLE_KEY (Public)
    └─→ VITE_API_BASE_URL (Public)

Backend (.env)
    ├─→ GOOGLE_API_KEY (Secret) ⚠️
    ├─→ FLASK_ENV (Config)
    └─→ FLASK_DEBUG (Config)
```

### Security Layers

```
1. File Upload Security
   ├─→ File type validation (PDF, DOC, DOCX only)
   ├─→ File size limit (10MB max)
   └─→ Temporary storage with cleanup

2. API Security
   ├─→ CORS configuration
   ├─→ Input validation
   └─→ Error handling

3. Authentication Security
   ├─→ Supabase Auth (JWT tokens)
   ├─→ Row Level Security (RLS)
   └─→ Secure session management

4. Data Security
   ├─→ Environment variables for secrets
   ├─→ .gitignore for sensitive files
   └─→ HTTPS in production
```

## 🚀 Deployment Architecture

### Recommended Production Setup

```
┌─────────────────────────────────────────────────────────┐
│                    CDN / Edge Network                    │
│                   (Cloudflare, etc.)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Frontend (Static Hosting)                   │
│         Vercel / Netlify / Cloudflare Pages             │
│                                                          │
│  - Automatic HTTPS                                       │
│  - Global CDN                                            │
│  - Instant deployments                                   │
└──────────────┬───────────────────────────┬───────────────┘
               │                           │
               │ HTTPS API Calls           │ SDK
               │                           │
┌──────────────▼──────────────┐  ┌────────▼──────────────┐
│  Backend (Container/PaaS)   │  │  Supabase (Cloud)     │
│  Railway / Render / Heroku  │  │                       │
│                             │  │  - Managed Database   │
│  - Auto-scaling             │  │  - Authentication     │
│  - Health monitoring        │  │  - Storage            │
│  - Environment variables    │  │  - Real-time          │
│  - HTTPS endpoints          │  │  - Backups            │
└──────────────┬──────────────┘  └───────────────────────┘
               │
               │ API Key
               │
┌──────────────▼──────────────┐
│   Google Gemini API         │
│   (Cloud AI Service)        │
└─────────────────────────────┘
```

## 📊 Performance Considerations

### Frontend Optimization
- Code splitting by route
- Lazy loading components
- Image optimization
- Caching strategies
- Minification and compression

### Backend Optimization
- File size limits
- Request timeout handling
- Error recovery
- Logging and monitoring
- API rate limiting

## 🔄 State Management

```
Frontend State Flow:

User Interaction
    ↓
React Component State (useState)
    ↓
API Call (via api.ts)
    ↓
TanStack Query (caching & refetching)
    ↓
Component Re-render
    ↓
UI Update
```

## 📝 Development Workflow

```
1. Local Development
   ├─→ Frontend: npm run dev (Port 5173)
   ├─→ Backend: python app.py (Port 5000)
   └─→ Hot reload enabled on both

2. Version Control
   ├─→ Git for source control
   ├─→ .gitignore for secrets
   └─→ Feature branches

3. Testing
   ├─→ Manual testing in browser
   ├─→ API testing with curl/Postman
   └─→ Console logging for debugging

4. Deployment
   ├─→ Frontend: Push to Vercel/Netlify
   ├─→ Backend: Deploy to Railway/Render
   └─→ Environment variables in platform
```

---

**This architecture provides a solid foundation for building a scalable, secure, and maintainable AI-driven job matching platform! 🚀**
