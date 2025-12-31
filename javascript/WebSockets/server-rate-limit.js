// // Exemplo conceitual usando Node.js e a biblioteca 'ws'
import { WebSocketServer } from 'ws';
const wss = new WebSocketServer({ port: 8080 });
import { v4 as uuidv4 } from 'uuid'; // Importa a função v4 do uuid

// Usaremos um Mapa (Map) em memória para rastrear o uso de cada cliente conectado
const clientUsage = new Map();
const RATE_LIMIT_MESSAGES_PER_SECOND = 30;

function getClientId(){
    return uuidv4();
}

wss.on('connection', function connection(ws) {
    // Gerar um ID único para a conexão, ou usar o IP (requer configuração extra)
    const connectionId = getClientId(); // Função fictícia para obter ID/IP
    clientUsage.set(connectionId, { count: 0, lastReset: Date.now() });

    ws.on('error', (error) => {
        console.error(`Erro na conexão ${connectionId}:`, error);
    });

    ws.on('message', function incoming(message) {
        const usage = clientUsage.get(connectionId);
        const now = Date.now();

        // Verificar se a janela de tempo expirou (a cada segundo, por exemplo)
        if (now - usage.lastReset > 1000) { // 1000ms = 1 segundo
            usage.count = 0;
            usage.lastReset = now;
        }

        usage.count++;

        if (usage.count > RATE_LIMIT_MESSAGES_PER_SECOND) {
            console.log(`Rate limit excedido para ${connectionId}. Desconectando...`);
            ws.send(JSON.stringify({
                error: "Too many messages",
                retryAfter: "Após 1 segundo"
            }));
            ws.close(1008, 'Policy Violation - Rate limit exceeded'); // 1008 = Policy Violation
            return;
        }

        // Processar a mensagem normalmente
        // ...
    });

    ws.on('close', () => {
        clientUsage.delete(connectionId); // Limpar o rastro ao fechar a conexão
    });
});

console.log("Rodando um server WebSocket básico com rate limite por conexão.");