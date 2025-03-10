from PyQt6.QtWidgets import QPushButton

class UserStats:
    def __init__(self):
        self.total_attempt = 0
        self.correct_answers = 0
        self.incorrect_answers = 0

        # Right/Wrong buttons
        self.right_btn = QPushButton("Got it Right ✓")
        self.right_btn.setStyleSheet("background-color: #8aff8a; font-weight: bold;")
        self.right_btn.clicked.connect(self.mark_right)

        self.wrong_btn = QPushButton("Got it Wrong ✗")
        self.wrong_btn.setStyleSheet("background-color: #ff8a8a; font-weight: bold;")
        self.wrong_btn.clicked.connect(self.mark_wrong)

    def update_feedback_buttons(self):
        """Mengubah tampilan tombol setelah ditekan"""
        self.right_btn.setText("✔ Marked as Right")  # Ubah teks tombol
        self.right_btn.setEnabled(False)  # Nonaktifkan tombol setelah ditekan

    def mark_right(self):
        """Menandai jawaban sebagai benar"""
        if hasattr(self, 'current_deck') and self.current_deck and self.current_deck.flashcards:
            self.feedback_given = True
            # Sinyal ke aplikasi utama
            self.cardMarkedRight.emit(self.current_index)
            self.update_feedback_buttons()
            self.total_attempt += 1
            self.correct_answers += 1  # Tambah jumlah jawaban benar

    def mark_wrong(self):
        """Menandai jawaban sebagai salah"""
        if hasattr(self, 'current_deck') and self.current_deck and self.current_deck.flashcards:
            self.feedback_given = True
            self.total_attempt += 1
            self.incorrect_answers += 1  # Tambah jumlah jawaban salah

    def get_akurasi(self):
        """Menghitung persentase akurasi jawaban"""
        if self.total_attempt == 0:
            return 0
        return (self.correct_answers / self.total_attempt) * 100

    def reset_stats(self):
        """Mengatur ulang statistik ke nol"""
        self.total_attempt = 0
        self.correct_answers = 0
        self.incorrect_answers = 0

    def get_stats_text(self):
        """Mengembalikan statistik sebagai teks untuk ditampilkan di UI"""
        return (f"Total kartu dijawab: {self.total_attempt}\n"
                f"Total jawaban benar: {self.correct_answers}\n"
                f"Total jawaban salah: {self.incorrect_answers}\n"
                f"Akurasi: {self.get_akurasi():.2f}%")
