import { useState } from 'react';
import SignUp from './pages/SignUp';
import LogIn from './pages/LogIn';
import Dashboard from './pages/Dashboard';
import Exercise from './pages/Exercise';

function App() {
  const [currentPage, setCurrentPage] = useState('signup');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setCurrentPage('exercise');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentPage('login');
  };

  const navigateTo = (page) => {
    setCurrentPage(page);
  };

  return (
    <div>
      {currentPage === 'signup' && <SignUp navigateTo={navigateTo} />}
      {currentPage === 'login' && <LogIn navigateTo={navigateTo} onLogin={handleLogin} />}
      {currentPage === 'dashboard' && <Dashboard onLogout={handleLogout} />}
      {currentPage === 'exercise' && <Exercise onLogout={handleLogout} />}
    </div>
  );
}

export default App;