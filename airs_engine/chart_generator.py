"""
AIRS SVG Chart Generator Module
Generates zero-dependency, pure inline vector SVG charts for assessment reports:
1. 7-Axis Domain Maturity Radar (Spider) Chart
2. AIRS Governance Index Progress Gauge
3. Domain Score Breakdown Visual Bars
"""

import math
from typing import Dict, Any
from .scoring import DomainResult

class SVGChartGenerator:
    @staticmethod
    def generate_radar_chart(domain_results: Dict[str, DomainResult], width: int = 400, height: int = 340) -> str:
        cx, cy = width // 2, (height // 2) - 10
        r = 110
        domains = list(domain_results.values())
        n = len(domains)
        if n == 0:
            return ""

        angles = [ (2 * math.pi * i / n) - (math.pi / 2) for i in range(n) ]

        # Web circles (20%, 40%, 60%, 80%, 100%)
        web_lines = ""
        for level in [0.2, 0.4, 0.6, 0.8, 1.0]:
            lr = r * level
            points = [f"{cx + lr * math.cos(a):.1f},{cy + lr * math.sin(a):.1f}" for a in angles]
            web_lines += f'<polygon points="{" ".join(points)}" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="3,3" />\n'

        # Axis lines
        axis_lines = ""
        labels_svg = ""
        for i, a in enumerate(angles):
            ax = cx + r * math.cos(a)
            ay = cy + r * math.sin(a)
            axis_lines += f'<line x1="{cx}" y1="{cy}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="#334155" stroke-width="1" />\n'

            # Label positions slightly outside radius
            lx = cx + (r + 25) * math.cos(a)
            ly = cy + (r + 20) * math.sin(a)
            anchor = "middle"
            if math.cos(a) > 0.3:
                anchor = "start"
            elif math.cos(a) < -0.3:
                anchor = "end"

            # Shorten label for radar
            short_name = domains[i].name.replace("Data Protection & Privacy", "Privacy").replace("Transparency & Incidents", "Transparency").replace("HR & High-Risk Systems", "HR / High Risk").replace("AI Literacy & Operations", "Literacy & Ops")
            labels_svg += f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" fill="#94A3B8" font-size="11" font-weight="600">{short_name}</text>\n'

        # Target Benchmark Zone (80 points)
        target_points = [f"{cx + (r * 0.8) * math.cos(a):.1f},{cy + (r * 0.8) * math.sin(a):.1f}" for a in angles]
        target_poly = f'<polygon points="{" ".join(target_points)}" fill="rgba(56, 189, 248, 0.08)" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="4,4" />\n'

        # Actual Company Polygon
        actual_points = []
        dots = ""
        for i, a in enumerate(angles):
            score_ratio = min(1.0, max(0.0, domains[i].score / 100.0))
            px = cx + (r * score_ratio) * math.cos(a)
            py = cy + (r * score_ratio) * math.sin(a)
            actual_points.append(f"{px:.1f},{py:.1f}")
            dots += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#38BDF8" stroke="#0F172A" stroke-width="2" />\n'

        actual_poly = f'<polygon points="{" ".join(actual_points)}" fill="rgba(6, 182, 212, 0.35)" stroke="#06B6D4" stroke-width="2.5" />\n'

        svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  {web_lines}
  {axis_lines}
  {target_poly}
  {actual_poly}
  {dots}
  {labels_svg}
  <text x="{width - 80}" y="{height - 10}" fill="#38BDF8" font-size="10" font-weight="600">--- Target (80%)</text>
  <text x="10" y="{height - 10}" fill="#06B6D4" font-size="10" font-weight="700">━ Acme Score</text>
</svg>"""
        return svg

    @staticmethod
    def generate_maturity_gauge(score: float, width: int = 500, height: int = 50) -> str:
        score_pos = min(width - 10, max(10, (score / 100.0) * width))

        svg = f"""<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E11D48" />
      <stop offset="30%" stop-color="#F59E0B" />
      <stop offset="55%" stop-color="#3B82F6" />
      <stop offset="80%" stop-color="#10B981" />
      <stop offset="100%" stop-color="#06B6D4" />
    </linearGradient>
  </defs>

  <!-- Track Background -->
  <rect x="0" y="15" width="{width}" height="14" rx="7" fill="url(#gaugeGrad)" opacity="0.85" />
  
  <!-- Tiers Dividers -->
  <line x1="{width * 0.30}" y1="15" x2="{width * 0.30}" y2="29" stroke="#0F172A" stroke-width="2" />
  <line x1="{width * 0.50}" y1="15" x2="{width * 0.50}" y2="29" stroke="#0F172A" stroke-width="2" />
  <line x1="{width * 0.70}" y1="15" x2="{width * 0.70}" y2="29" stroke="#0F172A" stroke-width="2" />
  <line x1="{width * 0.90}" y1="15" x2="{width * 0.90}" y2="29" stroke="#0F172A" stroke-width="2" />

  <!-- Tier Labels -->
  <text x="{width * 0.15}" y="42" text-anchor="middle" fill="#94A3B8" font-size="10">Initial</text>
  <text x="{width * 0.40}" y="42" text-anchor="middle" fill="#94A3B8" font-size="10">Developing</text>
  <text x="{width * 0.60}" y="42" text-anchor="middle" fill="#94A3B8" font-size="10">Managed</text>
  <text x="{width * 0.80}" y="42" text-anchor="middle" fill="#94A3B8" font-size="10">Advanced</text>
  <text x="{width * 0.95}" y="42" text-anchor="middle" fill="#94A3B8" font-size="10">Trusted</text>

  <!-- Pointer Pin -->
  <polygon points="{score_pos - 6},2 {score_pos + 6},2 {score_pos},12" fill="#38BDF8" />
  <circle cx="{score_pos}" cy="22" r="6" fill="#38BDF8" stroke="#0F172A" stroke-width="2" />
</svg>"""
        return svg
