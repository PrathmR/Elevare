# Elevare - AI-Driven Job Matching Platform

> An intelligent platform that analyzes resumes and skills for accurate job matches, providing authentic, updated, and domain-specific job openings with personalized recommendations.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Technology Stack](#technology-stack)
- [Setup Guide](#setup-guide)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## 🎯 About

Elevare is a full-stack AI-driven platform designed to revolutionize the job search experience for freshers and job seekers. By leveraging advanced AI technology, it provides:

1. **Intelligent Resume Analysis**: AI-powered resume parsing and skill extraction
2. **Authentic Job Listings**: Curated, verified, and up-to-date job openings
3. **Personalized Recommendations**: Career assistant that matches candidates with suitable positions
4. **Transparent Communication**: Built-in notifications and messaging system

## ✨ Features

### Core Features

- 🤖 **AI Resume Analysis**
  - Upload resumes in PDF, DOC, or DOCX format
  - Automatic skill extraction and experience parsing
  - ATS compatibility scoring
  - Personalized improvement suggestions

- 💼 **Smart Job Matching**
  - AI-driven job recommendations based on skills
  - Domain-specific job filtering
  - Real-time job updates
  - Duplicate and outdated listing removal

- 👤 **User Management**
  - Secure authentication via Supabase
  - Profile management
  - Application tracking
  - Resume storage

- 🔔 **Engagement Features**
  - Real-time notifications
  - Messaging system
  - Application status tracking
  - Interview preparation resources

## 📁 Project Structure

```
Codes/
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── lib/             # Utility functions and API client
│   │   ├── integrations/    # Supabase integration
│   │   └── hooks/           # Custom React hooks
│   ├── public/              # Static assets
│   ├── .env.example         # Environment variables template
│   └── package.json         # Frontend dependencies
│
├── backend/                  # Flask backend API
│   ├── ai/                  # AI modules
│   │   └── analyze_resume.py
│   ├── utils/               # Utility functions
│   │   └── extract_text.py
│   ├── uploads/             # Temporary file storage
│   ├── app.py               # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Backend environment template
│
├── SUPABASE_SETUP_GUIDE.md  # Detailed Supabase setup instructions
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download](https://python.org/)
- **Supabase Account** - [Sign up](https://supabase.com/)
- **Google Gemini API Key** - [Get API Key](https://makersuite.google.com/app/apikey)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Codes
   ```

2. **Set up Supabase** (Follow `SUPABASE_SETUP_GUIDE.md`):
   - Create a Supabase project
   - Get your project URL and anon key
   - Set up database tables (optional)

3. **Set up Backend**:
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   copy .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   
   python app.py
   ```

4. **Set up Frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   copy .env.example .env
   # Edit .env and add your Supabase credentials
   
   npm run dev
   ```

5. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Library**: shadcn/ui (Radix UI + Tailwind CSS)
- **Routing**: React Router v6
- **State Management**: React Query (TanStack Query)
- **Authentication**: Supabase Auth
- **Icons**: Lucide React
- **Styling**: Tailwind CSS

### Backend
- **Framework**: Flask 3.0
- **AI Model**: Google Gemini 2.5 Flash
- **Document Processing**: 
  - PyMuPDF (PDF parsing)
  - python-docx (Word document parsing)
- **CORS**: Flask-CORS
- **Environment**: python-dotenv

### Database & Auth
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Storage**: Supabase Storage (for resume files)

## 📖 Setup Guide

### 1. Supabase Configuration

Refer to `SUPABASE_SETUP_GUIDE.md` for detailed instructions on:
- Creating a Supabase project
- Setting up authentication
- Configuring database tables
- Setting up storage buckets
- Getting your API credentials

### 2. Backend Configuration

1. **Create `.env` file** in the `backend` directory:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

2. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the server**:
   ```bash
   python app.py
   ```

### 3. Frontend Configuration

1. **Create `.env` file** in the `frontend` directory:
   ```env
   VITE_SUPABASE_URL=https://your-project.supabase.co
   VITE_SUPABASE_PUBLISHABLE_KEY=your-anon-key
   VITE_API_BASE_URL=http://localhost:5000/api
   ```

2. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

## 📡 API Documentation

### Backend Endpoints

#### Health Check
```http
GET /api/health
```
Returns the health status of the backend.

#### Upload Resume
```http
POST /api/upload-resume
Content-Type: multipart/form-data

Body:
- file: Resume file (PDF, DOC, DOCX)
```

**Response**:
```json
{
  "success": true,
  "filename": "resume.pdf",
  "analysis": "AI-generated analysis...",
  "extracted_text": "Extracted resume text..."
}
```

#### Analyze Text
```http
POST /api/analyze-text
Content-Type: application/json

Body:
{
  "text": "Resume text content..."
}
```

**Response**:
```json
{
  "success": true,
  "analysis": "AI-generated analysis..."
}
```

## 🎨 Features in Detail

### Resume Analysis

The AI analyzes resumes and provides:

1. **Summary of Candidate**: Background, field, and key strengths
2. **Strengths**: Technical skills, soft skills, and experiences
3. **Weaknesses & Gaps**: Areas needing improvement
4. **ATS Score**: Applicant Tracking System compatibility (out of 100)
5. **Suggested Improvements**: Formatting and keyword recommendations
6. **Interview Questions**: Tailored technical and behavioral questions
7. **Course Recommendations**: Upskilling suggestions with platform links

### Job Matching Algorithm

- Skill-based matching using AI
- Domain-specific filtering
- Experience level consideration
- Location preferences
- Real-time updates

## 🔒 Security

- Environment variables for sensitive data
- Supabase Row Level Security (RLS)
- File type and size validation
- CORS configuration
- Secure authentication flow

## 🐛 Troubleshooting

### Common Issues

1. **Backend not starting**:
   - Ensure Python virtual environment is activated
   - Check if GOOGLE_API_KEY is set in `.env`
   - Verify all dependencies are installed

2. **Frontend not connecting to backend**:
   - Ensure backend is running on port 5000
   - Check VITE_API_BASE_URL in frontend `.env`
   - Verify CORS settings in backend

3. **Supabase authentication errors**:
   - Verify Supabase credentials in `.env`
   - Check if authentication is enabled in Supabase dashboard
   - Ensure redirect URLs are configured

4. **Resume upload fails**:
   - Check file size (max 10MB)
   - Verify file format (PDF, DOC, DOCX only)
   - Ensure backend `uploads/` directory exists

## 📝 Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow existing code style
   - Add comments for complex logic
   - Test thoroughly

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

4. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

- **Project Type**: Mini Project - Semester 5
- **Domain**: AI-Driven Job Matching Platform

## 📞 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Contact the development team

## 🎯 Roadmap

- [ ] Advanced AI matching algorithms
- [ ] Company profiles and reviews
- [ ] Video interview preparation
- [ ] Skill assessment tests
- [ ] Mobile application
- [ ] Resume builder tool
- [ ] Career path recommendations
- [ ] Salary insights and negotiation tips

---

**Built with ❤️ for job seekers and freshers**
