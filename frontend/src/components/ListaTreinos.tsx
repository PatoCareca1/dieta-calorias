// Em frontend/src/components/ListaTreinos.tsx

import { ListGroup, Button, Stack } from 'react-bootstrap';
import type { Treino } from '../models';

// Definindo as propriedades que o componente receberá do seu "pai"
interface ListaTreinosProps {
  treinos: Treino[];
  treinoSelecionadoId: number | null;
  onSelectTreino: (id: number) => void;
  onCriarNovo: () => void;
}

const ListaTreinos = ({ 
  treinos, 
  treinoSelecionadoId, 
  onSelectTreino, 
  onCriarNovo 
}: ListaTreinosProps) => {

  return (
    <Stack gap={3}>
      <Button variant="primary" onClick={onCriarNovo}>
        + Criar Novo Plano de Treino
      </Button>
      
      <ListGroup>
        {treinos.length > 0 ? (
          treinos.map((treino) => (
            <ListGroup.Item
              key={treino.id}
              action
              active={treino.id === treinoSelecionadoId}
              onClick={() => onSelectTreino(treino.id)}
              className="d-flex justify-content-between align-items-center"
            >
              {treino.nome}
              <small>{treino.itens.length} {treino.itens.length === 1 ? 'exercício' : 'exercícios'}</small>
            </ListGroup.Item>
          ))
        ) : (
          <ListGroup.Item disabled>
            Você ainda não criou nenhum plano de treino.
          </ListGroup.Item>
        )}
      </ListGroup>
    </Stack>
  );
};

export default ListaTreinos;