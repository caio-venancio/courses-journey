//dd-mm-aaaa
str = ".todo-16112025.txt"

const regex = /(\d{2})(\d{2})(\d{4})/; // Padrão mais específico para "dd de mês de yyyy"

const correspondencia = str.match(regex);

console.log(correspondencia[0])