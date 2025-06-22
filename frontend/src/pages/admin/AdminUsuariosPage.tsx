// frontend/src/pages/admin/AdminUsuariosPage.tsx

import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Spinner, Alert } from 'react-bootstrap';
import api from '../../services/api';

// Interfaces para tipagem dos dados
interface Profile {
  id_perfil: number;
  peso: number;
  altura: number;
  idade: number;
  sexo: string;
  nivel_atividade: string;
  objetivo: string;
}

interface User {
  id_usuario: number;
  nome: string;
  email: string;
  is_active: boolean;
  perfil: Profile | null;
}

const AdminUsuariosPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Estados para o Modal
  const [showModal, setShowModal] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  
  // Função para buscar os usuários da API
  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.get<User[]>('/users/'); // Endpoint que você criou
      setUsers(response.data);
    } catch (err) {
      setError('Falha ao carregar usuários. A API está rodando e acessível?');
      console.error("Erro ao buscar usuários:", err);
    } finally {
      setLoading(false);
    }
  };

  // Carrega os dados iniciais
  useEffect(() => {
    fetchUsers();
  }, []);

  const handleOpenCreateModal = () => {
    setIsEditMode(false);
    setCurrentUser(null);
    setShowModal(true);
  };

  const handleOpenEditModal = (user: User) => {
    setIsEditMode(true);
    setCurrentUser(user);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentUser(null);
  };
  
  const handleDelete = async (userId: number) => {
    if (window.confirm('Tem certeza que deseja excluir este usuário?')) {
        try {
            await api.delete(`/users/${userId}`);
            // Recarrega a lista após a exclusão
            fetchUsers();
        } catch (err) {
            console.error("Erro ao excluir usuário:", err);
            setError('Não foi possível excluir o usuário.');
        }
    }
  };

  // Lógica de salvar (criar ou editar)
  const handleSave = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const userData = {
        nome: formData.get('nome') as string,
        email: formData.get('email') as string,
        password: formData.get('password') as string, // Apenas para criação
    };

    try {
        if (isEditMode && currentUser) {
            // Lógica de Edição (PUT /users/{id})
            // Nota: a edição de senha deve ser tratada com cuidado, talvez em outra tela/modal
            await api.put(`/users/${currentUser.id_usuario}`, { nome: userData.nome, email: userData.email });
        } else {
            // Lógica de Criação (POST /users/)
            await api.post('/users/', userData);
        }
        fetchUsers(); // Recarrega a lista
        handleCloseModal(); // Fecha o modal
    } catch (err) {
        console.error("Erro ao salvar usuário:", err);
        setError('Não foi possível salvar o usuário.');
    }
  };

  if (loading) {
    return <Spinner animation="border" variant="primary" />;
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Gerenciar Usuários</h1>
        <Button onClick={handleOpenCreateModal}>
          Adicionar Usuário
        </Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Email</th>
            <th>Ativo</th>
            <th>Perfil (ID)</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id_usuario}>
              <td>{user.id_usuario}</td>
              <td>{user.nome}</td>
              <td>{user.email}</td>
              <td>{user.is_active ? 'Sim' : 'Não'}</td>
              <td>{user.perfil ? user.perfil.id_perfil : 'N/A'}</td>
              <td>
                <Button variant="info" size="sm" className="me-2" onClick={() => alert(JSON.stringify(user.perfil, null, 2))}>
                    Ver Perfil
                </Button>
                <Button variant="warning" size="sm" className="me-2" onClick={() => handleOpenEditModal(user)}>
                    Editar
                </Button>
                <Button variant="danger" size="sm" onClick={() => handleDelete(user.id_usuario)}>
                    Excluir
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Modal para Criar/Editar Usuário */}
      <Modal show={showModal} onHide={handleCloseModal}>
        <Form onSubmit={handleSave}>
            <Modal.Header closeButton>
                <Modal.Title>{isEditMode ? 'Editar Usuário' : 'Adicionar Novo Usuário'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form.Group className="mb-3">
                    <Form.Label>Nome</Form.Label>
                    <Form.Control type="text" name="nome" defaultValue={currentUser?.nome || ''} required />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" name="email" defaultValue={currentUser?.email || ''} required />
                </Form.Group>
                {!isEditMode && (
                    <Form.Group className="mb-3">
                        <Form.Label>Senha</Form.Label>
                        <Form.Control type="password" name="password" required />
                    </Form.Group>
                )}
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseModal}>
                    Cancelar
                </Button>
                <Button variant="primary" type="submit">
                    Salvar
                </Button>
            </Modal.Footer>
        </Form>
      </Modal>
    </>
  );
};

export default AdminUsuariosPage;