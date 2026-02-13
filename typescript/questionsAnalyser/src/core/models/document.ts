export interface Document {
  id: string;
  path: string;
  title: string;
  content: string;
  livro?: string;
  capitulo?: string;
  tipo?: string;
  tags?: string[];
}

export interface Question {
  id: string;
  // path: string;
  title: string;
  question: string;
  answer?: string;
  livro?: string;
  capitulo?: string;
  conteudo?: string;
  area?: string;
}