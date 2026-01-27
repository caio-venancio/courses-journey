import Database from "better-sqlite3";
import { Document } from "../models/Document";
import { IndexStore } from "./IndexStore";

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
    `).all(`%${query}%`);
  }

  clear(): void {
    this.db.exec("DELETE FROM documents");
  }
}
