// src/components/auth/LoginForm.tsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { jwtDecode } from 'jwt-decode';
import type { UserPayload } from '../../context/AuthContext';
import api from '../../services/api';

// 1. A importação de 'styles' foi removida. Não é mais necessária aqui.

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const navigate = useNavigate();
  const auth = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    try {
        const response = await api.post('/token', params, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        const { access_token } = response.data;
        const decodedToken = jwtDecode<UserPayload>(access_token);
        
        auth.login(access_token);

        if (decodedToken.role === 'admin') {
            navigate('/admin');
        } else {
            navigate('/dashboard');
        }
    } catch (err: any) {
        setError(err.response?.data?.detail || 'Falha no login');
    } finally {
        setLoading(false);
    }
  };

  return (
    // 2. Os classNames foram trocados por strings normais
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      {error && <p style={{color: 'red', fontSize: '12px'}}>{error}</p>}
      <div className="input-group">
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
      </div>
      <div className="input-group">
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      </div>
      <a href="#" className="forgot-password">Esqueceu sua senha?</a>
      <button type="submit" disabled={loading}>{loading ? 'Entrando...' : 'Login'}</button>
    </form>
  );
};

export default LoginForm;