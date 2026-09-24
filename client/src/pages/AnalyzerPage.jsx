import React, { useState, useRef } from 'react';
import Results from '../components/Results';
import { api } from '../services/api';

function AnalyzerPage({ user }) {
  const [resumeText, setResumeText] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [jd, setJd] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [drag, setDrag] = useState(false);
  const [error, setError] = useState('');
  const fileRef = useRef();

  const handleFile = (file) => {
    if (!file) return;
    setResumeFile(file);
  };

  const onDrop = e => {
    e.preventDefault(); setDrag(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const analyze = async () => {
    if (!resumeText.trim() && !resumeFile) return setError('Please upload a resume or paste resume text.');
    if (!jd.trim()) return setError('Please enter a job description.');
    setError(''); setLoading(true); setResults(null);

    try {
      const data = await api.analyzeResume({ resumeFile, resumeText, jobDescription: jd });
      setResults(data);
    } catch(e) {
      setError(e.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-[1240px] mx-auto p-10">
      <div className="mb-10 animate-slide-up">
        <div className="font-display text-[2.5rem] tracking-wider font-bold mb-2 [text-shadow:0_0_6px_rgba(0,255,255,0.3)]">RESUME <span className="text-cyan">ANALYZER</span></div>
        <div className="font-mono text-[1rem] text-text-muted mt-1 bg-[#000a14a6] backdrop-blur-[4px] py-2 px-4 inline-block rounded-md border border-border">neural match engine — upload resume + job description to begin</div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        {/* Resume Upload */}
        <div className="bg-[#000a14a6] backdrop-blur-[6px] rounded-xl border border-border p-8 relative animate-slide-up shadow-lg" style={{animationDelay:'0.1s'}}>
          <div className="absolute top-0 left-8 right-8 h-[2px] bg-gradient-to-r from-transparent via-cyan-dark to-transparent"></div>
          <div className="font-mono text-[0.95rem] text-cyan-dim tracking-[0.15em] uppercase mb-6 flex items-center gap-2">
            Resume Input
          </div>
          <div
            className={`border-2 border-dashed min-h-[160px] flex flex-col items-center justify-center gap-4 cursor-pointer transition-all p-10 rounded-lg text-center ${drag ? 'border-cyan bg-cyan-dark' : 'border-border bg-[#040c12] hover:border-cyan hover:bg-cyan-dark/50'}`}
            onDragOver={e=>{e.preventDefault();setDrag(true)}}
            onDragLeave={()=>setDrag(false)}
            onDrop={onDrop}
            onClick={()=>fileRef.current.click()}
          >
            {resumeFile ? (
              <div className="text-green font-mono text-[1rem]">✓ {resumeFile.name}</div>
            ) : (
              <>
                <div className="text-[3rem] opacity-50 mb-2">⬆</div>
                <div className="font-mono text-[1rem] text-text-sec">Drop PDF / DOCX here or click to browse</div>
                <div className="text-[0.85rem] text-text-muted">Supported: .pdf .docx .txt</div>
              </>
            )}
            <input ref={fileRef} type="file" accept=".pdf,.docx,.txt" className="hidden" onChange={e=>handleFile(e.target.files[0])} />
          </div>
          <div className="mt-6">
            <div className="font-mono text-[0.85rem] text-cyan-dim tracking-widest mb-3 uppercase">OR PASTE RESUME TEXT</div>
            <textarea className="w-full bg-[#040c12] border border-border rounded-lg text-text-primary font-mono text-[1rem] p-5 outline-none resize-y min-h-[120px] transition-colors leading-[1.6] focus:border-cyan placeholder-text-sec/60" placeholder="Paste your resume content here..." value={resumeText} onChange={e=>setResumeText(e.target.value)} />
          </div>
        </div>

        {/* Job Description */}
        <div className="bg-[#000a14a6] backdrop-blur-[6px] rounded-xl border border-border p-8 relative animate-slide-up shadow-lg" style={{animationDelay:'0.2s'}}>
          <div className="absolute top-0 left-8 right-8 h-[2px] bg-gradient-to-r from-transparent via-cyan-dark to-transparent"></div>
          <div className="font-mono text-[0.95rem] text-cyan-dim tracking-[0.15em] uppercase mb-6 flex items-center gap-2">
            Job Description
          </div>
          <textarea
            className="w-full bg-[#040c12] border border-border rounded-lg text-text-primary font-mono text-[1rem] p-5 outline-none resize-y h-[calc(100%-4rem)] min-h-[300px] transition-colors leading-[1.6] focus:border-cyan placeholder-text-sec/60"
            placeholder="Paste the job description here...&#10;&#10;Include role title, responsibilities, requirements, and preferred skills for best results."
            value={jd}
            onChange={e=>setJd(e.target.value)}
          />
        </div>
      </div>

      {error && <div className="font-mono text-[1rem] text-magenta mb-6 p-4 border border-mag-dim bg-[#ff006e0d] rounded-md">⚠ {error}</div>}

      <button className={`w-full bg-cyan text-bg-void border-none font-display text-[1.125rem] font-bold py-5 px-6 cursor-pointer tracking-[0.15em] uppercase transition-all mb-10 [clip-path:polygon(16px_0%,100%_0%,calc(100%-16px)_100%,0%_100%)] ${loading ? 'animate-pulse-glow disabled:opacity-50 disabled:cursor-not-allowed' : 'hover:bg-cyan-dim hover:shadow-[0_0_15px_rgba(0,255,255,0.5)]'}`} onClick={analyze} disabled={loading}>
        {loading ? '◉ ANALYZING...' : '◎ RUN ANALYSIS'}
      </button>

      {loading && (
        <div className="flex flex-col items-center justify-center gap-6 py-20 bg-[#000a14a6] backdrop-blur-[6px] rounded-xl border border-border shadow-lg">
          <div className="w-[56px] h-[56px] border-[3px] border-border border-t-cyan rounded-full animate-spin-slow shadow-[0_0_15px_rgba(0,255,255,0.3)]" />
          <div className="font-mono text-[1rem] text-text-sec tracking-widest animate-pulse-glow">NEURAL ENGINE PROCESSING...</div>
        </div>
      )}

      {results && <Results data={results} />}
    </div>
  );
}

export default AnalyzerPage;
