import { useEffect, useState } from 'react';
import Nav from './components/Nav';
import HomePage from './pages/HomePage';
import AnalyzerPage from './pages/AnalyzerPage';
import AuthModal from './pages/AuthModal';
import { api } from './services/api';

function App() {
  const [page, setPage] = useState('home');
  const [user, setUser] = useState(null);
  const [modal, setModal] = useState(null);

  // Restore the logged-in user from the saved token on page refresh.
  useEffect(() => {
    api.me().then((u) => u && setUser(u));
  }, []);

  const handleAuth = (u) => { 
    setUser(u); 
    setModal(null); 
    setPage('analyzer'); 
  };
  
  const onGoAnalyzer = () => {
    if (!user) setModal('login');
    else setPage('analyzer');
  };

  return (
    <div className="app-wrap">
      <Nav
        user={user} page={page}
        onLogin={()=>setModal('login')} onSignup={()=>setModal('signup')}
        onLogout={()=>{api.logout();setUser(null);setPage('home');}}
        onGoAnalyzer={onGoAnalyzer}
        onGoHome={()=>setPage('home')}
      />
      {page === 'home' && <HomePage onLogin={()=>setModal('login')} onSignup={()=>setModal('signup')} user={user} onGoAnalyzer={onGoAnalyzer} />}
      {page === 'analyzer' && <AnalyzerPage user={user} />}
      {modal && <AuthModal mode={modal} onClose={()=>setModal(null)} onAuth={handleAuth} />}
    </div>
  );
}

export default App;
