import base64

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton, QHBoxLayout, QFileDialog, QSpinBox, QDialog
from PyQt6.QtCore import Qt,QAbstractAnimation, QBuffer, QByteArray, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QImage 

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
        self.title = QLabel("Card Notes")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold; border-radius: 10px; padding: 5px;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)
        
        # Section text editor in Notes Panel
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText("Add your notes for this card here...")
        self.notes_text.setAcceptRichText(True)
        layout.addWidget(self.notes_text, 1)
        
        # Section save button in Notes Panel
        self.save_btn = QPushButton("Save Notes")
        layout.addWidget(self.save_btn)

        # Section insert image button in Notes Panel
        self.insert_image_btn = QPushButton("Insert Image")
        self.insert_image_btn.clicked.connect(self.insert_image)
        layout.addWidget(self.insert_image_btn)
        
        # Show all section
        self.setLayout(layout) 
        
    # Set text editor for write notes if card was selected
    def set_card(self, card):
        self.current_card = card #Obj card
        if card:
            self.notes_text.setHtml(card.notes) 
            self.setEnabled(True)
        else:
            self.notes_text.setHtml("")
            self.setEnabled(False)
            
    # Set visibility for notes
    def set_visible(self, visible):
        self.is_visible = visible
        self.notes_text.setVisible(visible)
        self.save_btn.setVisible(visible)
        self.insert_image_btn.setVisible(visible)
        
        # Show placeholder message if not visible
        if not visible:
            self.notes_text.setPlaceholderText("Notes are hidden. Click 'Show Notes' to view.")
        else:
            self.notes_text.setPlaceholderText("Add your notes for this card here...")
    
    # Save Notes
    def save_notes(self):
        if self.current_card and self.is_visible:
            self.current_card.notes = self.notes_text.toHtml()
            return True
        return False
    
    def insert_image(self):
        """Insert image into notes with resizing capability"""
        if not self.current_card or not self.is_visible:
            return False
            
        image = ImageHandler.load_image_from_file(self)
        if image:
            # Show resize dialog
            dialog = ImageResizeDialog(image.width(), image.height(), self)
            if dialog.exec():
                new_width, new_height = dialog.get_new_size()
                resized_image = ImageHandler.resize_image(image, new_width, new_height)
                
                # Convert to base64 for storage
                base64_str = ImageHandler.image_to_base64(resized_image)
                
                # Insert into notes text
                cursor = self.notes_text.textCursor()
                cursor.insertHtml(f'<img src="data:image/png;base64,{base64_str}">')
                self.notes_text.setTextCursor(cursor)
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

# Image Handler
class ImageHandler:
    """
    Kelas yang menangani operasi-operasi terkait gambar
    """
    @staticmethod
    def load_image_from_file(parent):
        """Memuat gambar dari file yang dipilih"""
        file_name, _ = QFileDialog.getOpenFileName(
            parent, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            return QImage(file_name)
        return None
    
    @staticmethod
    def resize_image(image, width, height):
        """Mengubah ukuran gambar"""
        return image.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    
    @staticmethod
    def image_to_base64(image):
        """Mengkonversi gambar ke format base64"""
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QBuffer.OpenModeFlag.WriteOnly)
        image.save(buffer, "PNG")
        return base64.b64encode(byte_array.data()).decode('utf-8')
    
    @staticmethod
    def base64_to_image(base64_str):
        """Mengkonversi string base64 kembali menjadi gambar"""
        image_data = base64.b64decode(base64_str)
        image = QImage()
        image.loadFromData(image_data)
        return image

# Resize Image
class ImageResizeDialog(QDialog):
    """
    Dialog untuk mengubah ukuran gambar
    """
    def __init__(self, current_width, current_height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resize Image")
        self.setMinimumWidth(300)
        
        # Setup layout
        layout = QVBoxLayout()
        
        # Width control
        width_layout = QHBoxLayout()
        width_label = QLabel("Width:")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(10, 2000)
        self.width_spinbox.setValue(current_width)
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_spinbox)
        
        # Height control
        height_layout = QHBoxLayout()
        height_label = QLabel("Height:")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(10, 2000)
        self.height_spinbox.setValue(current_height)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_spinbox)
        
        # Maintain aspect ratio checkbox (implemented as lock button)
        aspect_layout = QHBoxLayout()
        self.lock_aspect_btn = QPushButton("Lock Aspect Ratio")
        self.lock_aspect_btn.setCheckable(True)
        self.lock_aspect_btn.setChecked(True)
        self.aspect_ratio = current_width / current_height if current_height else 1
        aspect_layout.addWidget(self.lock_aspect_btn)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        # Connect signals
        self.width_spinbox.valueChanged.connect(self.width_changed)
        self.height_spinbox.valueChanged.connect(self.height_changed)
        
        # Add layouts to main layout
        layout.addLayout(width_layout)
        layout.addLayout(height_layout)
        layout.addLayout(aspect_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def width_changed(self, new_width):
        """Menyesuaikan tinggi saat lebar diubah jika aspect ratio dikunci"""
        if self.lock_aspect_btn.isChecked():
            self.height_spinbox.blockSignals(True)
            self.height_spinbox.setValue(int(new_width / self.aspect_ratio))
            self.height_spinbox.blockSignals(False)
    
    def height_changed(self, new_height):
        """Menyesuaikan lebar saat tinggi diubah jika aspect ratio dikunci"""
        if self.lock_aspect_btn.isChecked():
            self.width_spinbox.blockSignals(True)
            self.width_spinbox.setValue(int(new_height * self.aspect_ratio))
            self.width_spinbox.blockSignals(False)
    
    def get_new_size(self):
        """Mengembalikan ukuran baru yang dipilih"""
        return self.width_spinbox.value(), self.height_spinbox.value()
    