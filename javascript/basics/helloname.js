// Importa o módulo readline
const readline = require('readline');

// Cria uma instância de interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Faz a pergunta ao usuário
rl.question('Qual o seu nome? \n', (nome) => {
  // Esta função de callback é executada após o usuário digitar e apertar Enter
  console.log(`Olá, ${nome}!`);
  
  // Fecha a interface para finalizar o programa
  rl.close();
});

// Evento opcional para quando a interface é fechada
rl.on('close', () => {
  console.log('Programa encerrado.');
  process.exit(0);
});