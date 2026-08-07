"""
AIRS Data Mapper Module (Ultimate Multilingual Enterprise Version)
Converts raw Tally webhook submissions into standardized AIRS assessment objects.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class CompanyProfile:
    name: str = "Unknown Company"
    email: str = "unknown@example.com"
    country: str = "Poland"
    industry: str = "General"
    company_size: str = "1-9 employees"

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
    def parse_tally_submission(raw_json: Dict[str, Any]) -> AIRSAssessmentObject:
        data = raw_json.get("data", raw_json)
        response_id = data.get("responseId", "resp_mock_001")
        submission_time = raw_json.get("createdAt", "2026-08-06T16:00:00.000Z")

        fields = data.get("fields", [])
        field_map = {}
        for f in fields:
            label = f.get("label", "").strip()
            key = f.get("key", "").strip()
            val = f.get("value")
            if label:
                field_map[label] = val
            if key:
                field_map[key] = val

        # Company Info
        company = CompanyProfile(
            name=str(field_map.get("Company Name") or field_map.get("company_name") or "Acme Corp"),
            email=str(field_map.get("Corporate Email") or field_map.get("corporate_email") or "contact@example.com"),
            country=str(field_map.get("Country of Operation") or field_map.get("country") or "Poland"),
            industry=str(field_map.get("Industry") or field_map.get("industry") or "Technology"),
            company_size=str(field_map.get("Company Size") or field_map.get("company_size") or "10-49 employees")
        )

        # AI Adoption
        tools_val = field_map.get("Which AI tools does your company currently use?") or field_map.get("ai_tools") or []
        tools = [t.strip() for t in tools_val.split(",")] if isinstance(tools_val, str) else list(tools_val)

        licensing = str(field_map.get("Do employees use company-managed paid subscriptions or personal free accounts?") or field_map.get("ai_licensing_tier") or "Mostly personal free accounts")

        ai_role = str(field_map.get("Does your company develop custom AI software, fine-tune models, or integrate LLM APIs into your products?") or field_map.get("ai_role_architecture") or "Off-the-shelf apps only")

        data_residency = str(field_map.get("Where are your primary AI data processing servers hosted?") or field_map.get("data_residency") or "Unknown / Provider Default")

        shadow_control = str(field_map.get("How does your organization detect or control unauthorized AI tool usage (Shadow AI)?") or field_map.get("shadow_ai_control") or "None")

        ai_adoption = AIAdoptionProfile(
            tools=tools,
            licensing_tier=licensing,
            active_users=str(field_map.get("Approximately how many employees actively use AI every week?") or field_map.get("active_users") or "1-5"),
            ai_role_architecture=ai_role,
            data_residency=data_residency,
            shadow_ai_control=shadow_control
        )

        # Answers
        conf_upload = field_map.get("Do employees upload confidential customer or company information into AI tools?") or field_map.get("confidential_data_upload")
        conf_upload_bool = str(conf_upload).strip().lower() in ["yes", "true", "tak"]

        conf_details = str(field_map.get("If yes, what type of information is uploaded?") or field_map.get("confidential_data_details") or "")
        human_rev = str(field_map.get("Are AI-generated outputs reviewed before being delivered to customers?") or field_map.get("human_review") or "Usually")
        ai_pol = str(field_map.get("Does your company have an official AI Usage Policy?") or field_map.get("ai_policy") or "No")
        ai_train = str(field_map.get("Do employees receive AI-related training?") or field_map.get("ai_training") or "No")

        hr_uses_val = field_map.get("Is AI used for any of the following?") or field_map.get("ai_hr_automation") or []
        hr_uses = [h.strip() for h in hr_uses_val.split(",")] if isinstance(hr_uses_val, str) else list(hr_uses_val)

        sells_content = field_map.get("Do you sell AI-generated content or code to customers?") or field_map.get("sell_ai_content")
        sells_content_bool = str(sells_content).strip().lower() in ["yes", "true", "tak"]

        discloses_contracts = str(field_map.get("If yes, do your contracts disclose AI assistance?") or field_map.get("contract_disclose_ai") or "No")

        public_ai = str(field_map.get("Does your company publicly publish or deploy AI-generated content or code?") or field_map.get("public_ai_content") or "No")

        incidents_val = field_map.get("Has your company experienced any AI-related incidents during the last 12 months?") or field_map.get("ai_incidents") or []
        incidents = [i.strip() for i in incidents_val.split(",")] if isinstance(incidents_val, str) else list(incidents_val)

        concern = str(field_map.get("What is currently your biggest AI concern?") or field_map.get("biggest_concern") or "EU AI Act")
        consult_val = field_map.get("Would you like a complimentary 30-minute consultation to discuss your report?") or field_map.get("consultation_request")
        consult_bool = str(consult_val).strip().lower() in ["yes", "true", "tak"]

        answers = AssessmentAnswers(
            confidential_data_upload=conf_upload_bool,
            confidential_data_details=conf_details,
            human_review_frequency=human_rev,
            ai_policy_status=ai_pol,
            ai_training_status=ai_train,
            hr_automated_uses=hr_uses,
            sells_ai_content=sells_content_bool,
            discloses_ai_in_contracts=discloses_contracts,
            public_ai_content=public_ai,
            past_incidents=incidents,
            biggest_concern=concern,
            consultation_requested=consult_bool
        )

        return AIRSAssessmentObject(
            response_id=response_id,
            submission_time=submission_time,
            company=company,
            ai_adoption=ai_adoption,
            answers=answers
        )
