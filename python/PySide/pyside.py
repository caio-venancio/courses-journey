import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

# 1. Cria a aplicação (QApplication)
app = QApplication(sys.argv)

# 2. Cria o contêiner principal (janela)
window = QWidget()
window.setWindowTitle("Minha Primeira GUI")

# 3. Cria um layout e um widget (label)
layout = QVBoxLayout()
label = QLabel("Olá, PySide6!")
layout.addWidget(label)
window.setLayout(layout)

# 4. Exibe a janela
window.show()

# 5. Executa o loop de eventos
sys.exit(app.exec())
