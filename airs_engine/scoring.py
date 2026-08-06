"""
AIRS Scoring Engine Module (Expanded Version with Licensing & Provider Rules)
Computes domain scores, overall AIRS score, maturity level, risk level,
EU AI Act High-Risk flags, Provider vs Deployer roles, and remediation protocols.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .mapper import AIRSAssessmentObject

@dataclass
class RemediationProcedure:
    title: str
    timeline: str
    priority: str
    objective: str
    steps: List[str]
    starter_template: Optional[str] = None

@dataclass
class DomainResult:
    name: str
    weight: float
    score: float
    status: str
    finding: str
    recommendations: List[str]
    procedures: List[RemediationProcedure] = field(default_factory=list)

@dataclass
class HighRiskFlag:
    system_name: str
    regulation_reference: str
    severity: str
    description: str
    required_actions: List[str]

@dataclass
class ScoringReport:
    overall_score: float
    maturity_level: str
    risk_level: str
    domain_results: Dict[str, DomainResult]
    high_risk_flags: List[HighRiskFlag]
    top_recommendations: List[Dict[str, str]]
    remediation_procedures: List[RemediationProcedure]

class AIRSScoringEngine:
    @staticmethod
    def evaluate(assessment: AIRSAssessmentObject) -> ScoringReport:
        answers = assessment.answers
        company = assessment.company
        adoption = assessment.ai_adoption

        domain_results: Dict[str, DomainResult] = {}
        high_risk_flags: List[HighRiskFlag] = []
        all_procedures: List[RemediationProcedure] = []

        # --- 1. AI Governance (Weight: 20%) ---
        gov_score = 0.0
        gov_recs = []
        gov_procs = []

        if answers.ai_policy_status == "Yes":
            gov_score += 60.0
        elif answers.ai_policy_status == "Currently being prepared":
            gov_score += 30.0
            gov_recs.append("Finalize and publish the draft AI Policy across all company departments.")
        else:
            gov_recs.append("Draft and implement an official Corporate AI Usage Policy immediately.")
            gov_procs.append(RemediationProcedure(
                title="Establish Corporate AI Usage Policy",
                timeline="Days 1–7",
                priority="URGENT",
                objective="Create clear operational rules defining approved AI tools, data restrictions, and employee obligations.",
                steps=[
                    "Draft the official Acceptable Use Policy (AUP) for Artificial Intelligence.",
                    "Categorize tools into Approved (Whitelisted), Conditional, and Prohibited (Blacklisted).",
                    "Distribute policy to current employees and require signed acknowledgment."
                ],
                starter_template="""POLICY SNIPPET — CORPORATE AI USAGE POLICY v1.0
