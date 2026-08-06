"""
AIRS Report Generator Module (With Vector SVG Charts)
Generates comprehensive narrative content, detailed remediation procedures,
implementation timelines, ready-to-use policy templates, and vector SVG charts.
"""

from typing import Dict, Any, List
from .mapper import AIRSAssessmentObject
from .scoring import ScoringReport, RemediationProcedure
from .chart_generator import SVGChartGenerator

class AIReportGenerator:
    @staticmethod
    def generate_report_content(assessment: AIRSAssessmentObject, scoring: ScoringReport) -> Dict[str, Any]:
        company = assessment.company
        answers = assessment.answers
        adoption = assessment.ai_adoption

        # Executive Summary
        exec_summary = (
            f"This Responsible AI Risk Assessment report evaluates the artificial intelligence governance maturity of "
            f"**{company.name}** ({company.industry}, {company.company_size}). Based on our AIRS methodology, "
            f"{company.name} achieves an overall AI Governance Score of **{scoring.overall_score}/100**, "
            f"placing the organization at the **'{scoring.maturity_level}'** maturity level and classified as **'{scoring.risk_level}'**.\n\n"
            f"The evaluation identifies key operational strengths in active AI tool adoption ({', '.join(adoption.tools)}) and highlights "
            f"critical vulnerability areas in data protection, unmonitored confidential data upload, lack of formal policy governance, "
            f"and EU AI Act regulatory obligations."
        )

        # High Risk System Commentary
        if scoring.high_risk_flags:
            high_risk_text = (
                f"⚠️ **EU AI Act Regulatory High-Risk Notice:** Your organization reported using AI for automated human resources "
                f"and hiring evaluation ({', '.join([f.system_name for f in scoring.high_risk_flags])}). Under Annex III of the EU AI Act, "
                f"these use cases are legally classified as **High-Risk AI Systems**. High-risk deployments trigger strict compliance obligations, "
                f"including mandatory risk management procedures, technical logging, candidate transparency notices, and human override controls."
            )
        else:
            high_risk_text = (
                "✅ **EU AI Act Standard Classification:** Based on reported use cases, your current AI deployment does not involve high-risk "
                "biometric, critical infrastructure, or automated HR decision systems under Annex III of the EU AI Act. Continuous monitoring "
                "is recommended as new AI tools are adopted."
            )

        # Generate Vector SVG Charts
        radar_svg = SVGChartGenerator.generate_radar_chart(scoring.domain_results)
        gauge_svg = SVGChartGenerator.generate_maturity_gauge(scoring.overall_score)

        # Timeline-based Roadmap (7 Days, 30 Days, 90 Days)
        phase_7_days = [p for p in scoring.remediation_procedures if "7" in p.timeline or p.priority == "URGENT"]
        phase_30_days = [p for p in scoring.remediation_procedures if "30" in p.timeline and p not in phase_7_days]
        phase_90_days = [p for p in scoring.remediation_procedures if "90" in p.timeline and p not in phase_7_days and p not in phase_30_days]

        # Policy & Template Snippets
        templates = []
        for p in scoring.remediation_procedures:
            if p.starter_template:
                templates.append({
                    "title": p.title,
                    "template": p.starter_template
                })

        # Disclaimer
        disclaimer = (
            "IMPORTANT NOTICE: AI Risk Shield is a decision-support platform designed to help organizations evaluate operational AI risks "
            "and establish responsible AI governance practices. This assessment report is generated based on information provided by the organization "
            "and does not constitute formal legal counsel, regulatory certification, or a guarantee of compliance with EU AI Act, GDPR, or "
            "other statutory frameworks. Organizations should consult qualified legal counsel for binding regulatory opinions."
        )

        return {
            "executive_summary": exec_summary,
            "high_risk_commentary": high_risk_text,
            "radar_svg": radar_svg,
            "gauge_svg": gauge_svg,
            "remediation_procedures": scoring.remediation_procedures,
            "phase_7_days": phase_7_days,
            "phase_30_days": phase_30_days,
            "phase_90_days": phase_90_days,
            "policy_templates": templates,
            "disclaimer": disclaimer
        }
