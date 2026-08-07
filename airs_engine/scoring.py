"""
AIRS Scoring Engine Module (Expanded Version with Ultimate Enterprise Rules)
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

        if answers.ai_policy_status in ["Yes", "Tak"]:
            gov_score += 60.0
        elif answers.ai_policy_status in ["Currently being prepared", "Informal guidelines exist, but no official written policy"]:
            gov_score += 30.0
            gov_recs.append("Formalize and publish the official written AI Usage Policy across all company departments.")
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

        if answers.ai_training_status in ["Regularly", "Regularly (Ongoing formal security & prompt governance training)"]:
            gov_score += 40.0
        elif answers.ai_training_status in ["Occasionally", "Occasionally (One-off workshops)"]:
            gov_score += 20.0
            gov_recs.append("Formalize regular AI safety and prompt engineering training for employees.")
        else:
            gov_recs.append("Introduce mandatory employee training on responsible AI usage and risk awareness.")

        # Shadow AI Evaluation
        shadow_lower = adoption.shadow_ai_control.lower()
        if "sso" in shadow_lower or "network" in shadow_lower or "edr" in shadow_lower or "endpoint" in shadow_lower:
            gov_score = min(100.0, gov_score + 10.0)
        elif "informal" in shadow_lower or "trust" in shadow_lower or "none" in shadow_lower:
            gov_recs.append("Implement technical controls (DNS/SSO/EDR) to detect and manage unmonitored Shadow AI tool usage.")

        gov_status = "Good" if gov_score >= 70 else ("Attention" if gov_score >= 40 else "Critical")
        domain_results["AI Governance"] = DomainResult(
            name="AI Governance",
            weight=0.20,
            score=gov_score,
            status=gov_status,
            finding=f"Policy: {answers.ai_policy_status}. Training: {answers.ai_training_status}. Shadow AI control: {adoption.shadow_ai_control}.",
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

        # Data Residency evaluation (RODO Art. 44-49)
        residency_lower = adoption.data_residency.lower()
        if "eu" in residency_lower or "unim" in residency_lower:
            privacy_score = min(100.0, privacy_score + 5.0)
        elif "us" in residency_lower or "global" in residency_lower or "not sure" in residency_lower or "unknown" in residency_lower:
            privacy_score -= 15.0
            privacy_recs.append("Verify Data Processing Agreements (DPA) and EU Standard Contractual Clauses (SCC) for US/Cloud AI servers.")

        if answers.confidential_data_upload:
            privacy_score -= 40.0
            details_lower = answers.confidential_data_details.lower()
            if any(k in details_lower for k in ["source code", "api key", "password", "ticket", "contract", "financial", "client", "customer"]):
                privacy_score -= 20.0
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
            finding=f"Licensing: {adoption.licensing_tier}. Hosting: {adoption.data_residency}. Uploads: {'Yes' if answers.confidential_data_upload else 'No'}.",
            recommendations=privacy_recs,
            procedures=privacy_procs
        )

        # --- 3. Human Oversight (Weight: 15%) ---
        oversight_score = 0.0
        oversight_recs = []
        oversight_procs = []
        rev_freq = answers.human_review_frequency.lower()

        if "always" in rev_freq or "zawsze" in rev_freq:
            oversight_score = 100.0
        elif "usually" in rev_freq or "zazwyczaj" in rev_freq:
            oversight_score = 70.0
            oversight_recs.append("Enforce 100% human-in-the-loop review for all customer-facing AI deliverables.")
        else:
            oversight_score = 35.0 if ("sometimes" in rev_freq or "czasami" in rev_freq) else 0.0
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
        if "custom" in role_lower or "api" in role_lower or "fine-tune" in role_lower or "rag" in role_lower:
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

        # Check Chatbot Article 50 Transparency Rule
        hr_lower = [h.lower() for h in answers.hr_automated_uses]
        if any("chatbot" in h or "messaging" in h or "obsługi klienta" in h for h in hr_lower):
            high_risk_flags.append(HighRiskFlag(
                system_name="Customer Chatbots / Automated Messaging",
                regulation_reference="EU AI Act Article 50 — Transparency Obligations for Interactive AI",
                severity="Medium",
                description="AI systems interacting directly with natural persons (chatbots) must inform users clearly that they are interacting with an AI system.",
                required_actions=[
                    "Add explicit disclosure notice: 'You are interacting with an AI assistant.'",
                    "Provide clear opt-out path to transfer users to a human support agent."
                ]
            ))

        # Check Annex III High Risk Categories
        if any(k in h for h in hr_lower for k in ["recruitment", "cv", "candidate", "evaluation", "credit", "rekrutacja", "scoring"]):
            high_risk_flags.append(HighRiskFlag(
                system_name="HR / Automated Employment & Scoring System",
                regulation_reference="EU AI Act Annex III — High-Risk AI Category (Employment & Credit)",
                severity="Critical",
                description="Using AI for candidate selection, CV screening, or employee performance evaluation falls directly under Annex III High-Risk classification.",
                required_actions=[
                    "Conduct Fundamental Rights Impact Assessment (FRIA).",
                    "Establish human oversight and bias mitigation logging.",
                    "Register system with competent EU national authority upon enforcement."
                ]
            ))

        if answers.past_incidents and "None" not in answers.past_incidents and "Brak" not in answers.past_incidents:
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

        if "public" in answers.public_ai_content.lower() or "tak" in answers.public_ai_content.lower():
            ip_recs.append("Verify copyright clearance and training data compliance for publicly published AI content (EU AI Act Art. 53).")

        ip_status = "Good" if ip_score >= 70 else ("Attention" if ip_score >= 40 else "Critical")
        domain_results["Intellectual Property"] = DomainResult(
            name="Intellectual Property",
            weight=0.10,
            score=ip_score,
            status=ip_status,
            finding=f"Selling AI deliverables: {'Yes' if answers.sells_ai_content else 'No'}. Disclosed in contracts: {answers.discloses_ai_in_contracts}. Public Deployment: {answers.public_ai_content}.",
            recommendations=ip_recs,
            procedures=ip_procs
        )

        # --- 6. HR & High-Risk Systems (Weight: 10%) ---
        hr_score = 100.0
        hr_recs = []
        if any(h for h in answers.hr_automated_uses if h not in ["None", "Żadne z powyższych"]):
            hr_score = 30.0
            hr_recs.append("Perform EU AI Act Annex III High-Risk compliance audit for HR/Automated decision tools.")

        hr_status = "Good" if hr_score >= 70 else ("Attention" if hr_score >= 40 else "Critical")
        domain_results["HR & High-Risk Systems"] = DomainResult(
            name="HR & High-Risk Systems",
            weight=0.10,
            score=hr_score,
            status=hr_status,
            finding=f"Automated HR/AI uses: {', '.join(answers.hr_automated_uses) if answers.hr_automated_uses else 'None'}.",
            recommendations=hr_recs,
            procedures=[]
        )

        # --- 7. AI Literacy & Operations (Weight: 10%) ---
        ops_score = 50.0
        if answers.ai_training_status in ["Regularly", "Regularly (Ongoing formal security & prompt governance training)"]:
            ops_score += 50.0
        elif answers.ai_training_status in ["Occasionally", "Occasionally (One-off workshops)"]:
            ops_score += 25.0

        ops_status = "Good" if ops_score >= 70 else ("Attention" if ops_score >= 40 else "Critical")
        domain_results["AI Literacy & Operations"] = DomainResult(
            name="AI Literacy & Operations",
            weight=0.10,
            score=ops_score,
            status=ops_status,
            finding=f"Active users: {adoption.active_users}. Training: {answers.ai_training_status}.",
            recommendations=[],
            procedures=[]
        )

        # Overall Score Calculation
        overall = sum(res.score * res.weight for res in domain_results.values())
        overall = round(max(0.0, min(100.0, overall)), 1)

        # Maturity Level
        if overall >= 85:
            maturity = "Trusted / Advanced"
            risk = "Low Risk"
        elif overall >= 65:
            maturity = "Defined / Operational"
            risk = "Moderate Risk"
        elif overall >= 40:
            maturity = "Ad-Hoc / Developing"
            risk = "High Risk"
        else:
            maturity = "Initial / Uncontrolled"
            risk = "Critical Risk"

        # Collect top recommendations
        top_recs = []
        for d in domain_results.values():
            for r in d.recommendations:
                top_recs.append({"domain": d.name, "recommendation": r})

        # Collect all remediation procedures
        for d in domain_results.values():
            all_procedures.extend(d.procedures)

        return ScoringReport(
            overall_score=overall,
            maturity_level=maturity,
            risk_level=risk,
            domain_results=domain_results,
            high_risk_flags=high_risk_flags,
            top_recommendations=top_recs[:5],
            remediation_procedures=all_procedures
        )
