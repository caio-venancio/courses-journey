const { createInterface } = require('node:readline');

const rl = createInterface({
  input: process.stdin,
  output: process.stdout
});

const WebSocket = require('ws');

const isBrowser = typeof window !== "undefined";

const wsUrl = isBrowser //desse jeito, pode rodar tanto com node quanto em navegador
  ? `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}`
  : process.env.WS_URL || "ws://localhost:8080";

const socket = new WebSocket(wsUrl);

socket.on('open', event => {
  console.log('WebSocket connection established!');
  socket.send('Hello Server! I am not hardcoded.');
});

socket.on('message', message => {
  console.log('Message from server: ', message.toString());
});

socket.on('close', event => {
  console.log('WebSocket connection closed:', event.code, event.reason);
});

socket.on('error', error => {
  console.error('WebSocket error:', error);
});

// Primeira tentativa
// while(true){ //loop síncrono e não aguarda
//     let input = new Promise(function(Resolve){
//         setTimeout(Resolve("Acabo de te mandar mais uma mensagem :b"), 3000); //errado
//     });

//     input.then(function(value){
//         socket.send(value)
//     })
// }

// Segunda tentativa
// async function sendMessages() {
//     while(true){
//         await new Promise(resolve => setTimeout(resolve, 3000));
//         socket.send("Acabo de te mandar mais uma mensagem :b");
//     }
// }

// sendMessages();

rl.on('line', (line) => {
  const trimmed = line.trim();
  socket.send(trimmed);
  rl.prompt(); 
}).on('close', () => {
  console.log('Encerrando o programa. Obrigado.');
  process.exit(0);
});

rl.prompt(); 