/**
 * AIRS Scoring Engine Utility for Web Dashboard
 * Evaluates Tally questionnaire answers, calculates weighted 7-domain scores,
 * detects EU AI Act Annex III High-Risk flags, and builds remediation roadmaps.
 */

export function evaluateAssessment(submission) {
  const data = submission.data || submission;
  const answers = data.answers || {};
  const company = data.company || {};
  const adoption = data.ai_adoption || {};

  const domainResults = {};
  const highRiskFlags = [];
  const remediationProcedures = [];

  // 1. AI Governance (20%)
  let govScore = 0;
  let govRecs = [];
  let govProcs = [];

  if (answers.ai_policy_status === "Yes") {
    govScore += 60;
  } else if (answers.ai_policy_status === "Currently being prepared") {
    govScore += 30;
    govRecs.push("Finalize and publish the draft AI Policy across all company departments.");
  } else {
    govRecs.push("Draft and implement an official Corporate AI Usage Policy immediately.");
    govProcs.push({
      title: "Establish Corporate AI Usage Policy",
      timeline: "Days 1–7",
      priority: "URGENT",
      objective: "Create clear operational rules defining approved AI tools, data restrictions, and employee obligations.",
      steps: [
        "Draft the official Acceptable Use Policy (AUP) for Artificial Intelligence.",
        "Categorize tools into Approved (Whitelisted), Conditional, and Prohibited (Blacklisted).",
        "Distribute policy to current employees and require signed acknowledgment.",
        "Integrate AI Policy review into employee onboarding."
      ],
      template: `POLICY SNIPPET — CORPORATE AI USAGE POLICY v1.0\n1. APPROVED TOOLS: Only company-provided enterprise AI tools are permitted.\n2. CONFIDENTIALITY: Uploading personal data (PII), customer credentials, or source code into public models is strictly PROHIBITED.\n3. HUMAN OVERSIGHT: Every employee is personally accountable for verifying AI output.\n4. INCIDENT REPORTING: Report data leaks or major hallucinations within 2 hours.`
    });
  }

  if (answers.ai_training_status === "Regularly") {
    govScore += 40;
  } else if (answers.ai_training_status === "Occasionally") {
    govScore += 20;
    govRecs.push("Formalize regular AI safety and prompt engineering training for employees.");
  } else {
    govRecs.push("Introduce mandatory employee training on responsible AI usage and risk awareness.");
    govProcs.push({
      title: "Mandatory Responsible AI Employee Training",
      timeline: "Days 8–30",
      priority: "HIGH",
      objective: "Ensure 100% of active AI users understand prompt security, data privacy, and output verification.",
      steps: [
        "Develop a 30-minute training module covering Prompt Security, Data Anonymization, and Hallucination Risk.",
        "Conduct mandatory workshops for active AI users.",
        "Maintain a training completion log for auditing."
      ]
    });
  }

  domainResults["AI Governance"] = {
    name: "AI Governance",
    weight: 0.20,
    score: govScore,
    status: govScore >= 70 ? "Good" : (govScore >= 40 ? "Attention" : "Critical"),
    finding: `Policy status: ${answers.ai_policy_status || 'No'}. Employee training: ${answers.ai_training_status || 'No'}.`,
    recommendations: govRecs,
    procedures: govProcs
  };

  // 2. Data Protection & Privacy (25%)
  let privacyScore = 100;
  let privacyRecs = [];
  let privacyProcs = [];

  if (answers.confidential_data_upload) {
    privacyScore -= 60;
    const detailsLower = (answers.confidential_data_details || "").toLowerCase();
    if (["source code", "api key", "password", "ticket", "contract", "financial", "client", "customer"].some(k => detailsLower.includes(k))) {
      privacyScore -= 20;
      privacyRecs.push("Stop uploading sensitive customer data, source code, or API keys into public AI models.");
      privacyProcs.push({
        title: "Data Loss Prevention (DLP) & Anonymization Protocol",
        timeline: "Days 1–7",
        priority: "URGENT",
        objective: "Prevent unauthorized transmission of customer PII, source code, and API keys to third-party LLM providers.",
        steps: [
          "IMMEDIATE ACTION: Issue security bulletin pausing upload of un-sanitized client code, contracts, and PII.",
          "Migrate team to Enterprise/Team plans featuring Zero Data Retention (ZDR).",
          "Implement automated data scrubbing tools prior to prompt submission.",
          "Audit browser extensions and AI plugins installed on employee devices."
        ],
        template: `ANONYMIZATION CHECKLIST FOR PROMPTS:\n[ ] Remove all customer names, phone numbers, email addresses, and tax IDs.\n[ ] Replace real financial numbers with placeholder figures (e.g., [AMOUNT_X]).\n[ ] Strip secret tokens, passwords, and private API keys from code snippets.\n[ ] Verify tool privacy settings state: "Data not used for model training".`
      });
    }
  }

  domainResults["Data Protection & Privacy"] = {
    name: "Data Protection & Privacy",
    weight: 0.25,
    score: Math.max(0, privacyScore),
    status: privacyScore >= 70 ? "Good" : (privacyScore >= 40 ? "Attention" : "Critical"),
    finding: answers.confidential_data_upload ? "Confidential data uploaded to public AI tools" : "No confidential data uploads reported.",
    recommendations: privacyRecs,
    procedures: privacyProcs
  };

  // 3. Human Oversight (15%)
  let oversightScore = 0;
  let oversightRecs = [];
  let oversightProcs = [];
  const revFreq = (answers.human_review_frequency || "").toLowerCase();

  if (revFreq.includes("always")) {
    oversightScore = 100;
  } else if (revFreq.includes("usually")) {
    oversightScore = 70;
    oversightRecs.push("Enforce 100% human-in-the-loop review for all customer-facing AI deliverables.");
  } else {
    oversightScore = revFreq.includes("sometimes") ? 35 : 0;
    oversightRecs.push("URGENT: Establish mandatory human oversight for AI deliverables to eliminate unverified AI output liability.");
    oversightProcs.push({
      title: "Human-in-the-Loop (HITL) Output Verification Procedure",
      timeline: "Days 1–7",
      priority: "URGENT",
      objective: "Eliminate legal and commercial liability caused by unverified AI hallucinations or errors delivered to clients.",
      steps: [
        "Designate responsible Human Approvers for each operational department.",
        "Establish pre-release verification checklist (Fact Check, Citation Check, Code Security Audit).",
        "Require sign-off documentation for customer-facing AI deliverables."
      ],
      template: `HUMAN REVIEW SIGN-OFF TEMPLATE:\nProject / Deliverable: ____________________\nAI Tool Used: ___________________________\nReviewer Name: __________________________\nChecklist Verified:\n [x] Fact & Data Verification Completed\n [x] Source Code Security Audit Passed\n [x] Copyright & Originality Checked\nApproval Signature: ______________________ Date: _________`
    });
  }

  domainResults["Human Oversight"] = {
    name: "Human Oversight",
    weight: 0.15,
    score: oversightScore,
    status: oversightScore >= 70 ? "Good" : (oversightScore >= 40 ? "Attention" : "Critical"),
    finding: `Output review frequency: ${answers.human_review_frequency || 'Sometimes'}.`,
    recommendations: oversightRecs,
    procedures: oversightProcs
  };

  // 4. Transparency & Incidents (10%)
  let incScore = 100;
  let incRecs = [];
  let incProcs = [];
  const incidents = answers.past_incidents || [];

  if (incidents.length > 0 && !incidents.includes("None")) {
    incScore = Math.max(10, 100 - incidents.length * 35);
    incRecs.push(`Conduct root-cause analysis for past incidents (${incidents.join(", ")}) and create an Incident Log.`);
    incProcs.push({
      title: "AI Incident Management & Post-Mortem Framework",
      timeline: "Days 8–30",
      priority: "HIGH",
      objective: "Log, analyze, and mitigate AI-generated errors, hallucinations, and customer complaints.",
      steps: [
        "Create an internal AI Incident Log tracking date, tool, root cause, and financial impact.",
        "Conduct post-mortem review for all past hallucinations or complaints.",
        "Implement guardrails preventing recurrence."
      ]
    });
  }

  domainResults["Transparency & Incidents"] = {
    name: "Transparency & Incidents",
    weight: 0.10,
    score: incScore,
    status: incScore >= 70 ? "Good" : (incScore >= 40 ? "Attention" : "Critical"),
    finding: `Incidents reported: ${incidents.length > 0 ? incidents.join(", ") : 'None'}.`,
    recommendations: incRecs,
    procedures: incProcs
  };

  // 5. Intellectual Property (10%)
  let ipScore = 100;
  let ipRecs = [];
  let ipProcs = [];

  if (answers.sells_ai_content) {
    const disclose = (answers.discloses_ai_in_contracts || "").toLowerCase();
    if (!["yes", "tak"].includes(disclose)) {
      ipScore = ["no", "nie"].includes(disclose) ? 15 : 40;
      ipRecs.push("Add clear AI assistance disclosure and IP ownership clauses in commercial client agreements.");
      ipProcs.push({
        title: "Client Contract AI Disclosure & IP Clause Integration",
        timeline: "Days 8–30",
        priority: "HIGH",
        objective: "Ensure legal clarity regarding client IP ownership and disclosure of AI assistance in deliverables.",
        steps: [
          "Review current Master Services Agreement (MSA) templates.",
          "Insert standard AI Transparency & IP Warranty clauses into client contracts.",
          "Inform commercial team regarding client disclosure requirements."
        ],
        template: `CONTRACT CLAUSE — AI ASSISTANCE DISCLOSURE & IP WARRANTY:\n"Provider may utilize Artificial Intelligence tools (including code assistants) to support deliverables. All final deliverables undergo mandatory human verification. Provider warrants that deliverables do not knowingly infringe third-party IP rights and assigns all IP rights to Client."`
      });
    }
  }

  domainResults["Intellectual Property"] = {
    name: "Intellectual Property",
    weight: 0.10,
    score: ipScore,
    status: ipScore >= 70 ? "Good" : (ipScore >= 40 ? "Attention" : "Critical"),
    finding: `Commercial AI content delivery: ${answers.sells_ai_content ? 'Yes' : 'No'}. Contract disclosure: ${answers.discloses_ai_in_contracts || 'No'}.`,
    recommendations: ipRecs,
    procedures: ipProcs
  };

  // 6. HR & High-Risk Systems (10%)
  let hrScore = 100;
  let hrRecs = [];
  let hrProcs = [];
  const hrUses = (answers.hr_automated_uses || []).filter(u => !["none", "brak"].includes(u.toLowerCase()));

  if (hrUses.length > 0) {
    hrScore = 10;
    hrUses.forEach(use => {
      highRiskFlags.push({
        system_name: `AI in ${use}`,
        regulation_reference: "EU AI Act — Annex III (High-Risk AI Systems)",
        severity: "Critical",
        description: `Using AI for '${use}' triggers High-Risk classification under Annex III. Requires mandatory risk management, technical logging, and human oversight.`
      });
    });
    hrRecs.push(`Conduct formal EU AI Act High-Risk assessment for automated systems in: ${hrUses.join(", ")}.`);
    hrProcs.push({
      title: "EU AI Act High-Risk Governance Framework (HR & Candidate Screening)",
      timeline: "Days 31–90",
      priority: "URGENT",
      objective: "Achieve full compliance with EU AI Act High-Risk System obligations for HR and automated decision tools.",
      steps: [
        "Establish formal Risk Management System (EU AI Act Article 9) for recruitment tools.",
        "Perform bias testing to ensure candidate filtering does not discriminate.",
        "Implement candidate disclosure notice (Article 50).",
        "Maintain continuous human oversight enabling recruiters to override AI decisions."
      ],
      template: `CANDIDATE DISCLOSURE NOTICE (EU AI ACT ART. 50):\n"Please note that ${company.name || 'Company'} utilizes AI-assisted screening tools to evaluate application materials. All final hiring decisions are made exclusively by human recruiters. You have the right to request human review of your application."`
    });
  }

  domainResults["HR & High-Risk Systems"] = {
    name: "HR & High-Risk Systems",
    weight: 0.10,
    score: hrScore,
    status: hrScore >= 70 ? "Good" : "Critical",
    finding: `Automated HR use cases: ${hrUses.length > 0 ? hrUses.join(", ") : 'None'}.`,
    recommendations: hrRecs,
    procedures: hrProcs
  };

  // 7. AI Literacy & Operations (10%)
  const tools = adoption.tools || [];
  const opsScore = Math.min(100, 60 + (tools.length >= 3 ? 20 : 0) + (answers.ai_training_status !== "No" ? 20 : 0));
  domainResults["AI Literacy & Operations"] = {
    name: "AI Literacy & Operations",
    weight: 0.10,
    score: opsScore,
    status: opsScore >= 70 ? "Good" : "Attention",
    finding: `Active tools: ${tools.join(", ") || 'None'}. Weekly user tier: ${adoption.active_users || '1-5'}.`,
    recommendations: [],
    procedures: []
  };

  // Calculate Weighted Overall Score
  const totalScore = Math.round(Object.values(domainResults).reduce((sum, d) => sum + (d.score * d.weight), 0) * 10) / 10;

  const maturityLevel = totalScore >= 91 ? "Trusted" : (totalScore >= 71 ? "Advanced" : (totalScore >= 51 ? "Managed" : (totalScore >= 31 ? "Developing" : "Initial")));
  const riskLevel = totalScore >= 76 ? "Low Risk" : (totalScore >= 56 ? "Moderate Risk" : (totalScore >= 36 ? "High Risk" : "Critical Risk"));

  // Aggregate all procedures
  Object.values(domainResults).forEach(d => {
    remediationProcedures.push(...d.procedures);
  });

  return {
    overallScore: totalScore,
    maturityLevel,
    riskLevel,
    domainResults,
    highRiskFlags,
    remediationProcedures
  };
}
