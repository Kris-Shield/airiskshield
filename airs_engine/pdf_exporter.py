"""
AIRS Report Exporter Module (Visual Charts Version)
Renders and exports comprehensive HTML reports with SVG charts, remediation procedures,
timelines, and ready-to-use policy templates.
"""

import os
from typing import Dict, Any
from .mapper import AIRSAssessmentObject
from .scoring import ScoringReport
from .report_generator import AIReportGenerator

class ReportExporter:
    @staticmethod
    def export_html_report(assessment: AIRSAssessmentObject, scoring: ScoringReport, output_filepath: str) -> str:
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        template_path = os.path.join(template_dir, "report_template.html")

        with open(template_path, "r", encoding="utf-8") as f:
            html = f.read()

        report_content = AIReportGenerator.generate_report_content(assessment, scoring)
        risk_slug = scoring.risk_level.lower().replace(" ", "-")

        # 1. Domain Table Rows
        domain_rows_html = ""
        for dom_key, dom in scoring.domain_results.items():
            status_color = "#34D399" if dom.status == "Good" else ("#FBBF24" if dom.status == "Attention" else "#F87171")
            domain_rows_html += f"""
      <tr>
        <td><strong>{dom.name}</strong></td>
        <td>{int(dom.weight * 100)}%</td>
        <td><strong>{dom.score}</strong> / 100</td>
        <td><span style="font-weight: 700; color: {status_color};">{dom.status}</span></td>
        <td style="color: var(--text-muted); font-size: 13px;">{dom.finding}</td>
      </tr>
            """

        # 2. Detailed Procedures HTML
        procedures_html = ""
        for idx, proc in enumerate(scoring.remediation_procedures, 1):
            pill_class = "pill-urgent" if proc.priority == "URGENT" else "pill-high"
            steps_html = "".join([f"<li>{s}</li>" for s in proc.steps])
            procedures_html += f"""
  <div class="procedure-card">
    <div class="procedure-header">
      <div class="procedure-title">{idx}. {proc.title}</div>
      <div>
        <span class="{pill_class}">{proc.priority}</span>
        <span style="font-size: 11px; margin-left: 6px; color: #38BDF8; font-weight: 700;">{proc.timeline}</span>
      </div>
    </div>
    <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 10px;"><strong>Objective:</strong> {proc.objective}</p>
    <strong style="font-size: 13px; color: #CBD5E1;">Implementation Steps:</strong>
    <ol class="step-list">
      {steps_html}
    </ol>
  </div>
            """

        # 3. Timeline Columns HTML
        phase_7_html = "".join([f'<div style="font-size: 13px; margin-bottom: 8px; color: #F8FAFC;">• <strong>{p.title}</strong></div>' for p in report_content["phase_7_days"]])
        phase_30_html = "".join([f'<div style="font-size: 13px; margin-bottom: 8px; color: #F8FAFC;">• <strong>{p.title}</strong></div>' for p in report_content["phase_30_days"]])
        phase_90_html = "".join([f'<div style="font-size: 13px; margin-bottom: 8px; color: #F8FAFC;">• <strong>{p.title}</strong></div>' for p in report_content["phase_90_days"]])

        # 4. Policy Templates HTML
        templates_html = ""
        for t in report_content["policy_templates"]:
            templates_html += f"""
  <div class="card">
    <h4 style="font-size: 15px; color: #38BDF8; margin-bottom: 8px;">Template: {t['title']}</h4>
    <div class="template-box">{t['template']}</div>
  </div>
            """

        # 5. Alert Box
        alert_html = f"""
  <div class="alert-box">
    <strong style="color: #F87171;">⚠️ EU AI Act Regulatory High-Risk Alert</strong><br>
    {report_content['high_risk_commentary']}
  </div>
        """ if len(scoring.high_risk_flags) > 0 else ""

        # Perform replacement
        replacements = {
            "{{ response_id }}": str(assessment.response_id),
            "{{ submission_date }}": str(assessment.submission_time[:10]),
            "{{ overall_score }}": str(scoring.overall_score),
            "{{ risk_level }}": str(scoring.risk_level),
            "{{ risk_level_slug }}": risk_slug,
            "{{ maturity_level }}": str(scoring.maturity_level),
            "{{ company_name }}": str(assessment.company.name),
            "{{ corporate_email }}": str(assessment.company.email),
            "{{ country }}": str(assessment.company.country),
            "{{ industry }}": str(assessment.company.industry),
            "{{ company_size }}": str(assessment.company.company_size),
            "{{ ai_tools_list }}": ", ".join(assessment.ai_adoption.tools),
            "{{ executive_summary }}": report_content["executive_summary"],
            "{{ radar_svg }}": report_content["radar_svg"],
            "{{ gauge_svg }}": report_content["gauge_svg"],
            "{{ disclaimer }}": report_content["disclaimer"]
        }

        for key, val in replacements.items():
            html = html.replace(key, val)

        # Replace Blocks
        html = html.replace("{% if has_high_risk_flags %}\n  <div class=\"alert-box\">\n    <strong style=\"color: #F87171;\">⚠️ EU AI Act Regulatory High-Risk Alert</strong><br>\n    {{ high_risk_commentary }}\n  </div>\n  {% endif %}", alert_html)

        # Replace Domain Table
        table_marker = """      {% for dom_key, dom in domain_results.items() %}
      <tr>
        <td><strong>{{ dom.name }}</strong></td>
        <td>{{ (dom.weight * 100)|int }}%</td>
        <td><strong>{{ dom.score }}</strong> / 100</td>
        <td>
          <span style="font-weight: 700; color: {% if dom.status == 'Good' %}#34D399{% elif dom.status == 'Attention' %}#FBBF24{% else %}#F87171{% endif %};">
            {{ dom.status }}
          </span>
        </td>
        <td style="color: var(--text-muted); font-size: 13px;">{{ dom.finding }}</td>
      </tr>
      {% endfor %}"""
        html = html.replace(table_marker, domain_rows_html)

        # Replace Procedures Loop
        proc_marker = """  {% for proc in remediation_procedures %}
  <div class="procedure-card">
    <div class="procedure-header">
      <div class="procedure-title">{{ loop.index }}. {{ proc.title }}</div>
      <div>
        <span class="{% if proc.priority == 'URGENT' %}pill-urgent{% else %}pill-high{% endif %}">{{ proc.priority }}</span>
        <span style="font-size: 11px; margin-left: 6px; color: #38BDF8; font-weight: 700;">{{ proc.timeline }}</span>
      </div>
    </div>
    <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 10px;"><strong>Objective:</strong> {{ proc.objective }}</p>
    <strong style="font-size: 13px; color: #CBD5E1;">Implementation Steps:</strong>
    <ol class="step-list">
      {% for step in proc.steps %}
      <li>{{ step }}</li>
      {% endfor %}
    </ol>
  </div>
  {% endfor %}"""
        html = html.replace(proc_marker, procedures_html)

        # Replace Timeline Columns
        html = html.replace("""      {% for item in phase_7_days %}
      <div style="font-size: 13px; margin-bottom: 8px; color: #F8FAFC;">• <strong>{{ item.title }}</strong></div>
      {% endfor %}""", phase_7_html if phase_7_html else '<div style="font-size: 12px; color: #94A3B8;">No immediate actions required.</div>')

        html = html.replace("""      {% for item in phase_30_days %}
      <div style="font-size: 13px; margin-bottom: 8px; color: #F8FAFC;">• <strong>{{ item.title }}</strong></div>
      {% endfor %}""", phase_30_html if phase_30_html else '<div style="font-size: 12px; color: #94A3B8;">No 30-day actions required.</div>')

        html = html.replace("""      {% for item in phase_90_days %}
      <div style="font-size: 13px; margin-bottom: 8px; color: #F8FAFC;">• <strong>{{ item.title }}</strong></div>
      {% endfor %}""", phase_90_html if phase_90_html else '<div style="font-size: 12px; color: #94A3B8;">No 90-day actions required.</div>')

        # Replace Policy Templates
        template_marker = """  {% for t in policy_templates %}
  <div class="card">
    <h4 style="font-size: 15px; color: #38BDF8; margin-bottom: 8px;">Template: {{ t.title }}</h4>
    <div class="template-box">{{ t.template }}</div>
  </div>
  {% endfor %}"""
        html = html.replace(template_marker, templates_html)

        # Save HTML
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(html)

        return output_filepath
