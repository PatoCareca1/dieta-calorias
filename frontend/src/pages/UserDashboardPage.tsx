// frontend/src/pages/UserDashboardPage.tsx

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // 1. IMPORTAMOS O COMPONENTE LINK
import type { Usuario, PlanoAlimentar } from '../models'; 
import { Container, Card, Button, Spinner, Alert, Row, Col } from 'react-bootstrap';
import EditarPerfilModal from '../components/EditarPerfilModal'; 
import api from '../services/api';

const UserDashboardPage = () => {
    const [userData, setUserData] = useState<Usuario | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showEditModal, setShowEditModal] = useState(false);
    const [isCalculating, setIsCalculating] = useState(false);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                setLoading(true);
                const response = await api.get<Usuario>('/usuarios/me/');
                setUserData(response.data);
                setError('');
            } catch (err) {
                setError('Falha ao carregar os dados do perfil.');
            } finally {
                setLoading(false);
            }
        };
        fetchUserData();
    }, []);

    const handleProfileUpdate = (updatedUserData: Usuario) => {
        setUserData(updatedUserData);
        setShowEditModal(false);
    };

    const handleCalculateDiet = async () => {
        setIsCalculating(true);
        setError('');
        try {
            const response = await api.post<PlanoAlimentar>('/planos-alimentares/me/calcular');
            setUserData(prevUserData => {
                if (!prevUserData) return null;
                return { ...prevUserData, plano_alimentar: response.data };
            });
        } catch (err: any) {
            const detail = err.response?.data?.detail || "Ocorreu um erro ao calcular a dieta.";
            setError(detail);
        } finally {
            setIsCalculating(false);
        }
    };
    
    if (loading) return <Container className="text-center mt-5"><Spinner animation="border" /></Container>;

    return (
        <Container className="mt-4" style={{ maxWidth: '900px' }}>
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="mb-0">Dashboard de {userData?.nome}</h2>
                {/* 2. ADICIONAMOS O BOTÃO/LINK PARA A NOVA PÁGINA */}
                <Link to="/montar-treino" className="btn btn-success">
                    Montar Meu Treino
                </Link>
            </div>
            
            {error && <Alert variant="danger">{error}</Alert>}

            <Row>
                <Col md={5}>
                    <Card className="mb-4">
                        <Card.Header as="h5">Meu Perfil</Card.Header>
                        <Card.Body>
                            {userData ? (
                                <>
                                    <p><strong>Email:</strong> {userData.email}</p>
                                    <p><strong>Peso:</strong> {userData.peso_kg ? `${userData.peso_kg} kg` : 'Não informado'}</p>
                                    <p><strong>Altura:</strong> {userData.altura_cm ? `${userData.altura_cm} cm` : 'Não informado'}</p>
                                    <p><strong>Objetivo:</strong> {userData.objetivo ? userData.objetivo.replace(/_/g, ' ') : 'Não informado'}</p>
                                    <Button variant="secondary" size="sm" onClick={() => setShowEditModal(true)}>Editar Perfil</Button>
                                </>
                            ) : <p>Nenhum dado de usuário encontrado.</p>}
                        </Card.Body>
                    </Card>
                </Col>

                <Col md={7}>
                    <Card className="mb-4">
                        <Card.Header as="h5">Meu Plano Alimentar</Card.Header>
                        <Card.Body>
                            {userData?.plano_alimentar ? (
                                <div>
                                    <p><strong>Meta de Calorias:</strong> {userData.plano_alimentar.calorias_objetivo.toFixed(0)} kcal</p>
                                    <p><strong>Proteínas:</strong> {userData.plano_alimentar.proteinas_g.toFixed(0)} g</p>
                                    <p><strong>Carboidratos:</strong> {userData.plano_alimentar.carboidratos_g.toFixed(0)} g</p>
                                    <p><strong>Gorduras:</strong> {userData.plano_alimentar.gorduras_g.toFixed(0)} g</p>
                                </div>
                            ) : (
                                <p>Você ainda não calculou seu plano alimentar.</p>
                            )}
                            <Button variant="primary" onClick={handleCalculateDiet} disabled={isCalculating}>
                                {isCalculating ? <Spinner as="span" animation="border" size="sm" /> : (userData?.plano_alimentar ? 'Recalcular Dieta' : 'Calcular Minha Dieta')}
                            </Button>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            {userData && (
                <EditarPerfilModal
                    show={showEditModal}
                    onHide={() => setShowEditModal(false)}
                    userData={userData}
                    onUpdate={handleProfileUpdate}
                />
            )}
        </Container>
    );
};

export default UserDashboardPage;