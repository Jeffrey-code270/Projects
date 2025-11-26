import React, { useState } from 'react';
import { auth } from '../services/api';

const Auth = ({ onLogin, theme }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = isLogin 
        ? await auth.login({ email, password })
        : await auth.register({ username, email, password });
      
      localStorage.setItem('token', response.data.token);
      onLogin(response.data.user);
    } catch (error) {
      alert(error.response?.data?.message || 'Authentication failed');
    }
  };

  const authStyle = {
    maxWidth: '400px',
    margin: '100px auto',
    padding: '40px',
    background: 'var(--bg-card)',
    borderRadius: '15px',
    boxShadow: `0 15px 35px var(--shadow)`,
  };

  const inputStyle = {
    width: '100%',
    padding: '15px',
    margin: '10px 0',
    border: `2px solid var(--border)`,
    borderRadius: '8px',
    fontSize: '16px',
    background: 'var(--bg-card)',
    color: 'var(--text-primary)',
    transition: 'all 0.3s ease',
  };

  const buttonStyle = {
    width: '100%',
    padding: '15px',
    margin: '15px 0',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'transform 0.2s ease',
  };

  return (
    <div className="fade-in" style={authStyle}>
      <h2 style={{ textAlign: 'center', marginBottom: '30px', color: 'var(--text-primary)' }}>
        {isLogin ? '🔐 Login' : '📝 Register'}
      </h2>
      <form onSubmit={handleSubmit}>
        {!isLogin && (
          <input
            type="text"
            placeholder="👤 Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            style={inputStyle}
          />
        )}
        <input
          type="email"
          placeholder="📧 Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={inputStyle}
        />
        <input
          type="password"
          placeholder="🔒 Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={inputStyle}
        />
        <button 
          type="submit" 
          style={buttonStyle}
          onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
          onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
        >
          {isLogin ? 'Login' : 'Register'}
        </button>
      </form>
      <button 
        onClick={() => setIsLogin(!isLogin)} 
        style={{ ...buttonStyle, background: 'transparent', color: '#667eea', border: '2px solid #667eea' }}
      >
        {isLogin ? 'Need to register?' : 'Already have account?'}
      </button>
    </div>
  );
};

export default Auth;