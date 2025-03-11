from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt6.QtCore import QTimer, Qt
import sys
import json
import os 

# Notes Manager (Right Panel)
class NotesManager:
    def __init__(self, notes_file="notes.json"):
        """
        Initialize new notes on flashcard
        Class to store and retrieve flashcard notes separately.
        """
        self.notes_file = notes_file
        self.notes_file = self.load_notes()
    
    def _load_notes(self):
        """Load notes from JSON files."""
        if os.path.exists(self_notes_file):
            with open(self.notes_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return{}
        return{}
    
    def save_notes(self):
        """Saving notes to JSON files"""
        with open(self.notes_file, "w") as file:
            json.dump(self.notes_data, file, indent=4)

    def add_notes(self):
        """Create or update notes for certain flashcards"""
        self.notes_data[flashcard_id] = note 
        self.save_notes()

    def get_note(self, flashcard_id):
        """Dapatkan notes untuk flashcard tertentu."""
        return self.notes_data.get(flashcard_id, "")

    def delete_note(self, flashcard_id):
        """Hapus notes untuk flashcard tertentu."""
        if flashcard_id in self.notes_data:
            del self.notes_data[flashcard_id]
            self.save_notes()

class Timer:
    def create_timer(self, deck):
        self