console.log("Iniciando agora.")

import { drawGrid, drawArrows} from "./draw.js";

let selectedCell;

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
canvas.addEventListener("click", handleClick);

function drawSelection() {
  if (!selectedCell) return;

  const { i, j } = selectedCell;

  const x = j * cellSize;
  const y = i * cellSize;

  ctx.fillStyle = "rgba(0, 150, 255, 0.3)";
  ctx.fillRect(x, y, cellSize, cellSize);
}

function handleClick(event) {
  const rect = canvas.getBoundingClientRect();

  const px = event.clientX - rect.left;
  const py = event.clientY - rect.top;

  const j = Math.floor(px / cellSize);
  const i = Math.floor(py / cellSize);

  selectedCell = { i, j };
}

// tamanho inicial
canvas.width = 400;
canvas.height = 400;

const rows = 5;
const cols = 5;
let cellSize = 80;

let directionOption = ["UP", "DOWN", "LEFT", "RIGHT"]
let grid = Array.from({ length: rows }, () =>
  Array.from({ length: cols }, () => ({
    direction: directionOption[Math.floor(Math.random() * 4)]
  }))
);

function loop() {
    //   update(); // lógica
    //   draw();   // desenho

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawGrid(rows, cols, cellSize, ctx);
  drawSelection();
  drawArrows(ctx, grid, cellSize);

  requestAnimationFrame(loop);
}

loop();

function update() {
  // aqui você atualiza animações
  if (animation) {
    animation.progress += 0.05;
  }
}




// task: importar resize.js e adicionar ele como módulo
// window.addEventListener("resize", resizeCanvas);
// resizeCanvas();