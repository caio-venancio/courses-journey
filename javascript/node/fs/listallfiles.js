const fs = require('fs/promises');
const path = require('path');

async function lerArquivosDoDiretorioAtual() {
  try {
    // '.' representa o diretório atual
    const arquivos = await fs.readdir('.'); 
    console.log('Arquivos no diretório atual:', arquivos);

    // Se você precisar do caminho completo de cada arquivo:
    for (const arquivo of arquivos) {
      const caminhoCompleto = path.join(process.cwd(), arquivo);
      console.log(`Caminho completo: ${caminhoCompleto}`);
    }

  } catch (err) {
    console.error('Erro ao ler o diretório:', err);
  }
}

lerArquivosDoDiretorioAtual()