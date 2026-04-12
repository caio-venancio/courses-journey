console.log("Iniciando agora.")

import { drawGrid, drawArrows, drawArrowShape} from "./draw.js";

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

let movingSquares = [];

function handleClick(event) {
  const rect = canvas.getBoundingClientRect();

  const px = event.clientX - rect.left;
  const py = event.clientY - rect.top;

  const j = Math.floor(px / cellSize);
  const i = Math.floor(py / cellSize);

  selectedCell = { i, j };

  const dir = grid[i][j].direction;

  const speed = 3;

  let dx = 0, dy = 0;

  if (dir === "RIGHT") dx = speed;
  if (dir === "LEFT") dx = -speed;
  if (dir === "DOWN") dy = speed;
  if (dir === "UP") dy = -speed;

  if(grid[i][j].active){
    movingSquares.push({
      x: j * cellSize,
      y: i * cellSize,
      dx,
      dy
    });
  }

  grid[i][j].active = false
}

// tamanho inicial
canvas.width = 600;
canvas.height = 600;

const rows = 5;
const cols = 5;
let cellSize = 80;

let directionOption = ["UP", "DOWN", "LEFT", "RIGHT"]
let grid = Array.from({ length: rows }, () =>
  Array.from({ length: cols }, () => ({
    direction: directionOption[Math.floor(Math.random() * 4)],
    active: true
  }))
);

function getAngle(dx, dy) {
  return Math.atan2(dy, dx);
}

function drawMovingSquares() {
  // ctx.fillStyle = "red";

  for (let s of movingSquares) {
    ctx.strokeRect(s.x, s.y, cellSize, cellSize);
    // ctx.fillRect(s.x, s.y, cellSize, cellSize);
    // 🏹 seta
    const angle = getAngle(s.dx, s.dy);

    ctx.save();

    // centro do quadrado
    ctx.translate(
      s.x + cellSize / 2,
      s.y + cellSize / 2
    );

    ctx.rotate(angle);

    ctx.fillStyle = "white";
    drawArrowShape(ctx, cellSize);

    ctx.restore();
  }
}

function loop() {
  update(); // lógica
  //   draw();   // desenho

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawGrid(rows, cols, grid, cellSize, ctx);
  drawSelection();
  drawArrows(ctx, grid, cellSize);
  drawMovingSquares();

  requestAnimationFrame(loop);
}

loop();

function update() {
  for (let square of movingSquares) {
    square.x += square.dx;
    square.y += square.dy;
  }

  // remover os que saíram da tela
  movingSquares = movingSquares.filter(s =>
    s.x + cellSize > 0 &&
    s.x < canvas.width &&
    s.y + cellSize > 0 &&
    s.y < canvas.height
  );
}




// task: importar resize.js e adicionar ele como módulo
// window.addEventListener("resize", resizeCanvas);
// resizeCanvas();