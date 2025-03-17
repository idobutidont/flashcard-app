from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

# NotesPanel Handling 
class NotesPanel(QWidget):
    # Constructor 
    def __init__(self, parent=None):
        super().__init__(parent) 
        self.current_card = None
        self.is_visible = False
        self.init_ui()
        
    # Modele for Initialize User Interface
    def init_ui(self):
        # UI Set to vertical layout 
        """
        Title
        [Text Editor]
        Save
        """
        layout = QVBoxLayout()
         
        # Section title in Notes Panel
        title = QLabel("Card Notes")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Section text editor in Notes Panel
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText("Add your notes for this card here...")
        layout.addWidget(self.notes_text, 1)
        
        # Section save button in Notes Panel
        self.save_btn = QPushButton("Save Notes")
        layout.addWidget(self.save_btn)
        
        # Show all section
        self.setLayout(layout) 
        
    # Set text editor for write notes if card was selected
    def set_card(self, card):
        self.current_card = card #Obj card
        if card:
            self.notes_text.setText(card.notes) 
            self.setEnabled(True)
        else:
            self.notes_text.setText("")
            self.setEnabled(False)
            
    # Set visibility for notes
    def set_visible(self, visible):
        self.is_visible = visible
        self.notes_text.setVisible(visible)
        self.save_btn.setVisible(visible)
        
        # Show placeholder message if not visible
        if not visible:
            self.notes_text.setPlaceholderText("Notes are hidden. Click 'Show Notes' to view.")
        else:
            self.notes_text.setPlaceholderText("Add your notes for this card here...")
    
    # Save Notes
    def save_notes(self):
        if self.current_card and self.is_visible:
            self.current_card.notes = self.notes_text.toPlainText()
            return True
        return False

# Notes Visibility Handling
class NotesManager:
    # Constructor
    def __init__(self, notes_panel):
        self.notes_panel = notes_panel
        
    # Notes panel handling based on the current card and state
    def update_notes_panel(self, deck, card_index, showing_front, notes_visible):
        ''' Set notes based on set card '''
        if deck and deck.flashcards:
            card = deck.get_flashcard(card_index)
            self.notes_panel.set_card(card)
            
            ''' Set notes visibility based on card side and user preference '''
            is_showing_answer = not showing_front
            should_show_notes = is_showing_answer or notes_visible
            self.notes_panel.set_visible(should_show_notes)
        # If deck not selected, notes won't appear
        else:
            self.notes_panel.set_card(None)
            self.notes_panel.set_visible(False)
    
    # Visibility function on notes panel
    def toggle_notes_visibility(self, visible):
        self.notes_panel.set_visible(visible)
    
    # Section showing or hiding notes when the card is flipped
    def handle_card_flip(self, is_showing_answer, notes_visible):
        ''' When showing answer, always show notes '''
        if is_showing_answer:
            self.notes_panel.set_visible(True)
        # When back to question, use the user's preference 
        else:
            self.notes_panel.set_visible(notes_visible)

    # Section save current notes
    def save_notes(self):
        return self.notes_panel.save_notes()
    
    # Section ShowNotes button based on card state
    def update_toggle_notes_button(self, button, showing_front, notes_visible):
        if showing_front:
            button.setVisible(True)
            button.setText("Show Notes" if not notes_visible else "Hide Notes")
        # Otherwise button is not visible
        else: 
            button.setVisible(False)
