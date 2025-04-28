import sys
from PyQt6.QtWidgets import QApplication
from Virli_241524062 import FlashcardApp
from login import LoginWindow  


if __name__ == '__main__':
    app = QApplication(sys.argv)

    loginpage = LoginWindow()

    loginpage.show()
    app.setStyle("Fusion")
    app.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
    app.setStyleSheet("QLineEdit { background-color: #f0f0f0; }")
    app.setStyleSheet("QLabel { color: #333; }")
    app.setStyleSheet("QGridLayout { margin: 10px; }")
    window = FlashcardApp()
    window.setHidden(True)


    sys.exit(app.exec())
