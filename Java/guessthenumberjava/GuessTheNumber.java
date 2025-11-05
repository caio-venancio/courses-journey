import java.util.Random;
import java.util.Scanner;

public class GuessTheNumber {
    public static void main(String[] args){
        //gerar número aleatório
        int number = new Random().nextInt(100); //número aleatório entre 0 e 100

        //iniciar contador
        int contador = 1;
        Scanner scanner = new Scanner(System.in);
        System.out.println("Digite seu palpite:  ");
        int answer = scanner.nextInt();

        //iniciar loop
        while (number != answer){
            contador++;

            if(answer < number){
                System.out.println("O número certo é maior!");
            } else {
                System.out.println("O número certo é menor!");
            }

            System.out.println("Digite seu palpite:  ");
            answer = scanner.nextInt();
        }

        System.out.println("Você acertou em " + contador + " tentativas!");
        scanner.close();
    }
}