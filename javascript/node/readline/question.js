const readline = require('readline');

// Cria a interface de leitura e escrita
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Faz a pergunta
rl.question('Qual é o seu nome? ', (answer) => {
  console.log(`Olá, ${answer}!`);
  rl.close(); // Essencial para fechar a interface e finalizar o programa
});
