# Mengimpor modul PyQt6 yang digunakan untuk membuat tampilan UI
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget
from PyQt6.QtCore import Qt, pyqtSignal

# Kelas FlashcardDisplay untuk menampilkan kartu flashcard di tengah aplikasi
class FlashcardDisplay(QWidget):
    # Sinyal untuk komunikasi dengan bagian lain aplikasi
    cardFlipped = pyqtSignal(bool)  # Dipancarkan saat kartu dibalik
    cardChanged = pyqtSignal(int, bool) # Dipancarkan saat kartu berubah (index, apakah menampilkan sisi depan) 
    
    def __init__(self, parent=None):
        super().__init__(parent)    # Memanggil konstruktor QWidget
        self.current_index = 0  # Menyimpan indeks kartu yang sedang ditampilkan
        self.current_deck = None    # Menyimpan dek aktif
        self.showing_front = True   # Menandai apakah sisi depan kartu ditampilkan
        self.notes_visible = False  # Menyimpan status tampilan catatan
        self.init_ui()  # Memanggil metode untuk inisialisasi tampilan UI
        
    def init_ui(self):
        """Menginisialisasi tampilan UI"""
        layout = QVBoxLayout()  # Membuat layout vertikal untuk widget

        # Label judul yang menampilkan nama dek atau pesan default
        self.title_label = QLabel("Select a Deck")  
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Memusatkan teks ke tengah
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")  # Atur gaya teks
        layout.addWidget(self.title_label)  # Tambahkan ke layout
        
        # Widget untuk menampilkan halaman kartu dan halaman sambutan
        self.card_stack = QStackedWidget()

        # Halaman sambutan saat tidak ada dek yang dipilih
        self.welcome_widget = QLabel("Welcome! Please select or create a deck to start.")
        self.welcome_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_widget.setStyleSheet("font-size: 16px; color: gray;")
        self.card_stack.addWidget(self.welcome_widget)  # Tambahkan ke card_stack
        
        # Widget utama untuk menampilkan kartu
        self.card_widget = QWidget()
        card_layout = QVBoxLayout() #Layout kartu Vertikal
        
        # Area untuk menampilkan teks flashcard
        self.card_content = QLabel()
        self.card_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_content.setStyleSheet("""
            background-color: white;
            color: black;
            border: 1px solid #CCC;
            border-radius: 5px;
            padding: 30px;
            font-size: 16px;
            min-height: 200px;
        """)    # Desain/gaya tampilan kartu
        self.card_content.setWordWrap(True)
        card_layout.addWidget(self.card_content, 1)
        
        # Placeholder untuk elemen feedback 
        self.feedback_placeholder = QWidget()
        card_layout.addWidget(self.feedback_placeholder)
        
        self.card_widget.setLayout(card_layout)
        self.card_stack.addWidget(self.card_widget)
        layout.addWidget(self.card_stack)
        
        self.setLayout(layout)
    
    def set_deck(self, deck):
        """Mengatur dek yang sedang digunakan dan memperbarui tampilan"""
        self.current_deck = deck    # Menyimpan dek aktif
        self.current_index = 0  # Reset indeks kartu ke 0
        self.showing_front = True   # Mulai dengan menampilkan sisi depan kartu
        self.notes_visible = False
        self.title_label.setText(f"Deck: {deck.name}")
        self.card_stack.setCurrentIndex(1)  # Beralih ke tampilan kartu
        self.update_card_display()
        return self.showing_front, self.notes_visible
    
    def update_card_display(self):
        """Memperbarui tampilan flashcard berdasarkan indeks saat ini"""
        if not self.current_deck or not self.current_deck.flashcards:
            # Jika tidak ada dek atau kartu, tampilkan pesan default
            self.card_content.setText("No flashcards in this deck.\nClick 'Add New Flashcard' to create one.")
            return None
            
        card = self.current_deck.get_flashcard(self.current_index)
        if card:
            if self.showing_front:
                self.card_content.setText(card.front)
            else:
                self.card_content.setText(card.back)
            return card
        return None
    
    def flip_card(self):
        """Membalik flashcard antara sisi depan dan belakang"""
        self.showing_front = not self.showing_front
        card = self.update_card_display()
        # Emit signal to inform about card flip
        self.cardFlipped.emit(not self.showing_front)
        return self.showing_front, card
    
    def next_card(self):
        """Berpindah ke kartu berikutnya dalam dek"""
        if self.current_deck and self.current_deck.flashcards:
            self.current_index = (self.current_index + 1) % len(self.current_deck.flashcards)
            self.showing_front = True
            card = self.update_card_display()
            self.cardChanged.emit(self.current_index, self.showing_front)
            return self.current_index, self.showing_front, card
        return self.current_index, self.showing_front, None
    
    def prev_card(self):
        """Berpindah ke kartu sebelumnya dalam dek"""
        if self.current_deck and self.current_deck.flashcards:
            self.current_index = (self.current_index - 1) % len(self.current_deck.flashcards)
            self.showing_front = True
            card = self.update_card_display()
            self.cardChanged.emit(self.current_index, self.showing_front)
            return self.current_index, self.showing_front, card
        return self.current_index, self.showing_front, None
    
    def get_current_card(self):
        """Mengambil kartu yang sedang ditampilkan"""
        if self.current_deck and self.current_deck.flashcards:
            return self.current_deck.get_flashcard(self.current_index)
        return None
    
    def toggle_notes_visibility(self):
        """Menampilkan atau menyembunyikan catatan kartu"""
        self.notes_visible = not self.notes_visible
        return self.notes_visible
        
    def show_welcome_screen(self):
        """Menampilkan layar sambutan saat tidak ada dek yang dipilih"""
        self.card_stack.setCurrentIndex(0)
        self.title_label.setText("Select a Deck")
