// Em frontend/src/components/SeletorExercicio.tsx

import { useState, useMemo } from 'react';
import { Form, ListGroup, Button, InputGroup, Row, Col } from 'react-bootstrap';
import type { Exercicio } from '../models';

interface SeletorExercicioProps {
  exercicios: Exercicio[];
  onAddExercicio: (exercicioId: number) => void;
  disabled: boolean; // Para desabilitar os botões se nenhum treino estiver selecionado
}

const SeletorExercicio = ({ exercicios, onAddExercicio, disabled }: SeletorExercicioProps) => {
  const [filtroNome, setFiltroNome] = useState('');
  const [filtroGrupo, setFiltroGrupo] = useState('');

  // Usamos useMemo para otimizar e não recalcular os grupos musculares a cada renderização
  const gruposMusculares = useMemo(() => {
    const grupos = new Set(exercicios.map(e => e.grupo_muscular));
    return Array.from(grupos);
  }, [exercicios]);

  // Filtra os exercícios com base nos filtros de nome e grupo
  const exerciciosFiltrados = exercicios.filter(exercicio => {
    const nomeMatch = exercicio.nome.toLowerCase().includes(filtroNome.toLowerCase());
    const grupoMatch = !filtroGrupo || exercicio.grupo_muscular === filtroGrupo;
    return nomeMatch && grupoMatch;
  });

  return (
    <div>
      <Row className="mb-3">
        <Col md={6}>
          <Form.Group controlId="filtroNome">
            <Form.Label>Buscar por nome</Form.Label>
            <Form.Control
              type="text"
              placeholder="Ex: Supino, Agachamento..."
              value={filtroNome}
              onChange={(e) => setFiltroNome(e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col md={6}>
          <Form.Group controlId="filtroGrupo">
            <Form.Label>Filtrar por grupo muscular</Form.Label>
            <Form.Select value={filtroGrupo} onChange={(e) => setFiltroGrupo(e.target.value)}>
              <option value="">Todos os grupos</option>
              {gruposMusculares.map(grupo => (
                <option key={grupo} value={grupo}>{grupo}</option>
              ))}
            </Form.Select>
          </Form.Group>
        </Col>
      </Row>
      
      <ListGroup style={{ maxHeight: '60vh', overflowY: 'auto' }}>
        {exerciciosFiltrados.map(exercicio => (
          <ListGroup.Item key={exercicio.id} className="d-flex justify-content-between align-items-center">
            <div>
              <strong>{exercicio.nome}</strong>
              <br />
              <small className="text-muted">{exercicio.grupo_muscular}</small>
            </div>
            <Button
              variant="outline-primary"
              size="sm"
              onClick={() => onAddExercicio(exercicio.id)}
              disabled={disabled}
            >
              Adicionar +
            </Button>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );
};

export default SeletorExercicio;