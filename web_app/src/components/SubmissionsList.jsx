import React, { useState } from 'react';
import { Search, Building2, AlertTriangle, ArrowRight, ShieldAlert, Calendar } from 'lucide-react';

export default function SubmissionsList({ submissions, selectedId, onSelectSubmission }) {
  const [searchTerm, setSearchTerm] = useState('');

  const filtered = submissions.filter(sub => {
    const data = sub.data || sub;
    const name = data.company?.name || '';
    const industry = data.company?.industry || '';
    return name.toLowerCase().includes(searchTerm.toLowerCase()) || industry.toLowerCase().includes(searchTerm.toLowerCase());
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Search Bar */}
      <div style={{ position: 'relative' }}>
        <Search size={18} color="var(--text-muted)" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)' }} />
        <input
          type="text"
          placeholder="Search by company or industry..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px 12px 42px',
            background: 'var(--bg-card)',
            border: '1px solid var(--border-color)',
            borderRadius: '12px',
            color: 'var(--text-main)',
            fontSize: '14px',
            outline: 'none'
          }}
        />
      </div>

      {/* Submissions Cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {filtered.map(sub => {
          const isSelected = sub.id === selectedId;
          const evaluation = sub.evaluation || {};
          const company = sub.data?.company || {};
          const status = sub.status || 'Pending';
          const score = evaluation.overallScore || 0;
          const riskLevel = evaluation.riskLevel || 'High Risk';
          const hasHighRisk = evaluation.highRiskFlags && evaluation.highRiskFlags.length > 0;

          const riskBadgeClass = score >= 76 ? 'badge-low' : (score >= 56 ? 'badge-moderate' : (score >= 36 ? 'badge-high' : 'badge-critical'));
          const statusBadgeClass = status === 'Approved' ? 'badge-approved' : (status === 'Delivered' ? 'badge-delivered' : 'badge-pending');

          return (
            <div
              key={sub.id}
              onClick={() => onSelectSubmission(sub.id)}
              className="glass-card animate-fade-in"
              style={{
                cursor: 'pointer',
                borderColor: isSelected ? 'var(--accent-cyan)' : 'var(--border-color)',
                background: isSelected ? 'rgba(30, 41, 59, 0.9)' : 'var(--bg-card)',
                boxShadow: isSelected ? '0 0 20px rgba(56, 189, 248, 0.2)' : 'none',
                position: 'relative'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Building2 size={16} color="var(--accent-cyan)" />
                    <h3 style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text-main)' }}>{company.name || 'Company'}</h3>
                  </div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {company.industry} • {company.country} ({company.company_size})
                  </div>
                </div>

                <span className={`badge ${statusBadgeClass}`}>
                  {status}
                </span>
              </div>

              {/* High Risk Alert tag */}
              {hasHighRisk && (
                <div style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  background: 'rgba(239, 68, 68, 0.15)',
                  border: '1px solid #EF4444',
                  borderRadius: '6px',
                  padding: '3px 8px',
                  fontSize: '11px',
                  color: '#F87171',
                  marginBottom: '10px',
                  fontWeight: 600
                }}>
                  <ShieldAlert size={12} />
                  EU AI Act High-Risk Annex III
                </div>
              )}

              {/* Score & Risk Footer */}
              <div style={{
                display: 'flex',
                justify-content: 'space-between',
                alignItems: 'center',
                paddingTop: '10px',
                borderTop: '1px solid rgba(255, 255, 255, 0.06)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div style={{ fontSize: '20px', fontWeight: 900, color: '#38BDF8' }}>
                    {score} <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>/ 100</span>
                  </div>
                  <span className={`badge ${riskBadgeClass}`}>
                    {riskLevel}
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '13px', color: 'var(--accent-cyan)', fontWeight: 600 }}>
                  Review <ArrowRight size={14} />
                </div>
              </div>
            </div>
          );
        })}

        {filtered.length === 0 && (
          <div className="glass-card" style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
            No submissions match your search criteria.
          </div>
        )}
      </div>
    </div>
  );
}
