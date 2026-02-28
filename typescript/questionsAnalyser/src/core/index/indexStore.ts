import type { Document, Question } from "../models/document";

export interface IndexStore {
  save(doc: Document): void;
  saveQuestion(question: Question): void;
  search(query: string): Document[];
  verifyQuestion(questionTitle: string): boolean 
  clear(): void;
  check(): void;
}
