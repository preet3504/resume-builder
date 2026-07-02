'use client';

export default function JobDescriptionInput({
  onJobDescriptionChange,
  value,
  onTailor
}: {
  onJobDescriptionChange: (text: string) => void;
  value: string;
  onTailor: () => void;
}) {
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onJobDescriptionChange(e.target.value);
  };

  return (
    <div className="w-full space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-bold tracking-tight text-white">Define the Target Role</h1>
        <p className="text-slate-400 max-w-xl mx-auto">Paste the job description below. Our AI will analyze the key requirements and optimize your resume accordingly.</p>
      </div>

      <div className="content-container overflow-hidden">
        <textarea
          value={value}
          onChange={handleChange}
          className="w-full h-80 bg-transparent p-10 outline-none border-none text-lg resize-none custom-scrollbar placeholder:text-slate-600"
          placeholder="Paste the job description here..."
        />
        <div className="flex flex-col sm:flex-row justify-between items-center px-10 py-6 bg-white/[0.02] border-t border-white/5 gap-4">
          <span className="text-sm font-mono text-slate-500">
            {value.length.toLocaleString()} / 10,000 characters
          </span>
          <button
            onClick={onTailor}
            disabled={!value.trim()}
            className="btn-primary flex items-center gap-2 w-full sm:w-auto justify-center"
          >
            <span>Tailor Resume</span>
            <i className="ti ti-arrow-right"></i>
          </button>
        </div>
      </div>
    </div>
  );
}
