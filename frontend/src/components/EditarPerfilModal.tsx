import { useState, useEffect } from 'react';
import { Modal, Button, Form, Spinner, Alert, Col, Row } from 'react-bootstrap';
import api from '../services/api';
import { OBJETIVOS, NIVEIS_ATIVIDADE, GENEROS } from '../models'; // Importando as arrays para os selects
import type { FormEvent, ChangeEvent } from 'react';
import type { Usuario } from '../models';

interface EditarPerfilModalProps {
  show: boolean;
  onHide: () => void;
  userData: Usuario;
  onUpdate: (updatedUserData: Usuario) => void;
}

const EditarPerfilModal = ({ show, onHide, userData, onUpdate }: EditarPerfilModalProps) => {
  // Correção 3: Tipamos explicitamente o estado do formulário.
  const [formData, setFormData] = useState<Partial<Usuario>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (userData) {
      setFormData({
        nome: userData.nome,
        peso_kg: userData.peso_kg,
        altura_cm: userData.altura_cm,
        data_nascimento: userData.data_nascimento,
        genero: userData.genero,
        nivel_atividade: userData.nivel_atividade,
        objetivo: userData.objetivo,
        restricoes_alimentares: userData.restricoes_alimentares,
        observacoes: userData.observacoes,
      });
    }
  }, [userData, show]);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    // Correção 4: Converte o valor para número se o tipo do input for 'number'.
    // Isso resolve o erro de 'string' não ser atribuível a 'number'.
    const finalValue = type === 'number'
      ? (value === '' ? null : parseFloat(value))
      : (value === '' ? null : value);

    setFormData(prev => ({ ...prev, [name]: finalValue }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      const response = await api.put<Usuario>('/usuarios/me/', formData);
      onUpdate(response.data);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Falha ao atualizar o perfil.';
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const formatLabel = (value: string) => {
    return value.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
  };

  return (
    <Modal show={show} onHide={onHide} centered size="lg">
      <Form onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Editar Perfil</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error && <Alert variant="danger">{error}</Alert>}
          
          {/* O restante do JSX continua similar, mas agora populamos os selects com as arrays */}
          <Row>
            {/* Colunas para Nome e Data de Nascimento */}
          </Row>
          <Row>
            <Col md={6}><Form.Group className="mb-3">
                <Form.Label>Peso (kg)</Form.Label>
                <Form.Control type="number" step="0.1" name="peso_kg" value={formData.peso_kg ?? ''} onChange={handleChange} />
            </Form.Group></Col>
            <Col md={6}><Form.Group className="mb-3">
                <Form.Label>Altura (cm)</Form.Label>
                <Form.Control type="number" name="altura_cm" value={formData.altura_cm ?? ''} onChange={handleChange} />
            </Form.Group></Col>
          </Row>
          <Row>
            <Col md={4}><Form.Group className="mb-3">
              <Form.Label>Gênero</Form.Label>
              <Form.Select name="genero" value={formData.genero ?? ''} onChange={handleChange}>
                <option value="">Selecione...</option>
                {GENEROS.map(value => (
                  <option key={value} value={value}>{formatLabel(value)}</option>
                ))}
              </Form.Select>
            </Form.Group></Col>
            <Col md={4}><Form.Group className="mb-3">
              <Form.Label>Nível de Atividade</Form.Label>
              <Form.Select name="nivel_atividade" value={formData.nivel_atividade ?? ''} onChange={handleChange}>
                <option value="">Selecione...</option>
                {NIVEIS_ATIVIDADE.map(value => (
                  <option key={value} value={value}>{formatLabel(value)}</option>
                ))}
              </Form.Select>
            </Form.Group></Col>
            <Col md={4}><Form.Group className="mb-3">
              <Form.Label>Objetivo Principal</Form.Label>
              <Form.Select name="objetivo" value={formData.objetivo ?? ''} onChange={handleChange}>
                <option value="">Selecione...</option>
                {OBJETIVOS.map(value => (
                  <option key={value} value={value}>{formatLabel(value)}</option>
                ))}
              </Form.Select>
            </Form.Group></Col>
          </Row>
          {/* Outros campos como restrições e observações */}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onHide} disabled={isSubmitting}>Cancelar</Button>
          <Button variant="primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? <Spinner as="span" animation="border" size="sm" /> : 'Salvar'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default EditarPerfilModal;