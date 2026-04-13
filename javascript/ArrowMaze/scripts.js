console.log("Iniciando agora.")

import { drawGrid, drawArrows, drawArrowShape, getLineBlocking} from "./draw.js";

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

// tamanho inicial
canvas.width = 600;
canvas.height = 600;
const rows = 5;
const cols = 5;
let cellSize = 80;
// para o tempo
let startTime = null;
let elapsedTime = 0;
let gameRunning = false;
// para a quantidade de jogadas
let moves = 0;

function handleClick(event) {
  if (!gameRunning) return;

  
  const rect = canvas.getBoundingClientRect();

  const px = event.clientX - rect.left;
  const py = event.clientY - rect.top;

  const j = Math.floor(px / cellSize);
  const i = Math.floor(py / cellSize);

  selectedCell = { i, j };
  moves++;

  const dir = grid[i][j].direction;

  const speed = 3;

  let dx = 0, dy = 0;

  if (dir === "RIGHT") dx = speed;
  if (dir === "LEFT") dx = -speed;
  if (dir === "DOWN") dy = speed;
  if (dir === "UP") dy = -speed;

  if(getLineBlocking(i,j,rows,cols,grid)){
    // TriggerShake()
  } else if(grid[i][j].active){
    movingSquares.push({
      x: j * cellSize,
      y: i * cellSize,
      dx,
      dy
    });
    grid[i][j].active = false
  }

}

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

function loop(time) {
  update(time); // lógica
  //   draw();   // desenho

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawGrid(rows, cols, grid, cellSize, ctx);
  drawSelection();
  drawArrows(ctx, grid, cellSize);
  drawMovingSquares();
  drawUI();
  drawEndScreen();

  requestAnimationFrame(loop);
}

requestAnimationFrame(loop);
// loop();

if (!gameRunning) startGame();

function update(time) {
  if (gameRunning) {
    elapsedTime = time - startTime;
  }

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

function startGame() {
  startTime = performance.now();
  gameRunning = true;
}

function drawUI() {
  const seconds = (elapsedTime / 1000).toFixed(2);
  ctx.fillText(`Tempo: ${seconds}s`, 10, 20);

  ctx.fillText(`Jogadas: ${moves}`, 10, 40);
}

function isGameFinished() {
  return grid.every(row =>
    row.every(cell => !cell.active)
  );
}

function endGame() {
  gameRunning = false;
}

function calculateScore() {
  const timeScore = Math.max(0, 1000 - elapsedTime / 10);
  const moveScore = Math.max(0, 500 - moves * 10);

  return Math.floor(timeScore + moveScore);
}

function drawEndScreen() {
  if (gameRunning) return;

  ctx.fillStyle = "black";
  ctx.fillText("Fim de jogo!", 150, 150);

  const score = calculateScore();

  ctx.fillText(`Score: ${score}`, 150, 180);
}


// task: importar resize.js e adicionar ele como módulo
// window.addEventListener("resize", resizeCanvas);
// resizeCanvas();