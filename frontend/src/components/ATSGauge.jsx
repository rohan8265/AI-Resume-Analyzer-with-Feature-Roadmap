import { useEffect, useState } from 'react';

export default function ATSGauge({ score = 0 }) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedScore / 100) * circumference;

  useEffect(() => {
    let start = 0;
    const duration = 1500;
    const startTime = Date.now();
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setAnimatedScore(Math.round(score * eased));
      if (progress < 1) requestAnimationFrame(animate);
    };
    animate();
  }, [score]);

  const getColor = () => {
    if (animatedScore >= 80) return '#22c55e';
    if (animatedScore >= 60) return '#eab308';
    if (animatedScore >= 40) return '#f97316';
    return '#ef4444';
  };

  return (
    <div className="relative w-48 h-48">
      <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r={radius} fill="none" stroke="rgba(99,102,241,0.1)" strokeWidth="8" />
        <circle cx="50" cy="50" r={radius} fill="none" stroke={getColor()} strokeWidth="8"
          strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 0.1s ease' }} />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-extrabold" style={{ color: getColor() }}>{animatedScore}</span>
        <span className="text-xs text-surface-400">/ 100</span>
      </div>
    </div>
  );
}
