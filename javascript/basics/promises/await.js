// https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Operators/await

// O operador await é utilizado para esperar por uma Promise. Ele pode ser usado apenas dentro de uma async function.

// A expressão await faz a execução de uma função async pausar, para esperar pelo retorno da Promise, e resume a execução da função async quando o valor da Promise é resolvido. Ele então retorna o valor final da Promise. Se esse valor não for uma Promise, ele é convertido para uma Promise resolvida.

// Se a Promise for rejeitada, a expressão await invoca uma Exception com o valor rejeitado.

function resolveAfter2Seconds(x) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(x);
    }, 2000);
  });
}

async function f1() {
  var x = await resolveAfter2Seconds(10);
  console.log(x); // 10
}
f1();