import type { IndexStore } from "../index/indexStore";
import type { SearchQuery } from "../models/searchQuery";
import type { SearchResult } from "../models/searchResult";

export class SearchService {
  constructor(private index: IndexStore) {}

  search(query: SearchQuery): SearchResult[] {
    if (!query.text) return [];

    return this.index.search(query.text).map(doc => ({
      document: doc
    }));
  }
}
