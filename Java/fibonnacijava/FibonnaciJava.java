import java.util.Scanner;

public class FibonnaciJava {
    
    public static void main(String args[]){
        Scanner scanner = new Scanner(System.in);
        System.out.print("Digite algum posição de número da sequência de fibonnaci:  ");
        int pos = scanner.nextInt();
        scanner.close();

        FibonnaciJava fb = new FibonnaciJava();
        System.out.println(fb.fibbonacci(pos)); //não posso esquecer que fibonnaci só tem um 'b'
    }

    public int fibbonacci(int pos){
        if(pos == 0){
            return 0;
        } else if (pos == 1){
            return 1;
        } else if (pos == 2){
            return 1;
        }

        return fibbonacci(pos-1) + fibbonacci(pos-2);
    }
}
