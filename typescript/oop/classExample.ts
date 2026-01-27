class Pessoa {
  // Propriedades (atributos) com tipagem
  public nome: string;
  private idade: number;

  // Construtor para inicializar o objeto
  constructor(nome: string, idade: number) {
    this.nome = nome;
    this.idade = idade;
  }

  // Método (comportamento)
  public apresentar(): string {
    return `Olá, meu nome é ${this.nome} e tenho ${this.idade} anos.`;
  }
}

// Criando uma instância (objeto) da classe
const pessoa1 = new Pessoa("Ana", 25);
console.log(pessoa1.apresentar()); // "Olá, meu nome é Ana e tenho 25 anos."