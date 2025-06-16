import os, json, uuid, hashlib
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTextEdit, QPushButton, QListWidget, QListWidgetItem, 
                             QMessageBox, QFormLayout, QLineEdit, QGroupBox)
from PyQt6.QtCore import Qt
from Lukman_241524050 import ImageHandler, ImageResizeDialog

# User Management System
class UserManager:
    def __init__(self):
        self.users_file = "data/users.json"
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.users = self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_users(self):
        """Save users to JSON file"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password):
        """Register a new user"""
        # Validate username - must be at least 5 characters for compatibility with login.py
        if len(username) < 5:
            return False, "Username must be at least 5 characters long"
        
        if username in self.users:
            return False, "Username already exists"
        
        # Validate password - complex validation for compatibility with login.py
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if ' ' in password:
            return False, "Password cannot contain spaces"
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()-_=+[]{};:',.<>?/\\|`~" for c in password)
        
        if not (has_upper and has_lower and has_digit and has_special):
            return False, "Password must contain uppercase, lowercase, digit, and special character"
        
        # Create user
        self.users[username] = {
            "password": self.hash_password(password),
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        self.save_users()
        return True, "User registered successfully"
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        if username not in self.users:
            return False, "Username not found"
        
        if self.users[username]["password"] != self.hash_password(password):
            return False, "Incorrect password"
        
        # Update last login
        self.users[username]["last_login"] = datetime.now().isoformat()
        self.save_users()
        return True, "Login successful"
    
    def get_user_info(self, username):
        """Get user information"""
        if username in self.users:
            return self.users[username]
        return None


# Flashcard (Middle Panel)
class Flashcard:
    def __init__(self, front="", back="", notes="", id=None, right_count=0, wrong_count=0, difficulty=1, retention_score=0.0, last_reviewed=None, next_review=None):
        """
        Initialize a new flashcard.
        """
        self.front = front
        self.back = back
        self.notes = notes
        self.id = id if id is not None else str(uuid.uuid4())
        self.right_count = right_count
        self.wrong_count = wrong_count
        self.difficulty = difficulty
        self.retention_score = retention_score
        self.last_reviewed = last_reviewed if last_reviewed else datetime.now().isoformat()
        self.next_review = next_review if next_review else datetime.now().isoformat()


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
            "wrong_count": self.wrong_count,
            "difficulty": self.difficulty,
            "retention_score": self.retention_score,
            "last_reviewed": self.last_reviewed,
            "next_review": self.next_review, 
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
            wrong_count=data.get("wrong_count", 0),
            difficulty=data.get("difficulty", 1),
            retention_score=data.get("retention_score", 0.0),
            last_reviewed=data.get("last_reviewed", datetime.now().isoformat()),
            next_review=data.get("next_review", datetime.now().isoformat()),
        )


# Deck (Left Panel)
class Deck:
    def __init__(self, name, study_time=0, flashcards=None):
        """
        Initialize flashcard deck.
        """
        self.name = name
        self.study_time = study_time
        self.flashcards = flashcards if flashcards else []
    
    def add_flashcard(self, front, back, notes=""):
        card = Flashcard(front, back, notes)
        self.flashcards.append(card)
        return card
    
    def remove_flashcard(self, card_id):
        self.flashcards = [card for card in self.flashcards if card.id != card_id]
    
    def get_flashcard(self, index):
        if 0 <= index < len(self.flashcards):
            return self.flashcards[index]
        return None
    
    def to_dict(self):
        return {
            "name": self.name,
            "study_time": self.study_time,
            "flashcards": [card.to_dict() for card in self.flashcards]
        }
    
    @classmethod
    def from_dict(cls, data):
        flashcards = [Flashcard.from_dict(card_data) for card_data in data.get("flashcards", [])]
        return cls(name=data.get("name", ""), study_time=data.get("study_time", ""), flashcards=flashcards)


# Data Manager (stores json in txt)
class DataManager:
    def __init__(self, username=None):
        """
        Initialize DataManager for a specific user.
        If username is None, uses default behavior for backward compatibility.
        """
        self.username = username
        self.data_dir = "./data/userdata" if username else "data"
        
        if username:
            # Ensure user data directory exists
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
        else:
            # Backward compatibility
            os.makedirs(self.data_dir, exist_ok=True)
    
    def get_user_file_path(self, deck_name):
        """Get the file path for a deck, considering multi-user setup"""
        if self.username:
            return os.path.join(self.data_dir, f"{self.username}_{deck_name}.txt")
        else:
            return os.path.join(self.data_dir, f"{deck_name}.txt")
    
    def save_deck(self, deck):
        """Save a deck to file"""
        deck_path = self.get_user_file_path(deck.name)
        with open(deck_path, 'w', encoding='utf-8') as f:
            json.dump(deck.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load_decks(self):
        """Load all decks for the current user"""
        decks = []
        if not os.path.exists(self.data_dir):
            return decks
        
        # Get appropriate file prefix
        prefix = f"{self.username}_" if self.username else ""
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".txt"):
                # For multi-user, only load files that belong to this user
                if self.username and not filename.startswith(prefix):
                    continue
                
                deck_path = os.path.join(self.data_dir, filename)
                try:
                    with open(deck_path, 'r', encoding='utf-8') as f:
                        deck_data = json.load(f)
                        deck = Deck.from_dict(deck_data)
                        decks.append(deck)
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error loading deck from {filename}: {e}")
        return decks
    
    def delete_deck(self, deck_name):
        """Delete a deck file"""
        deck_path = self.get_user_file_path(deck_name)
        if os.path.exists(deck_path):
            os.remove(deck_path)
            return True
        return False
    
    def get_user_stats(self):
        """Get statistics for the current user"""
        decks = self.load_decks()
        total_decks = len(decks)
        total_cards = sum(len(deck.flashcards) for deck in decks)
        total_study_time = sum(deck.study_time for deck in decks)
        
        return {
            "username": self.username,
            "total_decks": total_decks,
            "total_cards": total_cards,
            "total_study_time": total_study_time
        }


# New Flashcard Window
class AddCardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_difficulty = 1
        self.difficulty_buttons = []
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Add New Flashcard")
        self.setMinimumWidth(600)
        
        layout = QVBoxLayout()
        
        # Front of card
        front_group = QGroupBox("Front (Question)")
        front_layout = QVBoxLayout()
        self.front_text = QTextEdit()
        self.front_text.setMaximumHeight(100)
        self.front_text.setAcceptRichText(True)
        self.insert_front_image_btn = QPushButton("Insert Image")
        self.insert_front_image_btn.clicked.connect(lambda: self.insert_image(self.front_text))
        front_layout.addWidget(self.front_text)
        front_layout.addWidget(self.insert_front_image_btn)
        front_group.setLayout(front_layout)
        layout.addWidget(front_group)
        
        # Back of card
        back_group = QGroupBox("Back (Answer)")
        back_layout = QVBoxLayout()
        self.back_text = QTextEdit()
        self.back_text.setMaximumHeight(100)
        self.back_text.setAcceptRichText(True)
        self.insert_back_image_btn = QPushButton("Insert Image")
        self.insert_back_image_btn.clicked.connect(lambda: self.insert_image(self.back_text))
        back_layout.addWidget(self.back_text)
        back_layout.addWidget(self.insert_back_image_btn)
        back_group.setLayout(back_layout)
        layout.addWidget(back_group)
        
        # Pre-defined Notes (optional) if the user wants it beforehand
        notes_group = QGroupBox("Notes (Optional)")
        notes_layout = QVBoxLayout()
        self.notes_text = QTextEdit()
        self.notes_text.setAcceptRichText(True)
        self.insert_notes_image_btn = QPushButton("Insert Image")
        self.insert_notes_image_btn.clicked.connect(lambda: self.insert_image(self.notes_text))
        notes_layout.addWidget(self.notes_text)
        notes_layout.addWidget(self.insert_notes_image_btn)
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        # Difficulty rating
        layout.addWidget(QLabel("Difficulty (1=Easy, 5=Hard):"))
        difficulty_layout = QHBoxLayout()
        for i in range(1, 6):
            btn = QPushButton(str(i))
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    border-radius: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:checked {
                    background-color: #3498db;
                    color: white;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self.select_difficulty(idx))
            self.difficulty_buttons.append(btn)
            difficulty_layout.addWidget(btn)
        self.difficulty_buttons[0].setChecked(True)  # Default to 1
        layout.addLayout(difficulty_layout)
        
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

    def insert_image(self, text_edit):
        image = ImageHandler.load_image_from_file(self)
        if image:
            # Resize dialog
            dialog = ImageResizeDialog(image.width(), image.height(), self)
            if dialog.exec():
                new_width, new_height = dialog.get_new_size()
                resized_image = ImageHandler.resize_image(image, new_width, new_height)
                
                # Convert to base64 for storage
                base64_str = ImageHandler.image_to_base64(resized_image)
                
                # Insert into text edit
                cursor = text_edit.textCursor()
                cursor.insertHtml(f'<img src="data:image/png;base64,{base64_str}">')
                text_edit.setTextCursor(cursor)

    def select_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
        for btn in self.difficulty_buttons:
            btn.setChecked(False)
        self.difficulty_buttons[difficulty-1].setChecked(True)
    
    def get_card_data(self):
        return {
            "front": self.front_text.toHtml(),
            "back": self.back_text.toHtml(),
            "notes": self.notes_text.toHtml(),
            "difficulty": self.selected_difficulty
        }


# Edit Card Window
class EditCardDialog(QDialog):
    def __init__(self, card, parent=None):
        super().__init__(parent)
        self.card = card
        self.selected_difficulty = card.difficulty
        self.difficulty_buttons = []
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Edit Flashcard")
        self.setMinimumWidth(600)
        
        layout = QVBoxLayout()
        
        # Front of card
        front_group = QGroupBox("Front (Question)")
        front_layout = QVBoxLayout()
        self.front_text = QTextEdit()
        self.front_text.setMaximumHeight(100)
        self.front_text.setAcceptRichText(True)
        self.front_text.setHtml(self.card.front)
        self.insert_front_image_btn = QPushButton("Insert Image")
        self.insert_front_image_btn.clicked.connect(lambda: self.insert_image(self.front_text))
        front_layout.addWidget(self.front_text)
        front_layout.addWidget(self.insert_front_image_btn)
        front_group.setLayout(front_layout)
        layout.addWidget(front_group)
        
        # Back of card
        back_group = QGroupBox("Back (Answer)")
        back_layout = QVBoxLayout()
        self.back_text = QTextEdit()
        self.back_text.setMaximumHeight(100)
        self.back_text.setAcceptRichText(True)
        self.back_text.setHtml(self.card.back)
        self.insert_back_image_btn = QPushButton("Insert Image")
        self.insert_back_image_btn.clicked.connect(lambda: self.insert_image(self.back_text))
        back_layout.addWidget(self.back_text)
        back_layout.addWidget(self.insert_back_image_btn)
        back_group.setLayout(back_layout)
        layout.addWidget(back_group)
        
        # Notes
        notes_group = QGroupBox("Notes (Optional)")
        notes_layout = QVBoxLayout()
        self.notes_text = QTextEdit()
        self.notes_text.setAcceptRichText(True)
        self.notes_text.setHtml(self.card.notes)
        self.insert_notes_image_btn = QPushButton("Insert Image")
        self.insert_notes_image_btn.clicked.connect(lambda: self.insert_image(self.notes_text))
        notes_layout.addWidget(self.notes_text)
        notes_layout.addWidget(self.insert_notes_image_btn)
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        # Difficulty rating
        layout.addWidget(QLabel("Difficulty (1=Easy, 5=Hard):"))
        difficulty_layout = QHBoxLayout()
        for i in range(1, 6):
            btn = QPushButton(str(i))
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    border-radius: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:checked {
                    background-color: #3498db;
                    color: white;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self.select_difficulty(idx))
            self.difficulty_buttons.append(btn)
            difficulty_layout.addWidget(btn)
        self.difficulty_buttons[self.card.difficulty-1].setChecked(True)
        layout.addLayout(difficulty_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def insert_image(self, text_edit):
        """Insert image into the specified text edit"""
        image = ImageHandler.load_image_from_file(self)
        if image:
            # Resize dialog
            dialog = ImageResizeDialog(image.width(), image.height(), self)
            if dialog.exec():
                new_width, new_height = dialog.get_new_size()
                resized_image = ImageHandler.resize_image(image, new_width, new_height)
                
                # Convert to base64 for storage
                base64_str = ImageHandler.image_to_base64(resized_image)
                
                # Insert into text edit
                cursor = text_edit.textCursor()
                cursor.insertHtml(f'<img src="data:image/png;base64,{base64_str}">')
                text_edit.setTextCursor(cursor)

    def select_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
        for btn in self.difficulty_buttons:
            btn.setChecked(False)
        self.difficulty_buttons[difficulty-1].setChecked(True)
    
    def get_card_data(self):
        return {
            "front": self.front_text.toHtml(),
            "back": self.back_text.toHtml(),
            "notes": self.notes_text.toHtml(),
            "difficulty": self.selected_difficulty
        }


# Card Manager Window
class ManageCardsDialog(QDialog):
    def __init__(self, deck, parent=None):
        super().__init__(parent)
        self.deck = deck
        self.init_ui()
        self.populate_cards()
        
    def init_ui(self):
        self.setWindowTitle(f"Manage Flashcards - {self.deck.name}")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel(f"Flashcards in deck: {self.deck.name}")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header_label)
        
        # Card list
        self.card_list = QListWidget()
        self.card_list.setAlternatingRowColors(True)
        layout.addWidget(self.card_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add New Card")
        self.add_btn.clicked.connect(self.add_card)
        
        self.edit_btn = QPushButton("Edit Selected Card")
        self.edit_btn.clicked.connect(self.edit_card)
        
        self.delete_btn = QPushButton("Delete Selected Card")
        self.delete_btn.clicked.connect(self.delete_card)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        
        layout.addLayout(btn_layout)
        
        # Close button at bottom
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    # Refresh card list when it's updated
    def populate_cards(self):
        self.card_list.clear()
        for card in self.deck.flashcards:
            # Extract plain text from HTML
            from PyQt6.QtGui import QTextDocument
            doc = QTextDocument()
            doc.setHtml(card.front)
            plain_text = doc.toPlainText()
            
            item = QListWidgetItem(f"Q: {plain_text[:30]}{'...' if len(plain_text) > 30 else ''} (Difficulty: {card.difficulty})")
            item.setData(Qt.ItemDataRole.UserRole, card.id)
            self.card_list.addItem(item)
    
    def add_card(self):
        dialog = AddCardDialog(self)
        if dialog.exec():
            card_data = dialog.get_card_data()
            if not card_data["front"] or not card_data["back"]:
                QMessageBox.warning(self, "Warning", "The front and back of the card cannot be empty.")
                return
                
            new_card = self.deck.add_flashcard(
                card_data["front"], card_data["back"], card_data["notes"]
            )
            new_card.difficulty = card_data["difficulty"]
            
            # Update the list
            self.populate_cards()
            
            # Return True to tell that the deck was modified
            self.setResult(QDialog.DialogCode.Accepted)
    
    def edit_card(self):
        if not self.card_list.currentItem():
            QMessageBox.warning(self, "Warning", "Please select a card to edit.")
            return
            
        card_id = self.card_list.currentItem().data(Qt.ItemDataRole.UserRole)
        card = next((card for card in self.deck.flashcards if card.id == card_id), None)
        
        if card:
            dialog = EditCardDialog(card, self)
            if dialog.exec():
                card_data = dialog.get_card_data()
                if not card_data["front"] or not card_data["back"]:
                    QMessageBox.warning(self, "Warning", "The front and back of the card cannot be empty.")
                    return
                    
                card.front = card_data["front"]
                card.back = card_data["back"]
                card.notes = card_data["notes"]
                card.difficulty = card_data["difficulty"]
                
                # Update the list display
                self.populate_cards()
                
                # Return True to tell that the deck was modified
                self.setResult(QDialog.DialogCode.Accepted)
    
    def delete_card(self):
        if not self.card_list.currentItem():
            QMessageBox.warning(self, "Warning", "Please select a card to delete.")
            return
            
        card_id = self.card_list.currentItem().data(Qt.ItemDataRole.UserRole)
        
        confirm = QMessageBox.question(
            self, 
            "Confirm Deletion",
            "Are you sure you want to delete this flashcard?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.deck.remove_flashcard(card_id)
            self.populate_cards()
            
            # Return True to tell that the deck was modified
            self.setResult(QDialog.DialogCode.Accepted)

# Difficulty Rating Dialog
class RateDifficultyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_difficulty = 1
        self.difficulty_buttons = []
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Rate Difficulty")
        self.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Rate the difficulty of this card (1=Easy, 5=Hard):"))
        
        difficulty_layout = QHBoxLayout()
        for i in range(1, 6):
            btn = QPushButton(str(i))
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    border-radius: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:checked {
                    background-color: #3498db;
                    color: white;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self.select_difficulty(idx))
            self.difficulty_buttons.append(btn)
            difficulty_layout.addWidget(btn)
        self.difficulty_buttons[0].setChecked(True)  # Default to 1
        layout.addLayout(difficulty_layout)
        
        self.setLayout(layout)
    
    def select_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
        for btn in self.difficulty_buttons:
            btn.setChecked(False)
        self.difficulty_buttons[difficulty-1].setChecked(True)
        self.accept()  # Automatically save and close
    
    def get_difficulty(self):
        return self.selected_difficulty

# Deck Rename Window
class RenameDeckDialog(QDialog):
    def __init__(self, deck, parent=None):
        super().__init__(parent)
        self.deck = deck
        self.data_manager = DataManager()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Edit Deck Properties")
        self.setMinimumWidth(300)
        layout = QFormLayout()
        
        # Deck name field
        self.name_edit = QLineEdit(self.deck.name)
        layout.addRow("Deck Name:", self.name_edit)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addRow(btn_layout)
        
        self.setLayout(layout)
    
    def get_deck_data(self):
        return {
            "name": self.name_edit.text().strip()
        }
    
    def accept(self):
        new_name = self.get_deck_data()["name"]
        
        if new_name and new_name != self.deck.name:
            self.data_manager.delete_deck(self.deck.name)
            self.deck.name = new_name
        super().accept()

# User Profile Dialog
class UserProfileDialog(QDialog):
    def __init__(self, username, user_manager, parent=None):
        super().__init__(parent)
        self.username = username
        self.user_manager = user_manager
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(f"User Profile - {self.username}")
        self.setMinimumSize(500, 250)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Profile: {self.username}")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # User info
        user_info = self.user_manager.get_user_info(self.username)
        if user_info:
            info_layout = QFormLayout()
            info_layout.addRow("Username:", QLabel(self.username))
            
            # Format dates
            created_at = user_info.get("created_at", "Unknown")
            if created_at != "Unknown":
                try:
                    created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    created_at = created_date.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            
            last_login = user_info.get("last_login", "Never")
            if last_login and last_login != "Never":
                try:
                    login_date = datetime.fromisoformat(last_login.replace('Z', '+00:00'))
                    last_login = login_date.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            
            info_layout.addRow("Account Created:", QLabel(created_at))
            info_layout.addRow("Last Login:", QLabel(last_login or "Never"))
            
            layout.addLayout(info_layout)
        
        # Change password section
        layout.addWidget(QLabel("Change Password:"))
        
        self.current_password = QLineEdit()
        self.current_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.current_password.setPlaceholderText("Current password")
        layout.addWidget(self.current_password)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setPlaceholderText("New password")
        layout.addWidget(self.new_password)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setPlaceholderText("Confirm new password")
        layout.addWidget(self.confirm_password)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        change_pass_btn = QPushButton("Change Password")
        change_pass_btn.clicked.connect(self.change_password)
        btn_layout.addWidget(change_pass_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def change_password(self):
        current_pass = self.current_password.text()
        new_pass = self.new_password.text()
        confirm_pass = self.confirm_password.text()
        
        if not current_pass or not new_pass or not confirm_pass:
            QMessageBox.warning(self, "Error", "Please fill in all password fields.")
            return
        
        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "New passwords do not match.")
            return
        
        if len(new_pass) < 6:
            QMessageBox.warning(self, "Error", "New password must be at least 6 characters long.")
            return
        
        # Verify current password
        if not self.user_manager.authenticate_user(self.username, current_pass)[0]:
            QMessageBox.warning(self, "Error", "Current password is incorrect.")
            return
        
        # Update password
        self.user_manager.users[self.username]["password"] = self.user_manager.hash_password(new_pass)
        self.user_manager.save_users()
        
        QMessageBox.information(self, "Success", "Password changed successfully!")
        
        # Clear fields
        self.current_password.clear()
        self.new_password.clear()
        self.confirm_password.clear()
