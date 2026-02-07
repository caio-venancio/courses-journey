#tem que consertar
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

class MainWindow(QMainWindow):
    # To handle key press events, you need to create a custom class that inherits from a PySide6 widget (like QtWidgets.QWidget or QtWidgets.QMainWindow) and override the keyPressEvent method. 

    def keyPressEvent(self, event: QKeyEvent):
        # Verifica se Alt está pressionado
        print("event.modifiers():", event.modifiers())
        print("Qt.AltModifier:", Qt.AltModifier)
        if event.modifiers() & Qt.AltModifier:
            #The event.modifiers() function returns the keyboard modifiers (like Shift, Ctrl, Alt) that were active at the time an input event occurred. 
            #Qt.AltModifier is a enum that represents the Alt key on the keyboard being pressed.
            print("Tecla ALT pressionada junto com:", event.text())
        
        # Verifica se foi apenas a tecla ALT
        print("event.key():", event.key())
        print("Qt.key_Alt:", Qt.Key_Alt)
        if event.key() == Qt.Key_Alt:
            # the event.key() method in a QKeyEvent handler returns an integer value representing the specific key pressed - QtCore.Qt.Key enum. 
            print("Apenas ALT pressionado")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
