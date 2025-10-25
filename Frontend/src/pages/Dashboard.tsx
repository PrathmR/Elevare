import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Search, Upload, Briefcase, LogOut, Menu } from "lucide-react";
import { toast } from "sonner";
import { startBackgroundScraping } from "@/lib/api";

const Dashboard = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    checkUser();
    initializeJobDatabase();
  }, []);

  const checkUser = async () => {
    const {
      data: { user },
    } = await supabase.auth.getUser();
    if (!user) {
      navigate("/auth");
    }
  };

  const initializeJobDatabase = async () => {
    // Check if we've scraped jobs in this session
    const lastScrape = localStorage.getItem('lastBackgroundScrape');
    const now = Date.now();
    
    // Only scrape if we haven't scraped in the last 24 hours
    if (!lastScrape || now - parseInt(lastScrape) > 24 * 60 * 60 * 1000) {
      try {
        console.log('🚀 Starting background job scraping...');
        await startBackgroundScraping(undefined, 5, true);
        localStorage.setItem('lastBackgroundScrape', now.toString());
        console.log('✅ Background scraping initiated');
      } catch (error) {
        console.error('Background scraping error:', error);
        // Don't show error to user - this is a background operation
      }
    }
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
    toast.success("Logged out successfully");
    navigate("/");
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/jobs?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-secondary/20">
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
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
        <div className="mb-12 text-center animate-fade-in">
          <h2 className="text-4xl font-bold mb-4">
            Find Your Dream Job with{" "}
            <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              AI Power
            </span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Upload your resume or search for opportunities tailored to your
            skills and experience
          </p>
        </div>

        <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-12">
          <div className="flex gap-2">
            <Input
              type="text"
              placeholder="Search jobs by role or keywords..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="h-12 text-base"
            />
            <Button type="submit" variant="hero" size="lg">
              <Search className="mr-2 h-5 w-5" />
              Search
            </Button>
          </div>
        </form>

        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Card
            className="hover:shadow-lg transition-all duration-300 cursor-pointer"
            onClick={() => navigate("/jobs")}
          >
            <CardHeader>
              <Search className="h-10 w-10 text-primary mb-2" />
              <CardTitle>Job Search</CardTitle>
              <CardDescription>
                Browse through curated job listings matched to your profile
              </CardDescription>
            </CardHeader>
          </Card>

          <Card
            className="hover:shadow-lg transition-all duration-300 cursor-pointer"
            onClick={() => navigate("/upload-resume")}
          >
            <CardHeader>
              <Upload className="h-10 w-10 text-accent mb-2" />
              <CardTitle>Upload Resume</CardTitle>
              <CardDescription>
                Let AI analyze your skills and recommend perfect matches
              </CardDescription>
            </CardHeader>
          </Card>

          <Card
            className="hover:shadow-lg transition-all duration-300 cursor-pointer"
            onClick={() => navigate("/my-jobs")}
          >
            <CardHeader>
              <Briefcase className="h-10 w-10 text-primary mb-2" />
              <CardTitle>My Jobs</CardTitle>
              <CardDescription>
                Track your applications and job search progress
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
