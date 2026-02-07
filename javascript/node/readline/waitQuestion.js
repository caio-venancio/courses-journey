const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Promisify a função question
const perguntar = (query) => new Promise((resolve) => rl.question(query, resolve));

async function rodar() {
  const nome = await perguntar("Qual seu nome? "); // Espera o enter
  console.log(`Olá ${nome}`);
  
  const idade = await perguntar("Qual sua idade? "); // Espera novamente
  console.log(`${nome} tem ${idade} anos.`);
  
  rl.close();
}

rodar();
console.log("Esperei.")
