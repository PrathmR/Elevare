"""
Extract basic candidate information from resume text using Google's Gemini AI
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Create the model
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_candidate_info(resume_text):
    """
    Extract basic candidate information from resume text
    
    Args:
        resume_text (str): The extracted text from the resume
        
    Returns:
        dict: Candidate information with name, email, mobile, experience, domain
    """
    prompt = f"""
You are an expert resume parser. Extract ONLY the following basic information from the resume.
Return the information in a clean, structured JSON format.

Resume:
\"\"\"
{resume_text}
\"\"\"

Extract the following:
1. **Name**: Full name of the candidate
2. **Email**: Email address
3. **Mobile**: Phone number (format: with country code if available)
4. **Experience**: Total years of experience (as a number, e.g., "3" for 3 years, "0" for fresher)
5. **Domain**: Primary domain/specialization (e.g., "Software Development", "Data Science", "UI/UX Design", "Marketing", etc.)
6. **Skills**: List of key technical skills (max 10 most relevant)

If any field is not found, use "Not Found" for text fields, "0" for experience, and empty array for skills.

Return ONLY a valid JSON object in this exact format:
{{
    "name": "Full Name",
    "email": "email@example.com",
    "mobile": "+1234567890",
    "experience": 3,
    "domain": "Software Development",
    "skills": ["Python", "JavaScript", "React"]
}}
"""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response (in case AI adds extra text)
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            json_str = json_match.group(0)
            candidate_info = json.loads(json_str)
            
            # Validate and clean data
            return {
                "name": candidate_info.get("name", "Not Found"),
                "email": candidate_info.get("email", "Not Found"),
                "mobile": candidate_info.get("mobile", "Not Found"),
                "experience": int(candidate_info.get("experience", 0)),
                "domain": candidate_info.get("domain", "Not Found"),
                "skills": candidate_info.get("skills", [])[:10]  # Limit to 10 skills
            }
        else:
            raise ValueError("Could not parse JSON from AI response")
            
    except Exception as e:
        print(f"Error extracting candidate info: {str(e)}")
        # Return default structure on error
        return {
            "name": "Not Found",
            "email": "Not Found",
            "mobile": "Not Found",
            "experience": 0,
            "domain": "Not Found",
            "skills": [],
            "error": str(e)
        }
