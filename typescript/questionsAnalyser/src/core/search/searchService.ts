import { IndexStore } from "../index/IndexStore";
import { SearchQuery } from "../models/searchQuery";
import { SearchResult } from "../models/searchResult";

export class SearchService {
  constructor(private index: IndexStore) {}

  search(query: SearchQuery): SearchResult[] {
    if (!query.text) return [];

    return this.index.search(query.text).map(doc => ({
      document: doc
    }));
  }
}
