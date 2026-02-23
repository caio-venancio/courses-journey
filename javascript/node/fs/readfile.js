const fs = require('fs');
const readline = require('readline');

async function lerArquivoLinhaPorLinha(caminhoArquivo) {
  // 1. Cria a stream de leitura do arquivo
  const fileStream = fs.createReadStream(caminhoArquivo);

  // 2. Configura a interface readline
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity // Reconhece \r\n como uma nova linha
  });

  // 3. Lê o arquivo linha por linha
  for await (const line of rl) {
    console.log(`Linha lida: ${line}`);
  }

  console.log('--- Fim do arquivo ---');
}

// Chame a função (certifique-se de ter um arquivo 'teste.txt')
lerArquivoLinhaPorLinha('listallfiles.js');
