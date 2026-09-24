import React, { useState } from 'react';

import { api } from '../services/api';

function AuthModal({ mode: initMode, onClose, onAuth }) {
  const [mode, setMode] = useState(initMode);
  const [email, setEmail] = useState('');
  const [pass, setPass] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async () => {
    if (busy) return;
    if (!email || !pass) return setError('All fields required.');
    setBusy(true);
    setError('');
    try {
      const user = mode === 'signup'
        ? await api.signup({ email, password: pass, name })
        : await api.login({ email, password: pass });
      onAuth(user);
    } catch (e) {
      setError(e.response?.data?.detail || 'Cannot reach the server. Please try again.');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[200] bg-[#020408]/90 backdrop-blur-sm flex items-center justify-center animate-slide-up" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="bg-[#040c12]/95 backdrop-blur-[12px] border border-border-bright w-full max-w-[460px] p-12 relative shadow-2xl">
        <div className="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-transparent via-cyan to-transparent"></div>
        <div className="corner-deco corner-tl"/><div className="corner-deco corner-tr"/>
        <div className="corner-deco corner-bl"/><div className="corner-deco corner-br"/>
        <button className="absolute top-4 right-4 bg-transparent border-none text-text-muted cursor-pointer text-2xl hover:text-cyan" onClick={onClose}>✕</button>
        
        <div className="font-display text-[1.5rem] text-cyan mb-2 tracking-widest [text-shadow:0_0_8px_rgba(0,255,255,0.4)]">{mode === 'login' ? 'SYSTEM LOGIN' : 'INITIALIZE ACCOUNT'}</div>
        <div className="text-[1rem] text-text-muted mb-8 font-mono bg-[#000a1499] px-2 py-1 inline-block">{mode === 'login' ? 'authenticate to continue' : 'create new user profile'}</div>
        
        {error && <div className="text-magenta text-[0.8rem] font-mono mb-4">⚠ {error}</div>}
        
        {mode === 'signup' && (
          <>
            <div className="text-[0.85rem] text-text-sec tracking-widest uppercase mb-2 font-mono mix-blend-lighten">Display Name</div>
            <input className="w-full bg-bg-deep border border-border text-text-primary font-mono text-[1rem] py-3 px-4 mb-6 outline-none transition-colors focus:border-cyan placeholder:text-text-muted/50" placeholder="agent_name" value={name} onChange={e=>setName(e.target.value)} />
          </>
        )}
        
        <div className="text-[0.85rem] text-text-sec tracking-widest uppercase mb-2 font-mono mix-blend-lighten">Email Address</div>
        <input className="w-full bg-bg-deep border border-border text-text-primary font-mono text-[1rem] py-3 px-4 mb-6 outline-none transition-colors focus:border-cyan placeholder:text-text-muted/50" type="email" placeholder="user@domain.io" value={email} onChange={e=>setEmail(e.target.value)} />
        
        <div className="text-[0.85rem] text-text-sec tracking-widest uppercase mb-2 font-mono mix-blend-lighten">Password</div>
        <input className="w-full bg-bg-deep border border-border text-text-primary font-mono text-[1rem] py-3 px-4 mb-6 outline-none transition-colors focus:border-cyan placeholder:text-text-muted/50" type="password" placeholder="••••••••" value={pass} onChange={e=>setPass(e.target.value)} onKeyDown={e=>e.key==='Enter'&&submit()} />
        
        <button className="w-full bg-cyan text-bg-void border-none font-display text-[1rem] font-bold p-4 cursor-pointer tracking-widest uppercase transition-all mb-4 mt-2 hover:bg-cyan-dim disabled:opacity-60" disabled={busy} onClick={submit}>
          {busy ? 'PLEASE WAIT...' : mode === 'login' ? 'AUTHENTICATE' : 'CREATE ACCOUNT'}
        </button>
        
        <div className="text-[0.95rem] text-text-muted mt-4 text-center">
          {mode === 'login' ? (
            <>No account? <button className="bg-transparent border-none text-cyan cursor-pointer text-[0.95rem] tracking-wide hover:text-white" onClick={()=>{setMode('signup');setError('');}}>Sign up</button></>
          ) : (
            <>Already have one? <button className="bg-transparent border-none text-cyan cursor-pointer text-[0.95rem] tracking-wide hover:text-white" onClick={()=>{setMode('login');setError('');}}>Login</button></>
          )}
        </div>
      </div>
    </div>
  );
}

export default AuthModal;
