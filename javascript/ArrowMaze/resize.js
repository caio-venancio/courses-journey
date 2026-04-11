function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  cellSize = Math.min(
    canvas.width / cols,
    canvas.height / rows
  );
}
