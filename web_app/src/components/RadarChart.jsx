import React from 'react';

export function RadarChart({ domainResults, width = 360, height = 300 }) {
  if (!domainResults) return null;
  
  const cx = width / 2;
  const cy = (height / 2) - 10;
  const r = 95;
  const domains = Object.values(domainResults);
  const n = domains.length;
  if (n === 0) return null;

  const angles = domains.map((_, i) => (2 * Math.PI * i / n) - (Math.PI / 2));

  // Web Circles
  const webPolygons = [0.2, 0.4, 0.6, 0.8, 1.0].map((level, idx) => {
    const lr = r * level;
    const points = angles.map(a => `${(cx + lr * Math.cos(a)).toFixed(1)},${(cy + lr * Math.sin(a)).toFixed(1)}`).join(' ');
    return <polygon key={idx} points={points} fill="none" stroke="#334155" strokeWidth="1" strokeDasharray="3,3" />;
  });

  // Axis Lines & Labels
  const axisLines = angles.map((a, i) => {
    const ax = cx + r * Math.cos(a);
    const ay = cy + r * Math.sin(a);
    const lx = cx + (r + 22) * Math.cos(a);
    const ly = cy + (r + 18) * Math.sin(a);
    
    let anchor = "middle";
    if (Math.cos(a) > 0.3) anchor = "start";
    else if (Math.cos(a) < -0.3) anchor = "end";

    const shortName = domains[i].name
      .replace("Data Protection & Privacy", "Privacy")
      .replace("Transparency & Incidents", "Transparency")
      .replace("HR & High-Risk Systems", "HR / High Risk")
      .replace("AI Literacy & Operations", "Literacy & Ops");

    return (
      <g key={i}>
        <line x1={cx} y1={cy} x2={ax} y2={ay} stroke="#334155" strokeWidth="1" />
        <text x={lx} y={ly} textAnchor={anchor} fill="#94A3B8" fontSize="10" fontWeight="600">{shortName}</text>
      </g>
    );
  });

  // Target Polygon (80%)
  const targetPoints = angles.map(a => `${(cx + (r * 0.8) * Math.cos(a)).toFixed(1)},${(cy + (r * 0.8) * Math.sin(a)).toFixed(1)}`).join(' ');

  // Company Score Polygon
  const actualPoints = angles.map((a, i) => {
    const scoreRatio = Math.min(1.0, Math.max(0.0, domains[i].score / 100.0));
    return `${(cx + (r * scoreRatio) * Math.cos(a)).toFixed(1)},${(cy + (r * scoreRatio) * Math.sin(a)).toFixed(1)}`;
  }).join(' ');

  const dots = angles.map((a, i) => {
    const scoreRatio = Math.min(1.0, Math.max(0.0, domains[i].score / 100.0));
    const px = cx + (r * scoreRatio) * Math.cos(a);
    const py = cy + (r * scoreRatio) * Math.sin(a);
    return <circle key={i} cx={px} cy={py} r="4" fill="#38BDF8" stroke="#0F172A" strokeWidth="2" />;
  });

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
      {webPolygons}
      {axisLines}
      <polygon points={targetPoints} fill="rgba(56, 189, 248, 0.08)" stroke="#38BDF8" strokeWidth="1.5" strokeDasharray="4,4" />
      <polygon points={actualPoints} fill="rgba(6, 182, 212, 0.35)" stroke="#06B6D4" strokeWidth="2.5" />
      {dots}
      <text x={width - 80} y={height - 8} fill="#38BDF8" fontSize="10" fontWeight="600">--- Target (80%)</text>
      <text x="10" y={height - 8} fill="#06B6D4" fontSize="10" fontWeight="700">━ Acme Score</text>
    </svg>
  );
}

export function GaugeBar({ score, width = 360, height = 40 }) {
  const scorePos = Math.min(width - 10, Math.max(10, (score / 100.0) * width));

  return (
    <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`}>
      <defs>
        <linearGradient id="gaugeGradReact" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#E11D48" />
          <stop offset="30%" stopColor="#F59E0B" />
          <stop offset="55%" stopColor="#3B82F6" />
          <stop offset="80%" stopColor="#10B981" />
          <stop offset="100%" stopColor="#06B6D4" />
        </linearGradient>
      </defs>

      <rect x="0" y="10" width={width} height="12" rx="6" fill="url(#gaugeGradReact)" opacity="0.85" />
      
      <text x={width * 0.15} y="34" textAnchor="middle" fill="#94A3B8" fontSize="9">Initial</text>
      <text x={width * 0.40} y="34" textAnchor="middle" fill="#94A3B8" fontSize="9">Developing</text>
      <text x={width * 0.60} y="34" textAnchor="middle" fill="#94A3B8" fontSize="9">Managed</text>
      <text x={width * 0.80} y="34" textAnchor="middle" fill="#94A3B8" fontSize="9">Advanced</text>
      <text x={width * 0.95} y="34" textAnchor="middle" fill="#94A3B8" fontSize="9">Trusted</text>

      <polygon points={`${scorePos - 5},0 ${scorePos + 5},0 ${scorePos},8`} fill="#38BDF8" />
      <circle cx={scorePos} cy="16" r="5" fill="#38BDF8" stroke="#0F172A" strokeWidth="2" />
    </svg>
  );
}
