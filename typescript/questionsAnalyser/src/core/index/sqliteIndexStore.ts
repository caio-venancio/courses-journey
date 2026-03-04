import Database from "better-sqlite3";
import type { Book, Document, Question, Chapter } from "../models/document";
import type { IndexStore } from "./indexStore";

export class SqliteIndexStore implements IndexStore {
  private db = new Database("index.db");

  constructor() {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS documents (
        id TEXT,
        path TEXT,
        title TEXT,
        content TEXT
      );

      CREATE TABLE IF NOT EXISTS questions (
        title TEXT PRIMARY KEY NOT NULL,
        question TEXT NOT NULL,
        answer TEXT,
        book_id TEXT,
        chapter INTEGER,
        has_document BOOLEAN DEFAULT 0
      );

      CREATE TABLE IF NOT EXISTS books ( 
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        book_id TEXT UNIQUE,
        edition INTEGER DEFAULT 1,
        has_document BOOLEAN DEFAULT 0,
        UNIQUE(title, edition)
      );

      CREATE TABLE IF NOT EXISTS chapters (
          title TEXT,
          number INTEGER NOT NULL,
          book_id TEXT NOT NULL,
          has_document BOOLEAN DEFAULT 0,
          PRIMARY KEY (book_id, number)
      );
    `);
  }

  save(doc: Document): void {
    this.db.prepare(`
      INSERT INTO documents (id, path, title, content)
      VALUES (?, ?, ?, ?)
    `).run(doc.id, doc.path, doc.title, doc.content);
  }

  saveQuestion(question: Question): void {
    try {
      this.db.prepare(`
      INSERT INTO questions (title, question, answer, book_id, chapter, has_document)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(question.title, question.question, question.answer, question.bookId, question.chapter, question.hasDocument);
    } catch (err) {
      console.warn('erro eh este:', err)
      console.log('-----------------------------------')
      console.log('A questao que deu erro:', question)
    }
  }

  saveBook(book: Book): void {
    try {
      this.db.prepare(`
      INSERT INTO books (title, book_id, edition, has_document)
      VALUES (?, ?, ?, ?)
    `).run(book.title, book.bookId, book.edition, book.hasDocument);
    } catch (err) {
      console.warn('erro eh este:', err)
      console.log('-----------------------------------')
      console.log('A questao que deu erro:', book)
    }
  }

  saveChapter(chapter: Chapter): void {
    try {
      this.db.prepare(`
      INSERT INTO chapters (title, book_id, number, has_document)
      VALUES (?, ?, ?, ?)
    `).run(chapter.title, chapter.bookId, chapter.number, chapter.hasDocument);
    } catch (err) {
      console.warn('erro eh este:', err)
      console.log('-----------------------------------')
      console.log('A questao que deu erro:', chapter)
    }
  }



  search(query: string): Document[] {
    return this.db.prepare(`
      SELECT * FROM documents
      WHERE content LIKE ?
    `).all(`%${query}%`) as Document[];
  }

  verifyQuestion(questionTitle: string): boolean {
    try {
      const stmt = this.db.prepare('SELECT EXISTS(SELECT 1 FROM questions WHERE title = ? LIMIT 1) AS existe');
      const resultado = stmt.get(questionTitle) as { existe: number };
      return resultado.existe === 1;
    } catch(err) {
      console.warn('erro eh este:', err)
      console.log('-----------------------------------')
      console.log('A questao que deu erro:', questionTitle)
      return false;
    }
  }

  clear(): void {
    this.db.exec("DELETE FROM documents");
  }

  resetTable(): void {
    this.db.exec("DROP TABLE IF EXISTS chapters;")
  }

  check(): void {
    const schema = this.db.prepare("SELECT sql FROM sqlite_master WHERE type='table'").all();
    console.log("tabelas:", JSON.stringify(schema, null, 2))
    this.printTableCounts()
  }

  printTableCounts() {
    const tableNames = this.db.prepare(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    ).all() as { name: string }[];

    console.log('--- Contagem de Itens por Tabela ---');

    for (const table of tableNames) {
        const tableName = table.name;
        const count = this.db.prepare(`SELECT COUNT(*) as count FROM "${tableName}"`).get() as { count: number };
        
        console.log(`Tabela: ${tableName} | Itens: ${count.count}`);
    }
    console.log('-----------------------------------');
  }

  close(): void {
    this.db.close(); //task: fazer classe receber o .db para melhor arquitetura algum dia
  }
}
