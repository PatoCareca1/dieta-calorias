// frontend/src/layouts/AdminLayout.tsx
import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Outlet } from 'react-router-dom';
import AdminSidebar from '../components/AdminSidebar';

const AdminLayout: React.FC = () => {
  return (
    <Container fluid>
      <Row>
        {/* Menu Lateral Fixo */}
        <Col md={2} className="bg-dark min-vh-100 p-0">
          <AdminSidebar />
        </Col>
        
        {/* Área de Conteúdo Dinâmico */}
        <Col md={10} className="p-4">
          <Outlet /> {/* O React Router renderizará a página da rota atual aqui */}
        </Col>
      </Row>
    </Container>
  );
};

export default AdminLayout;