import type { Document } from "../models/document";

export interface IndexStore {
  save(doc: Document): void;
  search(query: string): Document[];
  clear(): void;
}
