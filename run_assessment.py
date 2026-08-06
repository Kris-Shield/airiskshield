"""
AI Risk Shield — Assessment CLI Runner
Executes end-to-end assessment processing from Tally JSON to scored output report.
"""

import sys
import json
import os

# Fix Windows console UTF-8 output encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from airs_engine.mapper import TallyDataMapper
from airs_engine.scoring import AIRSScoringEngine
from airs_engine.pdf_exporter import ReportExporter

def main():
    json_path = "sample_tally_submission.json"
    if len(sys.argv) > 1:
        json_path = sys.argv[1]

    if not os.path.exists(json_path):
        print(f"Error: Submission file '{json_path}' not found.")
        sys.exit(1)

    print("==================================================")
    print("        AI RISK SHIELD ASSESSMENT ENGINE          ")
    print("==================================================")
    print(f"--> Reading Tally submission: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        raw_json = json.load(f)

    # 1. Parse Tally Submission
    assessment = TallyDataMapper.parse_tally_submission(raw_json)
    print(f"--> Organization: {assessment.company.name}")
    print(f"--> Industry / Size: {assessment.company.industry} ({assessment.company.company_size})")

    # 2. Compute AIRS Scoring & Governance Maturity
    scoring = AIRSScoringEngine.evaluate(assessment)
    print("--------------------------------------------------")
    print(f"AIRS GOVERNANCE SCORE: {scoring.overall_score} / 100")
    print(f"MATURITY LEVEL      : {scoring.maturity_level}")
    print(f"RISK CLASSIFICATION  : {scoring.risk_level}")
    print("--------------------------------------------------")

    if scoring.high_risk_flags:
        print("[!] EU AI ACT HIGH-RISK FLAGS DETECTED:")
        for flag in scoring.high_risk_flags:
            print(f"   * [{flag.severity}] {flag.system_name} ({flag.regulation_reference})")
        print("--------------------------------------------------")

    print("DOMAIN EVALUATION SUMMARY:")
    for dom_name, dom in scoring.domain_results.items():
        print(f"   [{dom.status:<9}] {dom_name:<28}: {dom.score:>5.1f}/100")

    # 3. Export HTML Report
    output_dir = "output"
    output_filename = f"AI_Risk_Assessment_{assessment.company.name.replace(' ', '_').replace('.', '')}.html"
    output_filepath = os.path.join(output_dir, output_filename)

    exported_path = ReportExporter.export_html_report(assessment, scoring, output_filepath)
    
    print("==================================================")
    print(f"[OK] ASSESSMENT COMPLETE!")
    print(f"Generated HTML Report: {os.path.abspath(exported_path)}")
    print("==================================================")

if __name__ == "__main__":
    main()
