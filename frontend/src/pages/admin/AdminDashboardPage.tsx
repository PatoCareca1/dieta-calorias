// frontend/src/pages/admin/AdminDashboardPage.tsx
import React from 'react';
import { Card } from 'react-bootstrap';

const AdminDashboardPage: React.FC = () => {
  return (
    <>
      <h1>Dashboard do Administrador</h1>
      <Card>
        <Card.Body>
          <Card.Title>Bem-vindo ao Painel!</Card.Title>
          <Card.Text>
            Selecione uma das opções no menu à esquerda para começar a gerenciar o conteúdo.
          </Card.Text>
        </Card.Body>
      </Card>
    </>
  );
};

// A linha mais importante que estava faltando!
export default AdminDashboardPage;