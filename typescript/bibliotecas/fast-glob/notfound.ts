import fg from 'fast-glob'

async function buscarArquivos() {
  const padrao = ['src/**/*.js', '!node_modules/**'];
  const arquivos = await fg(padrao);

  // Verificação de resposta vazia
  if (arquivos.length === 0) {
    console.log('Nenhum arquivo encontrado para o padrão informado.');
    return []; // Retorna um array vazio ou handle do seu erro
  }

  console.log(`${arquivos.length} arquivos encontrados:`, arquivos);
  return arquivos;
}

buscarArquivos()