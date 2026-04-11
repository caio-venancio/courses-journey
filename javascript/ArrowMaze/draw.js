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

function drawArrows(){}

function drawAnimation(){}