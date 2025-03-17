import sys
import os
from PyQt6.QtWidgets import QApplication
from Virli_241524062 import FlashcardApp

if __name__ == "__main__":
    # Create ./data directory if it doesn't exist yet
    os.makedirs("data", exist_ok=True)
    
    app = QApplication(sys.argv)
    window = FlashcardApp()
    window.show()
    sys.exit(app.exec())
