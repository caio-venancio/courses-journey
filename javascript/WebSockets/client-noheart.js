const WebSocket = require('ws');

const isBrowser = typeof window !== "undefined";

const wsUrl = isBrowser //desse jeito, pode rodar tanto com node quanto em navegador
  ? `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}`
  : process.env.WS_URL || "ws://localhost:8080";

const socket = new WebSocket(wsUrl);

socket.on('open', event => {
  console.log('WebSocket connection established!');
  socket.send('Hello Server! I am not hardcoded.');
  
  // Aguarda um pouco e então trava o event loop para falhar o heartbeat
  setTimeout(() => {
    console.log('Travando event loop para falhar heartbeat...');
    while(true) {} // Trava o event loop - não responderá mais aos pings
  }, 5000); // Espera 5 segundos antes de travar
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

// Intercepta o evento 'ping' para impedir resposta automática (método alternativo)
// socket.on('ping', () => {
//   console.log('Ping recebido, mas NÃO vou responder com pong');
//   // Não fazer nada aqui impede a resposta automática
// });