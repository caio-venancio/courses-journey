// const puppeteer = require('puppeteer');
// const fs = require('fs');
// const path = require('path');

// async function verificarMudancaSite(url, arquivoReferencia) {
//     const browser = await puppeteer.launch({ headless: "new" });
//     const page = await browser.newPage();

//     try {
//         console.log(`Acessando: ${url}`);
//         await page.goto(url, { waitUntil: 'networkidle2' });

//         // Seleciona o conteúdo que deseja monitorar (ex: body ou uma div específica)
//         const conteudoAtual = await page.evaluate(() => {
//             return document.body.innerText; // Monitora o texto do site
//         });

//         // Verifica se o arquivo de referência existe
//         if (fs.existsSync(arquivoReferencia)) {
//             const conteudoAnterior = fs.readFileSync(arquivoReferencia, 'utf8');

//             if (conteudoAtual !== conteudoAnterior) {
//                 console.log('--- Mudança detectada! ---');
//                 // Atualiza o arquivo com o novo conteúdo
//                 fs.writeFileSync(arquivoReferencia, conteudoAtual);
                
//                 // Opcional: tirar screenshot
//                 await page.screenshot({ path: `mudanca-${Date.now()}.png` });
//                 return true; // Site mudou
//             } else {
//                 console.log('Nenhuma mudança detectada.');
//                 return false; // Site não mudou
//             }
//         } else {
//             // Primeiro acesso, cria o arquivo
//             console.log('Criando arquivo de referência inicial.');
//             fs.writeFileSync(arquivoReferencia, conteudoAtual);
//             return false;
//         }
//     } catch (error) {
//         console.error('Erro ao verificar o site:', error);
//     } finally {
//         await browser.close();
//     }
// }

// // Uso da função
// const URL_ALVO = 'https://example.com';
// const ARQUIVO = path.join(__dirname, 'referencia.txt');

// verificarMudancaSite(URL_ALVO, ARQUIVO);
