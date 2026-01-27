import { NodeFileProvider } from './nodeFileProvider';

// Ponto de entrada do programa em CLI
const fileProvider = new NodeFileProvider();
// const parser = new MarkdownParser();
// const indexStore = new SqliteIndexStore();

// const indexer = new Indexer(fileProvider, parser, indexStore);
// await indexer.run();

// const searchService = new SearchService(indexStore);
// const results = searchService.search({ text: "maclaurin" });

console.log("fileProvider:", fileProvider);
console.log(JSON.parse(JSON.stringify(fileProvider)));