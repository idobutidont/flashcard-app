from PyQt6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import Qt
from Virli_241524062 import Flashcard  # Import model Flashcard dari kode Virli

class FlashcardViewer(QWidget):
    def __init__(self):
        super().__init__()
        
        self.current_card = None  # Kartu yang sedang ditampilkan
        self.is_flipped = False   # Status apakah kartu sedang dalam posisi terbalik

        # Label untuk menampilkan kartu
        self.card_label = QLabel("No flashcard available.\nPlease select a deck.")
        self.card_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 20px;")

        # Tombol untuk membalik kartu
        self.flip_button = QPushButton("Flip Card")
        self.flip_button.clicked.connect(self.flip_card)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.card_label)
        layout.addWidget(self.flip_button)
        self.setLayout(layout)
    
    def display_card(self, card: Flashcard):
        """Menampilkan kartu yang dipilih."""
        self.current_card = card
        self.is_flipped = False
        self.update_display()
    
    def flip_card(self):
        """Membalik kartu antara sisi depan dan belakang."""
        if self.current_card:
            self.is_flipped = not self.is_flipped
            self.update_display()
    
    def update_display(self):
        """Memperbarui tampilan teks kartu."""
        if self.current_card:
            text = self.current_card.back if self.is_flipped else self.current_card.front
            self.card_label.setText(text)
        else:
            self.card_label.setText("No flashcard available.\nPlease select a deck.")
