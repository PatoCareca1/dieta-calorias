// src/components/auth/RegisterForm.tsx

import React, { useState } from 'react';
import api from '../../services/api';
import { Alert } from 'react-bootstrap';

// 1. A importação de 'styles' foi removida.

interface RegisterFormProps {
  onRegisterSuccess: () => void;
}

const RegisterForm = ({ onRegisterSuccess }: RegisterFormProps) => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await api.post('/usuarios/', {
        nome,
        email,
        senha: password,
      });

      setSuccess('Conta criada com sucesso! Redirecionando para o login...');

      setTimeout(() => {
        onRegisterSuccess();
      }, 2000);

    } catch (err: any) {
      setError(err.response?.data?.detail || 'Falha ao criar a conta.');
    } finally {
      setLoading(false);
    }
  };

  return (
    // 2. Os classNames foram trocados por strings normais
    <form onSubmit={handleSubmit}>
      <h2>Criar Conta</h2>

      {error && <Alert variant="danger" className="p-2 w-100">{error}</Alert>}
      {success && <Alert variant="success" className="p-2 w-100">{success}</Alert>}

      <div className="input-group">
        <input type="text" placeholder="Nome" value={nome} onChange={e => setNome(e.target.value)} required />
      </div>
      <div className="input-group">
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
      </div>
      <div className="input-group">
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
      </div>
      <button type="submit" disabled={loading}>{loading ? 'Registrando...' : 'Registrar'}</button>
    </form>
  );
};

export default RegisterForm;