1. APPROVED TOOLS: Only company-provided enterprise AI tools with Zero Data Retention are permitted.
2. CONFIDENTIALITY: Uploading personal data (PII), customer credentials, or source code into public free models is strictly PROHIBITED.
3. HUMAN OVERSIGHT: Every employee is personally accountable for verifying AI output before client delivery."""
            ))

        if answers.ai_training_status == "Regularly":
            gov_score += 40.0
        elif answers.ai_training_status == "Occasionally":
            gov_score += 20.0
            gov_recs.append("Formalize regular AI safety and prompt engineering training for employees.")
        else:
            gov_recs.append("Introduce mandatory employee training on responsible AI usage and risk awareness.")

        gov_status = "Good" if gov_score >= 70 else ("Attention" if gov_score >= 40 else "Critical")
        domain_results["AI Governance"] = DomainResult(
            name="AI Governance",
            weight=0.20,
            score=gov_score,
            status=gov_status,
            finding=f"Policy status: {answers.ai_policy_status}. Employee training: {answers.ai_training_status}.",
            recommendations=gov_recs,
            procedures=gov_procs
        )

        # --- 2. Data Protection & Privacy (Weight: 25%) ---
        privacy_score = 100.0
        privacy_recs = []
        privacy_procs = []

        # Account licensing tier evaluation
        licensing_lower = adoption.licensing_tier.lower()
        if "100%" in licensing_lower or "enterprise" in licensing_lower:
            privacy_score += 15.0 # Bonus for company ZDR
        elif "free" in licensing_lower or "personal" in licensing_lower:
            privacy_score -= 25.0
            privacy_recs.append("Migrate employees from personal free accounts (which train on user prompts) to Enterprise Team subscriptions with Zero Data Retention.")

        if answers.confidential_data_upload:
            privacy_score -= 50.0
            details_lower = answers.confidential_data_details.lower()
            if any(k in details_lower for k in ["source code", "api key", "password", "ticket", "contract", "financial", "client", "customer"]):
                privacy_score -= 25.0
                privacy_recs.append("Stop uploading sensitive customer data, source code, or API keys into public AI models.")
                privacy_procs.append(RemediationProcedure(
                    title="Data Loss Prevention (DLP) & Anonymization Protocol",
                    timeline="Days 1–7",
                    priority="URGENT",
                    objective="Prevent unauthorized transmission of customer PII, source code, and API keys to third-party LLM providers.",
                    steps=[
                        "Issue immediate security bulletin pausing un-sanitized client code and contract uploads.",
                        "Enforce Enterprise Team plans with Zero Data Retention (ZDR).",
                        "Implement automated prompt scrubbing prior to LLM submission."
                    ],
                    starter_template="""ANONYMIZATION CHECKLIST:
[ ] Strip customer names, email addresses, and tax IDs.
[ ] Replace real financial figures with placeholders ([AMOUNT_X]).
[ ] Strip secret tokens, passwords, and private API keys from code snippets."""
                ))

        privacy_status = "Good" if privacy_score >= 70 else ("Attention" if privacy_score >= 40 else "Critical")
        domain_results["Data Protection & Privacy"] = DomainResult(
            name="Data Protection & Privacy",
            weight=0.25,
            score=max(0.0, min(100.0, privacy_score)),
            status=privacy_status,
            finding=f"Licensing: {adoption.licensing_tier}. Uploads: {'Yes' if answers.confidential_data_upload else 'No'}.",
            recommendations=privacy_recs,
            procedures=privacy_procs
        )

        # --- 3. Human Oversight (Weight: 15%) ---
        oversight_score = 0.0
        oversight_recs = []
        oversight_procs = []
        rev_freq = answers.human_review_frequency.lower()

        if "always" in rev_freq:
            oversight_score = 100.0
        elif "usually" in rev_freq:
            oversight_score = 70.0
            oversight_recs.append("Enforce 100% human-in-the-loop review for all customer-facing AI deliverables.")
        else:
            oversight_score = 35.0 if "sometimes" in rev_freq else 0.0
            oversight_recs.append("URGENT: Establish mandatory human oversight for AI deliverables to eliminate unverified AI output liability.")
            oversight_procs.append(RemediationProcedure(
                title="Human-in-the-Loop (HITL) Output Verification Procedure",
                timeline="Days 1–7",
                priority="URGENT",
                objective="Eliminate legal liability caused by unverified AI hallucinations or errors delivered to clients.",
                steps=[
                    "Designate responsible Human Approvers for each department.",
                    "Establish pre-release verification checklist (Fact Check, Security Audit).",
                    "Require sign-off documentation for customer deliverables."
                ],
                starter_template="""HUMAN REVIEW SIGN-OFF:
