# AI Risk Shield

# Data Flow & Privacy Model

**Version:** 0.1.0  
**Status:** Foundation Draft  
**Owner:** AI Risk Shield

---

# 1. Purpose

This document defines how information moves through the AI Risk Shield system.

The purpose is to ensure:

- transparency,
- privacy awareness,
- responsible data processing,
- clear separation between customer data and AI processing.

---

# 2. Core Privacy Principle

AI Risk Shield follows the principle:

> Collect only the information necessary to provide a meaningful assessment.

The system should avoid collecting unnecessary personal or confidential information.

---
# 3. High-Level Data Flow
---

# 4. Stage 1 — Data Collection

## Component

Tally.so Assessment Form

---

## Purpose

Collect information required for AI risk assessment.

---

## Initial Data Collected

Company information:

- company name,
- corporate email,
- country,
- industry,
- organization size.

AI usage information:

- tools used,
- business purpose,
- internal practices,
- risk assessment answers.

---

# 5. Data Minimization

AI Risk Shield does not require:

- customer passwords,
- private credentials,
- source code,
- confidential documents,
- unnecessary employee personal data.

---

# 6. Stage 2 — Automation Processing

## Component

Make.com

---

## Purpose

Workflow orchestration.

Responsibilities:

- receive form submission,
- validate fields,
- trigger assessment process,
- transfer structured information.

---

## Principle

Automation moves data.

Automation does not decide risk.

---

# 7. Stage 3 — Assessment Processing

## Component

AIRS Assessment Engine

---

## Responsibilities

The engine:

- maps answers to risk categories,
- applies scoring rules,
- identifies improvement areas.

---

## Important Rule

The score is generated from:

- defined methodology,
- documented rules.

Not from AI opinion.

---

# 8. Stage 4 — AI Processing

## Purpose

Generate understandable explanations.

AI receives:

- assessment results,
- selected knowledge sources,
- AIRS recommendations.

---

## AI Should Receive

Necessary context only.

---

## AI Should Not Receive

Unnecessary:

- private customer information,
- unrelated company data,
- sensitive information not required for analysis.

---

# 9. Stage 5 — Human Review

## Purpose

Quality assurance.

Before customer delivery:

A human reviewer checks:

- accuracy,
- logical consistency,
- recommendation relevance,
- unsupported statements.

---

# 10. Report Generation

The final report contains:

## Company AI Profile

Summary of AI adoption.

---

## AIRS Score

Maturity indicator.

---

## Risk Findings

Identified improvement areas.

---

## Recommendations

Practical actions.

---

## Limitations

Clear explanation that:

- report is an assessment,
- not legal advice,
- not certification.

---

# 11. Data Retention Principles

AI Risk Shield should define:

- what information is stored,
- how long it is stored,
- when it is deleted.

---

# 12. Security Principles

The system should support:

- encrypted communication,
- secure API usage,
- restricted access,
- separation of customer data.

---

# 13. Privacy by Design Checklist

Before every new feature:

Question:

## Is this data necessary?

If:

No

↓

Do not collect it.

---

Question:

## Does the customer understand why it is collected?

If:

No

↓

Improve transparency.

---

Question:

## Can the process work with less information?

If:

Yes

↓

Reduce data collection.

---

# 14. Future Development

Future versions may include:

- customer data dashboard,
- deletion controls,
- audit logs,
- privacy center,
- automated retention management.


---

# Status

Foundation privacy and data flow model.

Next document:

MVP Product Requirements Document
