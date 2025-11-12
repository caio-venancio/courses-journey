Que outras aplicações tem algoritmos específico (jogo tem gameloop por exemplo)?

Ótima pergunta — e a resposta é muito rica 👏
Assim como jogos têm o game loop, várias áreas de computação têm algoritmos característicos, tão importantes que praticamente definem como aqueles sistemas funcionam.

Aqui vai uma lista bem clara e organizada por domínio, com exemplos concretos de algoritmos específicos de cada área:

🖼️ 1. Processamento de Imagem / Foto / Vídeo

✔ Algoritmos específicos da área:

Filtro de convolução (blur, sharpen, edge-detection)

Demosaicing (reconstrução do padrão Bayer da câmera)

Compressão JPEG (DCT + quantização)

Detecção de bordas Canny

Equalização de histograma

EXIF parsing e normalização de orientação

Interpolação bilinear/bicúbica

Optical flow (Lucas–Kanade)

🔍 Aplicação: câmeras, editores de imagem, OpenCV.

🎮 2. Jogos

✔ Algoritmos fundamentais:

Game Loop (update + render)

A* (pathfinding)

Detecção de colisão (AABB, SAT)

Flocking / Steering behaviors

QuadTree / Octree (particionamento espacial)

Interpolação (lerp, easing)

Verlet Integration / Euler Integration

🔍 Aplicação: físicas, IA, animações, engines.

🧠 3. Inteligência Artificial / Machine Learning

✔ Algoritmos “assinatura”:

Gradiente descendente

Backpropagation (redes neurais)

k-means

SVM (margem máxima)

Random Forest / Decision Trees

PCA (redução de dimensionalidade)

Algoritmos genéticos

🔍 Aplicação: aprendizado, classificação, visão computacional.

🌐 4. Redes / Internet / Protocolos

✔ Usados constantemente:

Algoritmo de roteamento Dijkstra / Bellman–Ford

CSMA/CD (Ethernet)

Sliding Window / Go-Back-N (TCP/IP)

Checksum e CRC

DNS resolution

🔍 Aplicação: roteadores, protocolos, sistemas distribuídos.

💾 5. Bancos de Dados

✔ Algoritmos de alto impacto:

B-Tree / B+Tree (índices)

Hashing extensível / linear hashing

Algoritmos de Join (Nest-Loop, Merge-Join, Hash-Join)

Two-Phase Commit

Algoritmos de lock (MVCC, 2PL)

Algoritmos de recuperação (Write-Ahead Logging)

🔍 Aplicação: PostgreSQL, MySQL, Oracle, SQLite.

🖥️ 6. Sistemas Operacionais

✔ Algoritmos essenciais:

Escalonamento de CPU (Round Robin, SJF, Priority)

Page Replacement (LRU, Clock, Optimal)

Semaphore / Mutex / Monitor

Algoritmos de thread scheduling

Deadlock detection / avoidance (Banco de Dados de Recursos)

🔍 Aplicação: kernel, multitarefa, gerenciamento de memória.

📂 7. Sistemas de Arquivos

✔ Muito específicos da área:

FAT / NTFS cluster allocation

Journaling (ext4, NTFS)

Inodes + árvore de diretórios

Algoritmo de compactação zlib/deflate

Deduplicação por “content hashing”

🔍 Aplicação: Linux, Windows, discos, SSDs.

🔐 8. Criptografia / Segurança

✔ Algoritmos padrão:

AES, DES, ChaCha20

RSA, ECC

SHA-256, SHA-3

Diffie–Hellman (troca de chaves)

HMAC

PBKDF2 / Argon2 (hash de senha)

🔍 Aplicação: autenticação, HTTPS, assinatura digital.

📡 9. Geolocalização / Mapas

✔ Algoritmos próprios da área:

Haversine (distância geográfica)

R-tree (índice espacial)

Map matching (GPS → rua)

Quadkey (tiles de mapas)

A* com heurística geográfica

🔍 Aplicação: Google Maps, Waze, GIS.

🎧 10. Áudio / Sinal

✔ Muito específicos:

FFT (Transformada Rápida de Fourier)

Filtro digital FIR/IIR

Pitch shifting / time stretching (phase vocoder)

Algoritmo de compressão MP3 / AAC

🔍 Aplicação: mixers, equalizadores, players, DSP.

🧩 11. Compiladores e Linguagens

✔ Algoritmos essenciais:

Lexing (DFA)

Parsing (LL/LR, Earley)

Algoritmo de escopo e resolução de variáveis

AST construction

Register allocation (graph coloring)

🔍 Aplicação: GCC, JVM, Python, Swift, etc.

🚀 12. Computação gráfica 2D/3D

✔ Algoritmos estruturais:

Bresenham (linha/polígono)

Rasterização de triângulos

Z-buffer

Phong / Blinn-Phong shading

Ray tracing

Marching cubes

🔍 Aplicação: motores 3D, CAD, renderização.

Outras referências:
desenvolvimento web,
backend Java,
data science,
mobile,
sistemas embarcados,
engines de jogos,