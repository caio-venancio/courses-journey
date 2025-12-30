const { createInterface } = require('node:readline');

const rl = createInterface({
  input: process.stdin,
  output: process.stdout
});

function fakeSend(msg) {
  // simula request para um servidor
  console.log(`[enviando] ${msg}`);
}

rl.on('line', (line) => {
  const trimmed = line.trim();
  fakeSend(trimmed);
  console.log(`Recebido localmente: ${trimmed}`);
  rl.prompt(); // reaparece para o próximo input
}).on('close', () => {
  console.log('Encerrando o programa.');
  process.exit(0);
});

// async function sendMessages() {
//   while (true) {
//     await new Promise(resolve => setTimeout(resolve, 3000));
//     fakeSend('Acabo de te mandar mais uma mensagem :b');
//   }
// }

rl.prompt();   // primeiro prompt
// sendMessages();