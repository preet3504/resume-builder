'use client';

import { useState, useEffect } from 'react';

export default function ProcessingStatus({
  isGenerating,
  isGenerated
}: {
  isGenerating: boolean;
  isGenerated: boolean;
}) {
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('Analyzing your resume...');

  // Update progress when generating
  useEffect(() => {
    if (isGenerating) {
      // Simulate progress
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) return 100;
          return Math.min(prev + 10, 100);
        });

        // Update status text based on progress
        if (progress < 25) {
          setStatusText('Analyzing your resume...');
        } else if (progress < 50) {
          setStatusText('Extracting keywords from job description...');
        } else if (progress < 75) {
          setStatusText('Optimizing content for ATS...');
        } else {
          setStatusText('Generating final document...');
        }
      }, 300);

      return () => clearInterval(interval);
    } else if (!isGenerating && !isGenerated) {
      // Reset when not generating
      setProgress(0);
      setStatusText('Analyzing your resume...');
    }
  }, [isGenerating, progress]);

  return (
    <div className="flex-1 flex flex-col items-center justify-center space-y-4">
      {isGenerating && (
        <>
          <div className="w-full max-w-xs">
            <div className="flex justify-between text-sm font-medium text-gray-700 mb-1">
              <span>Processing...</span>
              <span id="progress-text">{progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                id="progress-bar"
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
          <p className="text-sm text-gray-500" id="status-text">
            {statusText}
          </p>
        </>
      )}
      {!isGenerating && isGenerated && (
        <div className="flex items-center space-x-3 text-green-600 font-medium">
          <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4a1 1 0 00-1.414-1.414L11 10.586V7a1 1 0 10-2 0v3.586l-.293-.293z" clipRule="evenodd" />
          </svg>
          <span>Resume generated successfully!</span>
        </div>
      )}
      {!isGenerating && !isGenerated && (
        <div className="text-sm text-gray-500">
          Ready to generate your optimized resume
        </div>
      )}
    </div>
  );
}