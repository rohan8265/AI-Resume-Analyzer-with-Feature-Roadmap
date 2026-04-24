import { useState } from 'react';

export default function RoadmapView({ roadmap = [], onComplete }) {
  const [expanded, setExpanded] = useState({});

  // Group by week
  const weeks = {};
  roadmap.forEach(item => {
    if (!weeks[item.week_number]) weeks[item.week_number] = [];
    weeks[item.week_number].push(item);
  });

  const totalItems = roadmap.length;
  const completedItems = roadmap.filter(r => r.is_completed).length;
  const progress = totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;

  const toggle = (week) => setExpanded(prev => ({ ...prev, [week]: !prev[week] }));

  const difficultyColor = (d) => {
    if (d === 'beginner') return 'text-green-400 bg-green-500/10 border-green-500/20';
    if (d === 'advanced') return 'text-red-400 bg-red-500/10 border-red-500/20';
    return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
  };

  return (
    <div>
      {/* Progress */}
      <div className="glass-card mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-surface-300">Roadmap Progress</span>
          <span className="text-primary-400 font-bold">{progress}%</span>
        </div>
        <div className="progress-bar-bg h-3">
          <div className="progress-bar-fill h-3" style={{ width: `${progress}%` }} />
        </div>
        <p className="text-xs text-surface-500 mt-2">{completedItems} / {totalItems} skills completed</p>
      </div>

      {/* Weeks accordion */}
      <div className="space-y-3">
        {Object.entries(weeks).map(([weekNum, items]) => {
          const weekCompleted = items.every(i => i.is_completed);
          const isOpen = expanded[weekNum] ?? false;

          return (
            <div key={weekNum} className={`glass-card transition-all ${weekCompleted ? 'border-green-500/20' : ''}`}>
              <button onClick={() => toggle(weekNum)}
                className="w-full flex items-center justify-between text-left">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold
                    ${weekCompleted ? 'bg-green-500 text-white' : 'bg-primary-500/20 text-primary-400'}`}>
                    {weekCompleted ? '✓' : weekNum}
                  </div>
                  <div>
                    <h4 className="text-white font-semibold text-sm">Week {weekNum}</h4>
                    <p className="text-xs text-surface-400">{items.map(i => i.skill_name).join(', ')}</p>
                  </div>
                </div>
                <span className="text-surface-400 text-lg">{isOpen ? '▲' : '▼'}</span>
              </button>

              {isOpen && (
                <div className="mt-4 space-y-4 border-t border-surface-800 pt-4">
                  {items.map((item, idx) => (
                    <div key={idx} className={`p-4 rounded-xl ${item.is_completed ? 'bg-green-500/5 border border-green-500/10' : 'bg-surface-900/50 border border-surface-800'}`}>
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <input type="checkbox" checked={item.is_completed}
                            onChange={(e) => onComplete(item.roadmap_id, e.target.checked)}
                            className="w-4 h-4 accent-primary-500" />
                          <span className={`font-semibold ${item.is_completed ? 'text-green-400 line-through' : 'text-white'}`}>
                            {item.skill_name}
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={`text-xs px-2 py-0.5 rounded-full border ${difficultyColor(item.difficulty)}`}>
                            {item.difficulty}
                          </span>
                          <span className="text-xs text-surface-500">{item.estimated_hours}h</span>
                        </div>
                      </div>

                      {/* Resources */}
                      <div className="grid sm:grid-cols-2 gap-2 text-xs">
                        {item.resources?.courses?.[0] && (
                          <a href={item.resources.courses[0]} target="_blank" rel="noreferrer"
                            className="flex items-center gap-1.5 p-2 rounded-lg bg-primary-500/5 hover:bg-primary-500/10 text-primary-300 transition-colors">
                            📚 Course Link
                          </a>
                        )}
                        {item.resources?.youtube?.[0] && (
                          <a href={item.resources.youtube[0]} target="_blank" rel="noreferrer"
                            className="flex items-center gap-1.5 p-2 rounded-lg bg-red-500/5 hover:bg-red-500/10 text-red-300 transition-colors">
                            🎬 YouTube Tutorial
                          </a>
                        )}
                      </div>

                      {/* Tasks */}
                      {item.tasks && (
                        <div className="mt-2 space-y-1 text-xs">
                          <div className="flex items-start gap-2 text-surface-400">
                            <span>📝</span><span>{item.tasks.practice}</span>
                          </div>
                          <div className="flex items-start gap-2 text-surface-400">
                            <span>🔨</span><span>{item.project_idea}</span>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
