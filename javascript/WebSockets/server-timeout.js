// const WebSocket = require('ws');

// // O tempo limite em milissegundos (ex: 30 segundos)
// const TIMEOUT_MS = 30000; 

// const wss = new WebSocket.Server({ port: 8080 });

// wss.on('connection', function connection(ws) {
//   // Adiciona uma propriedade para rastrear a atividade
//   ws.isAlive = true; 

//   // Quando o cliente envia um 'pong', marcamos como vivo
//   ws.on('pong', function heartbeat() {
//     ws.isAlive = true;
//   });

//   // Configura um temporizador para fechar a conexão se inativa
//   ws.timer = setTimeout(() => {
//     if (!ws.isAlive) {
//       console.log('Timeout: Conexão inativa encerrada.');
//       ws.terminate(); // Encerra a conexão forçadamente
//     }
//   }, TIMEOUT_MS);

//   ws.on('close', () => {
//     console.log('Conexão fechada. Limpando timer.');
//     clearTimeout(ws.timer); // Garante que o timer seja cancelado ao fechar
//   });
// });

// // Opcional: Um loop de ping/pong para manter a conexão ativa
// const interval = setInterval(() => {
//   wss.clients.forEach((ws) => {
//     if (!ws.isAlive) {
//       // Se já estava inativo na última checagem, encerra agora
//       console.log('Inativo: Encerrando conexão.');
//       return ws.terminate();
//     }

//     // Marca como inativo e envia um ping
//     ws.isAlive = false;
//     ws.ping();
//   });
// }, TIMEOUT_MS / 2); // Verifica a cada metade do tempo limite

// wss.on('close', () => {
//   clearInterval(interval);
// });

// console.log('Servidor WebSocket iniciado na porta 8080');
