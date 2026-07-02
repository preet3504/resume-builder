'use client';

import { useState } from 'react';
import ResumeUpload from '@/components/ResumeUpload';
import JobDescriptionInput from '@/components/JobDescriptionInput';
import UnifiedResultCard from '@/components/UnifiedResultCard';

export default function Home() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [isGenerated, setIsGenerated] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [pdfFileId, setPdfFileId] = useState<string | null>(null);
  const [docxFileId, setDocxFileId] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState(1);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

  // Handle resume upload
  const handleResumeChange = (file: File | null) => {
    setResumeFile(file);
    setFormError(null);
    if (file) {
      setTimeout(() => setCurrentStep(2), 500);
    }
  };

  // Handle job description change
  const handleJobDescriptionChange = (text: string) => {
    setJobDescription(text);
    setFormError(null);
  };

  // Handle generate API call
  const handleGenerateClick = async () => {
    if (!resumeFile || !jobDescription.trim()) return;

    setFormError(null);
    setIsGenerated(false);
    setIsGenerating(true);
    setCurrentStep(3);

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch(`${apiUrl}/api/v1/generate-optimized-resume`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || response.statusText);
      }

      const result = await response.json();
      setPdfFileId(result.pdf_file_id ?? null);
      setDocxFileId(result.docx_file_id ?? null);
      setIsGenerated(true);
    } catch (err: any) {
      setFormError(err.message || 'Unknown error');
      // If error occurs, stay on current step but show error
      setIsGenerating(false);
    } finally {
      // Don't set isGenerating false here immediately if successful, 
      // let UnifiedResultCard handle transition
    }
  };

  const handleReset = () => {
    setResumeFile(null);
    setJobDescription('');
    setIsGenerated(false);
    setIsGenerating(false);
    setPdfFileId(null);
    setDocxFileId(null);
    setFormError(null);
    setCurrentStep(1);
  };

  return (
    <div className="min-h-screen flex flex-col bg-bg">
      {/* Header / Navigation */}
      <header className="border-b border-white/5 py-6 px-8 flex justify-between items-center bg-black/20 backdrop-blur-sm sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-primary to-blue-600 rounded-lg flex items-center justify-center">
            <i className="ti ti-bolt text-black text-xl"></i>
          </div>
          <span className="font-bold text-xl tracking-tight text-white">Tailor<span className="text-primary">AI</span></span>
        </div>

        <nav className="hidden md:flex items-center gap-12">
          <div className="flex items-center gap-3">
            <div className={`step-dot ${currentStep >= 1 ? 'active' : ''}`}></div>
            <span className={`text-sm font-medium transition-opacity ${currentStep >= 1 ? 'opacity-100' : 'opacity-40'}`}>Resume</span>
          </div>
          <div className="flex items-center gap-3">
            <div className={`step-dot ${currentStep >= 2 ? 'active' : ''}`}></div>
            <span className={`text-sm font-medium transition-opacity ${currentStep >= 2 ? 'opacity-100' : 'opacity-40'}`}>Optimize</span>
          </div>
          <div className="flex items-center gap-3">
            <div className={`step-dot ${currentStep >= 3 ? 'active' : ''}`}></div>
            <span className={`text-sm font-medium transition-opacity ${currentStep >= 3 ? 'opacity-100' : 'opacity-40'}`}>Download</span>
          </div>
        </nav>
      </header>

      <main className="flex-grow flex flex-col items-center justify-center p-6 max-w-5xl mx-auto w-full">
        {formError && (
          <div className="w-full max-w-2xl mb-8 p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-sm text-red-400 flex items-center gap-3">
            <i className="ti ti-alert-circle text-lg"></i>
            {formError}
          </div>
        )}

        {currentStep === 1 && (
          <ResumeUpload onResumeChange={handleResumeChange} />
        )}

        {currentStep === 2 && (
          <JobDescriptionInput
            onJobDescriptionChange={handleJobDescriptionChange}
            value={jobDescription}
            onTailor={handleGenerateClick}
          />
        )}

        {currentStep === 3 && (
          <UnifiedResultCard
            isGenerating={isGenerating}
            isGenerated={isGenerated}
            pdfFileId={pdfFileId}
            docxFileId={docxFileId}
            onReset={handleReset}
          />
        )}
      </main>
    </div>
  );
}
