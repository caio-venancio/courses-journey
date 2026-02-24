import * as os from 'os';
import { NodeFileProvider } from './nodeFileProvider.js';
import { MarkdownParser } from '../core/parser/markdownParser.js';
import { SqliteIndexStore } from '../core/index/sqliteIndexStore.js';
import { Indexer } from '../core/indexer.js'
import { SearchService } from '../core/search/searchService.js';
import { checkConfig, checkDirectoryPath, saveConfig, getConfig } from './nodeConfigService.js';
import { createInterface } from 'node:readline'
import { exit } from 'node:process';
import { DocumentValidator } from '../core/parser/documentValidator.js';

const rl = createInterface({
  input: process.stdin,
  output: process.stdout,
});

const perguntar = (query: string) => new Promise((resolve) => rl.question(query, resolve));

if (!checkConfig()){
    const answer = await perguntar('Qual diretório de homedir deseja colocar seus estudos? ');// tem que checar a segurança por ser entrada de usuário
    console.log(`Testando o diretório ${answer}...`);
    if(checkDirectoryPath(answer as string)){ //tem que mandar caminho completo kkk //tem que verificar tipo depois
        console.log('Sucesso, vamos configurar com esse caminho.')
        saveConfig(answer as string); //tem que verificar tipo depois
    } else {
        console.log('Não foi possível conferir este diretório, tente novamente.')
        exit(0)
    }
}

const perguntaDaInterface: string = `
    O que deseja realizar?
    Sair do programa - 0
    Mostrar qual pasta está configurada - 1
    Mostrar quais arquivos foram detectados - 2
    Mostrar todas as questões detectadas - 5
    Verificar se há arquivos no padrão errado - 3
    Contar quantos arquivos de cada padrão tem - 4
    Formatar uma questão para exemplo - 6
    Mostrar banco de dados atual - 7
`

const fileProvider = new NodeFileProvider();
const documentValidador = new DocumentValidator(fileProvider)
const markdownParser = new MarkdownParser()
const indexStore = new SqliteIndexStore();

let answer = 1;
while(answer != 0){
    answer = await perguntar(perguntaDaInterface) as number

    if(answer == 1){
        console.log("Configuração para pasta", os.homedir() + '\\' + getConfig()?.targetFolder)
    }

    if(answer == 2){
        let list = await fileProvider.listMarkdownFiles()
        console.log("Lista de markdown:", list)
    }

    if(answer == 3){
        let badFormat = documentValidador.verifyTitles()
    }

    if(answer == 4){
        console.log("Brincadeiera, ainda não foi implementado kk")
    }

    if(answer == 5){
        let response = documentValidador.onlyQuestionsTitle()
        console.log("Essas são as questões detectadas:", await response)
    }

    if(answer == 6){
        let response = await documentValidador.onlyQuestionsTitle()
        if(response[1]){
            const content = await fileProvider.readFile(response[1]);
            const filename = await fileProvider.filenameOnly(response[1]);
            const parsedQuestion = await markdownParser.parseQuestion(content, filename)

            console.log("MarkdownParser.parseQuestion():", parsedQuestion)
        } else{
            console.log("Response em 6 falhou.")
        }
    }

    if(answer == 7){
        console.log("Banco atual:")
        indexStore.check()
    }
}
rl.close(); 

// Ponto de entrada do programa em CLI
// console.log("fileProvider:", fileProvider);
// console.log("Versão elegante do fileProvider:", JSON.parse(JSON.stringify(fileProvider)));

// const parser = new MarkdownParser();
// console.log("parser:", parser);
// console.log("Versão elegante do parser:", JSON.parse(JSON.stringify(parser)));

// const indexStore = new SqliteIndexStore();
// console.log("indexStore:", indexStore);
// console.log("Versão elegante do indexStore:", JSON.parse(JSON.stringify(indexStore)));

// const indexer = new Indexer(fileProvider, parser, indexStore);
// console.log("Indexer:", indexer);
// console.log("Versão elegante do Indexer:", JSON.parse(JSON.stringify(indexer)));
// await indexer.run();

// const searchService = new SearchService(indexStore);
// console.log("searchService:", searchService);
// console.log("Versão elegante do searchService:", JSON.parse(JSON.stringify(searchService)));

// const results = searchService.search({ text: "maclaurin" });
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

// console.log("arquivos markdown encontrados:", await fileProvider.listMarkdownFiles())

console.log("Thank you very much!")
