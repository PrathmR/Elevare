import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  LogOut,
  Code,
  Palette,
  TrendingUp,
  Users,
  Shield,
  Heart,
  Loader2,
} from "lucide-react";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";
import { getJobsByDomain } from "@/lib/api";

const Domains = () => {
  const navigate = useNavigate();
  const [domainCounts, setDomainCounts] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    toast.success("Logged out successfully");
    navigate("/");
  };

  // Load job counts for each domain
  useEffect(() => {
    loadDomainCounts();
  }, []);

  const loadDomainCounts = async () => {
    setLoading(true);
    const counts: Record<string, number> = {};
    
    try {
      // Load counts for each domain
      for (const domain of domains) {
        try {
          const result = await getJobsByDomain(domain.id, 1000);
          counts[domain.id] = result.count;
        } catch (error) {
          console.error(`Error loading ${domain.id} jobs:`, error);
          counts[domain.id] = 0;
        }
      }
      setDomainCounts(counts);
    } catch (error) {
      console.error("Error loading domain counts:", error);
    } finally {
      setLoading(false);
    }
  };

  const domains = [
    {
      id: "tech",
      name: "Technology & Engineering",
      icon: Code,
      description: "Software development, IT, and engineering roles",
      count: 1234,
    },
    {
      id: "design",
      name: "Design & Creative",
      icon: Palette,
      description: "UX/UI design, graphic design, and creative positions",
      count: 567,
    },
    {
      id: "business",
      name: "Business & Marketing",
      icon: TrendingUp,
      description: "Marketing, sales, and business development",
      count: 890,
    },
    {
      id: "hr",
      name: "Human Resources",
      icon: Users,
      description: "HR, recruitment, and people operations",
      count: 345,
    },
    {
      id: "security",
      name: "Cybersecurity",
      icon: Shield,
      description: "Security engineering and compliance roles",
      count: 456,
    },
    {
      id: "healthcare",
      name: "Healthcare & Life Sciences",
      icon: Heart,
      description: "Medical, pharmaceutical, and biotech positions",
      count: 678,
    },
  ];

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
          <h2 className="text-3xl font-bold mb-2">Job Domains</h2>
          <p className="text-muted-foreground">
            Explore opportunities by industry and specialization
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {domains.map((domain) => {
            const Icon = domain.icon;
            const count = domainCounts[domain.id] ?? domain.count;
            return (
              <Card
                key={domain.id}
                className="hover:shadow-lg transition-all duration-300 cursor-pointer hover:-translate-y-1"
                onClick={() => navigate(`/jobs?domain=${domain.id}`)}
              >
                <CardHeader>
                  <Icon className="h-10 w-10 text-primary mb-2" />
                  <CardTitle className="text-lg">{domain.name}</CardTitle>
                  <CardDescription>{domain.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  {loading ? (
                    <div className="flex items-center gap-2">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <p className="text-sm text-muted-foreground">Loading...</p>
                    </div>
                  ) : (
                    <p className="text-sm text-muted-foreground">
                      {count.toLocaleString()} open positions
                    </p>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default Domains;
