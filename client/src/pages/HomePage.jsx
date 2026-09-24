import React from 'react';

function HomePage({ onLogin, onSignup, user, onGoAnalyzer }) {
  const feats = [
    { icon: '◎', title: 'Match Score', desc: 'Quantified compatibility between your resume and the job posting.' },
    { icon: '◈', title: 'Skill Match', desc: 'Instantly see which of your skills align with employer requirements.' },
    { icon: '◬', title: 'Gap Analysis', desc: 'Identify missing skills before the recruiter does.' },
    { icon: '◉', title: 'Upskill Guide', desc: 'Actionable enhancement tips to fill every skill gap.' },
  ];
  return (
    <div className="min-h-[calc(100vh-60px)] flex flex-col items-center justify-center text-center p-8 md:p-16 relative">
      <div className="font-mono text-[0.85rem] text-cyan-dim border border-border py-2 px-5 mb-8 tracking-[0.15em] animate-slide-up bg-[#000a1499] backdrop-blur-[6px]">
        AI-POWERED CAREER INTELLIGENCE SYSTEM v2.0
      </div>
      <h1 className="font-display text-[clamp(2.5rem,7vw,5.5rem)] font-black leading-none tracking-tight mb-6 animate-slide-up" style={{animationDelay:'0.1s'}}>
        <span className="block text-text-primary">DECODE YOUR</span>
        <span className="block text-cyan drop-shadow-[0_0_40px_#00f5ff]">DREAM JOB</span>
      </h1>
      <p className="text-[1.25rem] text-text-sec max-w-[560px] leading-[1.7] mb-12 animate-slide-up bg-[#000a1499] backdrop-blur-[6px] p-5 rounded-md shadow-lg [text-shadow:0_0_6px_rgba(0,255,255,0.3)]" style={{animationDelay:'0.2s'}}>
        Upload your resume. Paste the job description. Our neural engine will analyze the match, surface gaps, and build your path forward.
      </p>
      <div className="flex gap-4 justify-center flex-wrap animate-slide-up bg-[#000a1499] backdrop-blur-[6px] p-4 rounded-xl" style={{animationDelay:'0.3s'}}>
        {user ? (
          <button className="bg-cyan text-bg-void border-none font-display text-[1rem] font-bold py-4 px-10 cursor-pointer tracking-widest uppercase transition-all [clip-path:polygon(8px_0%,100%_0%,calc(100%-8px)_100%,0%_100%)] hover:bg-cyan-dim hover:-translate-y-0.5" onClick={onGoAnalyzer}>OPEN ANALYZER</button>
        ) : (
          <>
            <button className="bg-cyan text-bg-void border-none font-display text-[1rem] font-bold py-4 px-10 cursor-pointer tracking-widest uppercase transition-all [clip-path:polygon(8px_0%,100%_0%,calc(100%-8px)_100%,0%_100%)] hover:bg-cyan-dim hover:-translate-y-0.5" onClick={onSignup}>GET STARTED FREE</button>
            <button className="bg-transparent text-cyan border-2 border-cyan font-display text-[1rem] font-bold py-4 px-10 cursor-pointer tracking-widest uppercase transition-all hover:bg-cyan-dark" onClick={onLogin}>SIGN IN</button>
          </>
        )}
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-[2px] bg-border mt-16 max-w-[1100px] border border-border w-full">
        {feats.map((f,i) => (
          <div className="bg-bg-panel py-10 px-8 animate-slide-up bg-[#000a14cc] backdrop-blur-[4px]" key={i} style={{animationDelay:`${0.4+i*0.1}s`}}>
            <div className="text-[2.5rem] mb-5">{f.icon}</div>
            <div className="font-display text-[1.15rem] leading-tight text-cyan tracking-widest mb-3 [text-shadow:0_0_6px_rgba(0,255,255,0.3)]">{f.title}</div>
            <div className="text-[1rem] text-text-sec leading-[1.6]">{f.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HomePage;
