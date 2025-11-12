import java.util.Scanner;
import java.util.Stack;

public class ValidarParenteses {

    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        System.out.print("Digite texto para testar parênteses:  ");
        String teste = scanner.nextLine();
        scanner.close();

        Stack<Character> myStack = new Stack<>();

        for(int i = 0; i< teste.length(); i++){
            if(teste.charAt(i) == '('){
                myStack.push(teste.charAt(i) );
            } else if (teste.charAt(i) == ')'){
                if(myStack.isEmpty()){
                    System.out.println("Ordem incorreta (fecha sem abrir)");
                    return;
                }
                myStack.pop();
            }
        }

        if(myStack.isEmpty()) System.out.println("Ordem correta");
        else System.out.println("Ordem incorreta");
    }

    
}
