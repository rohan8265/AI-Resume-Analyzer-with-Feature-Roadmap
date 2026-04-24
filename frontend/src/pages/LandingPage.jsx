import { Link } from 'react-router-dom';

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative overflow-hidden py-24 px-4">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-900/20 via-transparent to-accent-900/20" />
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl" />

        <div className="relative max-w-5xl mx-auto text-center animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 mb-8">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <span className="text-sm text-primary-300">AI-Powered Career Platform</span>
          </div>

          <h1 className="text-5xl sm:text-7xl font-extrabold mb-6 leading-tight">
            <span className="gradient-text">AI Resume</span><br />
            <span className="text-white">Analyzer & Roadmap</span>
          </h1>

          <p className="text-lg text-surface-300 max-w-2xl mx-auto mb-10 leading-relaxed">
            Upload your resume, get an instant ATS score, discover skill gaps,
            and receive a personalized weekly learning roadmap to land your dream job.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register" className="btn-primary text-lg py-4 px-8">Get Started Free →</Link>
            <Link to="/login" className="btn-secondary text-lg py-4 px-8">Sign In</Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-16">
            <span className="gradient-text">Everything You Need</span> to Level Up
          </h2>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { icon: "📄", title: "Smart Resume Parsing", desc: "Upload PDF, DOCX, or TXT. Our AI extracts and structures every section automatically." },
              { icon: "📊", title: "ATS Score Analysis", desc: "Get a detailed 0-100 score with section-wise breakdown and actionable improvement tips." },
              { icon: "🎯", title: "Skill Gap Detection", desc: "Compare your skills against 1200+ domain skills across 7 career domains." },
              { icon: "🧠", title: "NLP Skill Extraction", desc: "Hybrid pipeline using spaCy NER, BERT embeddings, and fuzzy matching." },
              { icon: "🗺️", title: "Learning Roadmap", desc: "8-24 week personalized plan with courses, projects, and practice tasks." },
              { icon: "📈", title: "Progress Tracking", desc: "Track your growth over time with interactive charts and completion metrics." }
            ].map((f, i) => (
              <div key={i} className="glass-card animate-slide-up" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="text-4xl mb-4">{f.icon}</div>
                <h3 className="text-lg font-semibold text-white mb-2">{f.title}</h3>
                <p className="text-sm text-surface-300 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Domains */}
      <section className="py-24 px-4 bg-surface-900/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4 gradient-text">7 Career Domains</h2>
          <p className="text-surface-300 mb-12">Choose your target domain and get a tailored analysis</p>
          <div className="flex flex-wrap justify-center gap-3">
            {["Data Science", "AI / Machine Learning", "Web Development", "Software Development",
              "Cloud & DevOps", "Cybersecurity", "Business Analytics"].map((d, i) => (
                <span key={i} className="skill-tag skill-tag-blue text-sm py-2 px-5">{d}</span>
              ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-surface-800">
        <div className="max-w-6xl mx-auto text-center text-sm text-surface-500">
          © 2026 AI Resume Analyzer. All Rights Reserved.
        </div>
      </footer>
    </div>
  );
}
