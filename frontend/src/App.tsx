import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdminLayout from './layouts/AdminLayout';
import ProtectedRoute from './components/ProtectedRoute';
import LandingPage from './pages/LandingPage';
import NotFoundPage from './pages/NotFoundPage';
import UserDashboardPage from './pages/UserDashboardPage';
import AdminDashboardPage from './pages/admin/AdminDashboardPage';
import AdminAlimentosPage from './pages/admin/AdminAlimentosPage';
import AdminUsuariosPage from './pages/admin/AdminUsuariosPage';
import CalculadoraPage from './pages/CalculadoraPage';
import AuthPage from './pages/AuthPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/calculadora" element={<CalculadoraPage />} /> 
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<UserDashboardPage />} />
          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<AdminDashboardPage />} />
            <Route path="alimentos" element={<AdminAlimentosPage />} />
            <Route path="usuarios" element={<AdminUsuariosPage />} />
          </Route>
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;