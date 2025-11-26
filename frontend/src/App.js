import React, { useState, useEffect } from 'react';
import Auth from './components/Auth';
import Notes from './components/Notes';

function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
    setTheme(savedTheme);
  }, []);

  const handleLogin = (userData) => {
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  const handleUserUpdate = (userData) => {
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
  };

  const handleThemeChange = (newTheme) => {
    localStorage.setItem('theme', newTheme);
    setTheme(newTheme);
  };

  return (
    <div className="App" data-theme={theme}>
      {user ? (
        <Notes user={user} onLogout={handleLogout} onUserUpdate={handleUserUpdate} theme={theme} onThemeChange={handleThemeChange} />
      ) : (
        <Auth onLogin={handleLogin} theme={theme} />
      )}
    </div>
  );
}

export default App;