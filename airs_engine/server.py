"""
AIRS Automated API & Webhook Server (Railway & Local Execution)
Receives live webhooks from Tally.so, calculates AIRS scores, generates vector reports,
dispatches customer emails, manages the Human Review queue, and serves customer deliverables.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

# Core Engine Imports
from .mapper import TallyDataMapper
from .scoring import AIRSScoringEngine
from .report_generator import AIReportGenerator
from .pdf_exporter import ReportExporter
from .email_sender import EmailSender

SUBMISSIONS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "submissions.json")

def load_submissions_db() -> List[Dict[str, Any]]:
    if os.path.exists(SUBMISSIONS_FILE):
        try:
            with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_submissions_db(data: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(SUBMISSIONS_FILE), exist_ok=True)
    with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def process_tally_payload(raw_json: Dict[str, Any]) -> Dict[str, Any]:
    assessment = TallyDataMapper.parse_tally_submission(raw_json)
    scoring = AIRSScoringEngine.evaluate(assessment)

    company_slug = assessment.company.name.replace(" ", "_").replace(".", "").replace("/", "")
    output_filename = f"AI_Risk_Assessment_{company_slug}.html"
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", output_filename)

    ReportExporter.export_html_report(assessment, scoring, output_path)

    # Dispatch Email to Client
    email_res = EmailSender.send_assessment_email(
        recipient_email=assessment.company.email,
        company_name=assessment.company.name,
        score=scoring.overall_score,
        risk_level=scoring.risk_level,
        report_filename=output_filename,
        report_filepath=output_path
    )

    submission_record = {
        "id": assessment.response_id,
        "status": "Pending",
        "createdAt": assessment.submission_time,
        "reportFile": output_filename,
        "advisorNotes": "",
        "emailStatus": email_res.get("status"),
        "data": {
            "company": {
                "name": assessment.company.name,
                "email": assessment.company.email,
                "country": assessment.company.country,
                "industry": assessment.company.industry,
                "company_size": assessment.company.company_size
            },
            "ai_adoption": {
                "tools": assessment.ai_adoption.tools,
                "licensing_tier": assessment.ai_adoption.licensing_tier,
                "active_users": assessment.ai_adoption.active_users,
                "ai_role_architecture": assessment.ai_adoption.ai_role_architecture
            },
            "answers": {
                "confidential_data_upload": assessment.answers.confidential_data_upload,
                "confidential_data_details": assessment.answers.confidential_data_details,
                "human_review_frequency": assessment.answers.human_review_frequency,
                "ai_policy_status": assessment.answers.ai_policy_status,
                "ai_training_status": assessment.answers.ai_training_status,
                "hr_automated_uses": assessment.answers.hr_automated_uses,
                "sells_ai_content": assessment.answers.sells_ai_content,
                "discloses_ai_in_contracts": assessment.answers.discloses_ai_in_contracts,
                "past_incidents": assessment.answers.past_incidents,
                "biggest_concern": assessment.answers.biggest_concern
            }
        },
        "evaluation": {
            "overallScore": scoring.overall_score,
            "maturityLevel": scoring.maturity_level,
            "riskLevel": scoring.risk_level,
            "highRiskFlags": [
                {
                    "system_name": f.system_name,
                    "regulation_reference": f.regulation_reference,
                    "severity": f.severity,
                    "description": f.description
                } for f in scoring.high_risk_flags
            ],
            "domainResults": {
                dom_name: {
                    "name": dom.name,
                    "weight": dom.weight,
                    "score": dom.score,
                    "status": dom.status,
                    "finding": dom.finding
                } for dom_name, dom in scoring.domain_results.items()
            },
            "remediationProcedures": [
                {
                    "title": p.title,
                    "timeline": p.timeline,
                    "priority": p.priority,
                    "objective": p.objective,
                    "steps": p.steps,
                    "template": p.starter_template
                } for p in scoring.remediation_procedures
            ]
        }
    }

    db = load_submissions_db()
    db = [s for s in db if s.get("id") != assessment.response_id]
    db.insert(0, submission_record)
    save_submissions_db(db)

    return submission_record

# Check FastAPI availability
try:
    from fastapi import FastAPI, Request, HTTPException, Response
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles

    app = FastAPI(
        title="AI Risk Shield Automated Webhook & API Engine",
        version="0.2.0",
        description="Receives Tally webhooks, evaluates AIRS scores, dispatches emails, and serves reports."
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def index():
        return {
            "service": "AI Risk Shield API & Webhook Engine",
            "status": "online",
            "version": "0.2.0",
            "endpoints": {
                "tally_webhook": "POST /api/webhook/tally",
                "submissions_list": "GET /api/submissions",
                "dashboard": "GET /dashboard.html",
                "health": "GET /health"
            }
        }

    @app.get("/health")
    def health():
        return {"status": "ok", "timestamp": datetime.now().isoformat()}

    @app.get("/api/webhook/tally")
    @app.head("/api/webhook/tally")
    def webhook_tally_get():
        return {
            "status": "online",
            "service": "AI Risk Shield Tally Webhook Receiver",
            "endpoint": "POST /api/webhook/tally"
        }

    @app.post("/api/webhook/tally")
    async def webhook_tally(request: Request):
        try:
            try:
                raw_data = await request.json()
            except Exception:
                raw_data = {}
            record = process_tally_payload(raw_data)
            return {
                "status": "success",
                "message": "Tally submission processed and email dispatched",
                "responseId": record["id"],
                "airs_score": record["evaluation"]["overallScore"],
                "risk_level": record["evaluation"]["riskLevel"],
                "email_status": record["emailStatus"],
                "report_file": record["reportFile"]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/submissions")
    def get_submissions():
        return load_submissions_db()

    @app.post("/api/submissions/{response_id}/approve")
    async def approve_submission(response_id: str, request: Request):
        body = await request.json()
        notes = body.get("notes", "")
        db = load_submissions_db()
        for sub in db:
            if sub.get("id") == response_id:
                sub["status"] = "Approved"
                sub["advisorNotes"] = notes
                save_submissions_db(db)

                # Re-dispatch email on approval
                comp = sub["data"]["company"]
                eval_data = sub["evaluation"]
                EmailSender.send_assessment_email(
                    recipient_email=comp["email"],
                    company_name=comp["name"],
                    score=eval_data["overallScore"],
                    risk_level=eval_data["riskLevel"],
                    report_filename=sub["reportFile"],
                    report_filepath=os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", sub["reportFile"])
                )

                return {"status": "success", "approvedId": response_id, "emailDispatched": True}
        raise HTTPException(status_code=404, detail="Submission not found")

    @app.get("/reports/{filename}", response_class=HTMLResponse)
    def get_report(filename: str):
        report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", filename)
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                return f.read()
        raise HTTPException(status_code=404, detail="Report file not found")

    # Serve static dashboard
    web_app_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web_app")
    if os.path.exists(web_app_dir):
        app.mount("/web_app", StaticFiles(directory=web_app_dir, html=True), name="web_app")

except ImportError:
    app = None

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"--> Starting AIRS Production Server on port {port}...")
    if app:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        print("[!] FastAPI/Uvicorn not found. Please install requirements.txt: pip install -r requirements.txt")
