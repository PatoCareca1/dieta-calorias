// frontend/src/pages/NotFoundPage.tsx
import React from 'react';
import { Container, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  return (
    <Container className="text-center mt-5">
      <Alert variant="danger">
        <Alert.Heading>Erro 404 - Página Não Encontrada</Alert.Heading>
        <p>
          A página que você está procurando não existe ou ainda não foi implementada.
        </p>
        <hr />
        <p className="mb-0">
          <Link to="/">Voltar para a Calculadora</Link> | <Link to="/admin">Ir para o Dashboard Admin</Link>
        </p>
      </Alert>
    </Container>
  );
};

// E aqui também, o export padrão
export default NotFoundPage;