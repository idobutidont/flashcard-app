from PyQt6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QWidget, QApplication, QGroupBox, QVBoxLayout, QDialog, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal, Qt, QElapsedTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import json
import os
from Ido_241524047 import Deck

class StatsManager(QObject):
    cardMarkedRight = pyqtSignal(int)  # Signal untuk menandai kartu sebagai benar
    cardMarkedWrong = pyqtSignal(int)  # Signal untuk menandai kartu sebagai salah
    
    def __init__(self):
        super().__init__()
        self.feedback_given = False
        self.deck_timers = {}  # Dictionary to store timers for each deck
        self.current_deck = None
        self.session_right = 0  # Add session tracking
        self.session_wrong = 0

    def save_study_time(self):
        """Save study time directly to deck data"""
        if self.current_deck:
            # Add current session time if timer is running
            if self.current_deck.name in self.deck_timers:
                timer = self.deck_timers[self.current_deck.name]
                if timer.isValid():
                    elapsed = timer.elapsed()
                    self.current_deck.study_time += elapsed
                    timer.restart()  # Restart timer to continue tracking

    def start_timer(self):
        """Start timer for current deck"""
        if self.current_deck and self.current_deck.name in self.deck_timers:
            if not self.deck_timers[self.current_deck.name].isValid():
                self.deck_timers[self.current_deck.name].start()
    
    def stop_timer(self, deck_name=None):
        """Stop timer and update deck study time"""
        deck_name = deck_name or (self.current_deck.name if self.current_deck else None)
        if deck_name and deck_name in self.deck_timers:
            timer = self.deck_timers[deck_name]
            if timer.isValid():
                elapsed = timer.elapsed()
                timer.invalidate()
                
                # Update study time in deck object
                if self.current_deck and self.current_deck.name == deck_name:
                    self.current_deck.study_time += elapsed
    
    def set_current_deck(self, deck):
        """Set current deck and initialize its study time"""
        # Stop timer for previous deck
        if self.current_deck and self.current_deck.name in self.deck_timers:
            self.stop_timer(self.current_deck.name)

        self.current_deck = deck
        if deck:
            # Create new timer for deck if it doesn't exist
            if deck.name not in self.deck_timers:
                self.deck_timers[deck.name] = QElapsedTimer()
            
            # Start timer for new deck
            if not self.deck_timers[deck.name].isValid():
                self.deck_timers[deck.name].start()

    def get_elapsed_time(self):
        """Return total study time in minutes including current session"""
        if not self.current_deck:
            return 0.0
            
        try:
            current_total = self.current_deck.study_time if hasattr(self.current_deck, 'study_time') else 0
            # Add current session time if timer is running
            if self.current_deck.name in self.deck_timers:
                timer = self.deck_timers[self.current_deck.name]
                if timer.isValid():
                    current_total += timer.elapsed()
            return current_total / 60000  # Convert milliseconds to minutes
        except Exception as e:
            print(f"Error calculating elapsed time: {e}")
            return 0.0

    def setup_feedback_elements(self):
        """Membuat UI untuk tombol benar/salah dan keterangan stats"""
        # Tombol benar salah
        self.right_btn = QPushButton("Got it Right ✓")
        self.right_btn.setStyleSheet("background-color: #8aff8a; font-weight: bold;")
        
        self.wrong_btn = QPushButton("Got it Wrong ✗")
        self.wrong_btn.setStyleSheet("background-color: #ff8a8a; font-weight: bold;")
        
        # Stats label
        self.stats_label = QLabel("")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        
        # Menyembunyikan keterangan statistik benar/salah
        self.stats_label.setVisible(False)
        
        return self.right_btn, self.wrong_btn, self.stats_label
    
    def reset_feedback_state(self):
        """Mengatur ulang statistik ke nol"""
        self.feedback_given = False
    
    def mark_right(self, card_index):
        """Fungsi yang dijalankan saat tombol benar ditekan"""
        self.feedback_given = True
        self.cardMarkedRight.emit(card_index)
    
    def mark_wrong(self, card_index):
        """Fungsi yang dijalankan saat tombol salah ditekan"""
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
        """Memperbarui jumlah benar, salah, dan Accuracy pada tampilan statistik"""
        if card:
            total = card.right_count + card.wrong_count
            accuracy = (card.right_count / total * 100) if total > 0 else 0
            stats_text = (f"Right: {card.right_count} | Wrong: {card.wrong_count} | "
                         f"Accuracy: {accuracy:.1f}% | Difficulty: {card.difficulty} | "
                         f"Retention: {card.retention_score:.2f}")
            self.stats_label.setText(stats_text)
            
            # Menentukan warna dari teks Accuracy sesuai dengan persen Accuracy
            if accuracy >= 70:
                self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
            elif accuracy >= 40:
                self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: orange;")
            else:
                self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
                
    def handle_card_right(self, deck, card_index):
        """Menangani pertambahan dari variabel jumlah Correct Answer"""
        if deck and deck.flashcards:
            card = deck.get_flashcard(card_index)
            if card:
                card.right_count += 1
                return True
        return False
    
    def handle_card_wrong(self, deck, card_index):
        """Menangani pertambahan dari variabel jumlah Incorrect Answer"""
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

    def get_session_score(self):
        """Calculate score for current session"""
        total = self.session_right + self.session_wrong
        return (self.session_right / total * 100) if total > 0 else 0

