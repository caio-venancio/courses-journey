const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const ajv = new Ajv(); // Cria uma instância do validador
addFormats(ajv); // Adiciona formatos como email, date, etc.

// 1. Carregue o esquema (pode ser de um arquivo ou string)
// Se for de um arquivo, você precisaria ler o arquivo primeiro
const schema = {
  type: "object",
  properties: {
    nome: { type: "string", minLength: 3 },
    idade: { type: "integer", minimum: 0 },
    email: { type: "string", format: "email" }
  },
  required: ["nome", "idade"]
};

// 2. Compile o esquema (opcional, mas recomendado para performance)
const validate = ajv.compile(schema);

// 3. Dados JSON para validar
const dadosValidos = {
  nome: "João",
  idade: 30,
  email: "joao@exemplo.com"
};

const dadosInvalidos = {
  nome: "J", // Muito curto
  idade: -5, // Inválido
  telefone: "123456789" // Não definido no schema
};

// 4. Valide os dados
const isValid1 = validate(dadosValidos); // true
const isValid2 = validate(dadosInvalidos); // false

console.log(`Dados válidos são válidos? ${isValid1}`); // Saída: true

console.log(`Dados inválidos são válidos? ${isValid2}`); // Saída: false
// Para ver os erros:
if (!isValid2) {
  console.log("Erros de validação:", validate.errors);
}
/* Saída:
Erros de validação: [
  {
    instancePath: '/nome',
    schemaPath: '#/properties/nome/minLength',
    keyword: 'minLength',
    params: { limit: 3 },
    message: 'deve ter no mínimo 3 caracteres'
  },
  {
    instancePath: '/idade',
    schemaPath: '#/properties/idade/minimum',
    keyword: 'minimum',
    params: { limit: 0 },
    message: 'deve ser maior ou igual a 0'
  },
  {
    instancePath: '',
    schemaPath: '#/required',
    keyword: 'required',
    params: { missingProperty: 'email' },
    message: 'deve conter a propriedade obrigatória'
  }
]
*/
