"""
AIRS Regulatory Intelligence & Knowledge Base Updater Engine
Monitors regulatory feeds (EUR-Lex, NIST, EDPB, OWASP), detects regulatory updates,
and syncs new reference entries into knowledge/kb_registry.json with audit logging.
"""

import json
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, Any, List

REGULATORY_FEEDS = [
  {
    "id": "EUR_LEX_AI",
    "name": "EUR-Lex Official EU AI Act & Digital Legislation",
    "url": "https://eur-lex.europa.eu/EN/feed/rss/latest.xml",
    "source_level": "Level_1"
  },
  {
    "id": "EDPB_NEWS",
    "name": "European Data Protection Board (EDPB) Guidelines",
    "url": "https://edpb.europa.eu/news/news_en.xml",
    "source_level": "Level_1"
  },
  {
    "id": "NIST_AI_NEWS",
    "name": "NIST AI Risk Management Updates",
    "url": "https://www.nist.gov/news-events/cybersecurity/rss.xml",
    "source_level": "Level_2"
  }
]

class RegulatoryUpdater:
    @staticmethod
    def fetch_feed(feed_url: str) -> List[Dict[str, str]]:
        items = []
        try:
            req = urllib.request.Request(feed_url, headers={"User-Agent": "AIRiskShield-RegulatoryBot/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                root = ET.fromstring(content)
                # Parse RSS items
                for item in root.findall(".//item"):
                    title = item.findtext("title", "")
                    link = item.findtext("link", "")
                    pubDate = item.findtext("pubDate", "")
                    desc = item.findtext("description", "")
                    if title:
                        items.append({
                            "title": title.strip(),
                            "link": link.strip(),
                            "pubDate": pubDate.strip(),
                            "summary": desc.strip()[:200]
                        })
        except Exception as e:
            # Fallback for offline/test environments
            pass
        return items

    @classmethod
    def run_update_check(cls) -> Dict[str, Any]:
        kb_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge", "kb_registry.json")
        history_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge", "update_history.json")

        if os.path.exists(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                kb_data = json.load(f)
        else:
            kb_data = {"regulatory_references": []}

        new_updates_found = 0
        detected_events = []

        for feed in REGULATORY_FEEDS:
            items = cls.fetch_feed(feed["url"])
            for item in items:
                title_lower = item["title"].lower()
                # Check for AI / Data / Resilience keywords
                if any(kw in title_lower for kw in ["artificial intelligence", "ai act", "gdpr", "dora", "cybersecurity", "nis2", "llm"]):
                    # Check if already present
                    existing = [r for r in kb_data.get("regulatory_references", []) if r.get("title") == item["title"]]
                    if not existing:
                        new_entry = {
                            "id": f"REG_AUTO_{len(kb_data['regulatory_references']) + 1:03d}",
                            "level": feed["source_level"],
                            "source": feed["name"],
                            "title": item["title"],
                            "citation": f"Auto-detected feed item: {item['pubDate']}",
                            "summary": item["summary"] if item["summary"] else item["title"],
                            "link": item["link"],
                            "added_at": datetime.now().isoformat()
                        }
                        kb_data["regulatory_references"].append(new_entry)
                        detected_events.append(new_entry)
                        new_updates_found += 1

        if new_updates_found > 0:
            kb_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            with open(kb_path, "w", encoding="utf-8") as f:
                json.dump(kb_data, f, indent=2, ensure_ascii=False)

        # Log to History
        history = []
        if os.path.exists(history_path):
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = []

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "CHECK_COMPLETE",
            "new_updates_detected": new_updates_found,
            "events": detected_events
        }
        history.insert(0, log_entry)

        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        return log_entry

if __name__ == "__main__":
    print("==================================================")
    print("  AIRS AUTOMATED REGULATORY INTELLIGENCE UPDATER  ")
    print("==================================================")
    result = RegulatoryUpdater.run_update_check()
    print(f"--> Scan complete: {result['new_updates_detected']} new regulatory updates detected & synchronized!")
    print(f"--> Audit Log: knowledge/update_history.json")
