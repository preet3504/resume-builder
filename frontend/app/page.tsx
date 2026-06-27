'use client';

import { useState } from 'react';
import ResumeUpload from '@/components/ResumeUpload';
import JobDescriptionInput from '@/components/JobDescriptionInput';
import GenerateButton from '@/components/GenerateButton';
import ProcessingStatus from '@/components/ProcessingStatus';
import DownloadButtons from '@/components/DownloadButtons';

export default function Home() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [isGenerated, setIsGenerated] = useState(false);
  const [pdfFileId, setPdfFileId] = useState<string | null>(null);
  const [docxFileId, setDocxFileId] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

  // Handle resume upload
  const handleResumeChange = (file: File | null) => {
    setResumeFile(file);
    setFormError(null); // Clear error when user uploads a new file
  };

  // Handle job description change
  const handleJobDescriptionChange = (text: string) => {
    setJobDescription(text);
    setFormError(null); // Clear error when user types
  };

  // Handle generate button click
  const handleGenerateClick = async () => {
    if (!resumeFile) {
      setFormError('Please upload a resume');
      return;
    }

    if (!jobDescription.trim()) {
      setFormError('Please enter a job description');
      return;
    }

    // Clear form error before API call
    setFormError(null);

    // Create form data
    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      // Call the API
      const response = await fetch(`${apiUrl}/api/v1/generate-optimized-resume`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || response.statusText);
      }

      const result = await response.json();
      setPdfFileId(result.pdf_file_id ?? null);
      setDocxFileId(result.docx_file_id ?? null);
      setIsGenerated(true);
    } catch (err: any) {
      setFormError(err.message || 'Unknown error');
    }
  };

  // Reset form
  const handleReset = () => {
    setResumeFile(null);
    setJobDescription('');
    setIsGenerated(false);
    setPdfFileId(null);
    setDocxFileId(null);
    setFormError(null);
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">
          ResumeTailor
        </h1>
        <p className="text-center text-gray-600 mb-10">
          Create optimized, ATS-friendly resumes tailored to your target job
          description
        </p>

        {(formError) && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md text-sm text-red-600">
            {formError}
          </div>
        )}

        <div className="space-y-8">
          <ResumeUpload onResumeChange={handleResumeChange} />
          <JobDescriptionInput
            onJobDescriptionChange={handleJobDescriptionChange}
            value={jobDescription}
          />
          <div className="flex flex-col sm:flex-row gap-4">
            <GenerateButton
              onClick={handleGenerateClick}
              isLoading={false} // We can add loading state if needed
              disabled={!resumeFile || !jobDescription.trim()}
            />
            <ProcessingStatus
              isGenerating={false} // We'll manage via state if needed
              isGenerated={isGenerated}
            />
          </div>
          {isGenerated && (
            <div className="mt-8 pt-4 border-t border-gray-200">
              <h2 className="text-xl font-semibold mb-4">Your resume is ready!</h2>
              <DownloadButtons
                pdfFileId={pdfFileId}
                docxFileId={docxFileId}
                onReset={handleReset}
              />
            </div>
          )}
        </div>
      </div>
    </main>
  );
}