'use client';

import { useState } from 'react';
import { useApi } from '@/lib/api';
import ResumeUpload from '@/components/ResumeUpload';
import JobDescriptionInput from '@/components/JobDescriptionInput';
import GenerateButton from '@/components/GenerateButton';
import ProcessingStatus from '@/components/ProcessingStatus';
import DownloadButtons from '@/components/DownloadButtons';

export default function Home() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [{ data, loading, error }, { execute }] = useApi<any>();
  const [isGenerated, setIsGenerated] = useState(false);

  // Handle resume upload
  const handleResumeChange = (file: File | null) => {
    setResumeFile(file);
  };

  // Handle job description change
  const handleJobDescriptionChange = (text: string) => {
    setJobDescription(text);
  };

  // Handle generate button click
  const handleGenerateClick = async () => {
    if (!resumeFile) {
      setError('Please upload a resume');
      return;
    }

    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    // Create form data
    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);

    try {
      // Call the API
      await execute(
        fetch('/api/v1/generate-optimized-resume', {
          method: 'POST',
          body: formData,
        })
      );

      // In a real app, we would get a file ID from the response
      // For now, we'll just simulate success
      setIsGenerated(true);
    } catch (err) {
      // Error is handled by the useApi hook
    }
  };

  // Reset form
  const handleReset = () => {
    setResumeFile(null);
    setJobDescription('');
    setIsGenerated(false);
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

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md text-sm text-red-600">
            {error}
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
              isLoading={loading}
              disabled={loading || !resumeFile || !jobDescription.trim()}
            />
            <ProcessingStatus
              isGenerating={loading}
              isGenerated={isGenerated}
            />
          </div>
          {isGenerated && (
            <div className="mt-8 pt-4 border-t border-gray-200">
              <h2 className="text-xl font-semibold mb-4">Your resume is ready!</h2>
              <DownloadButtons onReset={handleReset} />
            </div>
          )}
        </div>
      </div>
    </main>
  );
}