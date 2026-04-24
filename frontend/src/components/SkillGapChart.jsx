import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend } from 'recharts';

export default function SkillGapChart({ gap }) {
  if (!gap) return null;

  const data = [
    { subject: 'Essential', matched: gap.matched_counts?.essential || 0, total: gap.totals?.essential || 0 },
    { subject: 'Recommended', matched: gap.matched_counts?.recommended || 0, total: gap.totals?.recommended || 0 },
    { subject: 'Optional', matched: gap.matched_counts?.optional || 0, total: gap.totals?.optional || 0 },
  ];

  // Normalize for radar chart
  const radarData = data.map(d => ({
    subject: d.subject,
    'Your Skills': d.total > 0 ? Math.round((d.matched / d.total) * 100) : 0,
    'Required': 100,
  }));

  return (
    <div>
      <h3 className="text-lg font-semibold text-white mb-4">Skill Coverage Radar</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart data={radarData}>
          <PolarGrid stroke="rgba(99,102,241,0.15)" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 10 }} />
          <Radar name="Required" dataKey="Required" stroke="#6366f1" fill="#6366f1" fillOpacity={0.1} strokeDasharray="5 5" />
          <Radar name="Your Skills" dataKey="Your Skills" stroke="#22c55e" fill="#22c55e" fillOpacity={0.25} />
          <Legend wrapperStyle={{ color: '#cbd5e1', fontSize: 12 }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
