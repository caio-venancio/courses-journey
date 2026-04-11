console.log("Iniciando agora.")

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// tamanho inicial
canvas.width = 400;
canvas.height = 400;

const rows = 5;
const cols = 5;
const cellSize = 80;

function drawGrid() {
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const x = j * cellSize;
      const y = i * cellSize;

      ctx.strokeRect(x, y, cellSize, cellSize);
    }
  }
}

function loop() {
    //   update(); // lógica
    //   draw();   // desenho

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawGrid();
  //   drawArrows();

  //   requestAnimationFrame(loop);

  requestAnimationFrame(loop);
}

loop();

function update() {
  // aqui você atualiza animações
  if (animation) {
    animation.progress += 0.05;
  }
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawGrid();
  drawArrows();
  drawAnimation();
}

function drawArrows(){}
function drawAnimation(){}

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  cellSize = Math.min(
    canvas.width / cols,
    canvas.height / rows
  );
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();