Project: ____________________ Reviewer: __________________________
Checklist: [x] Fact Verification  [x] Security Audit  [x] IP Check
Approval Signature: ______________________ Date: _________"""
            ))

        oversight_status = "Good" if oversight_score >= 70 else ("Attention" if oversight_score >= 40 else "Critical")
        domain_results["Human Oversight"] = DomainResult(
            name="Human Oversight",
            weight=0.15,
            score=oversight_score,
            status=oversight_status,
            finding=f"Output review frequency: {answers.human_review_frequency}.",
            recommendations=oversight_recs,
            procedures=oversight_procs
        )

        # --- 4. Transparency & Technical Architecture (Weight: 10%) ---
        inc_score = 100.0
        inc_recs = []
        inc_procs = []

        # Technical Architecture Role (Provider vs Deployer)
        role_lower = adoption.ai_role_architecture.lower()
        if "custom" in role_lower or "api" in role_lower or "fine-tune" in role_lower:
            high_risk_flags.append(HighRiskFlag(
                system_name="AI Integration / Product Architecture",
                regulation_reference="EU AI Act Article 28 — Provider & Integrator Obligations",
                severity="High",
                description="Developing custom AI features, RAG, or integrating LLM APIs classifies your company as an AI Integrator/Provider under the EU AI Act, requiring technical documentation, logging, and security controls.",
                required_actions=[
                    "Maintain technical documentation for API data flows.",
                    "Store API keys securely in Vault / Secrets Manager.",
                    "Log all API prompts and model responses for auditing."
                ]
            ))
            inc_recs.append("Establish technical logging and secure secrets management for custom LLM API integrations.")

        if answers.past_incidents and "None" not in answers.past_incidents:
            inc_score = max(10.0, 100.0 - len(answers.past_incidents) * 30.0)

        inc_status = "Good" if inc_score >= 70 else ("Attention" if inc_score >= 40 else "Critical")
        domain_results["Transparency & Incidents"] = DomainResult(
            name="Transparency & Incidents",
            weight=0.10,
            score=inc_score,
            status=inc_status,
            finding=f"Architecture: {adoption.ai_role_architecture}. Incidents: {', '.join(answers.past_incidents) if answers.past_incidents else 'None'}.",
            recommendations=inc_recs,
            procedures=inc_procs
        )

        # --- 5. Intellectual Property (Weight: 10%) ---
        ip_score = 100.0
        ip_recs = []
        ip_procs = []

        if answers.sells_ai_content:
            if answers.discloses_ai_in_contracts.lower() not in ["yes", "tak"]:
                ip_score = 15.0 if answers.discloses_ai_in_contracts.lower() in ["no", "nie"] else 40.0
                ip_recs.append("Add clear AI assistance disclosure and IP ownership clauses in commercial client agreements.")
                ip_procs.append(RemediationProcedure(
                    title="Client Contract AI Disclosure & IP Clause Integration",
                    timeline="Days 8–30",
                    priority="HIGH",
                    objective="Ensure legal clarity regarding client IP ownership and disclosure of AI assistance in deliverables.",
                    steps=[
                        "Review Master Services Agreement (MSA) templates.",
                        "Insert standard AI Transparency & IP Warranty clauses."
                    ],
                    starter_template="""CONTRACT CLAUSE — AI ASSISTANCE DISCLOSURE:
