import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({
    port: 8080,
    maxPayload: 10 //só aceita strings com 10 letras por exemplo
});

wss.on('connection', function connection(ws) {
  ws.on('error', console.error);

  ws.on('message', function message(data) {
    console.log('received: %s', data);
  });

  ws.send('Hello, client!');
});