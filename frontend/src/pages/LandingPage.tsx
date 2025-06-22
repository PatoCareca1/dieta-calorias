// src/pages/LandingPage.tsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { animateScroll as scroll } from 'react-scroll';
import './LandingPage.css';

const LandingPage: React.FC = () => {
  // O estado 'scrolled' controlará a animação, como antes.
  const [scrolled, setScrolled] = useState(false);
  const navigate = useNavigate();

  // REMOVEMOS o useEffect e a função handleScroll que estavam causando o conflito.

  const handleScrollDown = () => {
    // 1. Ativa o estado 'scrolled' para iniciar a animação do CSS
    setScrolled(true); 
    // 2. Rola suavemente para a próxima seção
    scroll.scrollTo(window.innerHeight, { duration: 800, smooth: 'easeInOutQuart' });
  };

  const handleLoginRedirect = () => {
    navigate('/auth');
  };

  return (
    // A classe 'scrolled' continua sendo aplicada dinamicamente
    <div className={`landing-page ${scrolled ? 'scrolled' : ''}`}>
      <section className="welcome-section">
        <img src="/logo-fittrack.png" alt="FitTrack Logo" className="logo" width="150" height="auto"/>
        <h1>Bem-vindo ao FitTrack!</h1>
        <p className="tagline">
          Sua jornada fitness, de forma simples e inteligente.
        </p>
        <button className="scroll-down-btn" onClick={handleScrollDown}>
          ↓
        </button>
      </section>

      <section className="info-section">
        <h2>Transforme seu corpo e saúde com facilidade, segurança e precisão.</h2>
        <ul>
          <li><strong>Planos Alimentares Personalizados:</strong> Cálculos automáticos de calorias e macros adaptados ao seu perfil.</li>
          <li><strong>Acompanhamento Simples:</strong> Monitoramento de evolução em qualquer dispositivo.</li>
          <li><strong>Administração Fácil:</strong> Gestão completa de usuários e alimentos.</li>
          <li><strong>Segurança Total:</strong> Autenticação segura e dados protegidos.</li>
        </ul>
        <button className="login-btn" onClick={handleLoginRedirect}>
          Entrar no FitTrack
        </button>
      </section>
    </div>
  );
};

export default LandingPage;