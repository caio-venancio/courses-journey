import Database from 'better-sqlite3';

// 1. Conectar ao banco de dados (criar arquivo ou :memory: para memória)
const db = new Database('meu-banco.db', { verbose: console.log });

// 2. Criar uma tabela
const createTable = db.prepare(`
  CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER
  )
`);
createTable.run();

// 3. Inserir dados (Create)
const inserir = db.prepare('INSERT INTO usuarios (nome, idade) VALUES (?, ?)');
const info = inserir.run('Alice', 30);
console.log(`Usuário inserido com ID: ${info.lastInsertRowid}`);

// 4. Ler dados (Read)
const listar = db.prepare('SELECT * FROM usuarios WHERE idade > ?');
const usuarios = listar.all(25); // Passa parâmetros para o ?
console.log('Usuários maiores de 25:', usuarios);

// 5. Atualizar dados (Update)
const atualizar = db.prepare('UPDATE usuarios SET nome = ? WHERE id = ?');
atualizar.run('Alice Silva', 1);

// 6. Fechar o banco (boa prática)
db.close();