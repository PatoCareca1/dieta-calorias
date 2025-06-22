import { createContext, useState, useContext, useEffect } from 'react';
import type { ReactNode } from 'react';
import api from '../services/api';
import { jwtDecode } from 'jwt-decode';

export interface UserPayload {
  sub: string; // email do usuário
  role: 'admin' | 'user'; // ou outros papéis que você definir
  iat: number;
  exp: number;
}

interface AuthContextType {
  token: string | null;
  user: UserPayload | null; // Estado do usuário
  loading: boolean; // Para sabermos quando a verificação inicial está ocorrendo
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('authToken'));
  const [user, setUser] = useState<UserPayload | null>(null);
  const [loading, setLoading] = useState(true); // Começa como true

  useEffect(() => {
    // Esta é a "Verificação de Sessão" 
    const verifyToken = async () => {
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        try {
          const decoded = jwtDecode<UserPayload>(storedToken);
          // Verifica se o token não expirou
          if (decoded.exp * 1000 > Date.now()) {
            setToken(storedToken);
            setUser(decoded);
            // Configura o header do axios para todas as requisições futuras 
            api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
          } else {
            // Se o token expirou, limpa
            localStorage.removeItem('authToken');
          }
        } catch (error) {
          console.error("Token inválido:", error);
          localStorage.removeItem('authToken');
        }
      }
      setLoading(false); // Finaliza o carregamento inicial
    };

    verifyToken();
  }, []);

  const login = (newToken: string) => {
    const decoded = jwtDecode<UserPayload>(newToken);
    localStorage.setItem('authToken', newToken);
    setToken(newToken);
    setUser(decoded);
    api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setUser(null);
    delete api.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ token, user, loading, login, logout }}>
      {!loading && children} {/* Só renderiza a aplicação depois de verificar o token */}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};