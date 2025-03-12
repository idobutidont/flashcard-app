import os, json, uuid
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton)

# TODO: Proper Docstring


# Flashcard (Middle Panel)
class Flashcard:
    def __init__(self, front="", back="", notes="", id=None, right_count=0, wrong_count=0):
        """
        Initialize a new flashcard.
        """
        self.front = front
        self.back = back
        self.notes = notes
        self.id = id if id is not None else str(uuid.uuid4())
        self.right_count = right_count
        self.wrong_count = wrong_count
    
    def to_dict(self):
        """
        Store flashcard data as a dictionary.
        """
        return {
            "id": self.id,
            "front": self.front,
            "back": self.back,
            "notes": self.notes,
            "right_count": self.right_count,
            "wrong_count": self.wrong_count
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Load/parse flashcard data from a dictionary.
        """
        return cls(
            front=data.get("front", ""),
            back=data.get("back", ""),
            notes=data.get("notes", ""),
            id=data.get("id"),
            right_count=data.get("right_count", 0),
            wrong_count=data.get("wrong_count", 0)
        )


# Deck (Left Panel)
class Deck:
    def __init__(self, name, flashcards=None):
        """
        Initialize flashcard deck.
        """
        self.name = name
        self.flashcards = flashcards if flashcards else []
    
    def add_flashcard(self, front, back, notes=""):
        """
        
        """
        card = Flashcard(front, back, notes)
        self.flashcards.append(card)
        return card
    
    def remove_flashcard(self, card_id):
        """
        
        """
        self.flashcards = [card for card in self.flashcards if card.id != card_id]
    
    def get_flashcard(self, index):
        """
        
        """
        if 0 <= index < len(self.flashcards):
            return self.flashcards[index]
        return None
    
    def to_dict(self):
        """
        
        """
        return {
            "name": self.name,
            "flashcards": [card.to_dict() for card in self.flashcards]
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        
        """
        flashcards = [Flashcard.from_dict(card_data) for card_data in data.get("flashcards", [])]
        return cls(name=data.get("name", ""), flashcards=flashcards)


# Data Manager (stores json in txt)
class DataManager:
    def __init__(self, data_dir="data"):
        """
        
        """
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_deck(self, deck):
        """
        
        """
        deck_path = os.path.join(self.data_dir, f"{deck.name}.txt")
        with open(deck_path, 'w') as f:
            json.dump(deck.to_dict(), f, indent=2)
    
    def load_decks(self):
        """
        
        """
        decks = []
        if not os.path.exists(self.data_dir):
            return decks
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".txt"):
                deck_path = os.path.join(self.data_dir, filename)
                try:
                    with open(deck_path, 'r') as f:
                        deck_data = json.load(f)
                        deck = Deck.from_dict(deck_data)
                        decks.append(deck)
                except (json.JSONDecodeError, KeyError):
                    print(f"Error loading deck from {filename}")
        return decks
    
    def delete_deck(self, deck_name):
        """
        
        """
        deck_path = os.path.join(self.data_dir, f"{deck_name}.txt")
        if os.path.exists(deck_path):
            os.remove(deck_path)
            return True
        return False

# New Flashcard Window
class AddCardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Add New Flashcard")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Front of card
        layout.addWidget(QLabel("Front (Question):"))
        self.front_text = QTextEdit()
        self.front_text.setMaximumHeight(100)
        layout.addWidget(self.front_text)
        
        # Back of card
        layout.addWidget(QLabel("Back (Answer):"))
        self.back_text = QTextEdit()
        self.back_text.setMaximumHeight(100)
        layout.addWidget(self.back_text)
        
        # Predefined Notes
        layout.addWidget(QLabel("Notes (Optional):"))
        self.notes_text = QTextEdit()
        layout.addWidget(self.notes_text)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.add_btn = QPushButton("Add Card")
        self.add_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.add_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def get_card_data(self):
        return {
            "front": self.front_text.toPlainText(),
            "back": self.back_text.toPlainText(),
            "notes": self.notes_text.toPlainText()
        }
