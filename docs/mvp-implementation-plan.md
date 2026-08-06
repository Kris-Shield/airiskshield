# AI Risk Shield

# MVP Implementation Plan

**Version:** 0.1.0
**Status:** Development Blueprint
**Owner:** AI Risk Shield

---

# 1. MVP Objective

The objective of the AI Risk Shield MVP is to create a working AI Risk Assessment service that helps organizations understand their AI usage, identify potential risks, and receive practical improvement recommendations.

The MVP should allow a customer to:

1. Complete an AI Risk Assessment.
2. Receive a structured risk analysis.
3. Understand their current AI governance maturity.
4. Obtain a professional improvement roadmap.

---

# 2. MVP Philosophy

AI Risk Shield follows three core principles:

## Responsible Automation

Automation improves efficiency but does not remove human responsibility.

---

## Evidence-Based Assessment

Recommendations are based on:

* AIRS methodology,
* defined scoring rules,
* trusted knowledge sources.

---

## Human-in-the-Loop

Important outputs require human verification before customer delivery.

---

# 3. MVP System Architecture

High-level flow:

```
Customer

↓

Tally Assessment Form

↓

Make.com Automation Layer

↓

Assessment Processing

↓

AIRS Scoring Engine

↓

AI Analysis Layer

↓

Report Generator

↓

Human Review

↓

Customer Delivery
```

---

# 4. Component 1 — Assessment Form

## Technology

Tally.so

---

## Purpose

Collect structured information about:

* company profile,
* AI usage,
* governance practices,
* potential risk areas.

---

## Company Information

Required fields:

* Company name
* Corporate email
* Country
* Industry
* Company size

---

## AI Usage Information

Required fields:

* AI tools currently used
* Main AI usage scenarios
* Internal AI practices

Examples:

* ChatGPT
* Claude
* Microsoft Copilot
* Midjourney
* Other AI systems

---

## Core Risk Questions

Initial MVP assessment:

### Q001 — Data Privacy

Do employees use public AI tools to process confidential company or customer information?

Risk domain:

Data Protection & Privacy

---

### Q002 — Human Oversight

Are AI-generated outputs delivered externally without mandatory human review?

Risk domain:

Human Oversight

---

### Q003 — Automated Decisions

Does the company use AI for:

* recruitment,
* employee evaluation,
* customer scoring,
* automated decisions?

Risk domain:

Human Oversight / Transparency

---

### Q004 — Intellectual Property

Does the company deliver AI-generated content or assets commercially?

Risk domain:

Intellectual Property

---

### Q005 — AI Governance

Does the organization have an internal AI usage policy?

Risk domain:

AI Governance

---

# 5. Component 2 — Automation Layer

## Technology

Make.com

---

## Purpose

Connect all system components.

Automation responsibilities:

* receive form submission,
* validate information,
* prepare assessment data,
* trigger analysis workflow,
* generate report draft,
* notify reviewer.

---

## Workflow

```
New Tally Submission

↓

Data Validation

↓

Assessment Object Creation

↓

Risk Evaluation

↓

AI Report Draft

↓

Human Review Notification

↓

Final Report Delivery
```

---

# 6. Component 3 — Assessment Data Model

Internal assessment object:

```json
{
  "company": {
    "name": "",
    "email": "",
    "country": "",
    "industry": "",
    "size": ""
  },

  "ai_usage": {
    "tools": [],
    "description": ""
  },

  "answers": {
    "privacy": "",
    "human_review": "",
    "automation_usage": "",
    "ip": "",
    "governance": ""
  }
}
```

---

# 7. Component 4 — AIRS Assessment Engine

## Purpose

Convert customer answers into structured risk information.

Responsibilities:

* map answers to AIRS categories,
* calculate score,
* determine maturity level,
* identify priority risks.

---

## Input

Assessment object.

---

## Output

```
AIRS Score

↓

Risk Categories

↓

Findings

↓

Recommendations
```

---

# 8. Component 5 — AI Analysis Layer

## Purpose

Generate understandable explanations based on:

* assessment results,
* AIRS methodology,
* approved knowledge sources.

---

## AI Responsibilities

AI may:

* summarize findings,
* explain risks,
* generate business-friendly language,
* prepare report drafts.

---

## AI Restrictions

AI must not:

* provide unsupported legal conclusions,
* invent regulations,
* guarantee compliance,
* replace professional judgment.

---

# 9. Component 6 — Knowledge Layer

The AI system should use controlled knowledge sources.

Priority:

## Level 1

Official regulatory sources.

Examples:

* EU AI Act materials,
* official governmental guidance,
* data protection authority publications.

---

## Level 2

Recognized frameworks.

Examples:

* NIST AI RMF,
* ISO standards.

---

## Level 3

Industry best practices.

---

## Level 4

Internal AIRS knowledge base.

---

# 10. Component 7 — Human Review Process

Before customer delivery:

A reviewer checks:

* logical consistency,
* recommendation quality,
* unsupported statements,
* appropriate wording.

Workflow:

```
AI Draft

↓

Human Review

↓

Approved Report

↓

Customer
```

---

# 11. Component 8 — Report Generation

Initial output:

PDF report.

---

## Report Structure

```
AI Risk Shield Assessment Report

1. Executive Summary

2. Company AI Profile

3. AIRS Score

4. Risk Categories

5. Findings

6. Recommendations

7. Improvement Roadmap

8. Limitations & Disclaimer
```

---

# 12. MVP Development Order

## Phase 1 — Assessment

Tasks:

* finalize Tally form,
* add required questions,
* test user experience.

---

## Phase 2 — Automation

Tasks:

* connect Tally webhook,
* configure Make scenario,
* create data mapping.

---

## Phase 3 — Assessment Engine

Tasks:

* implement scoring rules,
* connect categories,
* generate findings.

---

## Phase 4 — AI Report Generation

Tasks:

* prepare prompts,
* connect knowledge base,
* generate draft reports.

---

## Phase 5 — Human Review

Tasks:

* define approval process,
* create review checklist.

---

## Phase 6 — Delivery

Tasks:

* generate PDF,
* send customer email,
* collect feedback.

---

# 13. MVP Success Criteria

The MVP is complete when:

✅ Customer completes assessment

✅ Data is transferred automatically

✅ AIRS score is calculated

✅ Risk areas are identified

✅ Recommendations are generated

✅ Human review is possible

✅ Final report reaches customer

---

# 14. What We Do Not Build Yet

The MVP intentionally avoids:

❌ Full SaaS dashboard

❌ Complex user accounts

❌ Automated legal certification

❌ Continuous AI monitoring

❌ Custom AI model training

❌ Enterprise integrations

---

# 15. First Customer Validation

The first goal is not scale.

The first goal is learning.

We collect:

* customer feedback,
* objections,
* missing questions,
* improvement opportunities.

---

# 16. Long-Term Evolution

Future versions may include:

* customer portal,
* AI inventory management,
* policy generator,
* employee AI training,
* continuous governance monitoring,
* subscription SaaS model.

---

# Status

MVP implementation blueprint completed.

Next step:

Build execution checklist and start technical implementation.
