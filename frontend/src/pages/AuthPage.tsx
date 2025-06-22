import { useState } from 'react';
import './AuthPage.css';
import LoginForm from '../components/auth/LoginForm';
import RegisterForm from '../components/auth/RegisterForm';

const AuthPage = () => {
  const [isSignUp, setIsSignUp] = useState(false);
  const containerClassName = `container ${isSignUp ? 'right-panel-active' : ''}`;

  return (
    <div className="auth-page-wrapper"> 
      <div className={containerClassName} id="container">
        <div className="form-box register-form-box">
          <RegisterForm onRegisterSuccess={() => setIsSignUp(false)} /> 
        </div>
        <div className="form-box login-box">
          <LoginForm />
        </div>
        <div className="overlay-container">
          <div className="overlay">
            <div className="overlay-panel overlay-left">
              <h1>Bem vindo!</h1>
              <p>Já têm uma conta?</p>
              <button className="ghost" onClick={() => setIsSignUp(false)}>
                Login
              </button>
            </div>
            <div className="overlay-panel overlay-right">
              <h1>Olá, Amigo!</h1>
              <p>Ainda não têm uma conta?</p>
              <button className="ghost" onClick={() => setIsSignUp(true)}>
                Cadastre-se
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;