<!-- GPT -->
# Game Loop

É um laço ininito que roda enquanto o jogo está aberto, responsável por:
1. Ler inputs
2. Atualizar estado do jogo
3. Renderizar
4. Controlar o tempo

A estrutura básica seria o seguinte:
```
while (running) {

    processInput();
    update(deltaTime);
    render();
}
```

### O que é deltaTime?

É o tempo (em segundos ou ms) entre um frame e outro.

Sem delta time, PCs rápidos andam rápido e PCs lentos andam devagar
Com delta time, o movimento é igual independente da quantidade de loops

### 4 modelos

1) Game Loop Simples (sem delta time)
2) Game Loop com delta time (Modelo fixo do Quake)
3) Game Loop com UPDATE FIXO e RENDER VARIÁVEL (modelo de física do Unity / Box2D)
4) Game Loop com interpolação (modelo usado em engines AAA)