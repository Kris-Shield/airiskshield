import React, { useState } from 'react';
import { X, Play, Sparkles, Building } from 'lucide-react';

export default function SubmissionSimulator({ onSimulate, onClose }) {
  const samplePresets = [
    {
      id: 'preset_high_risk',
      label: 'Software Development House (High Risk)',
      company: { name: 'DevMatrix Systems Ltd.', email: 'cto@devmatrix.eu', country: 'Poland', industry: 'Software & Cloud', company_size: '10-49 employees' },
      ai_adoption: { tools: ['ChatGPT', 'Claude', 'GitHub Copilot'], active_users: '21-50' },
      answers: {
        confidential_data_upload: true,
        confidential_data_details: 'Source code, API secrets, customer support DB dumps',
        human_review_frequency: 'Sometimes',
        ai_policy_status: 'No',
        ai_training_status: 'No',
        hr_automated_uses: ['Recruitment', 'CV Screening'],
        sells_ai_content: true,
        discloses_ai_in_contracts: 'No',
        past_incidents: ['AI Hallucination', 'Customer Complaint'],
        biggest_concern: 'EU AI Act'
      }
    },
    {
      id: 'preset_moderate_risk',
      label: 'Digital Marketing Agency (Moderate Risk)',
      company: { name: 'Vanguard Media Group', email: 'hello@vanguardmedia.com', country: 'Germany', industry: 'Marketing & PR', company_size: '1-9 employees' },
      ai_adoption: { tools: ['ChatGPT', 'Midjourney', 'Canva AI'], active_users: '6-20' },
      answers: {
        confidential_data_upload: false,
        confidential_data_details: '',
        human_review_frequency: 'Usually',
        ai_policy_status: 'Currently being prepared',
        ai_training_status: 'Occasionally',
        hr_automated_uses: ['None'],
        sells_ai_content: true,
        discloses_ai_in_contracts: 'Yes',
        past_incidents: ['None'],
        biggest_concern: 'Copyright'
      }
    },
    {
      id: 'preset_trusted',
      label: 'Enterprise Consultancy (Trusted Governance)',
      company: { name: 'Apex Advisory Partners', email: 'compliance@apexadvisory.com', country: 'Netherlands', industry: 'Professional Services', company_size: '50-249 employees' },
      ai_adoption: { tools: ['Microsoft Copilot Pro', 'ChatGPT Enterprise'], active_users: 'More than 50' },
      answers: {
        confidential_data_upload: false,
        confidential_data_details: '',
        human_review_frequency: 'Always',
        ai_policy_status: 'Yes',
        ai_training_status: 'Regularly',
        hr_automated_uses: ['None'],
        sells_ai_content: false,
        discloses_ai_in_contracts: 'Yes',
        past_incidents: ['None'],
        biggest_concern: 'Client Trust'
      }
    }
  ];

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
      <div className="glass-card animate-fade-in" style={{ width: '100%', maxWidth: '560px', border: '1px solid var(--accent-cyan)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Sparkles color="var(--accent-cyan)" size={22} />
            <h2 style={{ fontSize: '18px', fontWeight: 800 }}>Simulate Tally Form Submission</h2>
          </div>
          <button className="btn-secondary" onClick={onClose} style={{ padding: '6px 10px' }}>
            <X size={16} />
          </button>
        </div>

        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '20px' }}>
          Select a pre-configured organizational profile to simulate an incoming webhook from Tally.so and execute live AIRS scoring:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {samplePresets.map(preset => (
            <div
              key={preset.id}
              onClick={() => onSimulate(preset)}
              style={{
                background: 'rgba(15, 23, 42, 0.6)',
                border: '1px solid var(--border-color)',
                borderRadius: '12px',
                padding: '16px',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                display: 'flex',
                justify-content: 'space-between',
                alignItems: 'center'
              }}
              onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--accent-cyan)'}
              onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border-color)'}
            >
              <div>
                <strong style={{ fontSize: '14px', color: 'var(--text-main)' }}>{preset.label}</strong>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>
                  {preset.company.name} • {preset.company.industry}
                </div>
              </div>
              <button className="btn-primary" style={{ padding: '6px 14px', fontSize: '12px' }}>
                <Play size={12} /> Inject
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
