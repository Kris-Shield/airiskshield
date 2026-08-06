# AIRS Risk Categories & Assessment Mapping

## Artificial Intelligence Risk Standard

**Version:** 0.1.0  
**Status:** Foundation Draft  
**Owner:** AI Risk Shield

---

# 1. Purpose

This document defines how assessment questions are mapped to AIRS risk domains.

The purpose is to create a consistent relationship between:

- organization answers,
- risk categories,
- scoring impact,
- recommendations.

---

# 2. Assessment Model

---

# 3. Risk Category Overview

AIRS evaluates seven primary risk categories.

| Category | Code | Weight |
|---|---|---:|
| AI Governance | GOV | 20% |
| Data Protection & Privacy | PRIV | 25% |
| Human Oversight | HUMAN | 15% |
| Transparency | TRANS | 10% |
| Intellectual Property | IP | 10% |
| AI Literacy | EDU | 10% |
| Security & Operations | SEC | 10% |

---

# 4. Question Mapping

---

# Q001

## Data Entry & Privacy

Question:

Do your employees use free/public versions of AI tools to process client briefs, financial data, or proprietary code?

---

## Category

Data Protection & Privacy

Code:

PRIV

---

## Risk Factor

Uncontrolled processing of confidential or personal information.

---

## Impact

High

---

## Risk Logic

If:

YES

Then:

Increase privacy risk score.

Reason:

Public AI services may not provide appropriate organizational controls.

---

## Recommendation

Implement approved AI tools and establish internal rules regarding sensitive information.

---

# Q002

## Quality Control & Hallucinations

Question:

Are AI-generated outputs published or delivered to clients without mandatory human review?

---

## Category

Human Oversight

Code:

HUMAN

---

## Risk Factor

Insufficient review of AI-generated content.

---

## Impact

High

---

## Risk Logic

If:

YES

Then:

Increase human oversight risk.

---

## Recommendation

Introduce human review processes before external delivery.

---

# Q003

## Algorithmic Discrimination

Question:

Does your company use AI systems for screening CVs, evaluating employees, or customer segmentation?

---

## Category

Human Oversight

Code:

HUMAN

Secondary:

Transparency

---

## Risk Factor

Potential automated decision-making impact.

---

## Impact

High

---

## Risk Logic

If:

YES

Additional assessment required.

Reason:

Certain AI applications may require stronger governance controls.

---

## Recommendation

Document AI usage, establish oversight procedures, and evaluate potential impact.

---

# Q004

## Intellectual Property & Copyright

Question:

Do you sell AI-generated visual assets or copy to clients as your own proprietary work?

---

## Category

Intellectual Property

Code:

IP

---

## Risk Factor

Unclear ownership and licensing assumptions.

---

## Impact

Medium

---

## Risk Logic

If:

YES

Increase IP review requirement.

---

## Recommendation

Document AI usage and verify licensing and ownership conditions.

---

# Q005

## Corporate Governance

Question:

Has your staff signed an official Corporate AI Acceptable Use Policy?

---

## Category

AI Governance

Code:

GOV

---

## Risk Factor

Lack of organizational AI rules.

---

## Impact

Medium

---

## Risk Logic

If:

NO

Increase governance risk.

---

## Recommendation

Create and implement an internal AI usage policy.

---

# 5. Additional Assessment Questions

The MVP assessment should include additional context questions.

---

# Q006

## Company Size

Question:

How many employees or contractors work in your organization?

Options:

- 1-9
- 10-49
- 50+

Purpose:

Adjust risk interpretation based on organizational scale.

---

# Q007

## Industry

Question:

What industry does your company operate in?

Purpose:

Provide context for recommendations.

Examples:

- Software
- Marketing
- Accounting
- Real Estate
- Recruitment

---

# Q008

## AI Tools Used

Question:

Which AI tools does your organization currently use?

Examples:

- ChatGPT
- Claude
- Microsoft Copilot
- Midjourney
- Other tools

Purpose:

Improve recommendation relevance.

---

# 6. MVP Assessment Scope

Initial MVP includes:

Required:

- Company name
- Corporate email
- Country
- Industry
- Company size
- AI tools used
- Five core risk questions

---

# 7. Future Expansion

Future versions may include:

- industry-specific questions,
- evidence upload,
- policy review,
- AI inventory,
- vendor assessment.

---

# Status

Foundation assessment mapping.

Next document:

AIRS Recommendations Framework

Each assessment question follows this structure:
