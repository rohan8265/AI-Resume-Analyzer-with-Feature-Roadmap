import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';
import { getResume, scoreResume, selectDomain, getExtractedSkills, getSkillGap, generateRoadmap, completeWeek } from '../services/api';
import ATSGauge from '../components/ATSGauge';
import SkillGapChart from '../components/SkillGapChart';
import RoadmapView from '../components/RoadmapView';

const DOMAINS = [
  { name: "Data Science", icon: "📊" },
  { name: "Artificial Intelligence / Machine Learning", icon: "🧠" },
  { name: "Web Development", icon: "🌐" },
  { name: "Software Development", icon: "💻" },
  { name: "Cloud & DevOps", icon: "☁️" },
  { name: "Cybersecurity", icon: "🔒" },
  { name: "Business Analytics", icon: "📈" },
];

export default function AnalysisPage() {
  const { resumeId } = useParams();
  const { user } = useAuth();
  const [step, setStep] = useState(2); // Start at domain selection
  const [loading, setLoading] = useState(false);
  const [resume, setResume] = useState(null);
  const [domain, setDomain] = useState(null);
  const [atsScore, setAtsScore] = useState(null);
  const [skills, setSkills] = useState(null);
  const [gap, setGap] = useState(null);
  const [roadmap, setRoadmap] = useState(null);

  useEffect(() => {
    loadResume();
  }, [resumeId]);

  const loadResume = async () => {
    try {
      const { data } = await getResume(resumeId);
      setResume(data);
      if (data.selected_domain) setDomain(data.selected_domain);
    } catch (err) {
      toast.error('Failed to load resume');
    }
  };

  const handleDomainSelect = async (d) => {
    setLoading(true);
    try {
      await selectDomain(resumeId, d);
      setDomain(d);
      toast.success(`Domain set: ${d}`);
      
      // Run ATS scoring and Skill Extraction in parallel for much faster performance
      // Both operations take time (regex parsing + BERT NLP extraction)
      const [scoreRes, skillRes] = await Promise.all([
        scoreResume(parseInt(resumeId)),
        getExtractedSkills(resumeId)
      ]);
      
      setAtsScore(scoreRes.data);
      setSkills(skillRes.data);
      
      // Auto-get gap analysis (this is fast now because skills are extracted)
      const { data: gapData } = await getSkillGap(resumeId);
      setGap(gapData);
      
      setStep(3);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateRoadmap = async () => {
    setLoading(true);
    try {
      const { data } = await generateRoadmap(resumeId);
      setRoadmap(data);
      setStep(5);
      toast.success('Roadmap generated!');
    } catch (err) {
      toast.error('Failed to generate roadmap');
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteWeek = async (roadmapId, completed) => {
    try {
      await completeWeek(roadmapId, completed);
      // Update local state
      setRoadmap(prev => ({
        ...prev,
        roadmap: prev.roadmap.map(r => r.roadmap_id === roadmapId ? { ...r, is_completed: completed } : r)
      }));
      toast.success(completed ? 'Week completed!' : 'Week uncompleted');
    } catch (err) {
      toast.error('Update failed');
    }
  };

  const steps = ['Upload', 'Domain', 'ATS Score', 'Skill Gap', 'Roadmap'];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 animate-fade-in">
      {/* Step indicator */}
      <div className="flex items-center justify-center gap-2 mb-10">
        {steps.map((s, i) => (
          <div key={i} className="flex items-center gap-2">
            <button onClick={() => { if (i + 1 <= step) setStep(i + 1); }}
              className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold transition-all
                ${i + 1 < step ? 'bg-green-500 text-white' : i + 1 === step ? 'bg-primary-500 text-white ring-4 ring-primary-500/20' : 'bg-surface-800 text-surface-500'}`}>
              {i + 1 < step ? '✓' : i + 1}
            </button>
            <span className={`text-xs hidden sm:block ${i + 1 === step ? 'text-primary-400 font-semibold' : 'text-surface-500'}`}>{s}</span>
            {i < 4 && <div className={`w-8 h-px ${i + 1 < step ? 'bg-green-500' : 'bg-surface-700'}`} />}
          </div>
        ))}
      </div>

      {/* Loading overlay */}
      {loading && (
        <div className="fixed inset-0 bg-surface-950/80 flex items-center justify-center z-50">
          <div className="text-center">
            <div className="spinner w-12 h-12 mx-auto mb-4" />
            <p className="text-white font-semibold">Analyzing your resume...</p>
            <p className="text-surface-400 text-sm mt-1">This may take a moment</p>
          </div>
        </div>
      )}

      {/* Step 2: Domain Selection */}
      {step === 2 && (
        <div className="animate-slide-up">
          <h2 className="text-2xl font-bold text-white text-center mb-2">Select Your Target Domain</h2>
          <p className="text-surface-400 text-center mb-8">Choose the career path you're aiming for</p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 max-w-4xl mx-auto">
            {DOMAINS.map((d) => (
              <button key={d.name} onClick={() => handleDomainSelect(d.name)}
                className={`glass-card text-left transition-all hover:scale-[1.02]
                  ${domain === d.name ? 'border-primary-500 bg-primary-500/10' : ''}`}>
                <span className="text-3xl">{d.icon}</span>
                <h3 className="text-white font-semibold mt-3">{d.name}</h3>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Step 3: ATS Score */}
      {step === 3 && atsScore && (
        <div className="animate-slide-up">
          <h2 className="text-2xl font-bold text-white text-center mb-8">ATS Score Analysis</h2>
          <div className="grid lg:grid-cols-2 gap-6">
            <div className="glass-card flex flex-col items-center">
              <ATSGauge score={atsScore.total_score} />
              <p className="text-surface-400 mt-2 text-sm">Overall ATS Score</p>
            </div>
            <div className="glass-card">
              <h3 className="text-lg font-semibold text-white mb-4">Score Breakdown</h3>
              <div className="space-y-3">
                {Object.entries(atsScore.breakdown || {}).map(([key, val]) => (
                  <div key={key}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-surface-300">{val.label}</span>
                      <span className="text-primary-400 font-semibold">{val.score}/{val.max}</span>
                    </div>
                    <div className="progress-bar-bg">
                      <div className="progress-bar-fill" style={{ width: `${(val.score / val.max) * 100}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Suggestions */}
          {atsScore.suggestions?.length > 0 && (
            <div className="glass-card mt-6">
              <h3 className="text-lg font-semibold text-white mb-4">💡 Improvement Suggestions</h3>
              <div className="space-y-2">
                {atsScore.suggestions.map((s, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-yellow-500/5 border border-yellow-500/10">
                    <span className="text-yellow-400 mt-0.5">⚠️</span>
                    <span className="text-sm text-surface-300">{s}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Extracted Skills */}
          {skills && (
            <div className="glass-card mt-6">
              <h3 className="text-lg font-semibold text-white mb-4">🎯 Extracted Skills ({skills.extracted_skills?.length || 0})</h3>
              <div className="flex flex-wrap gap-2">
                {skills.extracted_skills?.map((s, i) => (
                  <span key={i} className="skill-tag skill-tag-green" title={`Score: ${(s.score * 100).toFixed(0)}% | Source: ${s.source}`}>
                    {s.name}
                  </span>
                ))}
              </div>
              {skills.similarity && (
                <div className="mt-4 p-3 rounded-lg bg-primary-500/5 border border-primary-500/10">
                  <span className="text-sm text-surface-300">Skill Coverage: </span>
                  <span className="text-primary-400 font-bold">{skills.similarity.coverage_percentage}%</span>
                </div>
              )}
            </div>
          )}

          <div className="text-center mt-8">
            <button onClick={() => setStep(4)} className="btn-primary py-3 px-8">View Skill Gap →</button>
          </div>
        </div>
      )}

      {/* Step 4: Skill Gap */}
      {step === 4 && gap && (
        <div className="animate-slide-up">
          <h2 className="text-2xl font-bold text-white text-center mb-8">Skill Gap Analysis</h2>
          
          <div className="grid lg:grid-cols-2 gap-6">
            <div className="glass-card">
              <SkillGapChart gap={gap} />
            </div>
            <div className="glass-card">
              <h3 className="text-lg font-semibold text-white mb-4">Coverage by Tier</h3>
              {['essential', 'recommended', 'optional'].map(tier => (
                <div key={tier} className="mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-surface-300 capitalize">{tier}</span>
                    <span className="text-primary-400 font-semibold">{gap.coverage?.[tier]}%</span>
                  </div>
                  <div className="progress-bar-bg">
                    <div className="progress-bar-fill" style={{ width: `${gap.coverage?.[tier]}%` }} />
                  </div>
                </div>
              ))}
              <div className="mt-4 p-3 rounded-lg bg-primary-500/10 border border-primary-500/20">
                <span className="text-sm text-surface-300">Overall Coverage: </span>
                <span className="text-xl font-bold gradient-text">{gap.overall_coverage}%</span>
              </div>
            </div>
          </div>

          {/* Missing Skills */}
          <div className="grid sm:grid-cols-3 gap-4 mt-6">
            {[
              { key: 'missing_essential', label: 'Missing Essential', cls: 'skill-tag-red' },
              { key: 'missing_recommended', label: 'Missing Recommended', cls: 'skill-tag-yellow' },
              { key: 'missing_optional', label: 'Missing Optional', cls: 'skill-tag-blue' },
            ].map(({ key, label, cls }) => (
              <div key={key} className="glass-card">
                <h4 className="font-semibold text-white text-sm mb-3">{label} ({gap[key]?.length || 0})</h4>
                <div className="flex flex-wrap gap-1.5">
                  {gap[key]?.slice(0, 15).map((s, i) => (
                    <span key={i} className={`skill-tag ${cls} text-xs`}>{s.name}</span>
                  ))}
                  {gap[key]?.length > 15 && <span className="text-xs text-surface-500">+{gap[key].length - 15} more</span>}
                </div>
              </div>
            ))}
          </div>

          {/* Matched */}
          <div className="glass-card mt-6">
            <h4 className="font-semibold text-white text-sm mb-3">✅ Matched Skills ({gap.matched?.length || 0})</h4>
            <div className="flex flex-wrap gap-1.5">
              {gap.matched?.map((s, i) => (
                <span key={i} className="skill-tag skill-tag-green text-xs">{s.name}</span>
              ))}
            </div>
          </div>

          <div className="text-center mt-8">
            <button onClick={handleGenerateRoadmap} disabled={loading} className="btn-primary py-3 px-8">
              Generate Learning Roadmap →
            </button>
          </div>
        </div>
      )}

      {/* Step 5: Roadmap */}
      {step === 5 && roadmap && (
        <div className="animate-slide-up">
          <h2 className="text-2xl font-bold text-white text-center mb-2">Your Learning Roadmap</h2>
          <p className="text-surface-400 text-center mb-8">{roadmap.total_weeks} week plan for {domain}</p>
          <RoadmapView roadmap={roadmap.roadmap} onComplete={handleCompleteWeek} />
        </div>
      )}
    </div>
  );
}
