// with input validation
// https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html

import Ajv from 'ajv';
import addFormats from 'ajv-formats';
const ajv = new Ajv(); // Cria uma instância do validador
addFormats(ajv);

import { WebSocketServer } from 'ws'; 

const wss = new WebSocketServer({ port: 8080 });

const schema = {
  type: "object",
  properties: {
    nome: { type: "string", minLength: 3 },
    idade: { type: "integer", minimum: 0 },
    email: { type: "string", format: "email" },
    texto: { type: "string", minLength: 3, maxLength: 20 }
  },
  required: ["nome", "idade"]
};

//Compile o esquema (opcional, mas recomendado para performance)
const validate = ajv.compile(schema);

wss.on('connection', function connection(ws) {
  ws.on('error', console.error);

  ws.on('message', function message(data) {
    try {
        const dataParsed = JSON.parse(data);
 
        if (!validate(dataParsed)) {
            throw new Error("Formato inválido");
        }

        ws.send("Formato válido, cliente.")

    } catch (e) {
        console.error("Mensagem inválida recebida");
        // Opcional: fechar a conexão se a mensagem for maliciosa
        ws.send('Formato inválido, cliente.')
        ws.close(1008, 'Invalid file type');
    }
  });

  ws.send('Hello, client!');
});