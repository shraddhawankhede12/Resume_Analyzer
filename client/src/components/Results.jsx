import React from 'react';
import { ScoreRing } from './ScoreRing';
import { SkillBars } from './SkillBars';

function Results({ data }) {
  const { ring, verdict, color } = ScoreRing({ score: data.score });

  return (
    <div className="animate-slide-up mt-10">
      <div className="font-display text-[1rem] text-cyan-dim tracking-[0.2em] uppercase mb-8 pb-3 border-b border-border">
        ANALYSIS COMPLETE — {new Date().toLocaleTimeString()}
      </div>

      {/* Score */}
      <div className="grid grid-cols-1 md:grid-cols-[240px_1fr] gap-10 items-center bg-[#000a14a6] backdrop-blur-[6px] rounded-xl border border-border p-10 mb-8 text-center md:text-left shadow-lg">
        {ring}
        <div>
          <div className="font-display text-[2.25rem] font-bold mb-3 [text-shadow:0_0_6px_rgba(0,255,255,0.3)]" style={{color}}>{verdict}</div>
          <div className="text-[1.125rem] text-text-sec leading-[1.7]">{data.summary}</div>
        </div>
      </div>

      {/* Skill bars */}
      <div className="bg-[#000a14a6] backdrop-blur-[6px] rounded-xl border border-border p-8 mb-8 shadow-lg">
        <div className="font-mono text-[1rem] tracking-[0.15em] uppercase mb-6 pb-3 border-b border-border text-green flex items-center gap-2">Skill Strength Analysis</div>
        <SkillBars data={data.skillBars || []} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        {/* Matched */}
        <div className="bg-[#000a14a6] backdrop-blur-[6px] rounded-xl border border-border p-8 shadow-lg">
          <div className="font-mono text-[1rem] tracking-[0.15em] uppercase mb-6 pb-3 border-b border-border text-green flex items-center gap-2">◎ Matched Skills</div>
          <div className="flex flex-wrap gap-2">{(data.matched || []).map((s,i)=>(
            <span className="inline-block py-2 px-4 font-mono text-[0.95rem] tracking-wider rounded-md border border-green-dim text-green bg-[#39ff140d]" key={i}>{s}</span>
          ))}</div>
        </div>

        {/* Missing */}
        <div className="bg-[#000a14a6] backdrop-blur-[6px] rounded-xl border border-border p-8 shadow-lg">
          <div className="font-mono text-[1rem] tracking-[0.15em] uppercase mb-6 pb-3 border-b border-border text-magenta flex items-center gap-2">◈ Missing Skills</div>
          <div className="flex flex-wrap gap-2">{(data.missing || []).map((s,i)=>(
            <span className="inline-block py-2 px-4 font-mono text-[0.95rem] tracking-wider rounded-md border border-mag-dim text-magenta bg-[#ff006e0d]" key={i}>{s}</span>
          ))}</div>
        </div>

        {/* Enhance — full width */}
        <div className="col-span-1 md:col-span-2 bg-[#000a14a6] backdrop-blur-[6px] rounded-xl border border-border p-8 shadow-lg">
          <div className="font-mono text-[1rem] tracking-[0.15em] uppercase mb-6 pb-3 border-b border-border text-[#ff9f1c] flex items-center gap-2">◬ Enhancement Roadmap</div>
          {(data.enhance || []).map((item,i)=>(
            <div className="p-5 border border-border mb-4 bg-bg-deep rounded-lg" key={i}>
              <div className="font-display font-bold text-[1.1rem] text-[#ff9f1c] mb-3 tracking-wider">▸ {item.skill}</div>
              <ul className="list-none space-y-2">
                {item.tips.map((tip,j)=>(
                  <li className="text-[1rem] text-text-sec flex gap-3 items-start" key={j}>
                    <span className="text-cyan-dim shrink-0 mt-0.5">→</span> <span className="leading-relaxed">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Results;
