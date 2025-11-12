//algoritmo das 3 reversões
// Usa bem o cache, usa menos branches, não precisa checar borda, e quando k cresce o tempo não cresce

public class RotateArray {

    public static void rotateRight(int[] arr, int k) {
        int n = arr.length;
        // Garante que k está dentro dos limites do array
        k = k % n;

        if (k == 0) {
            return; // Nenhuma rotação necessária
        }

        // Inverte todo o array
        reverse(arr, 0, n - 1);
        // Inverte os primeiros k elementos
        reverse(arr, 0, k - 1);
        // Inverte os elementos restantes
        reverse(arr, k, n - 1);
    }

    public static void rotateLeft(int [] arr, int k) {
        int n = arr.length;
        // Garante que k está dentro dos limites do array
        k = k % n;

        if (k == 0) {
            return; // Nenhuma rotação necessária
        }

        reverse(arr, 0, k - 1);
        reverse(arr, k, n - 1);
        reverse(arr, 0, n - 1);
    }

    private static void reverse(int[] arr, int start, int end) {
        while (start < end) {
            int temp = arr[start];
            arr[start] = arr[end];
            arr[end] = temp;
            start++;
            end--;
        }
    }

    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        int k = 2;
        rotateRight(arr, k);
        // Imprime o array rotacionado: {4, 5, 1, 2, 3}
        System.out.println(java.util.Arrays.toString(arr));
        rotateLeft(arr, k);
        System.out.println(java.util.Arrays.toString(arr));
    }

}