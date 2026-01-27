Sim, é perfeitamente normal e, muitas vezes, necessário e bom que uma classe dependa de outra no desenvolvimento de software orientado a objetos. Isso é conhecido como acoplamento. 

O objetivo não é eliminar dependências (o que tornaria o sistema um conjunto de partes isoladas), mas gerenciá-las para que o sistema seja flexível e fácil de manter. 

Aqui está uma análise detalhada:
Por que é Normal e Bom?
Modelagem de Domínio: No mundo real, os objetos interagem. Um Pedido depende de um Cliente. Uma ContaBancaria depende de um Cliente. Dependência reflete a vida real.
Reutilização de Código: Em vez de reescrever a funcionalidade de "calcular imposto" em todas as classes, a classe Pedido pode depender de uma classe CalculadoraImposto.
Organização e Coesão: Dependências permitem que você divida grandes responsabilidades em classes menores e mais focadas (alta coesão). 

Quando se torna Ruim (Acoplamento Forte)
Depender de outra classe torna-se um problema quando a dependência é muito direta e rígida, dificultando mudanças. Isso é chamado de alto acoplamento. 
Difícil de Testar: Se ClasseA depende diretamente de ClasseB, você não consegue testar A sem que B funcione perfeitamente.
Difícil de Alterar: Mudanças na ClasseB forçam alterações na ClasseA.
Fragilidade: Se você precisa alterar a forma como o Cliente é salvo, e a classe Pedido está "grudada" na lógica de banco de dados do cliente, tudo quebra. 

A Regra de Ouro: Dependa de Abstrações
A maneira "boa" de ter dependências é depender de interfaces ou classes abstratas, não de implementações concretas (o Princípio da Inversão de Dependência). 
Ruim (Acoplamento forte): Pedido depende diretamente de MySQLDatabase.
Bom (Baixo acoplamento): Pedido depende de uma interface IDatabase. Assim, você pode mudar o banco de dados sem alterar o Pedido.
Resumo

Característica	Dependência (Acoplamento)
Normal?	        Sim, todo sistema complexo possui.
Bom?	        Sim, se for baixo/fraco (interfases).
Ruim?	         Sim, se for alto/forte (classes concretas amarradas).

Em resumo: É essencial ter dependências, mas o ideal é que elas sejam "fracas", permitindo que você troque as peças sem quebrar o sistema todo.
