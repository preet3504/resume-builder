'use client';

export default function JobDescriptionInput({
  onJobDescriptionChange,
  value
}: {
  onJobDescriptionChange: (text: string) => void;
  value: string;
}) {
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onJobDescriptionChange(e.target.value);
  };

  return (
    <div className="space-y-4">
      <label className="block text-sm font-medium text-gray-700">Job Description</label>
      <div className="mt-1 relative">
        <textarea
          value={value}
          onChange={handleChange}
          rows={8}
          placeholder="Paste the complete job description here..."
          className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
        />
        <div className="absolute bottom-2 right-2 text-sm text-gray-500">
          {value.length}/10000 characters
        </div>
      </div>
      <p className="text-xs text-gray-500 mt-1">
        Include responsibilities, required skills, qualifications, and any specific keywords
      </p>
    </div>
  );
}