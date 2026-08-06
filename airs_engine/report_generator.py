"""
AIRS Report Generator Module (LLM Enhanced)
Aggregates assessment scoring objects into structured report data dicts,
utilizing LLMSynthesizer for executive summary generation.
"""

from typing import Dict, Any, List
from .mapper import AIRSAssessmentObject
from .scoring import ScoringReport
from .chart_generator import SVGChartGenerator
from .llm_synthesizer import LLMSynthesizer

class AIReportGenerator:
    @staticmethod
    def generate_report_content(assessment: AIRSAssessmentObject, scoring: ScoringReport) -> Dict[str, Any]:
        company = assessment.company
        answers = assessment.answers
        adoption = assessment.ai_adoption

        # Generate LLM Narrative or Deterministic Fallback
        exec_summary = LLMSynthesizer.generate_narrative(
            company_name=company.name,
            industry=company.industry,
            company_size=company.company_size,
            score=scoring.overall_score,
            risk_level=scoring.risk_level,
            maturity=scoring.maturity_level,
            tools=adoption.tools,
            high_risk_flags=[{"system_name": f.system_name} for f in scoring.high_risk_flags],
            data_upload=answers.confidential_data_upload
        )

        # Generate Vector SVG Charts
        radar_svg = SVGChartGenerator.generate_radar_chart(scoring.domain_results, width=400, height=340)
        gauge_svg = SVGChartGenerator.generate_maturity_gauge(scoring.overall_score, width=500, height=50)

        # Phased Timelines
        phase_7 = [p for p in scoring.remediation_procedures if p.timeline == "Days 1–7"]
        phase_30 = [p for p in scoring.remediation_procedures if p.timeline == "Days 8–30"]
        phase_90 = [p for p in scoring.remediation_procedures if p.timeline == "Days 31–90"]

        # Templates
        templates = []
        for proc in scoring.remediation_procedures:
            if proc.starter_template:
                templates.append({
                    "title": proc.title,
                    "template": proc.starter_template
                })

        # EU AI Act Commentary
        hr_commentary = ""
        if scoring.high_risk_flags:
            flag_names = ", ".join([f.system_name for f in scoring.high_risk_flags])
            hr_commentary = (
                f"⚠️ **EU AI Act Regulatory High-Risk Notice:** Your organization reported using AI for automated evaluation ({flag_names}). "
                f"Under Annex III / Article 28 / Article 50 of the EU AI Act, these use cases trigger legal obligations including mandatory "
                f"risk management, technical documentation, logging, transparency notices, and human oversight."
            )

        return {
            "executive_summary": exec_summary,
            "radar_svg": radar_svg,
            "gauge_svg": gauge_svg,
            "high_risk_commentary": hr_commentary,
            "phase_7_days": phase_7,
            "phase_30_days": phase_30,
            "phase_90_days": phase_90,
            "policy_templates": templates,
            "disclaimer": (
                "DISCLAIMER: AI Risk Shield is an executive decision-support framework designed to assist organizations in identifying "
                "AI risks and establishing responsible AI governance practices. This report does not constitute binding legal representation."
            )
        }