"Provider may utilize AI tools (including code assistants) to support deliverables. All deliverables undergo human verification. Provider assigns all IP rights to Client." """
                ))

        ip_status = "Good" if ip_score >= 70 else ("Attention" if ip_score >= 40 else "Critical")
        domain_results["Intellectual Property"] = DomainResult(
            name="Intellectual Property",
            weight=0.10,
            score=ip_score,
            status=ip_status,
            finding=f"Commercial AI content: {'Yes' if answers.sells_ai_content else 'No'}. Contract disclosure: {answers.discloses_ai_in_contracts}.",
            recommendations=ip_recs,
            procedures=ip_procs
        )

        # --- 6. HR & High-Risk Systems (Weight: 10%) ---
        hr_score = 100.0
        hr_recs = []
        hr_procs = []
        hr_uses = [u for u in answers.hr_automated_uses if u.strip().lower() not in ["none", "brak"]]

        if hr_uses:
            hr_score = 10.0
            for use in hr_uses:
                if "chatbot" in use.lower() or "customer support" in use.lower():
                    high_risk_flags.append(HighRiskFlag(
                        system_name="AI Customer Support Chatbot",
                        regulation_reference="EU AI Act Article 50 — Transparency Obligation for AI Systems",
                        severity="High",
                        description="Using AI for automated customer interaction requires clear disclosure informing users that they are interacting with an AI system.",
                        required_actions=["Implement clear AI chatbot transparency notice."]
                    ))
                else:
                    high_risk_flags.append(HighRiskFlag(
                        system_name=f"AI in {use}",
                        regulation_reference="EU AI Act — Annex III (High-Risk AI Systems)",
                        severity="Critical",
                        description=f"Using AI for '{use}' triggers High-Risk classification under Annex III. Requires risk management, bias testing, and human override.",
                        required_actions=["Perform bias testing.", "Provide candidate disclosure notice."]
                    ))

            hr_recs.append(f"Conduct formal EU AI Act High-Risk assessment for automated systems in: {', '.join(hr_uses)}.")
            hr_procs.append(RemediationProcedure(
                title="EU AI Act High-Risk Governance Framework (HR & Customer Chatbots)",
                timeline="Days 31–90",
                priority="URGENT",
                objective="Achieve full compliance with EU AI Act obligations for HR tools and automated chatbots.",
                steps=[
                    "Establish Risk Management System (Article 9) for HR screening tools.",
                    "Perform bias testing to prevent discriminatory filtering.",
                    "Implement candidate and chatbot transparency disclosures (Article 50)."
                ],
                starter_template="""CANDIDATE DISCLOSURE NOTICE (EU AI ACT ART. 50):
"Please note that Acme Software utilizes AI-assisted screening tools. All final hiring decisions are made exclusively by human recruiters. You have the right to request human review of your application." """
            ))

        hr_status = "Good" if hr_score >= 70 else "Critical"
        domain_results["HR & High-Risk Systems"] = DomainResult(
            name="HR & High-Risk Systems",
            weight=0.10,
            score=hr_score,
            status=hr_status,
            finding=f"Automated use cases: {', '.join(hr_uses) if hr_uses else 'None'}.",
            recommendations=hr_recs,
            procedures=hr_procs
        )

        # --- 7. AI Literacy & Operations (Weight: 10%) ---
        tools = adoption.tools
        ops_score = min(100.0, 60.0 + (20.0 if len(tools) >= 3 else 0.0) + (20.0 if answers.ai_training_status != "No" else 0.0))
        domain_results["AI Literacy & Operations"] = DomainResult(
            name="AI Literacy & Operations",
            weight=0.10,
            score=ops_score,
            status="Good" if ops_score >= 70 else "Attention",
            finding=f"Active tools: {', '.join(tools)}. User tier: {adoption.active_users}.",
            recommendations=[]
        )

        # Aggregate procedures
        for dom in domain_results.values():
            all_procedures.extend(dom.procedures)

        # Overall Score Calculation
        total_score = round(sum(res.score * res.weight for res in domain_results.values()), 1)

        maturity = "Trusted" if total_score >= 91 else ("Advanced" if total_score >= 71 else ("Managed" if total_score >= 51 else ("Developing" if total_score >= 31 else "Initial")))
        risk_level = "Low Risk" if total_score >= 76 else ("Moderate Risk" if total_score >= 56 else ("High Risk" if total_score >= 36 else "Critical Risk"))

        top_recs = []
        for dom_name, dom_res in domain_results.items():
            for rec in dom_res.recommendations:
                top_recs.append({
                    "domain": dom_name,
                    "priority": "Critical" if dom_res.status == "Critical" else ("High" if dom_res.status == "Attention" else "Medium"),
                    "action": rec
                })

        return ScoringReport(
            overall_score=total_score,
            maturity_level=maturity,
            risk_level=risk_level,
            domain_results=domain_results,
            high_risk_flags=high_risk_flags,
            top_recommendations=top_recs,
            remediation_procedures=all_procedures
        )
