'use client';

import { useState } from 'react';

export default function DownloadButtons({ onReset }: { onReset: () => void }) {
  const [isPreparing, setIsPreparing] = useState(false);

  const handleDownloadPDF = async () => {
    setIsPreparing(true);
    // Simulate API call to get PDF
    await new Promise(resolve => setTimeout(resolve, 1500));
    setIsPreparing(false);
    // In a real app: window.open(pdfUrl);
    alert('PDF download would start here');
    // Optionally call onReset after download?
    // onReset();
  };

  const handleDownloadDOCX = async () => {
    setIsPreparing(true);
    // Simulate API call to get DOCX
    await new Promise(resolve => setTimeout(resolve, 1500));
    setIsPreparing(false);
    // In a real app: window.open(docxUrl);
    alert('DOCX download would start here');
    // Optionally call onReset after download?
    // onReset();
  };

  return (
    <div className="mt-6 pt-5 border-t border-gray-200">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Download Your Resume</h3>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <button
          onClick={handleDownloadPDF}
          disabled={isPreparing}
          className="flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm bg-red-600 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 transition-colors"
        >
          {isPreparing ? (
            <>
              <span className="mr-2">⏳</span>
              <span>Preparing PDF...</span>
            </>
          ) : (
            <>
              <span className="mr-2">📄</span>
              <span>Download PDF</span>
            </>
          )}
        </button>

        <button
          onClick={handleDownloadDOCX}
          disabled={isPreparing}
          className="flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
        >
          {isPreparing ? (
            <>
              <span className="mr-2">⏳</span>
              <span>Preparing DOCX...</span>
            </>
          ) : (
            <>
              <span className="mr-2">📘</span>
              <span>Download DOCX</span>
            </>
          )}
        </button>
      </div>

      <p className="mt-3 text-xs text-gray-500">
        <span className="mr-1">💡</span>
        Both PDF and DOCX formats are optimized for Applicant Tracking Systems (ATS)
      </p>
    </div>
  );
}