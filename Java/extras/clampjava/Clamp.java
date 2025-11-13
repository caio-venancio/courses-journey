public class Clamp {
    public static void main(String[] args){
        int vida = 120;

        vida = clamp(vida, 0, 100);
        System.out.println(vida);
    }

    public static int clamp(int valor, int min, int max){
        return Math.max(min, Math.min(max, valor));
    }
}