# Supabase Setup Guide for Elevare

## Step 1: Create a Supabase Account
1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project" or "Sign In"
3. Sign up using GitHub, Google, or email

## Step 2: Create a New Project
1. Once logged in, click "New Project"
2. Fill in the following details:
   - **Project Name**: `elevare` (or your preferred name)
   - **Database Password**: Create a strong password (save this securely!)
   - **Region**: Select the region closest to your users
   - **Pricing Plan**: Select "Free" for development
3. Click "Create new project"
4. Wait 2-3 minutes for the project to be provisioned

## Step 3: Get Your API Credentials
1. In your Supabase dashboard, click on your project
2. Go to **Settings** (gear icon in the left sidebar)
3. Click on **API** in the settings menu
4. You'll find two important values:
   - **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
   - **anon public key**: A long string starting with `eyJ...`

## Step 4: Configure Your Frontend
1. Navigate to the `frontend` directory
2. Create a `.env` file in the root of the frontend directory
3. Add the following environment variables:

```env
VITE_SUPABASE_URL=your_project_url_here
VITE_SUPABASE_PUBLISHABLE_KEY=your_anon_public_key_here
```

**Example:**
```env
VITE_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzMjc0ODAwMCwiZXhwIjoxOTQ4MzI0MDAwfQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Step 5: Set Up Database Tables (Optional)
If you need to create tables for your application:

1. Go to **Table Editor** in the Supabase dashboard
2. Click "Create a new table"
3. Create tables as needed for your application:

### Suggested Tables for Elevare:

#### `profiles` table
```sql
CREATE TABLE profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  email TEXT,
  full_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### `resumes` table
```sql
CREATE TABLE resumes (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users,
  file_name TEXT,
  file_path TEXT,
  parsed_data JSONB,
  skills TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### `jobs` table
```sql
CREATE TABLE jobs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  description TEXT,
  requirements TEXT[],
  location TEXT,
  salary_range TEXT,
  domain TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### `job_applications` table
```sql
CREATE TABLE job_applications (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES auth.users,
  job_id UUID REFERENCES jobs,
  status TEXT DEFAULT 'pending',
  applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Step 6: Enable Authentication
1. Go to **Authentication** in the Supabase dashboard
2. Click on **Providers**
3. Enable the authentication methods you want:
   - **Email**: Already enabled by default
   - **Google**: Configure OAuth credentials
   - **GitHub**: Configure OAuth credentials

## Step 7: Set Up Storage (for Resume Uploads)
1. Go to **Storage** in the Supabase dashboard
2. Click "Create a new bucket"
3. Name it `resumes`
4. Set it to **Private** (only authenticated users can access)
5. Click "Create bucket"

### Set Storage Policies
Add policies to allow users to upload their own resumes:

```sql
-- Allow users to upload their own resumes
CREATE POLICY "Users can upload own resumes"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'resumes' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Allow users to read their own resumes
CREATE POLICY "Users can read own resumes"
ON storage.objects FOR SELECT
TO authenticated
USING (bucket_id = 'resumes' AND auth.uid()::text = (storage.foldername(name))[1]);
```

## Step 8: Test Your Connection
1. Start your frontend application:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Try to sign up or log in
3. Check the browser console for any errors

## Troubleshooting

### Common Issues:

1. **"Invalid API key"**
   - Double-check your `.env` file
   - Ensure there are no extra spaces or quotes
   - Restart your development server after changing `.env`

2. **CORS errors**
   - Supabase automatically handles CORS for your project URL
   - Make sure you're using the correct project URL

3. **Authentication not working**
   - Check if email authentication is enabled in Supabase
   - Verify your redirect URLs in Supabase settings

## Security Best Practices

1. **Never commit `.env` files** to version control
2. Add `.env` to your `.gitignore` file
3. Use environment variables for all sensitive data
4. Rotate your API keys if they're ever exposed
5. Use Row Level Security (RLS) policies in Supabase

## Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase React Guide](https://supabase.com/docs/guides/getting-started/quickstarts/reactjs)
- [Supabase Auth Guide](https://supabase.com/docs/guides/auth)

---

**Need Help?** Check the Supabase Discord or documentation for support.
