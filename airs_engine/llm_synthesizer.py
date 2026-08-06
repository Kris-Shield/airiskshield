"""
AIRS LLM Narrative Synthesizer Module
Connects to OpenAI / Anthropic LLM APIs to generate bespoke executive summaries
and strategic governance commentary, with automatic deterministic fallback.
"""

import os
import json
import urllib.request
from typing import Dict, Any, Optional

class LLMSynthesizer:
    @staticmethod
    def generate_narrative(company_name: str, industry: str, company_size: str, score: float, risk_level: str, maturity: str, tools: list, high_risk_flags: list, data_upload: bool, advisor_notes: str = "") -> str:
        openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

        flags_text = ", ".join([f.get("system_name", "") for f in high_risk_flags]) if high_risk_flags else "None"
        tools_text = ", ".join(tools) if tools else "None"

        # 1. Try OpenAI API if key available
        if openai_key:
            try:
                prompt = f"""You are a Lead AI Governance Auditor at AI Risk Shield. Write a concise, professional 2-paragraph Executive Summary in Polish for the following audit client:

Company: {company_name} ({industry}, {company_size})
AIRS Score: {score}/100 | Risk Level: {risk_level} | Maturity: {maturity}
Active AI Tools: {tools_text}
Confidential Data Upload Reported: {"Yes" if data_upload else "No"}
EU AI Act High-Risk Flags: {flags_text}
Advisor Note: {advisor_notes if advisor_notes else "None"}

Requirements:
- Paragraph 1: State the overall score, maturity level, and key risk findings.
- Paragraph 2: Highlight priority actions regarding data loss prevention and EU AI Act compliance.
- Keep a professional, authoritative executive tone (Gartner/McKinsey style). Write purely in Polish."""

                payload = {
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are a senior AI Risk Governance consultant."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 350
                }

                req = urllib.request.Request(
                    "https://api.openai.com/v1/chat/completions",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {openai_key}",
                        "Content-Type": "application/json"
                    }
                )

                with urllib.request.urlopen(req, timeout=8) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    text = res_data["choices"][0]["message"]["content"].strip()
                    if text:
                        return text
            except Exception as e:
                # Fallback on any API error or timeout
                pass

        # 2. Structured Fallback (Deterministic Generation)
        flag_commentary = f" Szczególną uwagę należy zwrócić na wykryte systemy wysokiego ryzyka EU AI Act: {flags_text}." if high_risk_flags else ""
        upload_commentary = " Zaobserwowano ryzyko nieautoryzowanego przesyłania danych poufnych do publicznych modeli AI." if data_upload else ""

        notes_commentary = f" Uwaga ekspercka audytora: {advisor_notes}" if advisor_notes else ""

        return (
            f"Raport audytowy AI Risk Shield ocenia poziom dojrzałości zarządzania sztuczną inteligencją w firmie **{company_name}** ({industry}, {company_size}). "
            f"Na podstawie metodyki AIRS organizacja uzyskała łączny wynik **{score}/100**, co klasyfikuje ją na poziomie dojrzałości **'{maturity}'** oraz w kategorii ryzyka **'{risk_level}'**.\n\n"
            f"Zidentyfikowano kluczowe obszary podatności operacyjnej przy korzystaniu z narzędzi {tools_text}.{upload_commentary}{flag_commentary}{notes_commentary} "
            f"Rekomendowane jest natychmiastowe wdrożenie 7-dniowego planu naprawczego obejmującego Politykę AI, procedury HITL oraz anonimizację promptów."
        )
