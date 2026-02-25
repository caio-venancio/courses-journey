import Database from 'better-sqlite3';

try {
    const db = new Database('meu-banco.db', { verbose: console.log, fileMustExist: true });
    console.log("O banco existe já.")
    db.close()
} catch (error){
    console.log("O banco de dados não existe.");
}