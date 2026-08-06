import React from 'react';
import { Shield, Sparkles, CheckCircle2, FileText, PlusCircle } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, pendingCount, onOpenSimulator }) {
  return (
    <header style={{
      background: 'rgba(15, 23, 42, 0.95)',
      borderBottom: '1px solid var(--border-color)',
      padding: '16px 32px',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      backdropFilter: 'blur(16px)'
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        display: 'flex',
        justify-content: 'space-between',
        align-items: 'center'
      }}>
        {/* Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            background: 'linear-gradient(135deg, #06B6D4, #3B82F6)',
            padding: '10px',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(56, 189, 248, 0.4)'
          }}>
            <Shield size={24} color="#0F172A" strokeWidth={2.5} />
          </div>
          <div>
            <div className="gradient-text" style={{ fontSize: '20px', fontWeight: 800, letterSpacing: '-0.5px' }}>
              AI RISK SHIELD
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
              Human Governance Review Portal
            </div>
          </div>
        </div>

        {/* Status Pills / Filter Tabs */}
        <div style={{ display: 'flex', gap: '8px', background: 'rgba(30, 41, 59, 0.6)', padding: '4px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <button
            onClick={() => setActiveTab('all')}
            className={`btn-secondary ${activeTab === 'all' ? 'active' : ''}`}
            style={{
              padding: '6px 14px',
              fontSize: '13px',
              border: 'none',
              background: activeTab === 'all' ? 'var(--accent-blue)' : 'transparent',
              color: activeTab === 'all' ? '#FFF' : 'var(--text-muted)'
            }}
          >
            All Submissions
          </button>
          
          <button
            onClick={() => setActiveTab('pending')}
            style={{
              padding: '6px 14px',
              fontSize: '13px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: activeTab === 'pending' ? 'rgba(245, 158, 11, 0.2)' : 'transparent',
              color: activeTab === 'pending' ? '#FBBF24' : 'var(--text-muted)'
            }}
          >
            Pending Review
            {pendingCount > 0 && (
              <span style={{
                background: '#F59E0B',
                color: '#0F172A',
                fontSize: '11px',
                fontWeight: 800,
                padding: '1px 6px',
                borderRadius: '10px'
              }}>
                {pendingCount}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('approved')}
            style={{
              padding: '6px 14px',
              fontSize: '13px',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: 600,
              background: activeTab === 'approved' ? 'rgba(16, 185, 129, 0.2)' : 'transparent',
              color: activeTab === 'approved' ? '#34D399' : 'var(--text-muted)'
            }}
          >
            Approved
          </button>
        </div>

        {/* Action Button */}
        <button className="btn-primary" onClick={onOpenSimulator}>
          <PlusCircle size={18} />
          Simulate Tally Entry
        </button>
      </div>
    </header>
  );
}
