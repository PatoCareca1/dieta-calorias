// Em frontend/src/components/ExerciciosDoTreino.tsx

import { Card, ListGroup, Button, Badge } from 'react-bootstrap';
import type { Treino } from '../models';

interface ExerciciosDoTreinoProps {
  treino: Treino | undefined;
  onRemoveExercicio: (itemId: number) => void;
}

const ExerciciosDoTreino = ({ treino, onRemoveExercicio }: ExerciciosDoTreinoProps) => {
  if (!treino) {
    return <Card body className="text-center text-muted">Selecione um plano de treino para ver os exercícios.</Card>;
  }

  return (
    <Card>
      <Card.Header as="h5">{treino.nome}</Card.Header>
      <ListGroup variant="flush">
        {treino.itens.length === 0 ? (
          <ListGroup.Item>Este plano de treino está vazio. Adicione exercícios da biblioteca ao lado.</ListGroup.Item>
        ) : (
          treino.itens.map(item => (
            <ListGroup.Item key={item.id} className="d-flex justify-content-between align-items-center">
              <div>
                <strong>{item.exercicio.nome}</strong>
                <div className="text-muted small mt-1">
                  <Badge pill bg="secondary" className="me-2">{item.series} séries</Badge>
                  <Badge pill bg="secondary" className="me-2">{item.repeticoes} reps</Badge>
                  <Badge pill bg="secondary">{item.descanso_segundos}s descanso</Badge>
                </div>
              </div>
              <Button variant="outline-danger" size="sm" onClick={() => onRemoveExercicio(item.id)}>
                Remover
              </Button>
            </ListGroup.Item>
          ))
        )}
      </ListGroup>
    </Card>
  );
};

export default ExerciciosDoTreino;