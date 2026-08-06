import React, { useState } from 'react';
import Navbar from './components/Navbar';
import SubmissionsList from './components/SubmissionsList';
import AssessmentReviewer from './components/AssessmentReviewer';
import ReportModal from './components/ReportModal';
import SubmissionSimulator from './components/SubmissionSimulator';
import { evaluateAssessment } from './utils/airsEngine';

const initialSubmissions = [
  {
    id: 'resp_89234712',
    status: 'Pending',
    createdAt: '2026-08-06T16:00:00.000Z',
    advisorNotes: '',
    data: {
      company: { name: 'Acme Software Solutions Ltd.', email: 'ceo@acmesoftware.eu', country: 'Poland', industry: 'Software Development & IT', company_size: '10-49 employees' },
      ai_adoption: { tools: ['ChatGPT', 'Claude', 'GitHub Copilot', 'Canva AI'], active_users: '6-20' },
      answers: {
        confidential_data_upload: true,
        confidential_data_details: 'Source code, API secrets, draft contracts, and support tickets.',
        human_review_frequency: 'Sometimes',
        ai_policy_status: 'No',
        ai_training_status: 'No',
        hr_automated_uses: ['Recruitment', 'CV Screening'],
        sells_ai_content: true,
        discloses_ai_in_contracts: 'No',
        past_incidents: ['AI Hallucination', 'Customer Complaint'],
        biggest_concern: 'EU AI Act'
      }
    }
  }
];

// Pre-evaluate initial dataset
initialSubmissions.forEach(sub => {
  sub.evaluation = evaluateAssessment(sub);
});

export default function App() {
  const [submissions, setSubmissions] = useState(initialSubmissions);
  const [selectedId, setSelectedId] = useState(initialSubmissions[0].id);
  const [activeTab, setActiveTab] = useState('all');
  const [previewSubmission, setPreviewSubmission] = useState(null);
  const [isSimulatorOpen, setIsSimulatorOpen] = useState(false);

  const pendingCount = submissions.filter(s => s.status === 'Pending').length;

  const filteredSubmissions = submissions.filter(sub => {
    if (activeTab === 'pending') return sub.status === 'Pending';
    if (activeTab === 'approved') return sub.status === 'Approved' || sub.status === 'Delivered';
    return true;
  });

  const selectedSubmission = submissions.find(s => s.id === selectedId) || filteredSubmissions[0];

  const handleApprove = (id, notes, customProcedures) => {
    setSubmissions(prev => prev.map(s => {
      if (s.id === id) {
        return {
          ...s,
          status: 'Approved',
          advisorNotes: notes,
          evaluation: {
            ...s.evaluation,
            remediationProcedures: customProcedures
          }
        };
      }
      return s;
    }));
  };

  const handleSimulateNewEntry = (preset) => {
    const newId = `resp_tally_${Math.floor(100000 + Math.random() * 900000)}`;
    const newSub = {
      id: newId,
      status: 'Pending',
      createdAt: new Date().toISOString(),
      advisorNotes: '',
      data: {
        company: preset.company,
        ai_adoption: preset.ai_adoption,
        answers: preset.answers
      }
    };
    newSub.evaluation = evaluateAssessment(newSub);

    setSubmissions([newSub, ...submissions]);
    setSelectedId(newId);
    setIsSimulatorOpen(false);
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-dark)' }}>
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        pendingCount={pendingCount}
        onOpenSimulator={() => setIsSimulatorOpen(true)}
      />

      <main style={{ maxWidth: '1380px', margin: '0 auto', padding: '32px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '380px 1fr', gap: '32px' }}>
          {/* Left Column: Submissions List */}
          <div>
            <div style={{ fontSize: '13px', color: 'var(--text-muted)', fontWeight: 700, uppercase: 'true', letterSpacing: '1px', marginBottom: '12px' }}>
              INCOMING ASSESSMENTS ({filteredSubmissions.length})
            </div>
            <SubmissionsList
              submissions={filteredSubmissions}
              selectedId={selectedId}
              onSelectSubmission={setSelectedId}
            />
          </div>

          {/* Right Column: Interactive Reviewer Workspace */}
          <div>
            <AssessmentReviewer
              submission={selectedSubmission}
              onApprove={handleApprove}
              onOpenPreview={setPreviewSubmission}
            />
          </div>
        </div>
      </main>

      {/* Report Modal */}
      {previewSubmission && (
        <ReportModal
          submission={previewSubmission}
          onClose={() => setPreviewSubmission(null)}
        />
      )}

      {/* Simulator Modal */}
      {isSimulatorOpen && (
        <SubmissionSimulator
          onSimulate={handleSimulateNewEntry}
          onClose={() => setIsSimulatorOpen(false)}
        />
      )}
    </div>
  );
}
