// const WebSocket = require('ws');

// // Cria um servidor WebSocket na porta 8080
// const wss = new WebSocket.Server({ port: 8080 });

// // Função para enviar pings periodicamente e verificar a atividade
// const interval = setInterval(function ping() {
//   wss.clients.forEach(function each(ws) {
//     // Se o cliente já estiver marcado como inativo (isAlive === false), encerra a conexão
//     if (ws.isAlive === false) return ws.terminate();

//     // Marca o cliente como inativo e envia um ping.
//     // A propriedade isAlive será redefinida para true quando o cliente responder com um pong.
//     ws.isAlive = false;
//     ws.ping();
//   });
// }, 10000); // Executa a cada 10 segundos (10000ms)

// wss.on('connection', function connection(ws) {
//   // Inicializa o status do cliente como vivo
//   ws.isAlive = true;

//   // Quando o cliente responde com um pong, redefine o status isAlive para true
//   ws.on('pong', function heartbeat() {
//     ws.isAlive = true;
//   });

//   ws.on('message', function incoming(message) {
//     console.log('received: %s', message);
//   });

//   ws.on('close', function close() {
//     console.log('Cliente desconectado');
//   });
// });

// wss.on('close', function close() {
//   clearInterval(interval);
// });

// console.log('Servidor WebSocket iniciado na porta 8080');

const WebSocket = require('ws');

const HEARTBEAT_INTERVAL = 10000;

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  ws.isAlive = true;

  ws.on('pong', () => {
    ws.isAlive = true;
  });

  ws.on('close', () => {
    console.log('Conexão fechada');
  });
});

const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (!ws.isAlive) {
      console.log('Heartbeat falhou, encerrando conexão');
      ws.send('Você falhou com o Heartbeat. Encerrando.')
      return ws.terminate();
    }

    ws.isAlive = false;
    ws.ping();
  });
}, HEARTBEAT_INTERVAL);

wss.on('close', () => {
  clearInterval(interval);
});

console.log('Servidor WebSocket com heartbeat iniciado na porta 8080');
