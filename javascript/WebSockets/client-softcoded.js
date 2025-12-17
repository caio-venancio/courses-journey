const WebSocket = require('ws');

const isBrowser = typeof window !== "undefined";

const wsUrl = isBrowser //desse jeito, pode rodar tanto com node quanto em navegador
  ? `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}`
  : process.env.WS_URL || "ws://localhost:8080";

const socket = new WebSocket(wsUrl);

socket.addEventListener('open', event => {
  console.log('WebSocket connection established!');
  socket.send('Hello Server! I am not hardcoded.');
});

socket.addEventListener('message', event => {
  console.log('Message from server: ', event.data);
});

socket.addEventListener('close', event => {
  console.log('WebSocket connection closed:', event.code, event.reason);
});

socket.addEventListener('error', error => {
  console.error('WebSocket error:', error);
});