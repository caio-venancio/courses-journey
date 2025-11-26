public class QuickSort {

    public static void quickSort(int[] arr, int inicio, int fim) {
        if (inicio < fim) {
            int p = partition(arr, inicio, fim); // índice do pivô após particionar
            quickSort(arr, inicio, p - 1);       // lado esquerdo
            quickSort(arr, p + 1, fim);          // lado direito
        }
    }

    private static int partition(int[] arr, int inicio, int fim) {
        int pivot = arr[fim];       // pivô = último elemento
        int i = inicio - 1;         // posição do menor elemento

        for (int j = inicio; j < fim; j++) {
            if (arr[j] <= pivot) {  // se o elemento atual é menor que o pivô
                i++;
                swap(arr, i, j);    // troca
            }
        }

        // coloca o pivô na posição correta
        swap(arr, i + 1, fim);

        return i + 1; // retorna o índice do pivô
    }

    private static void swap(int[] arr, int i, int j) {
        int aux = arr[i];
        arr[i] = arr[j];
        arr[j] = aux;
    }

    public static void main(String[] args) {
        int[] vetor = { 10, 7, 8, 9, 1, 5 };
        quickSort(vetor, 0, vetor.length - 1);

        for (int num : vetor) {
            System.out.print(num + " ");
        }
    }
}
