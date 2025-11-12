import java.util.Scanner;

public class PalindromeString {

    public static void main(String[] args){
        String str = "radar";
        Scanner scanner = new Scanner(System.in);
        System.out.println("Quer testar uma nova palavra? (enter - \"radar\"):  ");
        String input = scanner.nextLine();
         if (!input.isEmpty()) {
            str = input;
        }

        PalindromeString pn = new PalindromeString();
        if(pn.isPalindrome(str)){
            System.out.println("eh palindromo");
        } else {
            System.out.println("nao eh palindromo");
        }
        
        scanner.close();
    }

    public boolean isPalindrome(String original){
        int i = original.length()-1;
        int j = 0;
        while (i > j){
            if(original.charAt(i) != original.charAt(j)){
                return false;
            }
            i--;
            j++;
        }
        return true;
    }
}