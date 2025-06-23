// Em frontend/src/components/ModalCriarTreino.tsx

import { useState, useEffect } from 'react';
import { Modal, Button, Form, Spinner } from 'react-bootstrap';

interface ModalCriarTreinoProps {
  show: boolean;
  isSaving: boolean;
  onHide: () => void;
  onSave: (nome: string) => void;
}

const ModalCriarTreino = ({ show, isSaving, onHide, onSave }: ModalCriarTreinoProps) => {
  const [nome, setNome] = useState('');

  // Limpa o campo de nome sempre que o modal for aberto
  useEffect(() => {
    if (show) {
      setNome('');
    }
  }, [show]);

  const handleSave = () => {
    if (nome.trim()) { // Só salva se o nome não estiver vazio
      onSave(nome);
    }
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Criar Novo Plano de Treino</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group controlId="formTreinoNome">
            <Form.Label>Nome do Plano</Form.Label>
            <Form.Control
              type="text"
              placeholder="Ex: Treino A - Peito e Tríceps"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              autoFocus
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide} disabled={isSaving}>
          Cancelar
        </Button>
        <Button variant="primary" onClick={handleSave} disabled={isSaving || !nome.trim()}>
          {isSaving ? (
            <>
              <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
              {' '}Salvando...
            </>
          ) : (
            'Salvar'
          )}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalCriarTreino;