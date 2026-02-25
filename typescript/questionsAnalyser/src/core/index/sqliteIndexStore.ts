import Database from "better-sqlite3";
import type { Document } from "../models/document";
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
    `);
  }

  save(doc: Document): void {
    this.db.prepare(`
      INSERT INTO documents (id, path, title, content)
      VALUES (?, ?, ?, ?)
    `).run(doc.id, doc.path, doc.title, doc.content);
  }

  search(query: string): Document[] {
    return this.db.prepare(`
      SELECT * FROM documents
      WHERE content LIKE ?
    `).all(`%${query}%`) as Document[];
  }

  clear(): void {
    this.db.exec("DELETE FROM documents");
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
