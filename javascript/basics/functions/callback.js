//https://developer.mozilla.org/pt-BR/docs/Glossary/Callback_function
//Uma função callback é uma função passada a outra função como argumento, que é então invocado dentro da função externa para completar algum tipo de rotina ou ação.

function greeting(name) {
  console.log("Olá " + name);
}

function processUserInput(callback) {
  console.log("Por favor insira seu nome.");
  var name = "Usuário";
  callback(name);
}

processUserInput(greeting);