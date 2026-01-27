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
