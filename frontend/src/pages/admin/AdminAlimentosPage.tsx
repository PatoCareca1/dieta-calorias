// frontend/src/pages/admin/AdminAlimentosPage.tsx

import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Spinner, Alert } from 'react-bootstrap';
import api from '../../services/api';

// Interface para um Alimento (espelhando o schema Pydantic)
interface Alimento {
  id_alimento: number;
  nome: string;
  calorias_por_100g: number;
  proteinas: number;
  carboidratos: number;
  gorduras: number;
}

// Interface para o formulário (sem o ID, que é gerado pelo banco)
type AlimentoFormData = Omit<Alimento, 'id_alimento'>;

const AdminAlimentosPage: React.FC = () => {
    const [alimentos, setAlimentos] = useState<Alimento[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Estados para controlar o Modal e o formulário
    const [showModal, setShowModal] = useState(false);
    const [isEditMode, setIsEditMode] = useState(false);
    const [currentAlimento, setCurrentAlimento] = useState<Alimento | null>(null);
    const [formData, setFormData] = useState<AlimentoFormData>({
        nome: '',
        calorias_por_100g: 0,
        proteinas: 0,
        carboidratos: 0,
        gorduras: 0,
    });

    const fetchAlimentos = async () => {
        setLoading(true);
        try {
            const response = await api.get<Alimento[]>('/alimentos/');
            setAlimentos(response.data);
        } catch (err) {
            setError('Falha ao carregar alimentos.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAlimentos();
    }, []);
    
    // --- LÓGICA DO MODAL ---
    const handleShowCreateModal = () => {
        setIsEditMode(false);
        setFormData({ nome: '', calorias_por_100g: 0, proteinas: 0, carboidratos: 0, gorduras: 0 });
        setShowModal(true);
    };

    const handleShowEditModal = (alimento: Alimento) => {
        setIsEditMode(true);
        setCurrentAlimento(alimento);
        setFormData(alimento); // Preenche o formulário com os dados atuais
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setCurrentAlimento(null);
    };

    const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: parseFloat(value) || value }));
    };

    // --- AÇÕES DO CRUD ---
    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        const method = isEditMode ? 'put' : 'post';
        const url = isEditMode ? `/alimentos/${currentAlimento?.id_alimento}` : '/alimentos/';

        try {
            await api[method](url, formData);
            fetchAlimentos(); // Recarrega a lista
            handleCloseModal(); // Fecha o modal
        } catch (err) {
            setError('Erro ao salvar o alimento.');
            console.error(err);
        }
    };

    const handleDelete = async (id: number) => {
        if (window.confirm('Tem certeza que deseja excluir este alimento?')) {
            try {
                await api.delete(`/alimentos/${id}`);
                fetchAlimentos(); // Recarrega a lista
            } catch (err) {
                setError('Erro ao excluir o alimento.');
                console.error(err);
            }
        }
    };

    if (loading) return <Spinner animation="border" />;

    return (
        <>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h1>Gerenciar Alimentos</h1>
                <Button onClick={handleShowCreateModal}>Adicionar Alimento</Button>
            </div>

            {error && <Alert variant="danger" onClose={() => setError('')} dismissible>{error}</Alert>}

            <Table striped bordered hover responsive>
                <thead>
                    <tr>
                        <th>ID</th><th>Nome</th><th>Calorias</th><th>Proteínas</th><th>Carbs</th><th>Gorduras</th><th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {alimentos.map(alimento => (
                        <tr key={alimento.id_alimento}>
                            <td>{alimento.id_alimento}</td>
                            <td>{alimento.nome}</td>
                            <td>{alimento.calorias_por_100g}</td>
                            <td>{alimento.proteinas}</td>
                            <td>{alimento.carboidratos}</td>
                            <td>{alimento.gorduras}</td>
                            <td>
                                <Button variant="warning" size="sm" className="me-2" onClick={() => handleShowEditModal(alimento)}>Editar</Button>
                                <Button variant="danger" size="sm" onClick={() => handleDelete(alimento.id_alimento)}>Excluir</Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>

            <Modal show={showModal} onHide={handleCloseModal}>
                <Form onSubmit={handleSave}>
                    <Modal.Header closeButton>
                        <Modal.Title>{isEditMode ? 'Editar Alimento' : 'Adicionar Novo Alimento'}</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form.Group className="mb-3">
                            <Form.Label>Nome</Form.Label>
                            <Form.Control type="text" name="nome" value={formData.nome} onChange={handleFormChange} required />
                        </Form.Group>
                        {/* Outros campos numéricos */}
                        <Form.Group className="mb-3">
                            <Form.Label>Calorias (por 100g)</Form.Label>
                            <Form.Control type="number" name="calorias_por_100g" value={formData.calorias_por_100g} onChange={handleFormChange} required />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Proteínas</Form.Label>
                            <Form.Control type="number" name="proteinas" value={formData.proteinas} onChange={handleFormChange} required />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Carboidratos</Form.Label>
                            <Form.Control type="number" name="carboidratos" value={formData.carboidratos} onChange={handleFormChange} required />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Gorduras</Form.Label>
                            <Form.Control type="number" name="gorduras" value={formData.gorduras} onChange={handleFormChange} required />
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleCloseModal}>Cancelar</Button>
                        <Button variant="primary" type="submit">Salvar</Button>
                    </Modal.Footer>
                </Form>
            </Modal>
        </>
    );
};

export default AdminAlimentosPage;