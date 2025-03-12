from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QListWidget, QTextEdit,
    QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt6.QtCore import Qt
import sys

# === Bagian Kiri (Flashcard Decks) ===
class DeckPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.deck_list = QListWidget()
        self.btn_add_deck = QPushButton("Add New Deck")
        self.btn_delete_deck = QPushButton("Delete Deck")
        
        layout.addWidget(self.deck_list)
        layout.addWidget(self.btn_add_deck)
        layout.addWidget(self.btn_delete_deck)
        
        self.setLayout(layout)

# === Bagian Tengah (Tampilan Flashcard) ===
class FlashcardViewer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.main_label = QLabel("No flashcard available.\nPlease create or select a deck.")
        self.main_label.setStyleSheet("font-size: 14px; color: gray;")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Tombol Navigasi Flashcard
        nav_layout = QHBoxLayout()
        self.btn_previous = QPushButton("Previous")
        self.btn_flip = QPushButton("Flip Card")
        self.btn_next = QPushButton("Next")
        
        nav_layout.addWidget(self.btn_previous)
        nav_layout.addWidget(self.btn_flip)
        nav_layout.addWidget(self.btn_next)
        
        self.btn_add_card = QPushButton("Add New Flashcard")
        self.btn_manage_cards = QPushButton("Manage All Cards")
        
        layout.addWidget(self.main_label)
        layout.addLayout(nav_layout)
        layout.addWidget(self.btn_add_card)
        layout.addWidget(self.btn_manage_cards)
        
        self.setLayout(layout)

# === Bagian Kanan (Notes Panel) ===
class NotesPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText("Add your notes for this card here...")
        self.btn_save_notes = QPushButton("Save Notes")
        
        layout.addWidget(self.notes_text)
        layout.addWidget(self.btn_save_notes)
        
        self.setLayout(layout)

# === Aplikasi Utama ===
class FlashcardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard App")
        self.setGeometry(100, 100, 800, 500)
        
        # Header
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
        
        # Layout utama
        main_layout = QHBoxLayout()
        
        self.deck_panel = DeckPanel()
        self.flashcard_viewer = FlashcardViewer()
        self.notes_panel = NotesPanel()
        
        main_layout.addWidget(self.deck_panel, 2)
        main_layout.addWidget(self.flashcard_viewer, 5)
        main_layout.addWidget(self.notes_panel, 2)
        
        # Final Layout
        final_layout = QVBoxLayout()
        final_layout.addLayout(header_layout)
        final_layout.addLayout(main_layout)
        
        container = QWidget()
        container.setLayout(final_layout)
        self.setCentralWidget(container)