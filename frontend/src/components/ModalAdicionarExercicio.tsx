// Em frontend/src/components/ModalAdicionarExercicio.tsx

import { useState, useEffect } from 'react';
import { Modal, Button, Form, Spinner, Row, Col } from 'react-bootstrap';
import type { ItemTreinoCreate } from '../models';

// Omitimos 'exercicio_id' pois ele já é conhecido pela página pai
type DetalhesExercicio = Omit<ItemTreinoCreate, 'exercicio_id'>;

interface ModalAdicionarExercicioProps {
  show: boolean;
  isSaving: boolean;
  onHide: () => void;
  onSave: (detalhes: DetalhesExercicio) => void;
}

const ModalAdicionarExercicio = ({ show, isSaving, onHide, onSave }: ModalAdicionarExercicioProps) => {
  const [series, setSeries] = useState('');
  const [repeticoes, setRepeticoes] = useState('');
  const [descanso, setDescanso] = useState('');

  useEffect(() => {
    if (show) {
      setSeries('');
      setRepeticoes('');
      setDescanso('');
    }
  }, [show]);

  const handleSave = () => {
    onSave({
      series: series ? parseInt(series, 10) : undefined,
      repeticoes: repeticoes || undefined,
      descanso_segundos: descanso ? parseInt(descanso, 10) : undefined,
    });
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Modal.Header closeButton>
        <Modal.Title>Adicionar Detalhes do Exercício</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Row>
            <Col>
              <Form.Group controlId="formSeries">
                <Form.Label>Séries</Form.Label>
                <Form.Control type="number" placeholder="Ex: 4" value={series} onChange={e => setSeries(e.target.value)} />
              </Form.Group>
            </Col>
            <Col>
              <Form.Group controlId="formRepeticoes">
                <Form.Label>Repetições</Form.Label>
                <Form.Control type="text" placeholder="Ex: 10-12" value={repeticoes} onChange={e => setRepeticoes(e.target.value)} />
              </Form.Group>
            </Col>
            <Col>
              <Form.Group controlId="formDescanso">
                <Form.Label>Descanso (seg)</Form.Label>
                <Form.Control type="number" placeholder="Ex: 60" value={descanso} onChange={e => setDescanso(e.target.value)} />
              </Form.Group>
            </Col>
          </Row>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide} disabled={isSaving}>Cancelar</Button>
        <Button variant="primary" onClick={handleSave} disabled={isSaving}>
          {isSaving ? 'Adicionando...' : 'Adicionar ao Treino'}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default ModalAdicionarExercicio;