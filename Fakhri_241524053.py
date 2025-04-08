# Mengimpor modul PyQt6 yang digunakan untuk membuat tampilan UI
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QEasingCurve, pyqtSignal, QPropertyAnimation
from PyQt6.QtGui import QPixmap

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
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; background-color: #FF5733; padding: 10px; border-radius: 5px;")  # Atur gaya teks
        layout.addWidget(self.title_label)  # Tambahkan ke layout
        
        # Widget untuk menampilkan halaman kartu dan halaman sambutan
        self.card_stack = QStackedWidget()

        # Halaman sambutan saat tidak ada dek yang dipilih
        self.welcome_widget = QLabel("Welcome! Please select or create a deck to start.")
        self.welcome_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_widget.setStyleSheet("font-size: 16px; color: #444; background-color: #FFDD57; padding: 20px; border-radius: 5px;")
        self.card_stack.addWidget(self.welcome_widget)  # Tambahkan ke card_stack
        
        # Widget utama untuk menampilkan kartu
        self.card_widget = QWidget()
        card_layout = QVBoxLayout() #Layout kartu Vertikal
        
        # Area untuk menampilkan teks flashcard
        self.card_content = QLabel()

        self.star_label = QLabel(self)
        self.star_label.setPixmap(QPixmap("images/star.png").scaled(50, 50))  # Gambar bintang
        self.star_label.setStyleSheet("background: transparent;")  
        self.moon_label = QLabel(self)
        self.moon_label.setPixmap(QPixmap("images/moon.png").scaled(50, 50))  # Gambar bulan
        self.moon_label.setStyleSheet("background: transparent;")  

        self.card_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_content.setStyleSheet("""
            background-color: white;
            color: black;
            border: 2px solid #FF4500;
            border-radius: 10px;
            padding: 30px;
            font-size: 16px;
            min-height: 200px;
        """)    # Desain/gaya tampilan kartu

        self.init_animation()

        self.card_content.setWordWrap(True)
        card_layout.addWidget(self.card_content, 1)

        card_layout.addWidget(self.star_label, 0, Qt.AlignmentFlag.AlignLeft)
        card_layout.addWidget(self.moon_label, 0, Qt.AlignmentFlag.AlignRight)
        
        # Placeholder untuk elemen feedback 
        self.feedback_placeholder = QWidget()
        card_layout.addWidget(self.feedback_placeholder)
        
        self.card_widget.setLayout(card_layout)
        self.card_stack.addWidget(self.card_widget)
        layout.addWidget(self.card_stack)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #FFC300;")
        
        self.init_slide_animations()

    def init_animation(self):
        self.opacity_effect = QGraphicsOpacityEffect(self.card_content)
        self.card_content.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
    
    def animate_card_transition(self):
        self.animation.stop()
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

    def init_slide_animations(self):
        self.pos_animation = QPropertyAnimation(self.card_content, b"pos")
        self.pos_animation.setDuration(500)
        self.pos_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
    
    def animate_slide(self, direction):
        original_pos = self.card_content.pos()
        
        start_x = -direction * self.width()
        self.card_content.move(start_x, original_pos.y())
        
        self.pos_animation.stop()
        self.pos_animation.setStartValue(self.card_content.pos())
        self.pos_animation.setEndValue(original_pos)
        self.pos_animation.start()

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
                self.card_content.move(0, self.card_content.y())
            return card
        return None
    
    def flip_card(self):
        """Membalik flashcard antara sisi depan dan belakang"""
        if not self.current_deck:
            return
        self.showing_front = not self.showing_front
        card = self.update_card_display()

        self.animate_card_transition()

        # Emit signal to inform about card flip
        self.cardFlipped.emit(not self.showing_front)
        return self.showing_front, card
    
    def next_card(self):
        """Berpindah ke kartu berikutnya dalam dek"""
        if self.current_deck and self.current_deck.flashcards:
            self.current_index = (self.current_index + 1) % len(self.current_deck.flashcards)
            self.showing_front = True
            self.animate_slide(1)
            card = self.update_card_display()
            self.cardChanged.emit(self.current_index, self.showing_front)
            return self.current_index, self.showing_front, card
        return self.current_index, self.showing_front, None
    
    def prev_card(self):
        """Berpindah ke kartu sebelumnya dalam dek"""
        if self.current_deck and self.current_deck.flashcards:
            self.current_index = (self.current_index - 1) % len(self.current_deck.flashcards)
            self.showing_front = True
            self.animate_slide(-1)
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
    
    
