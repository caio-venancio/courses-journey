import { Document } from "./document";

export interface SearchResult {
  document: Document;
  score?: number;
}
