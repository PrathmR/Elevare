import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { LogOut, Upload, FileText, Sparkles, Loader2, Briefcase, User, Mail, Phone, Calendar, Target } from "lucide-react";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";
import { uploadResume, scrapeAndRecommend, type CandidateInfo } from "@/lib/api";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

const UploadResume = () => {
  const navigate = useNavigate();
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [candidateInfo, setCandidateInfo] = useState<CandidateInfo | null>(null);
  const [showInfo, setShowInfo] = useState(false);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    toast.success("Logged out successfully");
    navigate("/");
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error("Please select a file");
      return;
    }

    setUploading(true);

    try {
      // Upload and extract candidate info using backend API
      const result = await uploadResume(file);
      
      if (result.success) {
        toast.success("Resume processed successfully!");
        setCandidateInfo(result.candidate_info);
        setShowInfo(true);
        
        // Store info in localStorage for later use
        localStorage.setItem('lastCandidateInfo', JSON.stringify(result.candidate_info));
        localStorage.setItem('lastResumeText', result.resume_text);
      }
    } catch (error) {
      console.error("Error uploading resume:", error);
      toast.error(error instanceof Error ? error.message : "Failed to process resume");
    } finally {
      setUploading(false);
    }
  };

  const handleViewJobs = () => {
    setShowInfo(false);
    navigate("/jobs?ai=true");
  };

  const handleGetRecommendations = async () => {
    if (!candidateInfo) {
      toast.error("No candidate data available");
      return;
    }

    setLoadingRecommendations(true);
    try {
      toast.info("Finding matching jobs from database...");
      
      const result = await scrapeAndRecommend(
        candidateInfo.skills,
        candidateInfo.domain,
        undefined
      );
      
      // Store recommendations and navigate to jobs page
      localStorage.setItem('recommendedJobs', JSON.stringify(result.jobs));
      toast.success(`Found ${result.count} matching jobs!`);
      
      setShowInfo(false);
      navigate("/jobs?recommended=true");
    } catch (error) {
      console.error("Error getting recommendations:", error);
      toast.error("Failed to get job recommendations");
    } finally {
      setLoadingRecommendations(false);
    }
  };

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
        <div className="max-w-2xl mx-auto">
          <div className="mb-8 text-center">
            <Sparkles className="h-12 w-12 text-primary mx-auto mb-4" />
            <h2 className="text-3xl font-bold mb-2">Upload Your Resume</h2>
            <p className="text-muted-foreground">
              Let our AI analyze your skills and match you with perfect
              opportunities
            </p>
          </div>

          <Card className="shadow-xl">
            <CardHeader>
              <CardTitle>Upload Document</CardTitle>
              <CardDescription>
                Supported formats: PDF, DOC, DOCX (Max size: 10MB)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary transition-colors">
                  <input
                    type="file"
                    id="resume-upload"
                    className="hidden"
                    accept=".pdf,.doc,.docx"
                    onChange={handleFileChange}
                  />
                  <label
                    htmlFor="resume-upload"
                    className="cursor-pointer flex flex-col items-center gap-4"
                  >
                    {file ? (
                      <>
                        <FileText className="h-16 w-16 text-primary" />
                        <div>
                          <p className="font-medium">{file.name}</p>
                          <p className="text-sm text-muted-foreground">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </>
                    ) : (
                      <>
                        <Upload className="h-16 w-16 text-muted-foreground" />
                        <div>
                          <p className="font-medium">
                            Click to upload or drag and drop
                          </p>
                          <p className="text-sm text-muted-foreground">
                            PDF, DOC, or DOCX (max. 10MB)
                          </p>
                        </div>
                      </>
                    )}
                  </label>
                </div>

                <div className="space-y-3 text-sm text-muted-foreground">
                  <p className="flex items-start gap-2">
                    <span className="text-primary">✓</span>
                    <span>AI will extract your skills and experience</span>
                  </p>
                  <p className="flex items-start gap-2">
                    <span className="text-primary">✓</span>
                    <span>Get personalized job recommendations</span>
                  </p>
                  <p className="flex items-start gap-2">
                    <span className="text-primary">✓</span>
                    <span>Your data is securely encrypted</span>
                  </p>
                </div>

                <Button
                  variant="hero"
                  size="lg"
                  className="w-full"
                  onClick={handleUpload}
                  disabled={!file || uploading}
                >
                  {uploading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    "Upload & Analyze Resume"
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Candidate Info Dialog */}
      <Dialog open={showInfo} onOpenChange={setShowInfo}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Candidate Profile</DialogTitle>
          </DialogHeader>
          <div className="space-y-6">
            {candidateInfo && (
              <>
                {/* Basic Info */}
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <User className="h-5 w-5 text-primary" />
                    <div>
                      <p className="text-sm text-muted-foreground">Name</p>
                      <p className="font-medium">{candidateInfo.name}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <Mail className="h-5 w-5 text-primary" />
                    <div>
                      <p className="text-sm text-muted-foreground">Email</p>
                      <p className="font-medium">{candidateInfo.email}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <Phone className="h-5 w-5 text-primary" />
                    <div>
                      <p className="text-sm text-muted-foreground">Mobile</p>
                      <p className="font-medium">{candidateInfo.mobile}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <Calendar className="h-5 w-5 text-primary" />
                    <div>
                      <p className="text-sm text-muted-foreground">Experience</p>
                      <p className="font-medium">
                        {candidateInfo.experience === 0 ? 'Fresher' : `${candidateInfo.experience} years`}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <Target className="h-5 w-5 text-primary" />
                    <div>
                      <p className="text-sm text-muted-foreground">Domain</p>
                      <p className="font-medium">{candidateInfo.domain}</p>
                    </div>
                  </div>
                </div>

                {/* Skills */}
                <div>
                  <p className="text-sm text-muted-foreground mb-2">Skills</p>
                  <div className="flex flex-wrap gap-2">
                    {candidateInfo.skills.length > 0 ? (
                      candidateInfo.skills.map((skill, index) => (
                        <Badge key={index} variant="secondary">
                          {skill}
                        </Badge>
                      ))
                    ) : (
                      <p className="text-sm text-muted-foreground">No skills extracted</p>
                    )}
                  </div>
                </div>
              </>
            )}
          </div>
          
          <div className="flex gap-2 justify-end mt-4">
            <Button variant="outline" onClick={() => setShowInfo(false)}>
              Close
            </Button>
            <Button 
              variant="secondary" 
              onClick={handleGetRecommendations}
              disabled={loadingRecommendations}
            >
              {loadingRecommendations ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Finding Jobs...
                </>
              ) : (
                <>
                  <Briefcase className="mr-2 h-4 w-4" />
                  Get Job Recommendations
                </>
              )}
            </Button>
            <Button onClick={handleViewJobs}>
              Browse All Jobs
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default UploadResume;
