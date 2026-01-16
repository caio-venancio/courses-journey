import WebSocket, { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

const IDLE_TIMEOUT = 10_000; // 30 segundos

wss.on('connection', (ws) => {
  let timeout;

  const resetTimeout = () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      console.log('Conexão encerrada por inatividade');
      ws.close(4000, 'Idle timeout');
    }, IDLE_TIMEOUT);
  };

  // Primeira inicialização
  resetTimeout();

  ws.on('message', (data) => {
    console.log('Mensagem recebida:', data.toString());
    resetTimeout(); // atividade detectada
  });

  ws.on('close', () => {
    clearTimeout(timeout);
    console.log('Conexão fechada');
  });

  ws.on('error', () => {
    clearTimeout(timeout);
  });
});
