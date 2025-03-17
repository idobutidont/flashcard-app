from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal, Qt

class StatsManager(QObject):
    cardMarkedRight = pyqtSignal(int)  # Signal untuk menandai kartu sebagai benar
    cardMarkedWrong = pyqtSignal(int)  # Signal untuk menandai kartu sebagai salah
    
    def __init__(self):
        super().__init__()
        self.feedback_given = False

    def setup_feedback_elements(self):
        """Membuat UI untuk tombol benar/salah dan keterangan stats"""
        # Tombol benar salah
        self.right_btn = QPushButton("Got it Right ✓")
        self.right_btn.setStyleSheet("background-color: #8aff8a; font-weight: bold;")
        
        self.wrong_btn = QPushButton("Got it Wrong ✗")
        self.wrong_btn.setStyleSheet("background-color: #ff8a8a; font-weight: bold;")
        
        # Stats label
        self.stats_label = QLabel("")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Fixed alignment flag
        self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        
        # Menyembunyikan keterangan statistik benar/salah
        self.stats_label.setVisible(False)
        
        return self.right_btn, self.wrong_btn, self.stats_label
    
    def reset_feedback_state(self):
        """Mengatur ulang statistik ke nol"""
        self.feedback_given = False
    
    def mark_right(self, card_index):
        """Fungsi yang dijalankan saat tombol benar ditekan"""
        print("Tombol 'Got it Right ✓' ditekan")  # Debugging Output
        self.feedback_given = True
        self.cardMarkedRight.emit(card_index)
    
    def mark_wrong(self, card_index):
        """Fungsi yang dijalankan saat tombol salah ditekan"""
        print("Tombol 'Got it Wrong X' ditekan")  # Debugging Output
        self.feedback_given = True
        self.cardMarkedWrong.emit(card_index)
        
    def mark_card_feedback(self, is_right, card_index):
        """Menandai sebuah kartu benar atau salah"""
        if is_right:
            self.mark_right(card_index)
        else:
            self.mark_wrong(card_index)
    
    def update_feedback_buttons(self, showing_front, card=None):
        """Mengupdate tombol benar/salah dan keterangan stats berdasarkan kondisi"""
        if not card:
            # Menyembunyikan semua tombol ketika kondisi card = none
            self.right_btn.setVisible(False)
            self.wrong_btn.setVisible(False)
            self.stats_label.setVisible(False)
            return
            
        # Menampilkan tombol benar dan salah
        if not showing_front and not self.feedback_given:
            self.right_btn.setVisible(True)
            self.wrong_btn.setVisible(True)
            self.stats_label.setVisible(False)
        elif not showing_front and self.feedback_given:
            # Menampilkan hasil statistik yang didapat setelah menekan tombol benar/salah
            self.right_btn.setVisible(False)
            self.wrong_btn.setVisible(False)
            self.stats_label.setVisible(True)
            self.update_stats_display(card)
        else:
            # Menyembunyikan kembali tombol benar/salah saat ke soal berikutnya ( jawaban belum ditampilkan )
            self.right_btn.setVisible(False)
            self.wrong_btn.setVisible(False)
            self.stats_label.setVisible(False)
    
    def update_stats_display(self, card):
        """Memperbarui jumlah benar, salah, dan akurasi pada tampilan statistik"""
        if card:
            total = card.right_count + card.wrong_count
            accuracy = (card.right_count / total * 100) if total > 0 else 0
            stats_text = f"Right: {card.right_count} | Wrong: {card.wrong_count} | Accuracy: {accuracy:.1f}%"
            self.stats_label.setText(stats_text)
            
            # Menentukan warna dari teks akurasi sesuai dengan persen akurasi
            if accuracy >= 70:
                self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
            elif accuracy >= 40:
                self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: orange;")
            else:
                self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
                
    def handle_card_right(self, deck, card_index):
        """Menangani pertambahan dari variabel jumlah jawaban benar"""
        if deck and deck.flashcards:
            card = deck.get_flashcard(card_index)
            if card:
                card.right_count += 1
                return True
        return False
    
    def handle_card_wrong(self, deck, card_index):
        """Menangani pertambahan dari variabel jumlah jawaban salah"""
        if deck and deck.flashcards:
            card = deck.get_flashcard(card_index)
            if card:
                card.wrong_count += 1
                return True
        return False
        
    def process_feedback(self, deck, card_index, is_right):
        """Mengembalikan nilai dari variabel jumlah benar atau salah"""
        if is_right:
            return self.handle_card_right(deck, card_index)
        else:
            return self.handle_card_wrong(deck, card_index)
