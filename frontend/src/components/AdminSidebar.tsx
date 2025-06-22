// frontend/src/components/AdminSidebar.tsx
import React from 'react';
import { Nav } from 'react-bootstrap';
import { NavLink } from 'react-router-dom'; // Use NavLink para links de navegação

const AdminSidebar: React.FC = () => {
  return (
    // 'sticky-top' mantém o menu visível ao rolar
    <Nav className="flex-column p-3 text-white sticky-top">
      <Nav.Item className="mb-3">
        <h3 className="text-white">Admin</h3>
      </Nav.Item>
      
      {/* O NavLink do React Router adiciona uma classe 'active' automaticamente */}
      <Nav.Link as={NavLink} to="/admin" end className="text-white">
        Dashboard
      </Nav.Link>
      <Nav.Link as={NavLink} to="/admin/alimentos" className="text-white">
        Gerenciar Alimentos
      </Nav.Link>
      <Nav.Link as={NavLink} to="/admin/usuarios" className="text-white">
        Gerenciar Usuários
      </Nav.Link>
    </Nav>
  );
};

export default AdminSidebar;