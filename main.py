import sys
from PyQt6.QtWidgets import QApplication
from Virli_241524062 import FlashcardApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlashcardApp()
    window.show()
    sys.exit(app.exec())
