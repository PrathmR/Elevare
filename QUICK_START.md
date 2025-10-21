# Quick Start Guide - Elevare Platform

This guide will help you get the Elevare platform running in under 10 minutes.

## ✅ Prerequisites Checklist

Before starting, ensure you have:

- [ ] Node.js (v16+) installed - Check: `node --version`
- [ ] Python (v3.8+) installed - Check: `python --version`
- [ ] A Supabase account (free tier is fine)
- [ ] A Google Gemini API key

## 🚀 Setup Steps

### Step 1: Get Your API Keys (5 minutes)

#### Supabase Setup
1. Go to [https://supabase.com](https://supabase.com)
2. Create a new project (takes 2-3 minutes)
3. Go to Settings → API
4. Copy these two values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: `eyJxxx...`

#### Google Gemini API Key
1. Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key

### Step 2: Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
```

**Edit `backend/.env`** and add your Google API key:
```env
GOOGLE_API_KEY=your_actual_google_api_key_here
```

**Start the backend**:
```bash
python app.py
```

You should see: `Running on http://127.0.0.1:5000`

### Step 3: Frontend Setup (2 minutes)

Open a **NEW terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env
```

**Edit `frontend/.env`** and add your Supabase credentials:
```env
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=your_anon_public_key_here
VITE_API_BASE_URL=http://localhost:5000/api
```

**Start the frontend**:
```bash
npm run dev
```

You should see: `Local: http://localhost:5173/`

### Step 4: Test the Application (1 minute)

1. Open your browser to `http://localhost:5173`
2. Click "Sign Up" to create an account
3. After login, navigate to "Upload Resume"
4. Upload a test resume (PDF or DOCX)
5. Wait for AI analysis results!

## 🎯 What You Should See

### Backend Terminal
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
 * Debugger is active!
```

### Frontend Terminal
```
  VITE v5.4.19  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Browser
- Landing page with "Get Started" button
- Authentication pages (Sign Up/Sign In)
- Dashboard with navigation
- Upload Resume page with drag-and-drop

## 🐛 Troubleshooting

### Backend Issues

**"GOOGLE_API_KEY not set"**
- Make sure you created `.env` file in `backend/` directory
- Verify the API key is correct
- Restart the backend server

**"Module not found"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Port 5000 already in use**
- Change port in `backend/app.py`: `app.run(debug=True, port=5001)`
- Update `VITE_API_BASE_URL` in frontend `.env` to match

### Frontend Issues

**"Failed to fetch"**
- Ensure backend is running on port 5000
- Check `VITE_API_BASE_URL` in `.env`
- Verify no firewall is blocking localhost

**Supabase errors**
- Double-check your Supabase URL and key
- Ensure there are no extra spaces in `.env`
- Restart the frontend server after changing `.env`

**npm install fails**
- Try `npm install --legacy-peer-deps`
- Clear npm cache: `npm cache clean --force`

## 📁 Project Structure Overview

```
Codes/
├── backend/          ← Flask API (Port 5000)
│   ├── app.py       ← Main backend file
│   ├── .env         ← Backend config (GOOGLE_API_KEY)
│   └── uploads/     ← Temporary resume storage
│
├── frontend/         ← React App (Port 5173)
│   ├── src/         ← Source code
│   └── .env         ← Frontend config (Supabase keys)
│
└── README.md        ← Full documentation
```

## 🎓 Next Steps

Once everything is running:

1. **Explore the Features**:
   - Upload a resume and see AI analysis
   - Browse job listings
   - Check out different domains

2. **Customize**:
   - Add your own job listings
   - Modify the AI prompts in `backend/ai/analyze_resume.py`
   - Customize the UI in `frontend/src/pages/`

3. **Deploy** (Optional):
   - Backend: Deploy to Heroku, Railway, or Render
   - Frontend: Deploy to Vercel, Netlify, or Lovable
   - See deployment guides in respective README files

## 📚 Additional Resources

- **Full Documentation**: See `README.md` in root directory
- **Supabase Setup**: See `SUPABASE_SETUP_GUIDE.md`
- **Backend API**: See `backend/README.md`
- **Frontend Details**: See `frontend/README.md`

## ✅ Success Checklist

- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:5173
- [ ] Can create an account
- [ ] Can upload a resume
- [ ] AI analysis works
- [ ] Can navigate between pages

## 🎉 You're All Set!

If all checkboxes are ticked, you're ready to use Elevare!

**Need Help?** Check the troubleshooting section or refer to the detailed documentation.

---

**Happy Job Hunting! 🚀**
