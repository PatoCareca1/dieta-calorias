// Em frontend/src/components/ModalCriarExercicio.tsx

import { useState, useEffect } from 'react';
import { Modal, Button, Form, Spinner } from 'react-bootstrap';
import type { ExercicioCreate } from '../models';

// Lista de grupos musculares para o dropdown
const GRUPOS_MUSCULARES = ["Peito", "Costas", "Pernas", "Bíceps", "Tríceps", "Ombros", "Abdômen", "Outro"];

interface ModalCriarExercicioProps {
  show: boolean;
  isSaving: boolean;
  onHide: () => void;
  onSave: (data: ExercicioCreate) => void;
}

const ModalCriarExercicio = ({ show, isSaving, onHide, onSave }: ModalCriarExercicioProps) => {
  const [nome, setNome] = useState('');
  const [grupoMuscular, setGrupoMuscular] = useState(GRUPOS_MUSCULARES[0]);
  const [descricao, setDescricao] = useState('');

  useEffect(() => {
    if (show) {
      // Reseta o formulário quando o modal abre
      setNome('');
      setGrupoMuscular(GRUPOS_MUSCULARES[0]);
      setDescricao('');
    }
  }, [show]);

  const handleSave = () => {
    if (nome.trim() && grupoMuscular) {
      onSave({ nome, grupo_muscular: grupoMuscular, descricao });
    }
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Cadastrar Novo Exercício</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group className="mb-3" controlId="formExercicioNome">
            <Form.Label>Nome do Exercício</Form.Label>
            <Form.Control type="text" value={nome} onChange={(e) => setNome(e.target.value)} autoFocus />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formExercicioGrupo">
            <Form.Label>Grupo Muscular</Form.Label>
            <Form.Select value={grupoMuscular} onChange={(e) => setGrupoMuscular(e.target.value)}>
              {GRUPOS_MUSCULARES.map(g => <option key={g} value={g}>{g}</option>)}
            </Form.Select>
          </Form.Group>
          <Form.Group className="mb-3" controlId="formExercicioDescricao">
            <Form.Label>Descrição (Opcional)</Form.Label>
            <Form.Control as="textarea" rows={3} value={descricao} onChange={(e) => setDescricao(e.target.value)} />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide} disabled={isSaving}>Cancelar</Button>
        <Button variant="primary" onClick={handleSave} disabled={isSaving || !nome.trim()}>
          {isSaving ? 'Salvando...' : 'Salvar Exercício'}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalCriarExercicio;