import sys
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QListWidget,
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt6.QtCore import Qt
from 241524056 import FlashcardAppAnjay


class FlashcardApp(QMainWindow):
    def __init__(self):  
        super().__init__()
        self.setWindowTitle("Flashcard App")
        self.setGeometry(100, 100, 800, 500)

        # Struktur Data
        self.decks = []
        self.current_deck = None
        self.current_index = 0
        self.load_data()

        # === Layout Header ===
        header_layout = QHBoxLayout()
        title_deck = QLabel("Flashcard Decks")
        title_main = QLabel("Deck: -")
        title_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_notes = QLabel("Card Notes")
        
        header_layout.addWidget(title_deck, 2)
        header_layout.addWidget(title_main, 5)
        header_layout.addWidget(title_notes, 2)

        # === Layout Utama ===
        main_layout = QHBoxLayout()

        # === Sidebar Kiri (Decks) ===
        deck_layout = QVBoxLayout()
        self.deck_list = QListWidget()
        self.deck_list.itemClicked.connect(self.select_deck)
        self.btn_add_deck = QPushButton("Add New Deck")
        self.btn_delete_deck = QPushButton("Delete Deck")
        
        deck_layout.addWidget(self.deck_list)
        deck_layout.addWidget(self.btn_add_deck)
        deck_layout.addWidget(self.btn_delete_deck)

        # === Tampilan Flashcard Tengah ===
        self.flashcard_label = QLabel("Select a deck to start.")
        self.flashcard_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        

        def show_anjay_window(self):
            self.anjay_window = FlashcardAppAnjay()
            self.anjay_window.show()

        self.btn_prev = QPushButton("Previous")
        self.btn_flip = QPushButton("Flip Card")
        self.btn_next = QPushButton("Next")
        
        self.btn_prev.clicked.connect(self.previous_card)
        self.btn_flip.clicked.connect(self.flip_card)
        self.btn_next.clicked.connect(self.next_card)

        flashcard_layout = QVBoxLayout()
        flashcard_layout.addWidget(self.flashcard_label)
        flashcard_layout.addWidget(self.btn_prev)
        flashcard_layout.addWidget(self.btn_flip)
        flashcard_layout.addWidget(self.btn_next)

        # === Sidebar Kanan (Catatan) ===
        notes_layout = QVBoxLayout()
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText("Add your notes here...")
        self.btn_save_notes = QPushButton("Save Notes")
        
        notes_layout.addWidget(self.notes_text)
        notes_layout.addWidget(self.btn_save_notes)

        # Gabungkan layout utama
        main_layout.addLayout(deck_layout, 2)
        main_layout.addLayout(flashcard_layout, 5)
        main_layout.addLayout(notes_layout, 2)

        # Layout final
        final_layout = QVBoxLayout()
        final_layout.addLayout(header_layout)
        final_layout.addLayout(main_layout)

        container = QWidget()
        container.setLayout(final_layout)
        self.setCentralWidget(container)

        # Tampilkan deck yang tersedia
        self.update_deck_list()

    def load_data(self):
        """Memuat data dari file JSON."""
        if os.path.exists("flashcards.json"):
            with open("flashcards.json", "r") as file:
                data = json.load(file)
                self.decks = [Deck.from_dict(deck) for deck in data]

    def save_data(self):
        """Menyimpan data ke file JSON."""
        with open("flashcards.json", "w") as file:
            json.dump([deck.to_dict() for deck in self.decks], file, indent=4)

    def update_deck_list(self):
        """Menampilkan daftar deck di sidebar."""
        self.deck_list.clear()
        for deck in self.decks:
            self.deck_list.addItem(deck.name)

    def select_deck(self, item):
        """Memilih deck dan menampilkan kartu pertama."""
        for deck in self.decks:
            if deck.name == item.text():
                self.current_deck = deck
                self.current_index = 0
                self.show_card()
                break

    def show_card(self):
        """Menampilkan kartu saat ini."""
        if self.current_deck and self.current_deck.flashcards:
            card = self.current_deck.flashcards[self.current_index]
            self.flashcard_label.setText(card.question)
        else:
            self.flashcard_label.setText("No flashcards available.")

    def flip_card(self):
        """Membalik kartu antara pertanyaan dan jawaban."""
        if self.current_deck and self.current_deck.flashcards:
            card = self.current_deck.flashcards[self.current_index]
            if self.flashcard_label.text() == card.question:
                self.flashcard_label.setText(card.answer)
            else:
                self.flashcard_label.setText(card.question)

    def previous_card(self):
        """Navigasi ke kartu sebelumnya."""
        if self.current_deck and self.current_index > 0:
            self.current_index -= 1
            self.show_card()

    def next_card(self):
        """Navigasi ke kartu berikutnya."""
        if self.current_deck and self.current_index < len(self.current_deck.flashcards) - 1:
            self.current_index += 1
            self.show_card()

# === Menjalankan Aplikasi ===
if __name__ == "__main__":  
    app = QApplication(sys.argv)
    window = FlashcardApp()
    window.show()
    sys.exit(app.exec())