export interface AuthUser {
  id: number;
  nome_completo: string;
  email: string;
  empresa_id: number;
  perfil: 'ADMINISTRADOR' | 'FUNCIONARIO';
}

export interface AuthResponse {
  access_token: string;
  token_type: 'bearer';
  user: AuthUser;
}

export interface CompanyRegistration {
  nome_empresa: string;
  cnpj: string;
  nome_completo: string;
  cpf: string;
  email: string;
  telefone: string;
  senha: string;
}

export interface DashboardSummary {
  total_produtos: number;
  entradas_7_dias: number;
  saidas_7_dias: number;
  itens_estoque_baixo: number;
  produtos_estoque_baixo: {
    id: number;
    nome: string;
    quantidade: number;
    limite_minimo: number;
  }[];
  movimentacoes_recentes: {
    id: number;
    produto: string;
    tipo: 'ENTRADA' | 'SAIDA';
    quantidade: number;
    data_hora: string;
  }[];
  serie_movimentacoes: {
    data: string;
    entradas: number;
    saidas: number;
  }[];
}

export interface Company {
  id: number;
  nome_empresa: string;
  cnpj: string;
}
