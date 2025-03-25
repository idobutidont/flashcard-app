from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QWidget, QApplication, QGroupBox, QVBoxLayout, QDialog
from PyQt6.QtCore import QObject, pyqtSignal, Qt, QElapsedTimer
import json
import os

class StatsManager(QObject):
    cardMarkedRight = pyqtSignal(int)  # Signal untuk menandai kartu sebagai benar
    cardMarkedWrong = pyqtSignal(int)  # Signal untuk menandai kartu sebagai salah
    
    def __init__(self):
        super().__init__()
        self.feedback_given = False
        self.timer = QElapsedTimer()
        self.total_study_time = 0  # Menyimpan total waktu belajar dalam milidetik
        self.init_study_time()

    def init_study_time(self):
        """Create study_time.json if it doesn't exist and load saved time"""
        try:
            if os.path.exists("study_time.json") and os.path.getsize("study_time.json") > 0:
                with open("study_time.json", "r") as f:
                    data = json.load(f)
                    self.total_study_time = data.get("total_study_time", 0)
            else:
                # Create file with initial value if it doesn't exist
                self.save_study_time()
        except Exception as e:
            print(f"Error loading study time: {e}")
            self.total_study_time = 0
            self.save_study_time()

    def save_study_time(self):
        """Save total study time to JSON file"""
        # Include current session time if timer is running
        if self.timer.isValid():
            current_time = self.timer.elapsed()
            self.total_study_time += current_time  # Add current session
            self.timer.restart()  # Restart timer to keep tracking

        try:
            with open("study_time.json", "w") as f:
                json.dump({"total_study_time": self.total_study_time}, f, indent=2)
        except Exception as e:
            print(f"Error saving study time: {e}")

    def start_timer(self):
        """Memulai timer untuk menghitung waktu bermain."""
        if not self.timer.isValid():
            self.timer.start()
    
    def stop_timer(self):
        """Stop timer and save total time to file."""
        if self.timer.isValid():
            self.total_study_time += self.timer.elapsed()  # Add final session time
            self.timer.invalidate()
            self.save_study_time()
    
    def get_elapsed_time(self):
        """Return total study time in minutes including current session"""
        current_total = self.total_study_time
        if self.timer.isValid():
            current_total += self.timer.elapsed()
        return current_total / 60000  # Convert milliseconds to minutes

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
        
class StatsPage(QDialog):  # Change to QDialog instead of QWidget
    def __init__(self, card, last_session_score, total_study_time):
        super().__init__()

        self.setWindowTitle("Flashcard App - Statistik")
        self.setGeometry(100, 100, 500, 300)

        # Store card reference
        self.card = card

        # Get statistics from card
        self.correct = self.card.right_count if self.card else 0
        self.incorrect = self.card.wrong_count if self.card else 0
        self.total = self.correct + self.incorrect
        self.accuracy = (self.correct / self.total * 100) if self.total > 0 else 0

        # 🔹 Blok Kiri (Statistik Utama)
        main_stats_box = QGroupBox("📊 Statistik Utama")
        main_stats_layout = QVBoxLayout()
        main_stats_layout.addWidget(QLabel(f"✅ Jawaban Benar: {self.correct}"))
        main_stats_layout.addWidget(QLabel(f"❌ Jawaban Salah: {self.incorrect}"))
        main_stats_layout.addWidget(QLabel(f"🔄 Total Pertanyaan: {self.total}"))
        main_stats_layout.addWidget(QLabel(f"📈 Akurasi: {self.accuracy:.2f}%"))
        main_stats_box.setLayout(main_stats_layout)

        # 🔹 Blok Kanan (Detail Tambahan)
        extra_stats_box = QGroupBox("📂 Detail Tambahan")
        extra_stats_layout = QVBoxLayout()
        extra_stats_layout.addWidget(QLabel(f"🎯 Skor Sesi Terakhir: {last_session_score}%"))
        extra_stats_layout.addWidget(QLabel(f"⏳ Total Waktu Belajar: {total_study_time:.1f} menit"))
        extra_stats_box.setLayout(extra_stats_layout)

        # 🔹 Tombol Reset Statistik
        reset_button = QPushButton("🔄 Reset Statistik")
        reset_button.clicked.connect(self.reset_stats)

        # 🔹 Layout Utama (Menggabungkan Blok Kiri & Kanan)
        main_layout = QHBoxLayout()
        main_layout.addWidget(main_stats_box)
        main_layout.addWidget(extra_stats_box)

        # 🔹 Layout Keseluruhan
        page_layout = QVBoxLayout()
        page_layout.addLayout(main_layout)
        page_layout.addWidget(reset_button)

        self.setLayout(page_layout)

    def reset_stats(self):
        if self.card:
            self.card.right_count = 0
            self.card.wrong_count = 0
            
            # Update display
            self.correct = 0
            self.incorrect = 0
            self.total = 0
            self.accuracy = 0
            
            # Update labels
            for label in self.findChildren(QLabel):
                if "Jawaban Benar" in label.text():
                    label.setText(f"✅ Jawaban Benar: {self.correct}")
                elif "Jawaban Salah" in label.text():
                    label.setText(f"❌ Jawaban Salah: {self.incorrect}")
                elif "Total Pertanyaan" in label.text():
                    label.setText(f"🔄 Total Pertanyaan: {self.total}")
                elif "Akurasi" in label.text():
                    label.setText(f"📈 Akurasi: {self.accuracy:.2f}%")
            
            print("🔄 Statistik telah direset!")

