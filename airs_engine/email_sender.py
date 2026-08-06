"""
AIRS Transactional Email Dispatcher Module
Sends interactive HTML assessment reports and PDF deliverables to clients
via Resend API / SMTP, with fallback simulation mode.
"""

import os
import json
import urllib.request
import urllib.error
import base64
from typing import Dict, Any, Optional

class EmailSender:
    @staticmethod
    def send_assessment_email(recipient_email: str, company_name: str, score: float, risk_level: str, report_filename: str, report_filepath: str) -> Dict[str, Any]:
        resend_key = os.environ.get("RESEND_API_KEY", "").strip()
        sender_env = os.environ.get("SENDER_EMAIL", "").strip()
        railway_url = os.environ.get("PUBLIC_SERVER_URL", "https://web-production-4e41f.up.railway.app").rstrip("/")

        # Format sender email
        if sender_env:
            if "<anything>" in sender_env:
                sender_env = sender_env.replace("<anything>", "audit")
            sender = sender_env
        else:
            sender = "AI Risk Shield <audit@keepelee.resend.app>"

        report_url = f"{railway_url}/reports/{report_filename}"

        # Risk badge color
        badge_color = "#E11D48" if "Critical" in risk_level else ("#EF4444" if "High" in risk_level else ("#F59E0B" if "Moderate" in risk_level else "#10B981"))

        email_html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Inter', Arial, sans-serif; background-color: #0B0F19; color: #F8FAFC; margin: 0; padding: 0; }}
    .container {{ max-width: 600px; margin: 30px auto; background: #1E293B; border-radius: 16px; border: 1px solid #334155; padding: 32px; }}
    .brand {{ font-size: 22px; font-weight: 800; color: #38BDF8; letter-spacing: -0.5px; margin-bottom: 4px; }}
    .subbrand {{ font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 24px; }}
    .score-box {{ background: #0F172A; border-radius: 12px; border: 1px solid #334155; padding: 20px; text-align: center; margin: 20px 0; }}
    .score-number {{ font-size: 42px; font-weight: 900; color: #38BDF8; line-height: 1; }}
    .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; text-transform: uppercase; background: rgba(225,29,72,0.2); color: {badge_color}; border: 1px solid {badge_color}; margin-top: 8px; }}
    .btn {{ display: inline-block; background: linear-gradient(135deg, #38BDF8, #3B82F6); color: #0F172A; font-weight: 700; font-size: 14px; padding: 12px 24px; border-radius: 10px; text-decoration: none; margin-top: 16px; }}
    .footer {{ font-size: 11px; color: #64748B; margin-top: 30px; border-top: 1px solid #334155; padding-top: 16px; text-align: center; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="brand">AI RISK SHIELD</div>
    <div class="subbrand">Responsible AI Governance Audit</div>

    <h2>Dzień dobry,</h2>
    <p style="color: #CBD5E1; font-size: 14px; line-height: 1.6;">
      Twój raport audytowy odpowiedzialnego korzystania z AI dla firmy <strong>{company_name}</strong> został pomyślnie wygenerowany i przetworzony przez nasz silnik AIRS.
    </p>

    <div class="score-box">
      <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase;">AIRS GOVERNANCE INDEX</div>
      <div class="score-number">{score} <span style="font-size: 14px; color: #94A3B8;">/ 100</span></div>
      <div class="badge">{risk_level}</div>
    </div>

    <p style="color: #CBD5E1; font-size: 14px; line-height: 1.6;">
      W załączniku oraz pod poniższym linkiem znajdziesz pełny raport wizualny zawierający:
    </p>
    <ul style="color: #CBD5E1; font-size: 13px; line-height: 1.6;">
      <li>📊 Wykres radaryzacyjny dojrzałości 7 domen AI</li>
      <li>⚠️ Analizę zgodności z EU AI Act & RODO</li>
      <li>📋 Procedury naprawcze na 7, 30 i 90 dni</li>
      <li>📑 Gotowe szablony Polityki AI i klauzul umownych</li>
    </ul>

    <div style="text-align: center; margin: 24px 0;">
      <a href="{report_url}" class="btn" target="_blank">Otwórz Pełny Raport Online</a>
    </div>

    <div class="footer">
      AI Risk Shield — Responsible AI Governance & Decision Support Framework<br>
      Wiadomość wygenerowana automatycznie.
    </div>
  </div>
</body>
</html>
"""

        # 1. Send via Resend API if API Key is available
        if resend_key:
            try:
                # Read report attachment
                attachment_content = ""
                if os.path.exists(report_filepath):
                    with open(report_filepath, "rb") as f:
                        attachment_content = base64.b64encode(f.read()).decode("utf-8")

                payload = {
                    "from": sender,
                    "to": [recipient_email],
                    "subject": f"[AIRS AUDIT REPORT] AI Risk & Liability Assessment — {company_name}",
                    "html": email_html
                }

                if attachment_content:
                    payload["attachments"] = [
                        {
                            "filename": report_filename,
                            "content": attachment_content
                        }
                    ]

                req = urllib.request.Request(
                    "https://api.resend.com/emails",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {resend_key}",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AIRiskShield/1.0"
                    }
                )

                with urllib.request.urlopen(req, timeout=10) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    return {"status": "sent", "provider": "resend", "emailId": res_data.get("id")}

            except urllib.error.HTTPError as err:
                err_body = err.read().decode("utf-8") if err.fp else str(err)
                print(f"[!] Resend API HTTPError: {err.code} - {err_body}")
                return {"status": "error", "error_code": err.code, "error_details": err_body}
            except Exception as e:
                print(f"[!] Resend API Exception: {str(e)}")
                return {"status": "error", "error_details": str(e)}

        # 2. Simulation / Development Mode Output
        print(f"--> [EMAIL DISPATCH SIMULATION] Report email dispatched to: {recipient_email}")
        print(f"--> Subject: [AIRS AUDIT REPORT] AI Risk & Liability Assessment — {company_name}")
        print(f"--> Live Report URL: {report_url}")

        return {
            "status": "simulated",
            "provider": "simulation",
            "recipient": recipient_email,
            "report_url": report_url
        }
