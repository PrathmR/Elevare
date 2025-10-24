import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Search, MapPin, Briefcase, Clock, LogOut, Loader2, RefreshCw } from "lucide-react";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";
import { searchJobs, scrapeAllSources, getRecentJobs, Job } from "@/lib/api";

const Jobs = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const initialSearch = searchParams.get("search") || "";
  const [searchQuery, setSearchQuery] = useState(initialSearch);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [scraping, setScraping] = useState(false);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    toast.success("Logged out successfully");
    navigate("/");
  };

  // Load jobs from database on mount or when domain changes
  useEffect(() => {
    const domain = searchParams.get("domain");
    if (domain) {
      loadJobsByDomain(domain);
    } else {
      loadJobs();
    }
  }, [searchParams]);

  const loadJobs = async () => {
    setLoading(true);
    try {
      const result = await getRecentJobs(50);
      setJobs(result.jobs);
    } catch (error) {
      console.error("Error loading jobs:", error);
      toast.error("Failed to load jobs");
    } finally {
      setLoading(false);
    }
  };

  const loadJobsByDomain = async (domain: string) => {
    setLoading(true);
    try {
      const { getJobsByDomain } = await import("@/lib/api");
      const result = await getJobsByDomain(domain, 50);
      setJobs(result.jobs);
      toast.success(`Loaded ${result.count} jobs in ${domain} domain`);
    } catch (error) {
      console.error("Error loading jobs by domain:", error);
      toast.error("Failed to load jobs for this domain");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadJobs();
      return;
    }

    setLoading(true);
    try {
      const result = await searchJobs(searchQuery);
      setJobs(result.jobs);
      
      if (result.jobs.length === 0) {
        toast.info("No jobs found in database. Try scraping new jobs!");
      }
    } catch (error) {
      console.error("Error searching jobs:", error);
      toast.error("Failed to search jobs");
    } finally {
      setLoading(false);
    }
  };

  const handleScrapeJobs = async () => {
    if (!searchQuery.trim()) {
      toast.error("Please enter a search keyword");
      return;
    }

    setScraping(true);
    try {
      toast.info("Scraping jobs from multiple sources... This may take a minute.");
      
      const result = await scrapeAllSources(
        searchQuery,
        undefined,
        10,
        ['naukri', 'linkedin', 'unstop'],
        true
      );
      
      setJobs(result.jobs);
      
      const sourceStats = Object.entries(result.source_stats)
        .map(([source, count]) => `${source}: ${count}`)
        .join(", ");
      
      toast.success(
        `Scraped ${result.total_jobs} jobs! (${sourceStats})`
      );
      
      if (result.database?.success) {
        toast.success(`Saved ${result.database.inserted_count} jobs to database`);
      }
    } catch (error) {
      console.error("Error scraping jobs:", error);
      toast.error("Failed to scrape jobs. Please try again.");
    } finally {
      setScraping(false);
    }
  };

  const filteredJobs = searchQuery
    ? jobs.filter(
        (job) =>
          job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
          (job.description && job.description.toLowerCase().includes(searchQuery.toLowerCase()))
      )
    : jobs;

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/20">
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1
            className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent cursor-pointer"
            onClick={() => navigate("/dashboard")}
          >
            Elevare
          </h1>
          <nav className="hidden md:flex gap-6">
            <Button variant="ghost" onClick={() => navigate("/dashboard")}>
              Dashboard
            </Button>
            <Button variant="ghost" onClick={() => navigate("/jobs")}>
              Jobs
            </Button>
            <Button variant="ghost" onClick={() => navigate("/my-jobs")}>
              My Jobs
            </Button>
            <Button variant="ghost" onClick={() => navigate("/domains")}>
              Domains
            </Button>
          </nav>
          <Button variant="ghost" size="icon" onClick={handleLogout}>
            <LogOut className="h-5 w-5" />
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-4">Job Opportunities</h2>
          <p className="text-muted-foreground mb-4">
            Search our database or scrape fresh jobs from Naukri, LinkedIn, and Unstop
          </p>
          <div className="flex gap-2">
            <Input
              type="text"
              placeholder="Search jobs (e.g., python developer, react engineer)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="h-12"
            />
            <Button 
              variant="hero" 
              onClick={handleSearch}
              disabled={loading || scraping}
            >
              {loading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Search className="h-5 w-5" />
              )}
            </Button>
            <Button 
              variant="outline" 
              onClick={handleScrapeJobs}
              disabled={loading || scraping || !searchQuery.trim()}
            >
              {scraping ? (
                <>
                  <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                  Scraping...
                </>
              ) : (
                <>
                  <RefreshCw className="h-5 w-5 mr-2" />
                  Scrape Fresh Jobs
                </>
              )}
            </Button>
          </div>
        </div>

        <div className="space-y-4">
          {loading && jobs.length === 0 ? (
            <Card>
              <CardContent className="text-center py-12">
                <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
                <p className="text-muted-foreground">Loading jobs...</p>
              </CardContent>
            </Card>
          ) : (
            filteredJobs.map((job, index) => (
              <Card
                key={job.id || index}
                className="hover:shadow-lg transition-all duration-300 cursor-pointer"
                onClick={() => job.url && job.url !== 'N/A' && window.open(job.url, '_blank')}
              >
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-xl mb-2">{job.title}</CardTitle>
                      <CardDescription className="text-base">
                        {job.company}
                      </CardDescription>
                    </div>
                    <div className="flex gap-2">
                      {job.source && (
                        <Badge variant="secondary">{job.source}</Badge>
                      )}
                      {job.match_score !== undefined && (
                        <Badge variant="default">
                          {job.match_score}% Match
                        </Badge>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">
                    {job.description || 'No description available'}
                  </p>
                  <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                    {job.location && job.location !== 'N/A' && (
                      <div className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {job.location}
                      </div>
                    )}
                    {job.experience && job.experience !== 'N/A' && (
                      <div className="flex items-center gap-1">
                        <Briefcase className="h-4 w-4" />
                        {job.experience}
                      </div>
                    )}
                    {job.salary && job.salary !== 'N/A' && (
                      <div className="flex items-center gap-1">
                        <Briefcase className="h-4 w-4" />
                        {job.salary}
                      </div>
                    )}
                    {job.created_at && (
                      <div className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        {new Date(job.created_at).toLocaleDateString()}
                      </div>
                    )}
                  </div>
                  {job.matching_skills && job.matching_skills.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {job.matching_skills.map((skill, idx) => (
                        <Badge key={idx} variant="outline" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))
          )}

          {!loading && filteredJobs.length === 0 && (
            <Card>
              <CardContent className="text-center py-12">
                <p className="text-muted-foreground mb-4">
                  No jobs found matching your search.
                </p>
                {searchQuery && (
                  <Button onClick={handleScrapeJobs} disabled={scraping}>
                    {scraping ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Scraping...
                      </>
                    ) : (
                      <>
                        <RefreshCw className="h-4 w-4 mr-2" />
                        Scrape Jobs for "{searchQuery}"
                      </>
                    )}
                  </Button>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
};

export default Jobs;
