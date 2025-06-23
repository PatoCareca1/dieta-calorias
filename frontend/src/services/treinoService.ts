import api from './api';
import type { Treino, Exercicio, ItemTreinoCreate, ItemTreino, ExercicioCreate } from '../models'; 

// --- Funções para Exercícios ---

export const getExercicios = async (): Promise<Exercicio[]> => {
  const response = await api.get('/exercicios/');
  return response.data;
};

// --- Funções para Treinos ---

export const getTreinos = async (): Promise<Treino[]> => {
    const response = await api.get('/treinos/');
    return response.data;
};

export const createTreino = async (nome: string): Promise<Treino> => {
    const response = await api.post('/treinos/', { nome });
    return response.data;
};

export const addExercicioToTreino = async (treinoId: number, item: ItemTreinoCreate): Promise<ItemTreino> => {
    const response = await api.post(`/treinos/${treinoId}/exercicios/`, item);
    return response.data;
};

export const removeExercicioFromTreino = async (treinoId: number, itemId: number): Promise<void> => {
    await api.delete(`/treinos/${treinoId}/exercicios/${itemId}`);
};

export const createExercicio = async (data: ExercicioCreate): Promise<Exercicio> => {
  const response = await api.post('/exercicios/', data);
  return response.data;
};