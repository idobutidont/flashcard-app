from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QListWidget, QTextEdit,
    QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt6.QtCore import Qt

class FlashcardApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flashcard App Test")
        self.setGeometry(100, 100, 800, 500)

        # === Judul Bagian ===
        header_layout = QHBoxLayout()

        title_deck = QLabel("Flashcard Decks")
        title_deck.setStyleSheet("font-weight: bold; font-size: 16px;")

        title_main = QLabel("Flashcard Viewer")
        title_main.setStyleSheet("font-weight: bold; font-size: 16px;")
        title_main.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_notes = QLabel("Card Notes")
        title_notes.setStyleSheet("font-weight: bold; font-size: 16px;")

        header_layout.addWidget(title_deck, 2)
        header_layout.addWidget(title_main, 5)
        header_layout.addWidget(title_notes, 2)

        # === Layout utama ===
        main_layout = QHBoxLayout()

        # === Bagian Kiri (Flashcard Decks) ===
        deck_layout = QVBoxLayout()
        self.deck_list = QListWidget()
        self.btn_add_deck = QPushButton("Add New Deck")
        self.btn_delete_deck = QPushButton("Delete Deck")

        deck_layout.addWidget(self.deck_list)
        deck_layout.addWidget(self.btn_add_deck)
        deck_layout.addWidget(self.btn_delete_deck)

        # === Bagian Tengah (Tampilan Utama) ===
        flashcard_layout = QVBoxLayout()
        self.main_label = QLabel("No flashcard available.\nPlease create or select a deck.")
        self.main_label.setStyleSheet("font-size: 14px; color: gray;")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Tombol Navigasi Flashcard ===
        nav_layout = QHBoxLayout()
        self.btn_previous = QPushButton("Previous")
        self.btn_flip = QPushButton("Flip Card")
        self.btn_next = QPushButton("Next")

        nav_layout.addWidget(self.btn_previous)
        nav_layout.addWidget(self.btn_flip)
        nav_layout.addWidget(self.btn_next)

        # === Tombol Tambahan ===
        self.btn_add_card = QPushButton("Add New Flashcard")
        self.btn_manage_cards = QPushButton("Manage All Cards")

        flashcard_layout.addWidget(self.main_label)
        flashcard_layout.addLayout(nav_layout)
        flashcard_layout.addWidget(self.btn_add_card)
        flashcard_layout.addWidget(self.btn_manage_cards)

        # === Bagian Kanan (Card Notes) ===
        notes_layout = QVBoxLayout()
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText("Add your notes for this card here...")
        self.btn_save_notes = QPushButton("Save Notes")

        notes_layout.addWidget(self.notes_text)
        notes_layout.addWidget(self.btn_save_notes)

        # === Menggabungkan semua layout ke main_layout ===
        main_layout.addLayout(deck_layout, 2)
        main_layout.addLayout(flashcard_layout, 5)
        main_layout.addLayout(notes_layout, 2)

        # === Menggabungkan header dan main layout ===
        final_layout = QVBoxLayout()
        final_layout.addLayout(header_layout)  # Menambahkan header di atas
        final_layout.addLayout(main_layout)  # Menambahkan layout utama

        # === Membuat widget utama dan set layout ===
        container = QWidget()
        container.setLayout(final_layout)
        self.setCentralWidget(container)
