'use client';

import { useState, useEffect } from 'react';

interface UnifiedResultProps {
  isGenerating: boolean;
  isGenerated: boolean;
  pdfFileId: string | null;
  docxFileId: string | null;
  onReset: () => void;
}

export default function UnifiedResultCard({
  isGenerating,
  isGenerated,
  pdfFileId,
  docxFileId,
  onReset
}: UnifiedResultProps) {
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('Analyzing role mandate...');
  const [showSuccess, setShowSuccess] = useState(false);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

  const messages = [
    "Analyzing role mandate...",
    "Extracting key competencies...",
    "Mapping skills to requirements...",
    "Finalizing tailored profile..."
  ];

  // Handle simulated progress
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (isGenerating && !isGenerated) {
      // Normal simulation while waiting for API
      interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 95) return 95;
          return Math.min(prev + 1, 95);
        });
      }, 150);
    } else if (isGenerated) {
      // Speed up to 100% once API is complete
      interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return Math.min(prev + 5, 100);
        });
      }, 50);
    } else {
      setProgress(0);
      setShowSuccess(false);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isGenerating, isGenerated]);

  // Handle transition to success screen only after progress hits 100%
  useEffect(() => {
    if (progress === 100 && isGenerated) {
      const timer = setTimeout(() => {
        setShowSuccess(true);
      }, 600); // Visual breathing room at 100%
      return () => clearTimeout(timer);
    }
  }, [progress, isGenerated]);

  useEffect(() => {
    const msgIdx = Math.min(Math.floor(progress / 25), messages.length - 1);
    setStatusText(messages[msgIdx]);
  }, [progress, messages]);

  const downloadFile = (format: 'pdf' | 'docx', fileId: string) => {
    const url = `${apiUrl}/api/v1/download/${format}/${fileId}`;
    const link = document.createElement('a');
    link.href = url;
    link.download = `optimized-resume.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (!isGenerating && !isGenerated) return null;

  return (
    <div className="w-full max-w-2xl mx-auto overflow-hidden content-container relative transition-all duration-700 ease-in-out">
      {/* Processing State */}
      <div 
        className={`transition-all duration-700 ease-in-out p-12 md:p-20 flex flex-col items-center text-center ${
          showSuccess 
            ? 'opacity-0 scale-95 -translate-y-8 absolute inset-0 pointer-events-none' 
            : 'opacity-100 scale-100 translate-y-0 relative'
        }`}
      >
        <div className="relative w-24 h-24 mx-auto mb-10">
          <svg className="w-full h-full transform -rotate-90">
            <circle cx="48" cy="48" r="44" stroke="currentColor" strokeWidth="4" fill="transparent" className="text-white/5"></circle>
            <circle
              cx="48"
              cy="48"
              r="44"
              stroke="currentColor"
              strokeWidth="4"
              fill="transparent"
              strokeDasharray="276"
              strokeDashoffset={276 - (276 * progress) / 100}
              className="text-primary transition-all duration-300"
            ></circle>
          </svg>
          <div className="absolute inset-0 flex items-center justify-center font-bold text-xl text-white">
            {Math.floor(progress)}%
          </div>
        </div>
        <div className="space-y-2">
          <h3 className="text-2xl font-bold text-white">
            {progress === 100 ? "Optimization Complete" : statusText}
          </h3>
          <p className="text-sm text-slate-500">
            {progress === 100 ? "Your professional narrative has been precision-matched." : "Your tailored resume is being prepared"}
          </p>
        </div>
      </div>

      {/* Success & Download State */}
      <div 
        className={`transition-all duration-700 delay-150 ease-in-out p-10 md:p-12 flex flex-col items-center text-center ${
          showSuccess 
            ? 'opacity-100 scale-100 translate-y-0 relative' 
            : 'opacity-0 scale-105 translate-y-8 absolute inset-0 pointer-events-none'
        }`}
      >
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-green-500/10 mb-6 border border-green-500/20">
          <i className="ti ti-check text-4xl text-green-500"></i>
        </div>
        <h2 className="text-3xl font-bold mb-3 text-white">Resume Tailored Successfully</h2>
        <p className="text-slate-400 mb-10">Your professional profile has been precision-matched to the role requirements.</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
          <button
            onClick={() => pdfFileId && downloadFile('pdf', pdfFileId)}
            disabled={!pdfFileId}
            className="bg-white/[0.03] border border-white/10 p-8 rounded-xl flex flex-col items-center gap-4 group hover:bg-white/[0.08] hover:border-primary/30 transition-all"
          >
            <i className="ti ti-file-type-pdf text-4xl text-red-500 group-hover:scale-110 transition-transform"></i>
            <div className="flex flex-col gap-1">
              <span className="font-semibold text-white">Download PDF</span>
              <span className="text-[10px] text-slate-500 px-3 py-1 bg-white/5 rounded-full uppercase tracking-wider">Professional Format</span>
            </div>
          </button>
          <button
            onClick={() => docxFileId && downloadFile('docx', docxFileId)}
            disabled={!docxFileId}
            className="bg-white/[0.03] border border-white/10 p-8 rounded-xl flex flex-col items-center gap-4 group hover:bg-white/[0.08] hover:border-primary/30 transition-all"
          >
            <i className="ti ti-file-text text-4xl text-blue-500 group-hover:scale-110 transition-transform"></i>
            <div className="flex flex-col gap-1">
              <span className="font-semibold text-white">Download DOCX</span>
              <span className="text-[10px] text-slate-500 px-3 py-1 bg-white/5 rounded-full uppercase tracking-wider">Editable Version</span>
            </div>
          </button>
        </div>

        <button
          onClick={onReset}
          className="mt-10 px-6 py-2 text-slate-500 hover:text-white hover:bg-white/5 rounded-lg transition-all text-sm font-medium"
        >
          Start another optimization
        </button>
      </div>
    </div>
  );
}
