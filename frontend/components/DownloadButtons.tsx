'use client';

export default function DownloadButtons({
  pdfFileId,
  docxFileId,
  onReset
}: {
  pdfFileId: string | null;
  docxFileId: string | null;
  onReset: () => void
}) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

  // Trigger a file download from the backend without navigating the SPA away.
  const downloadFile = (format: 'pdf' | 'docx', fileId: string) => {
    const url = `${apiUrl}/api/v1/download/${format}/${fileId}`;
    const link = document.createElement('a');
    link.href = url;
    link.download = `optimized-resume.${format}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleDownloadPDF = () => {
    if (!pdfFileId) return;
    downloadFile('pdf', pdfFileId);
  };

  const handleDownloadDOCX = () => {
    if (!docxFileId) return;
    downloadFile('docx', docxFileId);
  };

  return (
    <div className="mt-6 pt-5 border-t border-gray-200">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Download Your Resume</h3>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <button
          onClick={handleDownloadPDF}
          disabled={!pdfFileId}
          className="flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm bg-red-600 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 transition-colors"
        >
          <>
            <span className="mr-2">📄</span>
            <span>Download PDF</span>
          </>
        </button>

        <button
          onClick={handleDownloadDOCX}
          disabled={!docxFileId}
          className="flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-colors"
        >
          <>
            <span className="mr-2">📘</span>
            <span>Download DOCX</span>
          </>
        </button>
      </div>

      <p className="mt-3 text-xs text-gray-500">
        <span className="mr-1">💡</span>
        Both PDF and DOCX formats are optimized for Applicant Tracking Systems (ATS)
      </p>
    </div>
  );
}