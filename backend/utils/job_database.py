"""
Database operations for jobs
"""

from typing import List, Dict, Optional
from .supabase_client import get_supabase_client
from datetime import datetime


class JobDatabase:
    """
    Handles all database operations for jobs
    """
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def insert_jobs(self, jobs: List[Dict]) -> Dict:
        """
        Insert multiple jobs into the database
        
        Args:
            jobs (List[Dict]): List of job dictionaries
        
        Returns:
            Dict with success status and inserted count
        """
        try:
            if not jobs:
                return {"success": False, "message": "No jobs to insert"}
            
            # Prepare jobs for insertion
            jobs_to_insert = []
            for job in jobs:
                job_data = {
                    'title': job.get('title', 'N/A'),
                    'company': job.get('company', 'N/A'),
                    'description': job.get('description', ''),
                    'location': job.get('location', 'N/A'),
                    'experience': job.get('experience', 'N/A'),
                    'salary': job.get('salary', 'N/A'),
                    'url': job.get('url', ''),
                    'source': job.get('source', 'Unknown'),
                    'keyword': job.get('keyword', ''),
                    'scraped_at': job.get('scraped_at', datetime.now().isoformat()),
                    'is_active': True
                }
                jobs_to_insert.append(job_data)
            
            # Insert into Supabase
            response = self.supabase.table('jobs').insert(jobs_to_insert).execute()
            
            return {
                "success": True,
                "inserted_count": len(response.data),
                "message": f"Successfully inserted {len(response.data)} jobs"
            }
        
        except Exception as e:
            print(f"Error inserting jobs: {str(e)}")
            return {
                "success": False,
                "message": f"Error inserting jobs: {str(e)}"
            }
    
    def search_jobs(
        self,
        keyword: Optional[str] = None,
        location: Optional[str] = None,
        domain: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Search jobs in the database
        
        Args:
            keyword (str): Search keyword (searches in title and description)
            location (str): Location filter
            domain (str): Domain filter
            source (str): Source filter (Naukri, LinkedIn, Unstop)
            limit (int): Maximum number of results
        
        Returns:
            List of job dictionaries
        """
        try:
            query = self.supabase.table('jobs').select('*').eq('is_active', True)
            
            # Apply filters
            if keyword:
                # Search in title and description
                query = query.or_(f"title.ilike.%{keyword}%,description.ilike.%{keyword}%")
            
            if location:
                query = query.ilike('location', f'%{location}%')
            
            if domain:
                query = query.eq('domain', domain)
            
            if source:
                query = query.eq('source', source)
            
            # Order by created_at descending and limit
            query = query.order('created_at', desc=True).limit(limit)
            
            response = query.execute()
            return response.data
        
        except Exception as e:
            print(f"Error searching jobs: {str(e)}")
            return []
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        """
        Get a single job by ID
        
        Args:
            job_id (str): Job UUID
        
        Returns:
            Job dictionary or None
        """
        try:
            response = self.supabase.table('jobs').select('*').eq('id', job_id).execute()
            return response.data[0] if response.data else None
        
        except Exception as e:
            print(f"Error getting job: {str(e)}")
            return None
    
    def get_jobs_by_domain(self, domain: str, limit: int = 50) -> List[Dict]:
        """
        Get jobs filtered by domain
        
        Args:
            domain (str): Domain name
            limit (int): Maximum number of results
        
        Returns:
            List of job dictionaries
        """
        try:
            response = self.supabase.table('jobs')\
                .select('*')\
                .eq('domain', domain)\
                .eq('is_active', True)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data
        
        except Exception as e:
            print(f"Error getting jobs by domain: {str(e)}")
            return []
    
    def get_recent_jobs(self, limit: int = 20) -> List[Dict]:
        """
        Get most recent jobs
        
        Args:
            limit (int): Maximum number of results
        
        Returns:
            List of job dictionaries
        """
        try:
            response = self.supabase.table('jobs')\
                .select('*')\
                .eq('is_active', True)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data
        
        except Exception as e:
            print(f"Error getting recent jobs: {str(e)}")
            return []
    
    def get_job_stats(self) -> Dict:
        """
        Get statistics about jobs in the database
        
        Returns:
            Dict with job statistics
        """
        try:
            # Total active jobs
            total_response = self.supabase.table('jobs')\
                .select('id', count='exact')\
                .eq('is_active', True)\
                .execute()
            
            # Jobs by source
            sources_response = self.supabase.table('jobs')\
                .select('source')\
                .eq('is_active', True)\
                .execute()
            
            source_counts = {}
            for job in sources_response.data:
                source = job['source']
                source_counts[source] = source_counts.get(source, 0) + 1
            
            return {
                "total_jobs": total_response.count,
                "jobs_by_source": source_counts
            }
        
        except Exception as e:
            print(f"Error getting job stats: {str(e)}")
            return {"total_jobs": 0, "jobs_by_source": {}}
    
    def delete_old_jobs(self, days: int = 30) -> Dict:
        """
        Mark jobs older than specified days as inactive
        
        Args:
            days (int): Number of days
        
        Returns:
            Dict with success status
        """
        try:
            from datetime import timedelta
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            response = self.supabase.table('jobs')\
                .update({'is_active': False})\
                .lt('created_at', cutoff_date)\
                .execute()
            
            return {
                "success": True,
                "message": f"Marked old jobs as inactive"
            }
        
        except Exception as e:
            print(f"Error deleting old jobs: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
