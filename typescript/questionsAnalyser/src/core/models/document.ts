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
  // path: string;
  title: string;
  question: string;
  answer?: string;
  bookId?: string;
  chapter?: number | null;
  areas?: string[];
  subjects?: string[];
  topic?: string[];
  rank?: number[];
  hasDocument?: boolean;
}

export interface Book {
  title: string;
  edition?: number;
  authors?: string[];
  chapters?: string[];
  area?: string[];
  conteudo?: string[];
  topic?: string[];
  hasDocument?: boolean;
}

export interface Chapter {
  title: string;
  activities?: string[];
  area?: string[];
  conteudo?: string[];
  topic?: string[];
  hasDocument?: boolean;
}

export interface CommonAsked {
  id: string;
  title: string;
  questions?: string[];
  area?: string[];
  conteudo?: string[];
  topic?: string[];
  hasDocument?: boolean;
}

