'use client';

import { useState } from 'react';

export default function ResumeUpload({ onResumeChange }: { onResumeChange: (file: File | null) => void }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFile = (file: File | null) => {
    setSelectedFile(file);
    onResumeChange(file);
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0] ?? null;
    if (file) {
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!validTypes.includes(file.type)) {
        alert('Please upload a PDF or DOCX file');
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
      }
      handleFile(file);
    }
  };

  return (
    <div className="w-full space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-bold tracking-tight text-white">Optimize Your Professional Narrative</h1>
        <p className="text-slate-400 max-w-xl mx-auto">Upload your current resume to begin the alignment process. We support PDF and DOCX formats up to 10MB.</p>
      </div>

      <div
        id="drop-zone"
        className={`content-container p-16 border-2 border-dashed ${dragActive ? 'border-primary bg-white/[0.05]' : 'border-white/10'} hover:border-primary/50 hover:bg-white/[0.02] cursor-pointer transition-all group flex flex-col items-center justify-center text-center`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById('resume-upload')?.click()}
      >
        <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
          <i className="ti ti-file-upload text-3xl text-primary"></i>
        </div>
        <h2 className="text-xl font-semibold mb-2">
          {selectedFile ? `Selected: ${selectedFile.name}` : 'Drag and drop your resume'}
        </h2>
        <p className="text-sm text-slate-500 mb-8">or click to browse from your computer</p>
        <button type="button" className="btn-primary">
          {selectedFile ? 'Change File' : 'Select File'}
        </button>
        <input
          id="resume-upload"
          type="file"
          accept=".pdf,.docx"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0] ?? null;
            if (file) {
              const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
              if (!validTypes.includes(file.type)) {
                alert('Please upload a PDF or DOCX file');
                return;
              }
              if (file.size > 10 * 1024 * 1024) {
                alert('File size must be less than 10MB');
                return;
              }
              handleFile(file);
            }
          }}
        />
      </div>
    </div>
  );
}
