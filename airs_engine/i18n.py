"""
AIRS Internationalization (i18n) Module
Provides multi-language support across all EU member state countries listed in the audit form:
English (EN), German (DE), French (FR), Dutch (NL), Polish (PL), Spanish (ES), Italian (IT), Czech (CZ), Swedish (SE), Danish (DK).
"""

from typing import Dict, Any

COUNTRY_TO_LANG_MAP = {
    "germany": "de",
    "austria": "de",
    "france": "fr",
    "belgium": "fr",
    "netherlands": "nl",
    "poland": "pl",
    "spain": "es",
    "italy": "it",
    "czech republic": "cz",
    "sweden": "se",
    "denmark": "dk",
    "ireland": "en",
    "united kingdom": "en",
    "united states": "en"
}

TRANSLATIONS = {
    "en": {
        "report_title": "AI RISK SHIELD ASSESSMENT REPORT",
        "report_subtitle": "Responsible AI Governance & Visual Audit",
        "governance_index": "AIRS GOVERNANCE INDEX",
        "maturity_level": "Maturity Level",
        "company_profile": "Company Profile",
        "executive_summary_title": "Executive Summary",
        "high_risk_alert_title": "⚠️ EU AI Act Regulatory High-Risk Alert",
        "section_1_title": "📊 Section 1 — Visual Governance & Radar Evaluation",
        "radar_title": "AIRS 7-Domain Maturity Radar",
        "procedures_title": "📋 Detailed Remediation Procedures",
        "templates_title": "📑 Ready-to-Use Policy & Clause Templates",
        "disclaimer_title": "LEGAL DISCLAIMER",
        "domains": {
            "AI Governance": "AI Governance",
            "Data Protection & Privacy": "Data Protection & Privacy",
            "Human Oversight": "Human Oversight",
            "Transparency & Incidents": "Transparency & Incidents",
            "Intellectual Property": "Intellectual Property",
            "HR & High-Risk Systems": "HR & High-Risk Systems",
            "AI Literacy & Operations": "AI Literacy & Operations"
        }
    },
    "de": {
        "report_title": "AI RISK SHIELD BEWERTUNGSBERICHT",
        "report_subtitle": "Verantwortungsvolle AI Governance & Audit",
        "governance_index": "AIRS GOVERNANCE INDEX",
        "maturity_level": "Reifegrad",
        "company_profile": "Unternehmensprofil",
        "executive_summary_title": "Zusammenfassung für die Geschäftsführung",
        "high_risk_alert_title": "⚠️ EU AI Act Hochrisiko-Warnung",
        "section_1_title": "📊 Abschnitt 1 — Visual Governance & Radarbewertung",
        "radar_title": "AIRS 7-Domänen Reifegrad-Radar",
        "procedures_title": "📋 Detaillierte Abhilfemaßnahmen",
        "templates_title": "📑 Vorlagen für Richtlinien & Verträge",
        "disclaimer_title": "RECHTLICHER HINWEIS",
        "domains": {
            "AI Governance": "KI Governance & Richtlinien",
            "Data Protection & Privacy": "Datenschutz & DSGVO",
            "Human Oversight": "Menschliche Aufsicht (HITL)",
            "Transparency & Incidents": "Transparenz & Vorfälle",
            "Intellectual Property": "Geistiges Eigentum (Urheberrecht)",
            "HR & High-Risk Systems": "Hochrisiko-Systeme (HR)",
            "AI Literacy & Operations": "KI-Kompetenz & Betrieb"
        }
    },
    "fr": {
        "report_title": "RAPPORT D'ÉVALUATION AI RISK SHIELD",
        "report_subtitle": "Gouvernance Responsable de l'IA & Audit",
        "governance_index": "INDICE DE GOUVERNANCE AIRS",
        "maturity_level": "Niveau de Maturité",
        "company_profile": "Profil de l'Entreprise",
        "executive_summary_title": "Résumé Exécutif",
        "high_risk_alert_title": "⚠️ Alerte de Haut Risque Règlement EU AI Act",
        "section_1_title": "📊 Section 1 — Évaluation Visuelle & Radar de Gouvernance",
        "radar_title": "Radar de Maturité 7 Domaines AIRS",
        "procedures_title": "📋 Procédures de Remédiation Détaillées",
        "templates_title": "📑 Modèles de Politiques & Clauses Contractuelles",
        "disclaimer_title": "AVERTISSEMENT LÉGAL",
        "domains": {
            "AI Governance": "Gouvernance de l'IA",
            "Data Protection & Privacy": "Protection des Données & RGPD",
            "Human Oversight": "Supervision Humaine (HITL)",
            "Transparency & Incidents": "Transparence & Incidents",
            "Intellectual Property": "Propriété Intellectuelle",
            "HR & High-Risk Systems": "Systèmes à Haut Risque (RH)",
            "AI Literacy & Operations": "Compétences & Opérations IA"
        }
    },
    "nl": {
        "report_title": "AI RISK SHIELD BEOORDELINGSRAPPORT",
        "report_subtitle": "Verantwoorde AI-Governance & Audit",
        "governance_index": "AIRS GOVERNANCE INDEX",
        "maturity_level": "Volwassenheidsniveau",
        "company_profile": "Bedrijfsprofiel",
        "executive_summary_title": "Managementsamenvatting",
        "high_risk_alert_title": "⚠️ EU AI Act Hoog-Risico Waarschuwing",
        "section_1_title": "📊 Sectie 1 — Visuele Governance & Radarevaluatie",
        "radar_title": "AIRS 7-Domeinen Volwassenheidsradar",
        "procedures_title": "📋 Gedetailleerde Herstelprocedures",
        "templates_title": "📑 Kant-en-klare Beleidssjablonen",
        "disclaimer_title": "JURIDISCHE DISCLAIMER",
        "domains": {
            "AI Governance": "AI Governance & Beleid",
            "Data Protection & Privacy": "Gegevensbescherming & AVG",
            "Human Oversight": "Menselijk Toezicht (HITL)",
            "Transparency & Incidents": "Transparantie & Incidenten",
            "Intellectual Property": "Intellectueel Eigendom",
            "HR & High-Risk Systems": "Hoog-Risicosystemen (HR)",
            "AI Literacy & Operations": "AI-Vaardigheden & Operaties"
        }
    },
    "pl": {
        "report_title": "RAPORT AUDYTU AI RISK SHIELD",
        "report_subtitle": "Zarządzanie AI i Audyt Ryzyka Regulacyjnego",
        "governance_index": "INDEKS DOJRZAŁOŚCI AIRS",
        "maturity_level": "Poziom Dojrzałości",
        "company_profile": "Profil Organizacji",
        "executive_summary_title": "Podsumowanie Zarządcze",
        "high_risk_alert_title": "⚠️ Ostrzeżenie Regulacyjne EU AI Act (Wysokie Ryzyko)",
        "section_1_title": "📊 Sekcja 1 — Wizualna Ocena Dojrzałości i Wykres Radaryzacyjny",
        "radar_title": "Wykres Dojrzałości 7 Domen AIRS",
        "procedures_title": "📋 Procedury Naprawcze i Plan Wdrożenia",
        "templates_title": "📑 Gotowe Szablony Polityk i Klauzul Umownych",
        "disclaimer_title": "ZASTRZEŻENIE PRAWNE",
        "domains": {
            "AI Governance": "Nadzór i Polityka AI",
            "Data Protection & Privacy": "Ochrona Danych i Prywatność",
            "Human Oversight": "Nadzór Ludzki (HITL)",
            "Transparency & Incidents": "Przejrzystość i Incydenty",
            "Intellectual Property": "Własność Intelektualna",
            "HR & High-Risk Systems": "Systemy Wysokiego Ryzyka (HR)",
            "AI Literacy & Operations": "Kompetencje i Operacje AI"
        }
    },
    "es": {
        "report_title": "INFORME DE EVALUACIÓN AI RISK SHIELD",
        "report_subtitle": "Gobernanza Responsable de IA & Auditoría",
        "governance_index": "ÍNDICE DE GOBERNANZA AIRS",
        "maturity_level": "Nivel de Madurez",
        "company_profile": "Perfil de la Empresa",
        "executive_summary_title": "Resumen Ejecutivo",
        "high_risk_alert_title": "⚠️ Alerta de Alto Riesgo Reglamento EU AI Act",
        "section_1_title": "📊 Sección 1 — Evaluación Visual & Radar de Gobernanza",
        "radar_title": "Radar de Madurez 7 Dominios AIRS",
        "procedures_title": "📋 Procedimientos de Remediación Detallados",
        "templates_title": "📑 Plantillas de Políticas y Cláusulas",
        "disclaimer_title": "AVISO LEGAL",
        "domains": {
            "AI Governance": "Gobernanza de IA",
            "Data Protection & Privacy": "Protección de Datos & RGPD",
            "Human Oversight": "Supervisión Humana (HITL)",
            "Transparency & Incidents": "Transparencia e Incidentes",
            "Intellectual Property": "Propiedad Intelectual",
            "HR & High-Risk Systems": "Sistemas de Alto Riesgo (RRHH)",
            "AI Literacy & Operations": "Competencia y Operaciones de IA"
        }
    },
    "it": {
        "report_title": "RAPPORTO DI VALUTAZIONE AI RISK SHIELD",
        "report_subtitle": "Governance Responsabile dell'IA & Audit",
        "governance_index": "INDICE DI GOVERNANCE AIRS",
        "maturity_level": "Livello di Maturità",
        "company_profile": "Profilo Aziendale",
        "executive_summary_title": "Sintesi Esecutiva",
        "high_risk_alert_title": "⚠️ Avviso di Alto Rischio Regolamento EU AI Act",
        "section_1_title": "📊 Sezione 1 — Valutazione Visuale & Radar di Governance",
        "radar_title": "Radar di Maturità 7 Domini AIRS",
        "procedures_title": "📋 Procedure di Rimedio Dettagliate",
        "templates_title": "📑 Modelli di Politiche & Clausole Contrattuali",
        "disclaimer_title": "AVVISO LEGALE",
        "domains": {
            "AI Governance": "Governance dell'IA",
            "Data Protection & Privacy": "Protezione Dati & GDPR",
            "Human Oversight": "Supervisione Umana (HITL)",
            "Transparency & Incidents": "Trasparenza e Incidenti",
            "Intellectual Property": "Proprietà Intellettuale",
            "HR & High-Risk Systems": "Sistemi ad Alto Rischio (Risorse Umane)",
            "AI Literacy & Operations": "Competenze e Operazioni IA"
        }
    }
}

class I18n:
    @staticmethod
    def get_lang_code(country_name: str) -> str:
        if not country_name:
            return "en"
        return COUNTRY_TO_LANG_MAP.get(country_name.strip().lower(), "en")

    @staticmethod
    def get(key: str, lang: str = "en") -> Any:
        lang_dict = TRANSLATIONS.get(lang.lower(), TRANSLATIONS["en"])
        return lang_dict.get(key, TRANSLATIONS["en"].get(key, key))

    @staticmethod
    def get_domain_name(domain_key: str, lang: str = "en") -> str:
        lang_dict = TRANSLATIONS.get(lang.lower(), TRANSLATIONS["en"])
        return lang_dict.get("domains", {}).get(domain_key, domain_key)
