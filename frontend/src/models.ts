export type Objetivo = "perder_peso" | "manter_peso" | "ganhar_massa";
export type NivelAtividade = "sedentario" | "levemente_ativo" | "moderadamente_ativo" | "muito_ativo" | "extremamente_ativo";
export type Genero = "masculino" | "feminino" | "outro" | "prefiro_nao_dizer";
export const OBJETIVOS: Objetivo[] = ["perder_peso", "manter_peso", "ganhar_massa"];
export const NIVEIS_ATIVIDADE: NivelAtividade[] = ["sedentario", "levemente_ativo", "moderadamente_ativo", "muito_ativo", "extremamente_ativo"];
export const GENEROS: Genero[] = ["masculino", "feminino", "outro", "prefiro_nao_dizer"];

export interface PlanoAlimentar {
  id: number;
  tmb: number;
  calorias_objetivo: number;
  proteinas_g: number;
  carboidratos_g: number;
  gorduras_g: number;
  data_criacao: string;
  usuario_id: number;
}

export interface Usuario {
  id: number;
  nome: string | null;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  peso_kg: number | null;
  altura_cm: number | null;
  data_nascimento: string | null;
  genero: Genero | null;
  nivel_atividade: NivelAtividade | null;
  objetivo: Objetivo | null;
  restricoes_alimentares: string | null;
  observacoes: string | null;
  plano_alimentar: PlanoAlimentar | null;
}

export interface Exercicio {
  id: number;
  nome: string;
  grupo_muscular: string;
  descricao?: string;
}

export interface ItemTreino {
  id: number;
  exercicio_id: number;
  series?: number;
  repeticoes?: string;
  descanso_segundos?: number;
  exercicio: Exercicio; 
}

export interface Treino {
  id: number;
  nome: string;
  usuario_id: number;
  itens: ItemTreino[];
}

export interface ItemTreinoCreate {
    exercicio_id: number;
    series?: number;
    repeticoes?: string;
    descanso_segundos?: number;
}

export interface ExercicioCreate {
  nome: string;
  grupo_muscular: string;
  descricao?: string;
}