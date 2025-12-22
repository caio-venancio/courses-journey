// const WebSocket = require('ws');
// const Redis = require('ioredis');

// const wss = new WebSocket.Server({ port: 8080 });
// const redis = new Redis(); // Conecta ao servidor Redis padrão

// // Armazena a contagem de mensagens por cliente (ex: por IP)
// const messageCounts = {};

// wss.on('connection', (ws, req) => {
//     const ip = req.socket.remoteAddress;
//     messageCounts[ip] = messageCounts[ip] || { count: 0, lastReset: Date.now() };

//     ws.on('message', (message) => {
//         const now = Date.now();
//         const clientData = messageCounts[ip];

//         // Redefine a contagem se o período de tempo (ex: 1 segundo) passou
//         if (now - clientData.lastReset > 1000) {
//             clientData.count = 0;
//             clientData.lastReset = now;
//         }

//         // Verifica o limite (ex: máximo de 10 mensagens/segundo)
//         if (clientData.count >= 10) {
//             console.log(`Rate limit excedido para o IP ${ip}. Mensagem descartada.`);
//             // Opcional: enviar um código de erro ou fechar a conexão
//             // ws.send(JSON.stringify({ error: 'Too many requests' })); 
//             return;
//         }

//         clientData.count++;
//         // Processa a mensagem normalmente
//         // ...
//     });

//     ws.on('close', () => {
//         // Limpar dados do cliente, se necessário
//         delete messageCounts[ip]; 
//     });
// });

// console.log('Servidor WebSocket com rate limit (básico) rodando em ws://localhost:8080');
