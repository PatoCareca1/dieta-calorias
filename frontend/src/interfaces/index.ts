interface Profile {
  // Baseado no schema ProfileRead
  id_perfil: number;
  peso: number;
  altura: number;
  idade: number;
  sexo: string;
  nivel_atividade: string;
  objetivo: string;
}

interface User {
  // Baseado no schema UserRead
  id_usuario: number;
  nome: string;
  email: string;
  is_active: boolean;
  perfil: Profile | null;
}