class PlotDialog(QDialog):
    """Custom dialog to display Matplotlib plots"""
    def __init__(self, fig, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 800, 600)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Embed Matplotlib figure
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

class StatsPage(QDialog):
    def __init__(self, card, last_session_score, total_study_time):
        super().__init__()
        
        # Set window properties 
        self.setWindowTitle("Flashcard App - Statistik")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f2f5;
                border-radius: 10px;
            }
            QGroupBox {
                background-color: white;
                border-radius: 8px;
                border: none;
                margin-top: 15px;
                font-weight: bold;
                color: #1a1a1a;
            }
            QGroupBox::title {
                color: #2c3e50;
                subcontrol-position: top center;
                padding: 5px;
                background-color: transparent;
            }
            QLabel {
                color: #34495e;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        # Add title header
        title_label = QLabel("📊 Performance Statistics")
        title_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-family: Tahoma, sans-serif;
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                border-radius: 10px;
                margin: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Store card reference and study time
        self.card = card
        self.correct = self.card.right_count if self.card else 0
        self.incorrect = self.card.wrong_count if self.card else 0
        self.total = self.correct + self.incorrect
        self.accuracy = (self.correct / self.total * 100) if self.total > 0 else 0
        self.difficulty = self.card.difficulty if self.card else 1
        self.retention = self.card.retention_score if self.card else 0.0
        self.total_study_time = total_study_time  # Store for use in visualizations

        # Main stats box with gradient background
        main_stats_box = QGroupBox("📊 Statistik Utama")
        main_stats_box.setStyleSheet("""
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #f0f8ff);
                padding: 15px;
                margin: 10px;
            }
        """)
        
        main_stats_layout = QVBoxLayout()
        stats_labels = [
            (f"✅ Correct Answer: {self.correct}", "#27ae60"),
            (f"❌ Incorrect Answer: {self.incorrect}", "#c0392b"),
            (f"🔄 Total Questions: {self.total}", "#2980b9"),
            (f"📈 Accuracy: {self.accuracy:.2f}%", self._get_accuracy_color()),
            (f"📊 Difficulity: {self.difficulty}", "#8e44ad"),
            (f"🧠 Retention Score: {self.retention:.2f}", "#16a085")
        ]
        
        for text, color in stats_labels:
            label = QLabel(text)
            label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-size: 15px;
                    font-weight: bold;
                    padding: 10px;
                    background-color: rgba(255, 255, 255, 0.7);
                    border-radius: 5px;
                    margin: 2px;
                }}
            """)
            main_stats_layout.addWidget(label)
        
        main_stats_box.setLayout(main_stats_layout)

        # Extra stats box
        extra_stats_box = QGroupBox("📂 Detail Tambahan")
        extra_stats_box.setStyleSheet("""
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #fff0f5);
                padding: 15px;
                margin: 10px;
            }
        """)
        
        extra_stats_layout = QVBoxLayout()
        extra_labels = [
            (f"🎯 Last Session Score: {last_session_score:.1f}%", "#8e44ad"),
            (f"⏳ Total Study Time: {total_study_time:.1f} minute", "#d35400")
        ]
        for text, color in extra_labels:
            label = QLabel(text)
            label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-size: 15px;
                    font-weight: bold;
                    padding: 10px;
                    background-color: rgba(255, 255, 255, 0.7);
                    border-radius: 5px;
                    margin: 2px;
                }}
            """)
            extra_stats_layout.addWidget(label)
        
        extra_stats_box.setLayout(extra_stats_layout)

        # Visualization section
        viz_box = QGroupBox("📊 Data Visualizations")
        viz_box.setStyleSheet("""
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ffffff, stop:1 #e8f5e9);
                padding: 15px;
                margin: 10px;
                border-radius: 8px;
            }
        """)
        
        viz_layout = QVBoxLayout()
        viz_layout.setSpacing(8)  # Reduce spacing for closer button placement
        
        # Create single row of visualization buttons
        viz_buttons_row = QHBoxLayout()
        
        # Add visualization buttons
        self.add_viz_button("📊 Performance Bar Chart", self.show_performance_chart, viz_buttons_row)
        self.add_viz_button("📈 Learning Progress", self.show_learning_progress, viz_buttons_row)
        self.add_viz_button("🎯 Accuracy Distribution", self.show_accuracy_dist, viz_buttons_row)
        
        # Reset button with full width
        reset_button = QPushButton("🔄 Reset Statistics")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 500px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        reset_button.clicked.connect(self.reset_stats)

        # Add buttons to visualization layout
        viz_layout.addLayout(viz_buttons_row)
        viz_layout.addWidget(reset_button, alignment=Qt.AlignmentFlag.AlignCenter)

        viz_box.setLayout(viz_layout)

        # Layout setup
        main_layout = QHBoxLayout()
        main_layout.addWidget(main_stats_box)
        main_layout.addWidget(extra_stats_box)

        page_layout = QVBoxLayout()
        page_layout.addWidget(title_label)
        page_layout.addLayout(main_layout)
        page_layout.addWidget(viz_box)
        page_layout.addStretch()  # Add stretch to fill remaining space

        # Add some spacing
        page_layout.setSpacing(15)
        page_layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(page_layout)

    def _get_accuracy_color(self):
        """Return color based on accuracy score"""
        if self.accuracy >= 80:
            return "#27ae60"  # Green
        elif self.accuracy >= 50:
            return "#f39c12"  # Orange
        return "#c0392b"  # Red

    def reset_stats(self):
        if self.card:
            self.card.right_count = 0
            self.card.wrong_count = 0
            self.card.retention_score = 0.0
            self.card.difficulty = 1
            
            # Update display
            self.correct = 0
            self.incorrect = 0
            self.total = 0
            self.accuracy = 0
            self.difficulty = 1
            self.retention = 0.0
            
            # Update labels
            for label in self.findChildren(QLabel):
                if "Correct Answer" in label.text():
                    label.setText(f"✅ Correct Answer: {self.correct}")
                elif "Incorrect Answer" in label.text():
                    label.setText(f"❌ Incorrect Answer: {self.incorrect}")
                elif "Total Questions" in label.text():
                    label.setText(f"🔄 Total Questions: {self.total}")
                elif "Accuracy" in label.text():
                    label.setText(f"📈 Accuracy: {self.accuracy:.2f}%")
                elif "Difficulity" in label.text():
                    label.setText(f"📊 Difficulity: {self.difficulty}")
                elif "Retention Score" in label.text():
                    label.setText(f"🧠 Retention Score: {self.retention:.2f}")

    def add_viz_button(self, text, callback, layout):
        """Helper method to create and add visualization buttons"""
        btn = QPushButton(text)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        btn.clicked.connect(callback)
        
        # Only show button if there is data to display
        has_data = (self.correct + self.incorrect) > 0
        btn.setVisible(has_data)
        
        layout.addWidget(btn)

    def show_performance_chart(self):
        """Show performance metrics using Matplotlib bar plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        metrics = ['Correct', 'Incorrect', 'Accuracy']
        values = [self.correct, self.incorrect, self.accuracy]
        colors = ['#27ae60', '#e74c3c', '#3498db']
        
        bars = ax.bar(metrics, values, color=colors)
        ax.set_title('Performance Metrics', pad=20, fontsize=14)
        ax.set_ylabel('Value')
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}', va='bottom', fontsize=12)
        
        plt.tight_layout()
        self.show_plot(fig, "Performance Metrics")

    def show_learning_progress(self):
        """Show learning progress over time using line plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        reviews = range(1, self.total + 1)
        accuracy_trend = [min(100, self.accuracy * (1 + i * 0.05)) for i in range(len(reviews))]
        retention_trend = [min(100, self.retention * 100 * (1 + i * 0.03)) for i in range(len(reviews))]
        
        ax.plot(reviews, accuracy_trend, 'o-', label='Accuracy', color='#3498db')
        ax.plot(reviews, retention_trend, 's-', label='Retention', color='#e67e22')
        
        ax.set_title('Learning Progress Over Time', pad=20, fontsize=14)
        ax.set_xlabel('Review Number')
        ax.set_ylabel('Score (%)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        self.show_plot(fig, "Learning Progress")

    def show_accuracy_dist(self):
        """Show accuracy distribution using Matplotlib pie chart"""
        # Add safety check
        if (self.correct + self.incorrect) == 0:
            QMessageBox.warning(self, "No Data", "No study data available yet.")
            return
            
        fig, ax = plt.subplots(figsize=(8, 8))
        
        labels = ['Correct', 'Incorrect']
        sizes = [self.correct, self.incorrect]
        colors = ['#27ae60', '#e74c3c']
        
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title('Accuracy Distribution', pad=20, fontsize=14)
        
        plt.tight_layout()
        self.show_plot(fig, "Accuracy Distribution")

    def show_plot(self, fig, title):
        """Display the plot in a new non-blocking dialog"""
        plot_dialog = PlotDialog(fig, title, self)
        plot_dialog.exec()