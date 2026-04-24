import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadResume } from '../services/api';
import { toast } from 'react-toastify';

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragActive(false);
    const f = e.dataTransfer?.files?.[0];
    if (f) validateAndSet(f);
  }, []);

  const handleChange = (e) => {
    const f = e.target.files?.[0];
    if (f) validateAndSet(f);
  };

  const validateAndSet = (f) => {
    const ext = f.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx', 'txt'].includes(ext)) {
      toast.error('Only PDF, DOCX, and TXT files are accepted');
      return;
    }
    if (f.size > 10 * 1024 * 1024) {
      toast.error('File size must be under 10MB');
      return;
    }
    setFile(f);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    try {
      const { data } = await uploadResume(file);
      toast.success('Resume uploaded and parsed!');
      navigate(`/analysis/${data.resume_id}`);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-12 animate-fade-in">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-white mb-2">Upload Your Resume</h1>
        <p className="text-surface-400">Step 1 of 5 — Let's analyze your resume</p>
        
        {/* Step indicator */}
        <div className="flex items-center justify-center gap-2 mt-6">
          {['Upload', 'Domain', 'ATS Score', 'Skill Gap', 'Roadmap'].map((step, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold
                ${i === 0 ? 'bg-primary-500 text-white' : 'bg-surface-800 text-surface-500'}`}>
                {i + 1}
              </div>
              <span className={`text-xs hidden sm:block ${i === 0 ? 'text-primary-400' : 'text-surface-500'}`}>{step}</span>
              {i < 4 && <div className="w-8 h-px bg-surface-700" />}
            </div>
          ))}
        </div>
      </div>

      {/* Drop zone */}
      <div
        className={`glass-card border-2 border-dashed cursor-pointer transition-all
          ${dragActive ? 'border-primary-400 bg-primary-500/5' : 'border-surface-700 hover:border-primary-500/40'}
          ${file ? 'border-green-500/40 bg-green-500/5' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input').click()}
      >
        <input id="file-input" type="file" accept=".pdf,.docx,.txt" onChange={handleChange} className="hidden" />
        
        <div className="text-center py-12">
          {file ? (
            <>
              <div className="text-5xl mb-4">✅</div>
              <p className="text-lg font-semibold text-green-400">{file.name}</p>
              <p className="text-sm text-surface-400 mt-1">{(file.size / 1024).toFixed(1)} KB • Ready to upload</p>
              <button onClick={(e) => { e.stopPropagation(); setFile(null); }}
                className="text-xs text-red-400 mt-3 hover:text-red-300">Remove</button>
            </>
          ) : (
            <>
              <div className="text-5xl mb-4">📄</div>
              <p className="text-lg font-semibold text-white mb-2">Drop your resume here</p>
              <p className="text-sm text-surface-400">or click to browse</p>
              <div className="flex justify-center gap-3 mt-4">
                {['PDF', 'DOCX', 'TXT'].map(f => (
                  <span key={f} className="skill-tag skill-tag-blue">{f}</span>
                ))}
              </div>
            </>
          )}
        </div>
      </div>

      {/* Upload button */}
      {file && (
        <div className="mt-6 text-center">
          <button onClick={handleUpload} disabled={uploading} className="btn-primary py-3 px-12 text-lg">
            {uploading ? (
              <span className="flex items-center gap-2"><div className="spinner w-5 h-5" /> Analyzing...</span>
            ) : 'Upload & Analyze →'}
          </button>
        </div>
      )}
    </div>
  );
}
