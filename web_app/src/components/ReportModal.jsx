import React from 'react';
import { X, Printer, Download, CheckCircle, ShieldAlert } from 'lucide-react';
import { RadarChart, GaugeBar } from './RadarChart';

export default function ReportModal({ submission, onClose }) {
  if (!submission) return null;

  const evaluation = submission.evaluation || {};
  const company = submission.data?.company || {};
  const answers = submission.data?.answers || {};
  const adoption = submission.data?.ai_adoption || {};
  const procedures = evaluation.remediationProcedures || [];

  const handlePrint = () => {
    window.print();
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(5, 8, 15, 0.85)',
      backdropFilter: 'blur(10px)',
      zIndex: 1000,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '24px'
    }}>
      <div style={{
        background: '#0B0F19',
        border: '1px solid var(--border-color)',
        borderRadius: '20px',
        width: '100%',
        maxWidth: '960px',
        maxHeight: '90vh',
        overflowY: 'auto',
        padding: '32px',
        position: 'relative',
        boxShadow: '0 20px 50px rgba(0,0,0,0.8)'
      }}>
        {/* Modal Controls */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', paddingBottom: '16px', borderBottom: '1px solid var(--border-color)' }}>
          <div style={{ fontSize: '14px', color: 'var(--accent-cyan)', fontWeight: 700 }}>
            PREVIEW: AI RISK SHIELD ASSESSMENT REPORT
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button className="btn-secondary" onClick={handlePrint}>
              <Printer size={16} /> Print / Save PDF
            </button>
            <button className="btn-secondary" onClick={onClose} style={{ padding: '8px 12px' }}>
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Printable Report Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', paddingBottom: '16px', borderBottom: '2px solid var(--border-color)' }}>
          <div>
            <div className="gradient-text" style={{ fontSize: '26px', fontWeight: 800 }}>AI RISK SHIELD</div>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>Responsible AI Governance & Visual Audit</div>
          </div>
          <div style={{ textAlign: 'right', fontSize: '12px', color: 'var(--text-muted)' }}>
            <div>Report ID: <strong>{submission.id}</strong></div>
            <div>Date: <strong>{new Date().toISOString().slice(0, 10)}</strong></div>
          </div>
        </div>

        {/* Hero Score & Profile */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
          <div style={{ background: 'var(--bg-card)', padding: '20px', borderRadius: '14px', border: '1px solid var(--border-color)', textFill: 'center', textAlign: 'center' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>AIRS GOVERNANCE INDEX</div>
            <div style={{ fontSize: '48px', fontWeight: 900, color: '#38BDF8', lineHeight: 1, margin: '6px 0' }}>
              {evaluation.overallScore} <span style={{ fontSize: '14px', color: 'var(--text-muted)' }}>/ 100</span>
            </div>
            <span className="badge badge-critical" style={{ marginTop: '4px' }}>{evaluation.riskLevel}</span>
            <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '8px' }}>Maturity Level: <strong>{evaluation.maturityLevel}</strong></div>
            <div style={{ marginTop: '12px' }}>
              <GaugeBar score={evaluation.overallScore} width={320} height={34} />
            </div>
          </div>

          <div style={{ background: 'var(--bg-card)', padding: '20px', borderRadius: '14px', border: '1px solid var(--border-color)' }}>
            <h3 style={{ fontSize: '15px', color: 'var(--accent-cyan)', marginBottom: '10px' }}>Company Profile</h3>
            <div style={{ fontSize: '13px', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              <p>Organization: <strong style={{ color: '#FFF' }}>{company.name}</strong></p>
              <p>Email: <strong style={{ color: '#FFF' }}>{company.email}</strong></p>
              <p>Industry / Country: <strong style={{ color: '#FFF' }}>{company.industry} ({company.country})</strong></p>
              <p>Company Size: <strong style={{ color: '#FFF' }}>{company.company_size}</strong></p>
              <p>Active AI Tools: <strong style={{ color: '#FFF' }}>{(adoption.tools || []).join(', ')}</strong></p>
            </div>
          </div>
        </div>

        {/* Executive Summary */}
        <div style={{ background: 'var(--bg-card)', padding: '20px', borderRadius: '14px', border: '1px solid var(--border-color)', marginBottom: '24px' }}>
          <h3 style={{ fontSize: '16px', color: 'var(--accent-cyan)', marginBottom: '8px' }}>Executive Summary</h3>
          <p style={{ fontSize: '13.5px', color: '#CBD5E1', lineHeight: 1.6 }}>
            This Responsible AI Risk Assessment report evaluates the artificial intelligence governance maturity of <strong>{company.name}</strong> ({company.industry}, {company.company_size}).
            Based on our AIRS methodology, {company.name} achieves an overall AI Governance Score of <strong>{evaluation.overallScore}/100</strong>, placing the organization at the <strong>'{evaluation.maturityLevel}'</strong> maturity level and classified as <strong>'{evaluation.riskLevel}'</strong>.
            {submission.advisorNotes && ` Advisor Note: ${submission.advisorNotes}`}
          </p>
        </div>

        {/* EU AI Act Alert */}
        {evaluation.highRiskFlags && evaluation.highRiskFlags.length > 0 && (
          <div style={{ background: 'rgba(239, 68, 68, 0.12)', borderLeft: '4px solid #EF4444', padding: '16px', borderRadius: '8px', marginBottom: '24px', fontSize: '13px', lineHeight: 1.6 }}>
            <strong style={{ color: '#F87171' }}>⚠️ EU AI Act Regulatory High-Risk Alert</strong><br />
            Your organization reported using AI for automated human resources and candidate evaluation ({evaluation.highRiskFlags.map(f => f.system_name).join(', ')}). Under Annex III of the EU AI Act, these use cases trigger High-Risk classification requiring mandatory risk management, technical logging, and human oversight.
          </div>
        )}

        {/* Radar & Table Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
          <div style={{ background: 'var(--bg-card)', padding: '16px', borderRadius: '14px', border: '1px solid var(--border-color)', textAlign: 'center' }}>
            <h4 style={{ fontSize: '13px', color: 'var(--accent-cyan)', marginBottom: '8px' }}>AIRS 7-Domain Maturity Radar</h4>
            <RadarChart domainResults={evaluation.domainResults} width={340} height={260} />
          </div>

          <div style={{ background: 'var(--bg-card)', padding: '16px', borderRadius: '14px', border: '1px solid var(--border-color)' }}>
            <h4 style={{ fontSize: '13px', color: 'var(--accent-cyan)', marginBottom: '8px' }}>7-Domain Score Summary</h4>
            <table style={{ width: '100%', fontSize: '12px', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ color: 'var(--text-muted)', borderBottom: '1px solid var(--border-color)', textAlign: 'left' }}>
                  <th style={{ padding: '4px' }}>Domain</th>
                  <th style={{ padding: '4px' }}>Score</th>
                  <th style={{ padding: '4px' }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {evaluation.domainResults && Object.values(evaluation.domainResults).map((dom, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '6px 4px', fontWeight: 600 }}>{dom.name}</td>
                    <td style={{ padding: '6px 4px' }}>{dom.score}/100</td>
                    <td style={{ padding: '6px 4px', fontWeight: 700, color: dom.status === 'Good' ? '#34D399' : (dom.status === 'Attention' ? '#FBBF24' : '#F87171') }}>
                      {dom.status}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Detailed Procedures */}
        <h3 style={{ fontSize: '18px', fontWeight: 800, marginBottom: '14px', borderBottom: '1px solid var(--border-color)', paddingBottom: '6px' }}>
          📋 Detailed Remediation Procedures
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '24px' }}>
          {procedures.map((proc, idx) => (
            <div key={idx} style={{ background: 'var(--bg-card)', padding: '16px 20px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <strong style={{ fontSize: '15px', color: '#38BDF8' }}>{idx + 1}. {proc.title}</strong>
                <span className="badge badge-critical" style={{ fontSize: '10px' }}>{proc.priority} • {proc.timeline}</span>
              </div>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '6px' }}><strong>Objective:</strong> {proc.objective}</p>
              <ol style={{ marginLeft: '18px', fontSize: '13px', color: '#CBD5E1' }}>
                {(proc.steps || []).map((step, sIdx) => <li key={sIdx}>{step}</li>)}
              </ol>
              {proc.template && (
                <pre style={{ background: '#090D16', border: '1px dashed var(--accent-cyan)', padding: '10px', borderRadius: '6px', fontSize: '11px', color: '#A5F3FC', marginTop: '10px', whiteSpace: 'pre-wrap' }}>
                  {proc.template}
                </pre>
              )}
            </div>
          ))}
        </div>

        {/* Disclaimer */}
        <div style={{ fontSize: '11px', color: 'var(--text-muted)', borderTop: '1px solid var(--border-color)', paddingTop: '16px' }}>
          <strong>DISCLAIMER:</strong> AI Risk Shield is a decision-support framework designed to assist organizations in identifying AI risks and establishing responsible AI governance practices. This report does not constitute binding legal advice or compliance certification.
        </div>
      </div>
    </div>
  );
}
