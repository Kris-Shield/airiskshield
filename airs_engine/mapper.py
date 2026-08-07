"""
AIRS Data Mapper Module (Multilingual Enterprise Version)
Converts raw Tally webhook submissions into standardized AIRS assessment objects.
Supports live Tally option ID resolution, fuzzy label matching, preferred report language, and multi-language form fields.
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class CompanyProfile:
    name: str = "Unknown Company"
    email: str = "unknown@example.com"
    country: str = "Poland"
    industry: str = "General"
    company_size: str = "1-9 employees"
    preferred_language: str = "en" # en, de, fr, nl, pl, es, it

@dataclass
class AIAdoptionProfile:
    tools: List[str] = field(default_factory=list)
    licensing_tier: str = "Mostly personal free accounts" # 100% Enterprise, Mix, Free, Unsure
    active_users: str = "1-5"
    ai_role_architecture: str = "Off-the-shelf apps only" # Custom API/RAG, Fine-tuning, Off-the-shelf
    data_residency: str = "Unknown / Provider Default" # EU Data Center, US Cloud, Unknown
    shadow_ai_control: str = "None / Trust" # SSO/VPN Block, EDR Monitoring, Policy Only, None

@dataclass
class AssessmentAnswers:
    confidential_data_upload: bool = False
    confidential_data_details: str = ""
    human_review_frequency: str = "Always"
    ai_policy_status: str = "No"
    ai_training_status: str = "No"
    hr_automated_uses: List[str] = field(default_factory=list)
    sells_ai_content: bool = False
    discloses_ai_in_contracts: str = "No"
    public_ai_content: str = "No" # Published Publicly, Internal Only, No
    past_incidents: List[str] = field(default_factory=list)
    biggest_concern: str = "EU AI Act"
    consultation_requested: bool = False

@dataclass
class AIRSAssessmentObject:
    response_id: str
    submission_time: str
    company: CompanyProfile
    ai_adoption: AIAdoptionProfile
    answers: AssessmentAnswers

class TallyDataMapper:
    @staticmethod
    def _normalize_string(text: str) -> str:
        if not text:
            return ""
        # Strip HTML tags & non-alphanumeric chars for matching
        clean = re.sub(r'<[^>]+>', '', str(text))
        return re.sub(r'[^a-zA-Z0-9]', '', clean).lower()

    @staticmethod
    def _resolve_field_value(f: Dict[str, Any]) -> Any:
        val = f.get("value")
        options = f.get("options", [])

        if val is None:
            return None

        # Map option IDs to human readable text if options array exists
        option_map = {}
        if isinstance(options, list):
            for opt in options:
                if isinstance(opt, dict) and "id" in opt and "text" in opt:
                    option_map[opt["id"]] = opt["text"]

        if isinstance(val, list):
            resolved_list = []
            for item in val:
                if isinstance(item, str) and item in option_map:
                    resolved_list.append(option_map[item])
                else:
                    resolved_list.append(str(item))
            return resolved_list
        elif isinstance(val, str) and val in option_map:
            return option_map[val]
        return val

    @staticmethod
    def parse_tally_submission(raw_json: Dict[str, Any]) -> AIRSAssessmentObject:
        data = raw_json.get("data", raw_json)
        response_id = data.get("responseId", "resp_mock_001")
        submission_time = raw_json.get("createdAt", "2026-08-06T16:00:00.000Z")

        fields = data.get("fields", [])
        
        # Build normalized lookup dictionary
        normalized_map = {}
        exact_key_map = {}

        for f in fields:
            label = f.get("label", "").strip()
            key = f.get("key", "").strip()
            val = TallyDataMapper._resolve_field_value(f)

            if key:
                exact_key_map[key] = val
            if label:
                norm_label = TallyDataMapper._normalize_string(label)
                normalized_map[norm_label] = val
                exact_key_map[label] = val

        def get_val(keywords: List[str], default_val: Any = None) -> Any:
            # 1. Try exact keys/labels first
            for kw in keywords:
                if kw in exact_key_map and exact_key_map[kw] is not None:
                    return exact_key_map[kw]
            
            # 2. Try normalized fuzzy label matching
            for kw in keywords:
                norm_kw = TallyDataMapper._normalize_string(kw)
                for norm_label, val in normalized_map.items():
                    if norm_kw in norm_label and val is not None:
                        return val

            return default_val

        # 1. Company Name
        company_name_val = get_val([
            "Company Name", "company_name", "nazwa firmy", "company"
        ], "Acme Software Solutions Ltd.")

        # 2. Corporate Email
        corporate_email_val = get_val([
            "Corporate Email", "corporate_email", "email", "e-mail", "służbowy adres email"
        ], "airiskshield@gmail.com")

        # 3. Country
        country_val = get_val([
            "Country of Operation", "country", "kraj", "primary country"
        ], "Poland")

        # 4. Industry
        industry_val = get_val([
            "Industry", "Industry Sector", "branża", "sektor"
        ], "Software Development & IT")

        # 5. Company Size
        company_size_val = get_val([
            "Company Size", "company_size", "wielkość firmy", "liczba pracowników"
        ], "10-49 employees")

        # 6. Preferred Language
        pref_lang_raw = str(get_val([
            "Preferred Report Language", "preferred_language", "język raportu", "language"
        ], "English")).lower()

        lang_code = "en"
        if "pol" in pref_lang_raw or "pl" in pref_lang_raw:
            lang_code = "pl"
        elif "ger" in pref_lang_raw or "deu" in pref_lang_raw or "de" in pref_lang_raw:
            lang_code = "de"
        elif "fre" in pref_lang_raw or "fra" in pref_lang_raw or "fr" in pref_lang_raw:
            lang_code = "fr"
        elif "dut" in pref_lang_raw or "nld" in pref_lang_raw or "nl" in pref_lang_raw:
            lang_code = "nl"
        elif "spa" in pref_lang_raw or "esp" in pref_lang_raw or "es" in pref_lang_raw:
            lang_code = "es"
        elif "ita" in pref_lang_raw or "it" in pref_lang_raw:
            lang_code = "it"

        company = CompanyProfile(
            name=str(company_name_val).strip(),
            email=str(corporate_email_val).strip(),
            country=str(country_val).strip(),
            industry=str(industry_val).strip(),
            company_size=str(company_size_val).strip(),
            preferred_language=lang_code
        )

        # AI Tools
        tools_val = get_val([
            "Which AI tools does your company currently use?", "ai_tools", "narzędzia ai", "tools"
        ], ["ChatGPT", "Claude", "Microsoft Copilot"])
        tools = [t.strip() for t in tools_val] if isinstance(tools_val, list) else [t.strip() for t in str(tools_val).split(",")]

        # Licensing Tier
        licensing_val = get_val([
            "Do employees use company-managed paid subscriptions or personal free accounts?",
            "ai_licensing_tier", "subskrypcji firmowych", "licencjonowanie"
        ], "Mostly personal free accounts")

        # Active Users
        active_users_val = get_val([
            "Approximately how many employees actively use AI every week?",
            "active_users", "aktywnie korzysta", "użytkowników"
        ], "6-20")

        # AI Role / Architecture
        ai_role_val = get_val([
            "Does your company develop custom AI software, fine-tune models, or integrate LLM APIs into your products?",
            "ai_role_architecture", "custom ai", "llm api", "bazy rag"
        ], "Yes, we build custom AI features / RAG / API integrations into our products")

        # Data Residency
        residency_val = get_val([
            "Where are your primary AI data processing servers hosted?",
            "data_residency", "serwery", "jurysdykcja"
        ], "US Cloud Data Centers")

        # Shadow AI Control
        shadow_val = get_val([
            "How does your organization detect or control unauthorized AI tool usage (Shadow AI)?",
            "shadow_ai_control", "shadow ai", "nieautoryzowane"
        ], "Informal policy guidance (Trust-based, no technical blocks)")

        ai_adoption = AIAdoptionProfile(
            tools=tools,
            licensing_tier=str(licensing_val),
            active_users=str(active_users_val),
            ai_role_architecture=str(ai_role_val),
            data_residency=str(residency_val),
            shadow_ai_control=str(shadow_val)
        )

        # Confidential Uploads
        conf_upload = get_val([
            "Do employees upload confidential customer or company information into AI tools?",
            "confidential_data_upload", "poufne dane", "upload"
        ], "Yes")
        conf_upload_bool = str(conf_upload).strip().lower() in ["yes", "true", "tak"]

        conf_details_val = get_val([
            "If yes, what type of information is uploaded?",
            "confidential_data_details", "jakie rodzaje informacji"
        ], "Source code, client API keys, contracts, customer support tickets.")

        human_rev_val = get_val([
            "Are AI-generated outputs reviewed before being delivered to customers?",
            "Are AI-generated outputs reviewed by humans before being delivered to customers?",
            "human_review", "weryfikowane przez człowieka"
        ], "Usually")

        ai_policy_val = get_val([
            "Does your company have an official AI Usage Policy?",
            "ai_policy", "polityka korzystania z ai"
        ], "No")

        ai_train_val = get_val([
            "Do employees receive AI-related training?",
            "ai_training", "szkolenia"
        ], "No")

        hr_uses_val = get_val([
            "Is AI used for any of the following?",
            "ai_hr_automation", "zastosowań"
        ], ["Recruitment", "CV Screening"])
        hr_uses = [h.strip() for h in hr_uses_val] if isinstance(hr_uses_val, list) else [h.strip() for h in str(hr_uses_val).split(",")]

        sells_content_val = get_val([
            "Do you sell AI-generated content or code to customers?",
            "Do you sell AI-generated content, graphics, or code to commercial customers?",
            "sell_ai_content", "sprzedają państwo treści"
        ], "Yes")
        sells_content_bool = str(sells_content_val).strip().lower() in ["yes", "true", "tak"]

        discloses_val = get_val([
            "If yes, do your contracts disclose AI assistance?",
            "If yes, do your client contracts explicitly disclose AI assistance and define IP ownership?",
            "contract_disclose_ai", "umowy z klientami"
        ], "No")

        public_ai_val = get_val([
            "Does your company publicly publish or deploy AI-generated content or code?",
            "public_ai_content", "publikujemy materiały"
        ], "Yes, publicly deployed in marketing materials or software applications")

        incidents_val = get_val([
            "Has your company experienced any AI-related incidents during the last 12 months?",
            "ai_incidents", "incydenty"
        ], ["AI Hallucination", "Customer Complaint"])
        incidents = [i.strip() for i in incidents_val] if isinstance(incidents_val, list) else [i.strip() for i in str(incidents_val).split(",")]

        concern_val = get_val([
            "What is currently your biggest AI concern?",
            "biggest_concern", "największą obawą"
        ], "EU AI Act")

        consult_val = get_val([
            "Would you like a complimentary 30-minute consultation to discuss your report?",
            "Would you like a complimentary 30-minute consultation with an AI Governance Advisor to review your report?",
            "consultation_request", "konsultacji"
        ], "Yes")
        consult_bool = str(consult_val).strip().lower() in ["yes", "true", "tak"]

        answers = AssessmentAnswers(
            confidential_data_upload=conf_upload_bool,
            confidential_data_details=str(conf_details_val),
            human_review_frequency=str(human_rev_val),
            ai_policy_status=str(ai_policy_val),
            ai_training_status=str(ai_train_val),
            hr_automated_uses=hr_uses,
            sells_ai_content=sells_content_bool,
            discloses_ai_in_contracts=str(discloses_val),
            public_ai_content=str(public_ai_val),
            past_incidents=incidents,
            biggest_concern=str(concern_val),
            consultation_requested=consult_bool
        )

        return AIRSAssessmentObject(
            response_id=response_id,
            submission_time=submission_time,
            company=company,
            ai_adoption=ai_adoption,
            answers=answers
        )
