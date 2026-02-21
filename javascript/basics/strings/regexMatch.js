let texto = `
**Pergunta baseada na página 67 (ou 37)
Quais etapas genéricas de um pipeline de NLP?**
`
const regex = /\*\*Pergunta.*?\n([\s\S]*?)\*\*/;
const match = texto.match(regex);

if (match) {
  console.log(match[1]); // CONTEUDO_AQUI
}