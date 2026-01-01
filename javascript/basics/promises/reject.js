function verificarIdade(idade) {
  return new Promise((resolve, reject) => {
    if (idade >= 18) {
      resolve("Usuário maior de idade, acesso permitido.");
    } else {
      // Rejeita a promise se a condição não for atendida
      reject(new Error("Usuário menor de idade, acesso negado."));
    }
  });
}

// Uso da função
verificarIdade(15)
  .then((mensagem) => {
    console.log(mensagem); // Não será executado neste caso
  })
  .catch((erro) => {
    console.error("Ocorreu um erro:", erro.message); // Output: Ocorreu um erro: Usuário menor de idade, acesso negado.
  });