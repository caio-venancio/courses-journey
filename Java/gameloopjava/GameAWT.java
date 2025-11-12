import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferStrategy;

public class GameAWT extends Canvas implements Runnable {
  private JFrame frame;
  private volatile boolean running = true;

  // mundo simples
  private double xPrev, xCurr, vx = 100; // px/s
  private static final double DT = 1.0 / 60.0;
  private static final int W = 640, H = 360;

  public GameAWT() {
    frame = new JFrame("Game Loop Java");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setPreferredSize(new Dimension(W, H));
    frame.add(this);
    frame.pack();
    frame.setLocationRelativeTo(null);
    frame.setVisible(true);
    createBufferStrategy(3);
  }

  public void run() {
    long last = System.nanoTime();
    double acc = 0.0, NANO = 1_000_000_000.0;

    while (running) {
      long now = System.nanoTime();
      double frameTime = (now - last) / NANO;
      if (frameTime > 0.25) frameTime = 0.25;
      last = now;
      acc += frameTime;

      while (acc >= DT) {
        xPrev = xCurr;
        update(DT);
        acc -= DT;
      }
      double alpha = acc / DT;
      render(alpha);
      // opcional: limitar FPS com pequeno sleep
      try { Thread.sleep(1); } catch (InterruptedException ignored) {}
    }
  }

  private void update(double dt) {
    xCurr += vx * dt;
    if (xCurr < 0 || xCurr > W - 50) { // quica
      vx = -vx;
    }
  }

  private void render(double alpha) {
    BufferStrategy bs = getBufferStrategy();
    Graphics2D g = (Graphics2D) bs.getDrawGraphics();
    // fundo
    g.setColor(Color.DARK_GRAY);
    g.fillRect(0, 0, W, H);

    // interpola
    double x = xPrev + (xCurr - xPrev) * alpha;

    g.setColor(Color.CYAN);
    g.fillRect((int) Math.round(x), H/2 - 25, 50, 50);

    g.setColor(Color.WHITE);
    g.drawString("Fixed update + interpolação", 10, 20);

    g.dispose();
    bs.show();
    Toolkit.getDefaultToolkit().sync(); // ajuda em alguns sistemas
  }

  public static void main(String[] args) {
    GameAWT game = new GameAWT();
    new Thread(game, "game-loop").start();
  }
}
