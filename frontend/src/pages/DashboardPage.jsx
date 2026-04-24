import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getDashboard } from '../services/api';
import { toast } from 'react-toastify';
import ATSGauge from '../components/ATSGauge';
import SkillGapChart from '../components/SkillGapChart';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const { data: d } = await getDashboard(user.user_id);
      setData(d);
    } catch (err) {
      // No data yet
    } finally {
      setLoading(false);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="spinner" />
    </div>
  );

  if (!data || !data.resumes?.length) return (
    <div className="max-w-2xl mx-auto px-4 py-20 text-center animate-fade-in">
      <div className="text-6xl mb-6">📄</div>
      <h2 className="text-2xl font-bold text-white mb-3">No Resumes Yet</h2>
      <p className="text-surface-400 mb-8">Upload your first resume to get started with AI analysis</p>
      <Link to="/upload" className="btn-primary py-3 px-8 text-lg">Upload Resume →</Link>
    </div>
  );

  const latestScore = data.latest_score;
  const scoreHistory = data.ats_scores?.map((s, i) => ({
    name: `Score ${i + 1}`,
    score: s.total_score,
    date: new Date(s.scored_at).toLocaleDateString()
  }));

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 animate-fade-in">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Welcome, {user?.name}</h1>
          <p className="text-surface-400 text-sm">Your career analytics dashboard</p>
        </div>
        <Link to="/upload" className="btn-primary">Upload New Resume</Link>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Resumes', value: data.resumes?.length || 0, icon: '📄', color: 'from-blue-500 to-indigo-500' },
          { label: 'ATS Score', value: latestScore?.total_score || '-', icon: '📊', color: 'from-green-500 to-emerald-500' },
          { label: 'Skills Found', value: data.skills?.length || 0, icon: '🎯', color: 'from-purple-500 to-fuchsia-500' },
          { label: 'Roadmap', value: `${data.roadmap_progress?.percentage || 0}%`, icon: '🗺️', color: 'from-orange-500 to-amber-500' },
        ].map((s, i) => (
          <div key={i} className="glass-card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl">{s.icon}</span>
              <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${s.color} opacity-20`} />
            </div>
            <p className="text-2xl font-bold text-white">{s.value}</p>
            <p className="text-xs text-surface-400">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* ATS Score */}
        {latestScore && (
          <div className="glass-card">
            <h3 className="text-lg font-semibold text-white mb-4">Latest ATS Score</h3>
            <div className="flex items-center justify-center">
              <ATSGauge score={latestScore.total_score} />
            </div>
            <div className="mt-4 space-y-2">
              {Object.entries(latestScore.breakdown || {}).map(([k, v]) => (
                <div key={k} className="flex justify-between text-xs">
                  <span className="text-surface-400">{v.label}</span>
                  <span className="text-primary-400">{v.score}/{v.max}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Score History */}
        {scoreHistory?.length > 1 && (
          <div className="glass-card">
            <h3 className="text-lg font-semibold text-white mb-4">Score Trend</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={scoreHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.1)" />
                <XAxis dataKey="name" tick={{ fill: '#64748b', fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 11 }} />
                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, color: '#e2e8f0' }} />
                <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={2} dot={{ fill: '#6366f1' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Skills */}
        {data.skills?.length > 0 && (
          <div className="glass-card">
            <h3 className="text-lg font-semibold text-white mb-4">Your Skills</h3>
            <div className="flex flex-wrap gap-1.5 max-h-48 overflow-y-auto">
              {data.skills.map((s, i) => (
                <span key={i} className="skill-tag skill-tag-green text-xs">{s.skill_name}</span>
              ))}
            </div>
          </div>
        )}

        {/* Roadmap Progress */}
        {data.roadmap?.length > 0 && (
          <div className="glass-card">
            <h3 className="text-lg font-semibold text-white mb-4">Roadmap Progress</h3>
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-surface-300">Completion</span>
                <span className="text-primary-400 font-bold">{data.roadmap_progress.percentage}%</span>
              </div>
              <div className="progress-bar-bg h-3">
                <div className="progress-bar-fill h-3" style={{ width: `${data.roadmap_progress.percentage}%` }} />
              </div>
            </div>
            <p className="text-xs text-surface-500">{data.roadmap_progress.completed} / {data.roadmap_progress.total} tasks</p>
            <div className="mt-3 space-y-1 max-h-36 overflow-y-auto">
              {data.roadmap.slice(0, 8).map((r, i) => (
                <div key={i} className="flex items-center gap-2 text-xs">
                  <span>{r.is_completed ? '✅' : '⬜'}</span>
                  <span className={r.is_completed ? 'text-green-400 line-through' : 'text-surface-300'}>
                    Week {r.week_number}: {r.skill_name}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Resume List */}
      <div className="glass-card mt-6">
        <h3 className="text-lg font-semibold text-white mb-4">Your Resumes</h3>
        <div className="space-y-2">
          {data.resumes.map((r) => (
            <Link key={r.resume_id} to={`/analysis/${r.resume_id}`}
              className="flex items-center justify-between p-3 rounded-xl bg-surface-900/50 hover:bg-surface-800/50 border border-surface-800 hover:border-primary-500/20 transition-all">
              <div className="flex items-center gap-3">
                <span className="text-xl">📄</span>
                <div>
                  <p className="text-sm text-white font-medium">{r.filename}</p>
                  <p className="text-xs text-surface-500">{new Date(r.uploaded_at).toLocaleDateString()} • {r.file_format?.toUpperCase()}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                {r.selected_domain && <span className="skill-tag skill-tag-blue text-xs">{r.selected_domain}</span>}
                <span className="text-surface-500">→</span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
