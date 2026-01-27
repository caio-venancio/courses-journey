import { NodeFileProvider } from './nodeFileProvider.js';
import { MarkdownParser } from '../core/parser/markdownParser.js';
import { SqliteIndexStore } from '../core/index/sqliteIndexStore.js';
import { Indexer } from '../core/indexer.js'
import { SearchService } from '../core/search/searchService.js';

// Ponto de entrada do programa em CLI
const fileProvider = new NodeFileProvider();
// console.log("fileProvider:", fileProvider);
// console.log("Versão elegante do fileProvider:", JSON.parse(JSON.stringify(fileProvider)));

const parser = new MarkdownParser();
// console.log("parser:", parser);
// console.log("Versão elegante do parser:", JSON.parse(JSON.stringify(parser)));

const indexStore = new SqliteIndexStore();
// console.log("indexStore:", indexStore);
// console.log("Versão elegante do indexStore:", JSON.parse(JSON.stringify(indexStore)));

const indexer = new Indexer(fileProvider, parser, indexStore);
// console.log("Indexer:", indexer);
// console.log("Versão elegante do Indexer:", JSON.parse(JSON.stringify(indexer)));
await indexer.run();

const searchService = new SearchService(indexStore);
// console.log("searchService:", searchService);
// console.log("Versão elegante do searchService:", JSON.parse(JSON.stringify(searchService)));

const results = searchService.search({ text: "maclaurin" });
// console.log("results:", results[0]);
// console.log("Versão elegante do results:", JSON.parse(JSON.stringify(results)));

//    Object.entries(results).forEach(([chave, valor]) => {
//         Object.entries(valor).forEach(([chave1, valor1]) => {
//             Object.entries(valor1).forEach(([chave2, valor2]) => {
//                 if (chave2.includes("path")) {
//                     console.log(`Chave2: ${chave2}, Valor2: ${valor2}`);
//                 }
//             })
//         })
//    });

console.log("arquivos markdown encontrados:", await fileProvider.listMarkdownFiles())
