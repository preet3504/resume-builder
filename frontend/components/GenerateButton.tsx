'use client';

export default function GenerateButton({
  onClick,
  isLoading,
  disabled
}: {
  onClick: () => void;
  isLoading: boolean;
  disabled?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || isLoading}
      className="w-full flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-medium rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 transition-all duration-200"
    >
      {isLoading ? (
        <>
          <span className="mr-2">
            <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
          </span>
          <span>Generating your resume...</span>
        </>
      ) : (
        <>
          <span className="mr-2">✨</span>
          <span>Generate Optimized Resume</span>
        </>
      )}
    </button>
  );
}