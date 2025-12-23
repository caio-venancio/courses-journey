// const WebSocket = require('ws');
import { WebSocketServer } from 'ws';

// // Definir o limite máximo de conexões
const MAX_CONNECTIONS = 5; 
let connectedClients = 0;


// // Criar um servidor WebSocket na porta 8080
// const wss = new WebSocket.Server({ port: 8080 });
const wss = new WebSocketServer({ port: 8080 });

console.log(`Servidor WebSocket iniciado na porta 8080. Limite de conexões: ${MAX_CONNECTIONS}`);

wss.on('connection', function connection(ws) {
    // Verificar se o limite de conexões foi atingido
    if (connectedClients >= MAX_CONNECTIONS) {
        console.log('Limite de conexões atingido. Nova conexão rejeitada.');

        ws.send(JSON.stringify({
            error: 'Limite máximo de conexões atingido. Tente novamente mais tarde.'
        }));
        
        ws.close(1013, 'Limite máximo de conexões atingido'); // Código de status 1013 (Too Big) é apropriado
        return;
    }

    // Incrementar a contagem de clientes conectados
    connectedClients++;
    console.log(`Novo cliente conectado. Total de conexões: ${connectedClients}`);

    // Lidar com mensagens recebidas do cliente
    ws.on('message', function incoming(message) {
        console.log('Recebido: %s', message);
        // Exemplo: ecoar a mensagem de volta para o cliente
        ws.send(`Servidor recebeu sua mensagem: ${message}`);
    });

    // Lidar com o fechamento da conexão
    ws.on('close', function close() {
        connectedClients--;
        console.log(`Cliente desconectado. Total de conexões: ${connectedClients}`);
    });

    // Lidar com erros de conexão
    ws.on('error', function error(err) {
        console.error('Erro na conexão WebSocket:', err);
    });

    // Enviar uma mensagem de boas-vindas inicial para o novo cliente
    ws.send(JSON.stringify({
        status: 'Conectado com sucesso!',
        connections: connectedClients,
        limit: MAX_CONNECTIONS
    }));
});

wss.on('listening', () => {
    console.log('Servidor está ouvindo...');
});
