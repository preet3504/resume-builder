'use client';

export default function ResumeUpload({ onResumeChange }: { onResumeChange: (file: File | null) => void }) {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    if (file) {
      // Validate file type
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!validTypes.includes(file.type)) {
        alert('Please upload a PDF or DOCX file');
        return;
      }
      // Validate file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
      }
    }
    onResumeChange(file);
  };

  return (
    <div className="space-y-4">
      <label className="block text-sm font-medium text-gray-700">Resume Upload</label>
      <div className="mt-1 flex flex-col space-y-2">
        <div className="flex items-center justify-between w-full border-2 border-dashed border-gray-300 rounded-lg px-4 py-6 text-center hover:border-gray-400 transition-colors">
          <div className="flex flex-col items-center">
            <svg className="h-8 w-8 text-gray-400 mb-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 29h6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M9 7h6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M18 4v4a2 2 0 002 2v10a2 2 0 00-2 2h-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M6 4v4a2 2 0 00-2 2v10a2 2 0 002 2h4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M9 16V10L12 13l3-3v6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <div className="text-sm text-gray-600">Drag & drop your resume here, or</div>
            <label className="text-primary-600 hover:text-primary-500 cursor-inline">
              Browse files
            </label>
          </div>
        </div>
        <input
          type="file"
          accept=".pdf,.docx"
          className="hidden"
          onChange={handleFileChange}
        />
        <p className="text-xs text-gray-500">
          PDF or DOCX format, max 10MB
        </p>
      </div>
    </div>
  );
}