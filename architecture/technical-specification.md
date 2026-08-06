# AI Risk Shield

# Technical Architecture Specification

**Version:** 0.1.0
**Status:** MVP Technical Blueprint
**Owner:** AI Risk Shield

---

# 1. Purpose

This document defines the technical architecture of the AI Risk Shield MVP.

The purpose is to create a clear implementation blueprint for a responsible AI risk assessment system.

The architecture describes:

* system components,
* data movement,
* processing logic,
* AI usage principles,
* automation workflow,
* human review process.

---

# 2. Architecture Philosophy

AI Risk Shield follows the principle:

> Automation should increase efficiency without removing human responsibility.

The system is designed around:

```
Data Collection

↓

Rules & Assessment Logic

↓

Knowledge Retrieval

↓

AI Assistance

↓

Human Review

↓

Customer Report
```

---

# 3. MVP Architecture Overview

The MVP consists of six primary layers:

```
Layer 1

User Interface

↓

Layer 2

Automation Layer

↓

Layer 3

Assessment Engine

↓

Layer 4

Knowledge Layer

↓

Layer 5

AI Generation Layer

↓

Layer 6

Human Review & Delivery
```

---

# 4. Layer 1 — User Interface

## Technology

Tally.so

---

## Purpose

Collect structured information from organizations.

The form is the first interaction point between the customer and AI Risk Shield.

---

## Data Collected

### Company Information

* Company name
* Corporate email
* Country
* Industry
* Company size

---

### AI Usage Information

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

### Risk Assessment Questions

Initial assessment areas:

* Data Privacy
* Human Oversight
* Automated Decision Making
* Intellectual Property
* AI Governance

---

## Output

Structured assessment submission.

Example:

```json
{
  "company": {},
  "ai_usage": {},
  "answers": {}
}
```

---

# 5. Layer 2 — Automation Layer

## Technology

Make.com

---

## Purpose

Coordinate the movement of information between system components.

Automation handles workflow execution.

Automation does not independently determine risk.

---

## Responsibilities

The automation layer:

* receives Tally submissions,
* validates data,
* transforms information,
* creates assessment objects,
* triggers analysis,
* manages report workflow.

---

## Workflow

```
New Tally Submission

↓

Webhook Trigger

↓

Data Validation

↓

Assessment Object Creation

↓

Risk Processing

↓

AI Report Generation

↓

Human Review Notification

↓

Customer Delivery
```

---

# 6. Layer 3 — Assessment Engine

## Purpose

Apply the AIRS methodology.

The assessment engine converts customer answers into structured risk information.

---

## Responsibilities

The engine:

* maps answers to risk categories,
* applies scoring rules,
* calculates AIRS score,
* identifies maturity level,
* selects recommendations.

---

## Example

Input:

```
Question:

Employees use public AI tools with customer information.

Answer:

YES
```

Processing:

```
Risk Category:

Data Protection & Privacy


Impact:

High


Recommendation:

Implement approved AI usage controls.
```

---

# 7. Assessment Data Model

Initial internal structure:

```json
{
  "company": {
    "name": "",
    "email": "",
    "country": "",
    "industry": "",
    "size": ""
  },

  "ai_profile": {
    "tools": [],
    "usage_description": ""
  },

  "assessment": {
    "privacy": "",
    "human_review": "",
    "automation_usage": "",
    "intellectual_property": "",
    "governance": ""
  }
}
```

---

# 8. Layer 4 — Knowledge Layer

## Purpose

Provide reliable context for AI-generated analysis.

The knowledge layer protects the system from unsupported assumptions.

---

# Knowledge Priority

## Level 1 — Official Sources

Examples:

* European regulations,
* governmental guidance,
* regulatory publications.

---

## Level 2 — Recognized Standards

Examples:

* NIST AI Risk Management Framework,
* ISO standards,
* professional frameworks.

---

## Level 3 — Research Sources

Examples:

* academic publications,
* recognized institutions.

---

## Level 4 — Industry Practices

Examples:

* security recommendations,
* implementation guides.

---

## Level 5 — AIRS Internal Knowledge

Examples:

* scoring methodology,
* recommendations library,
* assessment rules.

---

# 9. Layer 5 — AI Generation Layer

## Purpose

Generate understandable assessment reports.

AI works as an analysis assistant.

AI does not replace legal, security, or business expertise.

---

## AI Inputs

The AI receives:

* assessment results,
* AIRS score,
* risk categories,
* approved knowledge context,
* recommendation rules.

---

## AI Outputs

The AI generates:

* executive summary,
* risk explanations,
* recommendations,
* improvement roadmap.

---

# 10. AI Safety Rules

The AI system must:

## Always

* explain assumptions,
* use available evidence,
* communicate uncertainty,
* avoid unsupported statements.

---

## Never

* invent regulations,
* create fake legal references,
* claim certification,
* guarantee compliance,
* replace human judgment.

---

# 11. Layer 6 — Human Review & Delivery

## Purpose

Ensure responsible customer communication.

---

## Review Process

Before delivery, a reviewer checks:

* factual accuracy,
* logical consistency,
* recommendation relevance,
* appropriate language,
* absence of unsupported claims.

---

Workflow:

```
AI Generated Draft

↓

Human Review

↓

Approved Report

↓

Customer Delivery
```

---

# 12. Report Generation

## Initial Output Format

PDF Report

---

## Report Structure

```
AI Risk Shield Assessment Report


1. Executive Summary


2. Company AI Profile


3. AIRS Score


4. Risk Categories


5. Key Findings


6. Recommendations


7. Improvement Roadmap


8. Limitations & Disclaimer
```

---

# 13. MVP Infrastructure

## Customer Interface

Tally.so

---

## Automation

Make.com

---

## AI Layer

LLM API with controlled instructions.

---

## Knowledge

Structured AIRS knowledge base.

---

## Reporting

PDF generation service.

---

## Storage

Initial MVP:

Secure cloud storage.

Future:

Dedicated database infrastructure.

---

# 14. Security Requirements

The system should support:

* encrypted communication,
* secure API key management,
* minimum data collection,
* controlled access,
* separation of customer information.

---

# 15. Audit Logging

The system should track:

* assessment ID,
* submission timestamp,
* processing status,
* report generation status,
* human review status,
* delivery status.

---

# 16. Future Architecture Expansion

Future modules may include:

---

## Customer Portal

Capabilities:

* assessment history,
* reports,
* improvement tracking.

---

## AI Inventory Management

Capabilities:

* AI tool registry,
* ownership tracking,
* risk monitoring.

---

## Policy Generator

Capabilities:

* AI acceptable use policies,
* employee guidelines,
* internal procedures.

---

## Continuous AI Governance

Capabilities:

* AI usage monitoring,
* governance updates,
* recurring assessments.

---

# 17. MVP Implementation Rule

The first version should optimize:

1. Reliability

2. Trust

3. Customer value

4. Simplicity

5. Automation

Complexity should be introduced only when validated by real customer needs.

---

# Status

Technical architecture specification completed.

Next phase:

Implementation of the first working workflow:

```
Tally

↓

Make.com

↓

Assessment Object

↓

AIRS Processing

↓

AI Draft Report

↓

Human Review
```
