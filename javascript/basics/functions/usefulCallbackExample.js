// 1. A função principal (que faz o trabalho demorado)
function buscarUsuario(id, callback) {
    console.log(`Buscando usuário ${id}...`);
    
    // Simula uma requisição assíncrona com 2 segundos de delay
    setTimeout(() => {
        console.log("Dados recebidos!");
        const usuario = { id: id, nome: "João Silva" };
        
        // 2. Chama o callback passando o resultado
        callback(usuario);
    }, 2000);
}

// 3. A função de callback (o que fazer depois)
function exibirPerfil(usuario) {
    console.log(`Exibindo perfil de: ${usuario.nome}`);
}

// 4. Execução: Passando exibirPerfil como argumento
buscarUsuario(101, exibirPerfil);

// Mensagem que aparece antes da resposta do "servidor"
console.log("Outras tarefas continuam rodando...");
