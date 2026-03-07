import type { Document, Question, Book, Chapter } from "../models/document";

export interface IndexStore {
  save(doc: Document): void;
  saveQuestion(question: Question): void;
  saveBook(book: Book): void;
  saveChapter(chapter: Chapter): void;
  search(query: string): Document[];
  findAllBooks(): Book[];
  verifyQuestion(questionTitle: string): boolean 
  
  clear(): void;
  check(): void;
}
