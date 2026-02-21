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
  area?: string[];
  conteudo?: string[];
  topic?: string[];
  rank?: number[];
  hasDocument?: boolean;
}

export interface Book {
  id: string;
  title: string;
  chapters?: string[];
  area?: string[];
  conteudo?: string[];
  topic?: string[];
  hasDocument?: boolean;
}

export interface Chapter {
  id: string;
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

