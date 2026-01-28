# Compila cada arquivo separadamente (-c)
g++ -c main.cpp -o main.o
g++ -c header.cpp -o header.o

# Liga os arquivos objeto para criar o executável
g++ main.o header.o -o programa
