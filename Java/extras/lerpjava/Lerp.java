// LERP — Linear Interpolation (Interpolação Linear)

public class Lerp {

    public static double lerp(double a, double b, double t) {
        return a + (b - a) * t;
    }
    
    public static void main(String args[]){
        double x = 0;     // posição inicial
        double target = 90; // posição final

        for (int i = 0; i <= 10; i++) {
            double t = i / 10.0;  // vai de 0 a 1
            double cur = lerp(x, target, t);
            System.out.println(cur);
        }
    }
}
