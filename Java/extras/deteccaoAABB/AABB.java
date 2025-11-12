// Detecção de colisão AABB (Axis-Aligned Bounding Box)

public class AABB {
    static class Rect {
        double x, y, w, h;
        Rect(double x, double y, double w, double h) {
            this.x = x;
            this.y = y;
            this.w = w;
            this.h = h;
        }
    }

    public static boolean intersects(Rect a, Rect b) {
        return a.x < b.x + b.w &&
               a.x + a.w > b.x &&
               a.y < b.y + b.h &&
               a.y + a.h > b.y;
    }
    public static void main(String[] args){
        Rect player = new Rect(10, 10, 32, 32);
        Rect wall   = new Rect(30, 20, 50, 10);
        Rect far    = new Rect(200, 200, 10, 10);

        System.out.println("Player x Wall: " + intersects(player, wall)); // true
        System.out.println("Player x Far : " + intersects(player, far));  // false
    }
}
