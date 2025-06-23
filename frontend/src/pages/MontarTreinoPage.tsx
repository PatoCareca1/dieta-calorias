// frontend/src/pages/MontarTreinoPage.tsx

import { useState, useEffect, useMemo } from 'react';
import { Container, Row, Col, Spinner, Alert, Button } from 'react-bootstrap';
import type { Treino, Exercicio, ItemTreinoCreate, ExercicioCreate } from '../models';
import { 
  getTreinos, 
  getExercicios, 
  createTreino, 
  addExercicioToTreino, 
  removeExercicioFromTreino, 
  createExercicio 
} from '../services/treinoService';
import ListaTreinos from '../components/ListaTreinos';
import ModalCriarTreino from '../components/ModalCriarTreino';
import SeletorExercicio from '../components/SeletorExercicio';
import ModalAdicionarExercicio from '../components/ModalAdicionarExercicio';
import ExerciciosDoTreino from '../components/ExerciciosDoTreino';
import ModalCriarExercicio from '../components/ModalCriarExercicio';

type DetalhesExercicio = Omit<ItemTreinoCreate, 'exercicio_id'>;

const MontarTreinoPage = () => {
  // Estados para dados da API
  const [treinos, setTreinos] = useState<Treino[]>([]);
  const [exercicios, setExercicios] = useState<Exercicio[]>([]);

  // Estados para controle da UI (carregamento, erros, seleção)
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [treinoSelecionadoId, setTreinoSelecionadoId] = useState<number | null>(null);

  // Estados para controle dos Modais
  const [showCriarTreinoModal, setShowCriarTreinoModal] = useState(false);
  const [showAddExercicioModal, setShowAddExercicioModal] = useState(false);
  const [showCriarExercicioModal, setShowCriarExercicioModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [exercicioParaAdicionarId, setExercicioParaAdicionarId] = useState<number | null>(null);

  // Deriva o objeto do treino selecionado a partir do ID
  const treinoSelecionado = useMemo(() => {
    return treinos.find(t => t.id === treinoSelecionadoId);
  }, [treinos, treinoSelecionadoId]);

  // Efeito para carregar dados iniciais
  useEffect(() => {
    const carregarDados = async () => {
      try {
        setIsLoading(true);
        const [treinosData, exerciciosData] = await Promise.all([
          getTreinos(),
          getExercicios(),
        ]);
        setTreinos(treinosData);
        setExercicios(exerciciosData);
        if (treinosData.length > 0) {
          setTreinoSelecionadoId(treinosData[0].id);
        }
        setError(null);
      } catch (err) {
        setError('Falha ao carregar os dados. Tente novamente mais tarde.');
      } finally {
        setIsLoading(false);
      }
    };
    carregarDados();
  }, []);

  // Handlers para Treinos
  const handleSelectTreino = (id: number) => setTreinoSelecionadoId(id);
  const handleShowCriarTreinoModal = () => setShowCriarTreinoModal(true);
  const handleSaveTreino = async (nome: string) => {
    setIsSaving(true);
    setError(null);
    try {
      const novoTreino = await createTreino(nome);
      setTreinos(prev => [...prev, novoTreino]);
      setTreinoSelecionadoId(novoTreino.id);
      setShowCriarTreinoModal(false);
    } catch (err) {
      setError("Falha ao criar o treino.");
    } finally {
      setIsSaving(false);
    }
  };

  // Handlers para adicionar exercício a um treino
  const handleShowAddExercicioModal = (exercicioId: number) => {
    setExercicioParaAdicionarId(exercicioId);
    setShowAddExercicioModal(true);
  };
  const handleSaveExercicioNoTreino = async (detalhes: DetalhesExercicio) => {
    if (!treinoSelecionadoId || !exercicioParaAdicionarId) return;
    setIsSaving(true);
    setError(null);
    try {
      const payload: ItemTreinoCreate = { exercicio_id: exercicioParaAdicionarId, ...detalhes };
      const novoItem = await addExercicioToTreino(treinoSelecionadoId, payload);
      setTreinos(prev => prev.map(t => t.id === treinoSelecionadoId ? { ...t, itens: [...t.itens, novoItem] } : t));
      setShowAddExercicioModal(false);
    } catch (err) {
      setError("Falha ao adicionar o exercício ao treino.");
    } finally {
      setIsSaving(false);
    }
  };

  // Handler para remover exercício de um treino
  const handleRemoveExercicioDoTreino = async (itemId: number) => {
    if (!treinoSelecionadoId || !window.confirm("Remover este exercício do treino?")) return;
    try {
      await removeExercicioFromTreino(treinoSelecionadoId, itemId);
      setTreinos(prev => prev.map(t => t.id === treinoSelecionadoId ? { ...t, itens: t.itens.filter(item => item.id !== itemId) } : t));
    } catch (err) {
      setError("Falha ao remover o exercício.");
    }
  };

  // Handlers para criar um novo exercício na biblioteca
  const handleShowCriarExercicioModal = () => setShowCriarExercicioModal(true);
  const handleSaveNovoExercicio = async (data: ExercicioCreate) => {
    setIsSaving(true);
    setError(null);
    try {
      const novoExercicio = await createExercicio(data);
      setExercicios(prev => [...prev, novoExercicio]);
      setShowCriarExercicioModal(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Falha ao criar o exercício.");
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return <Container className="text-center mt-5"><Spinner animation="border" /></Container>;
  }

  return (
    <>
      <Container fluid className="p-4">
        {error && <Alert variant="danger" onClose={() => setError(null)} dismissible>{error}</Alert>}
        <Row>
          <Col md={5} lg={4}>
            <h2>Meus Planos de Treino</h2>
            <hr />
            <ListaTreinos 
              treinos={treinos}
              treinoSelecionadoId={treinoSelecionadoId}
              onSelectTreino={handleSelectTreino}
              onCriarNovo={handleShowCriarTreinoModal}
            />
            <hr />
            <ExerciciosDoTreino 
              treino={treinoSelecionado}
              onRemoveExercicio={handleRemoveExercicioDoTreino}
            />
          </Col>
          <Col md={7} lg={8}>
            <div className="d-flex justify-content-between align-items-center">
              <h2 className="mb-0">Biblioteca de Exercícios</h2>
              <Button variant="outline-success" size="sm" onClick={handleShowCriarExercicioModal}>
                + Novo Exercício
              </Button>
            </div>
            <hr />
            <SeletorExercicio 
              exercicios={exercicios}
              onAddExercicio={handleShowAddExercicioModal}
              disabled={!treinoSelecionadoId}
            />
          </Col>
        </Row>
      </Container>
      
      <ModalCriarTreino show={showCriarTreinoModal} isSaving={isSaving} onHide={() => setShowCriarTreinoModal(false)} onSave={handleSaveTreino} />
      <ModalAdicionarExercicio show={showAddExercicioModal} isSaving={isSaving} onHide={() => setShowAddExercicioModal(false)} onSave={handleSaveExercicioNoTreino} />
      <ModalCriarExercicio show={showCriarExercicioModal} isSaving={isSaving} onHide={() => setShowCriarExercicioModal(false)} onSave={handleSaveNovoExercicio} />
    </>
  );
};

export default MontarTreinoPage;