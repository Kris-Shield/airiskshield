import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, CheckCircle, Edit3, Eye, FileCheck, ExternalLink, MessageSquare } from 'lucide-react';
import { RadarChart, GaugeBar } from './RadarChart';

export default function AssessmentReviewer({ submission, onApprove, onOpenPreview }) {
  if (!submission) {
    return (
      <div className="glass-card" style={{ textFill: 'center', padding: '60px', textAlign: 'center', color: 'var(--text-muted)' }}>
        <Shield size={48} color="var(--accent-cyan)" style={{ marginBottom: '16px', opacity: 0.5 }} />
        <h3>Select a submission from the list to begin Human Governance Review</h3>
      </div>
    );
  }

  const evaluation = submission.evaluation || {};
  const company = submission.data?.company || {};
  const answers = submission.data?.answers || {};
  const adoption = submission.data?.ai_adoption || {};

  const [notes, setNotes] = useState(submission.advisorNotes || '');
  const [customRec, setCustomRec] = useState('');
  const [recommendations, setRecommendations] = useState(evaluation.remediationProcedures || []);

  useEffect(() => {
    setNotes(submission.advisorNotes || '');
    setRecommendations(evaluation.remediationProcedures || []);
  }, [submission.id]);

  const handleAddCustomRec = () => {
    if (!customRec.trim()) return;
    setRecommendations([
      ...recommendations,
      {
        title: customRec,
        timeline: "Days 1–30",
        priority: "HIGH",
        objective: "Custom Advisor Recommendation added during Human Review.",
        steps: ["Execute custom recommendation as advised by AIRS Governance Partner."]
      }
    ]);
    setCustomRec('');
  };

  const isApproved = submission.status === 'Approved' || submission.status === 'Delivered';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Banner */}
      <div className="glass-card" style={{ background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95))' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <div style={{ fontSize: '12px', color: 'var(--accent-cyan)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px' }}>
              HUMAN GOVERNANCE REVIEW WORKSPACE
            </div>
            <h1 style={{ fontSize: '24px', fontWeight: 800, marginTop: '4px' }}>{company.name}</h1>
            <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '2px' }}>
              Email: <strong>{company.email}</strong> • Size: <strong>{company.company_size}</strong> • Country: <strong>{company.country}</strong>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            <button className="btn-secondary" onClick={() => onOpenPreview(submission)}>
              <Eye size={16} /> Preview Report
            </button>
            <button
              className="btn-primary"
              disabled={isApproved}
              onClick={() => onApprove(submission.id, notes, recommendations)}
              style={{
                opacity: isApproved ? 0.6 : 1,
                background: isApproved ? 'var(--status-good)' : undefined
              }}
            >
              <CheckCircle size={16} />
              {isApproved ? 'Approved & Ready' : 'Approve Report'}
            </button>
          </div>
        </div>

        {/* Score & Gauge Header Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px', marginTop: '20px', paddingTop: '20px', borderTop: '1px solid var(--border-color)' }}>
          <div style={{ textAlign: 'center', background: 'rgba(15, 23, 42, 0.6)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>AIRS Score</div>
            <div style={{ fontSize: '42px', fontWeight: 900, color: '#38BDF8', lineHeight: 1, margin: '8px 0' }}>
              {evaluation.overallScore} <span style={{ fontSize: '14px', color: 'var(--text-muted)' }}>/ 100</span>
            </div>
            <span className={`badge ${evaluation.overallScore >= 76 ? 'badge-low' : (evaluation.overallScore >= 56 ? 'badge-moderate' : 'badge-critical')}`}>
              {evaluation.riskLevel}
            </span>
          </div>

          <div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '6px' }}>
              Governance Maturity Stage: <strong style={{ color: 'var(--accent-cyan)' }}>{evaluation.maturityLevel}</strong>
            </div>
            <GaugeBar score={evaluation.overallScore} width={420} height={38} />
          </div>
        </div>
      </div>

      {/* Visual Radar & High Risk Alert Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Radar Chart Card */}
        <div className="glass-card" style={{ textAlign: 'center' }}>
          <h3 style={{ fontSize: '15px', color: 'var(--accent-cyan)', marginBottom: '12px', fontWeight: 700 }}>AIRS 7-Domain Radar Footprint</h3>
          <RadarChart domainResults={evaluation.domainResults} width={360} height={280} />
        </div>

        {/* High Risk & Key Vulnerabilities Card */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h3 style={{ fontSize: '16px', color: 'var(--text-main)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertTriangle color="#F87171" size={18} />
              Regulatory & Risk Flags
            </h3>

            {evaluation.highRiskFlags && evaluation.highRiskFlags.length > 0 ? (
              <div style={{ background: 'rgba(239, 68, 68, 0.1)', borderLeft: '4px solid #EF4444', padding: '14px', borderRadius: '8px', fontSize: '13px', lineHeight: 1.5 }}>
                <strong style="color: #F87171;">⚠️ EU AI Act Annex III High-Risk Systems Detected:</strong>
                <ul style={{ marginLeft: '16px', marginTop: '6px' }}>
                  {evaluation.highRiskFlags.map((flag, idx) => (
                    <li key={idx}><strong>{flag.system_name}</strong> — {flag.description}</li>
                  ))}
                </ul>
              </div>
            ) : (
              <div style={{ background: 'rgba(16, 185, 129, 0.1)', borderLeft: '4px solid #10B981', padding: '14px', borderRadius: '8px', fontSize: '13px', color: '#34D399' }}>
                ✅ No EU AI Act High-Risk automated HR or biometric systems detected.
              </div>
            )}
          </div>

          <div style={{ marginTop: '16px', background: 'rgba(15, 23, 42, 0.5)', padding: '12px 16px', borderRadius: '8px', border: '1px solid var(--border-color)', fontSize: '12px', color: 'var(--text-muted)' }}>
            Active Tools: <strong style={{ color: 'var(--text-main)' }}>{(adoption.tools || []).join(', ')}</strong><br />
            Confidential Data Uploads: <strong style={{ color: answers.confidential_data_upload ? '#F87171' : '#34D399' }}>{answers.confidential_data_upload ? 'YES' : 'NO'}</strong>
          </div>
        </div>
      </div>

      {/* Domain Breakdown Table */}
      <div className="glass-card">
        <h3 style={{ fontSize: '16px', color: 'var(--text-main)', marginBottom: '16px', fontWeight: 700 }}>
          🛡️ 7-Domain Governance Breakdown
        </h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)', textAlign: 'left' }}>
              <th style={{ padding: '8px 12px' }}>Domain</th>
              <th style={{ padding: '8px 12px' }}>Weight</th>
              <th style={{ padding: '8px 12px' }}>Score</th>
              <th style={{ padding: '8px 12px' }}>Status</th>
              <th style={{ padding: '8px 12px' }}>Key Finding</th>
            </tr>
          </thead>
          <tbody>
            {evaluation.domainResults && Object.values(evaluation.domainResults).map((dom, idx) => (
              <tr key={idx} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
                <td style={{ padding: '10px 12px', fontWeight: 700 }}>{dom.name}</td>
                <td style={{ padding: '10px 12px' }}>{Math.round(dom.weight * 100)}%</td>
                <td style={{ padding: '10px 12px', fontWeight: 700 }}>{dom.score} / 100</td>
                <td style={{ padding: '10px 12px' }}>
                  <span style={{ fontWeight: 700, color: dom.status === 'Good' ? '#34D399' : (dom.status === 'Attention' ? '#FBBF24' : '#F87171') }}>
                    {dom.status}
                  </span>
                </td>
                <td style={{ padding: '10px 12px', color: 'var(--text-muted)' }}>{dom.finding}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Human Reviewer Notes & Custom Recommendations */}
      <div className="glass-card" style={{ border: '1px solid var(--accent-blue)' }}>
        <h3 style={{ fontSize: '16px', color: 'var(--accent-cyan)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <MessageSquare size={18} />
          Advisor Notes & Custom Remediation Additions
        </h3>
        
        <div style={{ marginBottom: '16px' }}>
          <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px', fontWeight: 600 }}>
            HUMAN ADVISOR NOTES (Included in Executive Summary)
          </label>
          <textarea
            rows={3}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add specific comments, client context, or custom instructions..."
            style={{
              width: '100%',
              padding: '12px',
              background: '#090D16',
              border: '1px solid var(--border-color)',
              borderRadius: '8px',
              color: 'var(--text-main)',
              fontSize: '13px',
              outline: 'none'
            }}
          />
        </div>

        <div>
          <label style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginBottom: '6px', fontWeight: 600 }}>
            ADD CUSTOM ADVISOR RECOMMENDATION
          </label>
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="text"
              value={customRec}
              onChange={(e) => setCustomRec(e.target.value)}
              placeholder="e.g., Conduct bi-weekly DLP audits for the Engineering team..."
              style={{
                flex: 1,
                padding: '10px 12px',
                background: '#090D16',
                border: '1px solid var(--border-color)',
                borderRadius: '8px',
                color: 'var(--text-main)',
                fontSize: '13px',
                outline: 'none'
              }}
            />
            <button className="btn-secondary" onClick={handleAddCustomRec}>
              Add Action
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
