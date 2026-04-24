import { useState, useEffect } from 'react';
import { getAdminStats } from '../services/api';
import { toast } from 'react-toastify';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#6366f1', '#d946ef', '#22c55e', '#f59e0b', '#ef4444'];

export default function AdminPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const { data } = await getAdminStats();
      setStats(data);
    } catch (err) {
      toast.error('Admin access required');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="flex items-center justify-center min-h-[60vh]"><div className="spinner" /></div>;
  if (!stats) return <div className="text-center py-20 text-surface-400">Admin access required</div>;

  const distData = Object.entries(stats.score_distribution || {}).map(([range, count]) => ({
    range, count
  }));

  const domainData = Object.entries(stats.domain_popularity || {}).map(([name, value]) => ({
    name: name?.length > 15 ? name.substring(0, 15) + '...' : name, value
  }));

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 animate-fade-in">
      <h1 className="text-2xl font-bold text-white mb-8">Admin Dashboard</h1>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { label: 'Total Users', value: stats.total_users, icon: '👥' },
          { label: 'Total Resumes', value: stats.total_resumes, icon: '📄' },
          { label: 'Avg ATS Score', value: stats.average_ats_score, icon: '📊' },
        ].map((s, i) => (
          <div key={i} className="glass-card text-center">
            <span className="text-3xl">{s.icon}</span>
            <p className="text-3xl font-bold text-white mt-2">{s.value}</p>
            <p className="text-sm text-surface-400">{s.label}</p>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Score Distribution */}
        <div className="glass-card">
          <h3 className="text-lg font-semibold text-white mb-4">ATS Score Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={distData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.1)" />
              <XAxis dataKey="range" tick={{ fill: '#64748b', fontSize: 11 }} />
              <YAxis tick={{ fill: '#64748b', fontSize: 11 }} />
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, color: '#e2e8f0' }} />
              <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Domain Popularity */}
        <div className="glass-card">
          <h3 className="text-lg font-semibold text-white mb-4">Domain Popularity</h3>
          {domainData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={domainData} dataKey="value" nameKey="name" cx="50%" cy="50%"
                  outerRadius={80} label={({ name, value }) => `${name}: ${value}`}>
                  {domainData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8, color: '#e2e8f0' }} />
              </PieChart>
            </ResponsiveContainer>
          ) : <p className="text-surface-500 text-center py-8">No domain data yet</p>}
        </div>
      </div>

      {/* Recent Users */}
      <div className="glass-card mt-6">
        <h3 className="text-lg font-semibold text-white mb-4">Recent Users</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-800">
                <th className="text-left py-2 text-surface-400 font-medium">ID</th>
                <th className="text-left py-2 text-surface-400 font-medium">Name</th>
                <th className="text-left py-2 text-surface-400 font-medium">Email</th>
                <th className="text-left py-2 text-surface-400 font-medium">Joined</th>
              </tr>
            </thead>
            <tbody>
              {stats.recent_users?.map((u) => (
                <tr key={u.user_id} className="border-b border-surface-800/50">
                  <td className="py-2 text-surface-300">{u.user_id}</td>
                  <td className="py-2 text-white">{u.name}</td>
                  <td className="py-2 text-surface-400">{u.email}</td>
                  <td className="py-2 text-surface-500">{new Date(u.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
