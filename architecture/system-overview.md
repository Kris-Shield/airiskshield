# AI Risk Shield

# System Architecture Overview

**Version:** 0.1.0  
**Status:** Foundation Draft  
**Owner:** AI Risk Shield

---

# 1. Purpose

This document describes the high-level architecture of AI Risk Shield.

The architecture defines how user information moves through the system:

- data collection,
- assessment processing,
- risk evaluation,
- knowledge retrieval,
- AI-assisted analysis,
- human review,
- final report delivery.

---

# 2. Architecture Philosophy

AI Risk Shield follows this principle:

> Automation should increase efficiency without removing human responsibility.
> 
---

# 3. High-Level System Flow

---

# 4. System Components

---

# Component 1

# Client Interface

## Purpose

Collect structured information from organizations.

Initial implementation:

Tally.so Form

---

## Data Collected

Company information:

- company name,
- email,
- country,
- industry,
- company size.

AI usage information:

- AI tools used,
- business applications,
- risk assessment answers.

---

# Component 2

# Automation Layer

## Technology

Make.com

---

## Purpose

Connect system components.

Responsibilities:

- receive form submission,
- validate data,
- trigger assessment workflow,
- send data to AI engine,
- create report workflow.

---

# Component 3

# Assessment Engine

## Purpose

Apply AIRS methodology.

Responsibilities:

- map answers to risk categories,
- calculate scores,
- determine maturity level,
- generate findings.

---

# Component 4

# AIRS Scoring Engine

## Purpose

Calculate assessment results.

Inputs:

- questionnaire answers,
- risk weights,
- category rules.

Outputs:

- AIRS score,
- maturity level,
- priority areas.

---

# Component 5

# Knowledge Layer

## Purpose

Provide trusted information.

Sources:

- official regulations,
- standards,
- documented frameworks,
- AIRS internal knowledge.

---

## Principle

The AI system does not rely on general knowledge alone.

It retrieves relevant information before generating recommendations.

---

# Component 6

# AI Analysis Engine

## Purpose

Generate understandable explanations.

AI responsibilities:

- summarize findings,
- explain risks,
- prepare recommendations,
- adapt language to customer context.

---

## AI Limitations

AI does not:

- make legal decisions,
- certify compliance,
- replace experts.

---

# Component 7

# Human Review Layer

## Purpose

Ensure quality before delivery.

Reviewer checks:

- logical consistency,
- recommendation accuracy,
- unsupported claims,
- appropriate wording.

---

# Component 8

# Report Generator

## Purpose

Create customer-facing output.

Report includes:

## Executive Summary

Overview for management.

---

## AIRS Score

Overall maturity indicator.

---

## Risk Areas

Main findings.

---

## Recommendations

Practical improvement steps.

---

## Next Actions

Suggested roadmap.

---

# 5. Data Protection Principles

AI Risk Shield follows privacy-first design.

Principles:

- collect only necessary information,
- minimize sensitive data,
- protect customer information,
- avoid unnecessary storage.

---

# 6. MVP Architecture

Initial MVP:

---

# 7. Future Architecture

Future versions may include:

---

# 8. Security Principles

The system should support:

- secure API communication,
- controlled access,
- audit logging,
- separation of customer data.

---

# 9. Design Decision

AI Risk Shield is not designed as a fully autonomous AI compliance system.

It is designed as:

> A human-centered AI governance assistant.

---

# Status

Foundation architecture.

Next document:

Data Flow & Privacy Model

The system is designed around:
