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
//   socket.send('Hello Server! I am not hardcoded.'); //agora isso faz fracassar
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

const dadosValidos = {
  nome: "Usuario",
  idade: 30,
  email: "joao@exemplo.com",
  texto: ""
};

rl.on('line', (line) => {
  const trimmed = line.trim();
  dadosValidos.texto = trimmed;
//   console.log("dadosValidos:", dadosValidos)
  socket.send(JSON.stringify(dadosValidos));
  rl.prompt(); 
}).on('close', () => {
  console.log('Encerrando o programa. Obrigado.');
  process.exit(0);
});

rl.prompt(); 