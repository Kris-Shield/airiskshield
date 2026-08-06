# AI Risk Shield

# Make.com Assessment Workflow v1

**Version:** 0.1.0
**Status:** MVP Automation Design
**Owner:** AI Risk Shield

---

# 1. Purpose

This document defines the first automation workflow for AI Risk Shield MVP.

The purpose is to connect:

* customer assessment form,
* automation layer,
* AIRS assessment methodology,
* AI analysis,
* report generation,
* human review.

The first MVP objective:

> Transform a customer questionnaire submission into a reviewed AI Risk Assessment report.

---

# 2. Workflow Philosophy

The automation system follows three principles:

## Automation Supports Decisions

Make.com automates repetitive tasks.

It does not replace human responsibility.

---

## AI Assists Analysis

AI helps:

* summarize,
* organize,
* explain,
* prepare recommendations.

AI does not:

* certify compliance,
* provide legal opinions,
* replace experts.

---

## Human Approval Before Delivery

Every customer-facing report requires review before sending.

---

# 3. High-Level Workflow

```text
Customer

↓

Tally Assessment Form

↓

Make.com Trigger

↓

Data Validation

↓

Assessment Object Creation

↓

AIRS Scoring

↓

Risk Analysis

↓

AI Report Draft

↓

Human Review

↓

Final PDF Delivery
```

---

# 4. Workflow Components

## Component Overview

| Component    | Technology    | Purpose                 |
| ------------ | ------------- | ----------------------- |
| Form         | Tally.so      | Collect assessment data |
| Automation   | Make.com      | Workflow orchestration  |
| Logic        | AIRS Engine   | Risk evaluation         |
| Intelligence | LLM API       | Report generation       |
| Storage      | Cloud Storage | Save reports            |
| Delivery     | Email Service | Customer communication  |

---

# 5. Module 1 — Tally Form Trigger

## Application

Tally.so

---

## Trigger

Event:

```
New Form Submission
```

---

## Expected Input

Example:

```json
{
  "company": {
    "name": "Example Company",
    "email": "contact@example.com",
    "country": "Poland",
    "industry": "Software",
    "size": "10-49"
  },

  "ai_usage": {
    "tools": [
      "ChatGPT",
      "Claude"
    ],
    "description": "Marketing and customer communication"
  },

  "answers": {
    "privacy": "Yes",
    "human_review": "No",
    "automation_usage": "No",
    "intellectual_property": "Yes",
    "governance": "No"
  }
}
```

---

# 6. Module 2 — Data Validation

## Purpose

Ensure incoming information is complete before processing.

---

## Required Fields

Company:

* name
* email
* country
* industry

Assessment:

* all risk questions answered

---

## Validation Logic

If valid:

```
Continue Workflow
```

If invalid:

```
Stop Workflow

↓

Notify Administrator
```

---

# 7. Module 3 — Assessment Object Creation

## Purpose

Convert external form data into internal AI Risk Shield format.

---

## Internal Object

```json
{
  "assessment_id": "",

  "company": {
    "name": "",
    "country": "",
    "industry": "",
    "size": ""
  },

  "ai_profile": {
    "tools": [],
    "usage_description": ""
  },

  "risk_answers": {
    "privacy": false,
    "human_review": false,
    "automation_usage": false,
    "ip_risk": false,
    "governance": false
  }
}
```

---

# 8. Module 4 — AIRS Risk Scoring

## Purpose

Calculate initial risk level.

---

## MVP Scoring Rules

### Data Privacy

Public AI tools processing sensitive data:

```
YES = +25 points
```

---

### Human Oversight

No mandatory human review:

```
YES = +20 points
```

---

### Automated Decisions

AI influencing decisions:

```
YES = +20 points
```

---

### Intellectual Property

Commercial AI-generated assets:

```
YES = +15 points
```

---

### AI Governance

No internal AI policy:

```
YES = +20 points
```

---

# 9. Risk Classification

Total score:

Maximum:

```
100 points
```

---

Classification:

```
0-25

Low Risk


26-50

Moderate Risk


51-75

High Risk


76-100

Critical Attention
```

---

# 10. Module 5 — Risk Mapping

The system converts score into categories.

Example:

Input:

```
Privacy = YES
Governance = YES
Human Review = NO
```

Output:

```
Risk Categories:

1. Data Protection

2. AI Governance

3. Human Oversight
```

---

# 11. Module 6 — AI Analysis

## Technology

LLM API

---

## AI Role

AI Risk Shield Analyst

---

## AI Input

The model receives:

* company information,
* AI usage profile,
* AIRS score,
* risk categories,
* recommendations database.

---

## System Rules

```
You are an AI Risk Shield Analyst.

Your role is to create a responsible AI risk assessment.

Rules:

- Do not provide legal certification.
- Do not invent regulations.
- Do not create unsupported claims.
- Explain uncertainty.
- Provide practical recommendations.
- Follow AIRS methodology.
```

---

# 12. Module 7 — Report Draft Generation

## Output Structure

```text
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

# 13. Module 8 — Human Review Workflow

## Purpose

Quality control before delivery.

---

## Reviewer Checks

The reviewer verifies:

* information accuracy,
* logical consistency,
* recommendation usefulness,
* appropriate language,
* absence of unsupported legal claims.

---

## Status Flow

```text
Draft Generated

↓

Human Review

↓

Approved

↓

Delivered
```

---

# 14. Module 9 — PDF Generation

## Purpose

Create professional customer document.

---

## PDF Contains

* AI Risk Shield branding,
* company information,
* AIRS score,
* findings,
* recommendations,
* improvement plan,
* disclaimer.

---

# 15. Module 10 — Customer Delivery

After approval:

Customer receives:

* PDF report,
* summary,
* recommended next steps.

---

# 16. Complete Make.com Scenario v1

```text
1. Tally - Watch Submission

↓

2. Data Formatter

↓

3. Validation Module

↓

4. AIRS Scoring Logic

↓

5. Risk Category Mapping

↓

6. LLM Analysis

↓

7. PDF Generator

↓

8. Human Review Notification

↓

9. Email Delivery
```

---

# 17. MVP Implementation Order

## Step 1

Connect Tally webhook.

---

## Step 2

Receive test submission.

---

## Step 3

Create assessment object.

---

## Step 4

Implement scoring rules.

---

## Step 5

Connect AI analysis.

---

## Step 6

Generate first draft report.

---

## Step 7

Create human approval process.

---

## Step 8

Send first customer report.

---

# 18. Future Workflow Improvements

Future versions may include:

* database storage,
* customer dashboard,
* automated reminders,
* recurring assessments,
* AI inventory tracking,
* continuous governance monitoring.

---

# Status

Make.com Assessment Workflow v1 completed.

Next implementation step:

Build the first working Make.com scenario:

```
Tally

↓

Make Webhook

↓

Test JSON

↓

Assessment Object
```
