# Elevare - AI-Driven Job Matching Platform (Frontend)

## Project Overview

Elevare is an AI-driven platform that analyzes resumes and skills for accurate job matches. It provides authentic, updated, and domain-specific job openings with personalized recommendations acting as a career assistant for freshers.

### Key Features

- 🤖 **AI Resume Analysis**: Upload resumes for intelligent skill extraction and analysis
- 💼 **Job Matching**: Personalized job recommendations based on skills and experience
- 🎯 **Domain-Specific**: Targeted job listings across various domains
- 🔔 **Notifications**: Real-time updates on job applications
- 💬 **Messaging**: Direct communication with recruiters
- 🔐 **Secure Authentication**: Powered by Supabase

## Project info

**URL**: https://lovable.dev/projects/2375f454-302d-44b4-89b4-5bb4fe5a7b13

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/2375f454-302d-44b4-89b4-5bb4fe5a7b13) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the frontend directory.
cd frontend

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Set up environment variables
# Copy .env.example to .env and fill in your credentials
copy .env.example .env

# Step 5: Start the development server with auto-reloading and an instant preview.
npm run dev
```

## Environment Setup

Before running the application, you need to configure your environment variables:

1. **Copy the example file**:
   ```bash
   copy .env.example .env
   ```

2. **Configure Supabase** (see `SUPABASE_SETUP_GUIDE.md` in the root directory):
   - `VITE_SUPABASE_URL`: Your Supabase project URL
   - `VITE_SUPABASE_PUBLISHABLE_KEY`: Your Supabase anon/public key

3. **Configure Backend API**:
   - `VITE_API_BASE_URL`: Backend API URL (default: `http://localhost:5000/api`)

4. **Start the backend server** (see `backend/README.md` for instructions)

5. **Start the frontend**:
   ```bash
   npm run dev
   ```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/2375f454-302d-44b4-89b4-5bb4fe5a7b13) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/features/custom-domain#custom-domain)
