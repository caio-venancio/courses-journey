export function drawGrid(rows, cols, cellSize, ctx) {
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const x = j * cellSize;
      const y = i * cellSize;

      ctx.strokeRect(x, y, cellSize, cellSize);
    }
  }
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  drawGrid();
  drawArrows();
  drawAnimation();
}

export function drawArrows(ctx, grid, cellSize) {
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      drawArrow(ctx, i, j, grid[i][j].direction, cellSize);
    }
  }
}

function drawArrow(ctx, i, j, direction, cellSize) {
  const x = j * cellSize;
  const y = i * cellSize;

  ctx.save();

  // move para o centro da célula
  ctx.translate(x + cellSize / 2, y + cellSize / 2);

  // define rotação
  let angle = 0;

  if (direction === "RIGHT") angle = 0;
  if (direction === "DOWN") angle = Math.PI / 2;
  if (direction === "LEFT") angle = Math.PI;
  if (direction === "UP") angle = -Math.PI / 2;

  ctx.rotate(angle);

  // desenha no centro
  drawArrowShape(ctx, 0, 0, cellSize);

  ctx.restore();
}

function drawArrowShape(ctx, x, y, size) {
  const center = size / 2;

  ctx.beginPath();

  // corpo (linha)
  ctx.moveTo(-center / 2, 0);
  ctx.lineTo(center / 2, 0);

  // ponta (triângulo)
  ctx.lineTo(center / 4, -center / 4);
  ctx.moveTo(center / 2, 0);
  ctx.lineTo(center / 4, center / 4);

  ctx.stroke();
}

function drawAnimation(){}