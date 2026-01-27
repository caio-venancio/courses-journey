A resposta curta é: depende do contexto e da complexidade do seu projeto, mas a tendência moderna é colocar em arquivos separados apenas quando necessário para reuso ou organização. 

Aqui está uma análise detalhada baseada nas práticas atuais:

Quando definir no MESMO arquivo (Colocalização)
Se a interface (ou tipo) for usada apenas por uma classe ou componente, o melhor é mantê-la no mesmo arquivo. 
Vantagem: Facilita a manutenção. Quando você altera a lógica da classe, altera o tipo junto, sem abrir dois arquivos.
Exemplo: Componentes React (MyComponent.tsx contendo interface Props).
Regra geral: "Coisas que mudam juntas, ficam juntas".

Quando definir em um arquivo SEPARADO
Defina em um arquivo à parte (ex: IUsuario.ts, IService.cs) quando:
Reuso: A interface é compartilhada entre várias classes, componentes ou módulos.
API/Contrato: Você está definindo um contrato que será implementado por diferentes classes (injeção de dependência), facilitando testes (mocks).
Organização: O arquivo principal está ficando muito grande e poluído com definições de tipos. 
Vantagens da separação (Arquivos à parte)
Modularidade: Permite reutilizar contratos sem arrastar a implementação (código) junto.
Abstração: Facilita a substituição de implementações (ex: trocar um banco de dados real por um em memória durante testes). 

Resumo prático
Cenário 	Onde colocar?
Interface de Props/State de componente único    Mesmo arquivo (.tsx, .vue)
Interface de DTO (Data Transfer Object)	        Arquivo separado (modelos)
Contrato de um Service/Repository	            Arquivo separado (camada de domínio)
Tipos genéricos de uso global	                Arquivo types.ts ou pasta types/

Em projetos modernos (TypeScript/React/etc.), a tendência é evitar a "arquivite" (criar muitos arquivos pequenos) e colocalizar tipos a menos que eles precisem ser compartilhados. 