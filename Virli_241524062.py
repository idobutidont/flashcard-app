from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QInputDialog, QMessageBox, QSplitter, QPushButton, QListWidget, QLabel, QDialog, QFormLayout, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from datetime import datetime

from Ido_241524047 import Deck, DataManager, AddCardDialog, ManageCardsDialog, RenameDeckDialog
from Zein_241524056 import StatsManager, StatsPage
from Lukman_241524050 import NotesPanel, NotesManager
from Fakhri_241524053 import FlashcardDisplay
from Scheduler import Scheduler



class DeckListPanel(QWidget):  # Class untuk panel daftar deck pada flashcard
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout() # Menggunakan layout vertikal 
        
        # Judul pada panel 
        title = QLabel("Flashcard Decks")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Daftar deck 
        self.deck_list = QListWidget()
        layout.addWidget(self.deck_list)
        
        # Tombol untuk menambah, menghapus, dan rename deck 
        self.add_deck_btn = QPushButton("Add New Deck")
        self.delete_deck_btn = QPushButton("Delete Deck")
        self.edit_deck_btn = QPushButton("Rename Deck")
        
        layout.addWidget(self.add_deck_btn)
        layout.addWidget(self.delete_deck_btn)
        layout.addWidget(self.edit_deck_btn)
        
        self.setLayout(layout)  # Untuk mengatur layout utama 
    
    def populate_decks(self, decks): # Mengisi daftar deck dengan nama - nama deck yang tersedia 
        self.deck_list.clear()
        for deck in decks:
            self.deck_list.addItem(deck.name)
    
    def get_selected_deck_name(self): # Mengambil nama deck yang dipiih dalam daftar
        if self.deck_list.currentItem():
            return self.deck_list.currentItem().text()
        return None

# Clas dari aplikasi di flashcard
class FlashcardApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Menyimpan referensi ke LoginWindow (parent)
        self.setWindowIcon(QIcon("images/icon.png"))
        self.data_manager = DataManager()
        self.decks = []  # Daftar deck
        self.current_deck = None  # Deck yang dipilih
        self.init_ui()
        self.load_decks()
        self.stats_manager.start_timer()

    def init_ui(self):
        self.setWindowTitle("Flashcard App")
        self.setMinimumSize(900, 600)

        # Widget utama
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Untuk membagi tampilan jadi beberapa panel 
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Membuat panel-panel utama
        self.deck_panel = DeckListPanel()
        self.flashcard_display = FlashcardDisplay()
        self.notes_panel = NotesPanel()
        
        # Membuat objek pengelola statistik dan catatan 
        self.stats_manager = StatsManager()
        self.notes_manager = NotesManager(self.notes_panel)

        # Menambahkan panel daftar deck ke dalam splitter
        splitter.addWidget(self.deck_panel)
        
        # Panel tengah berisi tampilan flashcard dan kontrol navigasi
        center_panel = QWidget()
        center_layout = QVBoxLayout()
        
        # Menambahkan tampilan flashcard
        center_layout.addWidget(self.flashcard_display, 1)
        
        # Layout untuk tombol navigasi
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Previous")
        self.flip_btn = QPushButton("Flip Card")
        self.next_btn = QPushButton("Next")
        self.toggle_notes_btn = QPushButton("Show Notes")
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.flip_btn)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.toggle_notes_btn)
        center_layout.addLayout(nav_layout)
        
        # Layout untuk tombol feedback (benar/salah)
        feedback_layout = QHBoxLayout()
        right_btn, wrong_btn, stats_label = self.stats_manager.setup_feedback_elements()
        feedback_layout.addWidget(right_btn)
        feedback_layout.addWidget(wrong_btn)
        feedback_layout.addWidget(stats_label)
        center_layout.addLayout(feedback_layout)
        
        # Layout untuk tombol manajemen kartu
        card_mgmt_layout = QHBoxLayout()
        self.add_card_btn = QPushButton("Add New Flashcard")
        self.manage_cards_btn = QPushButton("Manage All Cards")
        self.stats_btn = QPushButton("View Statistics") 

        card_mgmt_layout.addWidget(self.add_card_btn)
        card_mgmt_layout.addWidget(self.manage_cards_btn)
        card_mgmt_layout.addWidget(self.stats_btn)
        center_layout.addLayout(card_mgmt_layout)
        
        center_panel.setLayout(center_layout)
        splitter.addWidget(center_panel)
        
        # Menambahkan catetan ke dalam splitter
        splitter.addWidget(self.notes_panel)

        # Mengatur ukuran awal masing-masing panel dalam splitter
        splitter.setSizes([200, 500, 200])

        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)

        # Menyembunyikan tombol tertentu hingga deck sudah dipilih
        self.update_button_visibility(False)
        
        # Menghubungkan sinyal
        self.connect_signals()

        # Menambahkan tombol logout
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        card_mgmt_layout.addWidget(self.logout_btn)

    def logout(self):
        confirm = QMessageBox.question(self, "Logout", "Are you sure you want to logout?")
        if confirm == QMessageBox.StandardButton.Yes:
            self.close()  # Menutup FlashcardApp
            self.parent.show()  # Menampilkan LoginWindow lagi


    def update_button_visibility(self, has_deck_selected):
        """Mengatur visibilitas tombol berdasarkan apakah ada deck yang dipilih"""
        # Navigation buttons
        self.prev_btn.setVisible(has_deck_selected)
        self.flip_btn.setVisible(has_deck_selected)
        self.next_btn.setVisible(has_deck_selected)
        self.toggle_notes_btn.setVisible(has_deck_selected and self.flashcard_display.showing_front)
        
        # Card management buttons
        self.add_card_btn.setVisible(has_deck_selected)
        self.manage_cards_btn.setVisible(has_deck_selected)
        
        # Stats button visibility
        self.stats_btn.setVisible(has_deck_selected)

        # Mengatur tombol feedback (benar/salah)
        if has_deck_selected:
            # Hanya perbarui jika kita memiliki deck, jika tidak biarkan tersembunyi
            self.stats_manager.update_feedback_buttons(
                self.flashcard_display.showing_front,
                self.flashcard_display.get_current_card()
            )
        else:
            # Sembunyikan secara eksplisit jika tidak ada deck yang dipilih
            self.stats_manager.right_btn.setVisible(False)
            self.stats_manager.wrong_btn.setVisible(False)
            self.stats_manager.stats_label.setVisible(False)

    def connect_signals(self):
        # Menghubungkan sinyal untuk interaksi dalam aplikasi 
        # Deck panel signals
        self.deck_panel.add_deck_btn.clicked.connect(self.add_deck)
        self.deck_panel.delete_deck_btn.clicked.connect(self.delete_deck)
        self.deck_panel.edit_deck_btn.clicked.connect(self.edit_deck)
        self.deck_panel.deck_list.itemClicked.connect(self.select_deck)

        # Flashcard navigation signals
        self.flip_btn.clicked.connect(self.flip_card)
        self.next_btn.clicked.connect(self.next_card)
        self.prev_btn.clicked.connect(self.prev_card)
        self.toggle_notes_btn.clicked.connect(self.toggle_notes)

        # Card management signals
        self.add_card_btn.clicked.connect(self.add_flashcard)
        self.manage_cards_btn.clicked.connect(self.manage_flashcards)
        
        # Stats manager signals
        self.stats_manager.right_btn.clicked.connect(lambda: self.mark_card_feedback(True))
        self.stats_manager.wrong_btn.clicked.connect(lambda: self.mark_card_feedback(False))
        self.stats_manager.cardMarkedRight.connect(lambda idx: self.handle_card_feedback(idx, True))
        self.stats_manager.cardMarkedWrong.connect(lambda idx: self.handle_card_feedback(idx, False))
        
        # Connect flashcard display signals
        self.flashcard_display.cardFlipped.connect(self.handle_card_flip)
        self.flashcard_display.cardChanged.connect(self.handle_card_changed)
        
        # Notes panel signals
        self.notes_panel.save_btn.clicked.connect(self.save_notes)

        # Add stats button signal
        self.stats_btn.clicked.connect(self.show_stats)

    def load_decks(self):
        self.decks = self.data_manager.load_decks()
        self.deck_panel.populate_decks(self.decks)

    def add_deck(self):
        name, ok = QInputDialog.getText(self, "Add New Deck", "Enter deck name:")
        if ok and name:
            # Mengecek duplikat nama
            if any(deck.name == name for deck in self.decks):
                QMessageBox.warning(
                    self, "Warning", "A deck with this name already exists."
                )
                return

            new_deck = Deck(name)
            self.decks.append(new_deck)
            self.data_manager.save_deck(new_deck)
            self.deck_panel.populate_decks(self.decks)

    def delete_deck(self):
        deck_name = self.deck_panel.get_selected_deck_name()
        if not deck_name:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the deck '{deck_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.data_manager.delete_deck(deck_name)
            self.decks = [deck for deck in self.decks if deck.name != deck_name]
            self.deck_panel.populate_decks(self.decks)

            # Hapus tampilan saat ini jika dek yang dihapus dipilih
            if self.current_deck and self.current_deck.name == deck_name:
                self.current_deck = None
                self.stats_manager.set_current_deck(None)  # Reset stats manager's current deck
                self.flashcard_display.show_welcome_screen()
                self.notes_panel.set_card(None)
                
                # Sembunyikan tombol saat tidak ada dek yang dipilih
                self.update_button_visibility(False)

    def edit_deck(self):
        deck_name = self.deck_panel.get_selected_deck_name()
        if not deck_name:
            return

        for deck in self.decks:
            if deck.name == deck_name:
                dialog = RenameDeckDialog(deck, self)
                if dialog.exec():
                    deck_data = dialog.get_deck_data()
                    deck.name = deck_data["name"]
                    self.data_manager.save_deck(deck)
                    self.deck_panel.populate_decks(self.decks)
                break

    def select_deck(self):
        deck_name = self.deck_panel.get_selected_deck_name()
        if deck_name:
            for deck in self.decks:
                if deck.name == deck_name:
                    # Need to save previous deck's study time
                    if self.current_deck:
                        self.stats_manager.stop_timer()
                        self.data_manager.save_deck(self.current_deck)
                    self.current_deck = deck
                    self.stats_manager.set_current_deck(deck)  # Set current deck in StatsManager
                    self.scheduler.update_learning_rate(deck)
                    self.flashcard_display.current_index = self.scheduler.get_next_card_index(deck)
                    showing_front, notes_visible = self.flashcard_display.set_deck(deck)
                    
                    # Mengupdate notes dan stats display
                    self.notes_manager.update_notes_panel(
                        deck, 
                        self.flashcard_display.current_index, 
                        showing_front,
                        notes_visible
                    )
                    
                    # Mengreset stats manager state
                    self.stats_manager.reset_feedback_state()
                    self.stats_manager.update_feedback_buttons(
                        showing_front, 
                        self.flashcard_display.get_current_card()
                    )
                    
                    # Update the toggle notes button (Untuk card sebelum di flip tidak terlihat jawaban nya)
                    self.notes_manager.update_toggle_notes_button(
                        self.toggle_notes_btn,
                        showing_front,
                        notes_visible
                    )
                    
                    # Tampilkan tombol sekarang setelah dek dipilih
                    self.update_button_visibility(True)
                    break

    def flip_card(self):
        showing_front, card = self.flashcard_display.flip_card()
        
        # Update stats display
        self.stats_manager.update_feedback_buttons(showing_front, card)
        
        # Perbarui visibilitas catatan berdasarkan sisi kartu
        self.notes_manager.handle_card_flip(
            not showing_front, 
            self.flashcard_display.notes_visible
        )
        
        # Update toggle notes button
        self.notes_manager.update_toggle_notes_button(
            self.toggle_notes_btn,
            showing_front,
            self.flashcard_display.notes_visible
        )

    def next_card(self):
        # Panggil metode untuk mendapatkan indeks kartu berikutnya dari scheduler
        self.flashcard_display.current_index = self.scheduler.get_next_card_index(self.current_deck)
        self.flashcard_display.showing_front = True
        card = self.flashcard_display.update_card_display()
        self.flashcard_display.cardChanged.emit(self.flashcard_display.current_index, self.flashcard_display.showing_front)

    def prev_card(self):
        # Panggil metode untuk menampilkan kartu sebelumnya
        if self.current_deck and self.current_deck.flashcards:
            self.flashcard_display.current_index = (self.flashcard_display.current_index - 1) % len(self.current_deck.flashcards)
            self.flashcard_display.showing_front = True
            card = self.flashcard_display.update_card_display()
            self.flashcard_display.cardChanged.emit(self.flashcard_display.current_index, self.flashcard_display.showing_front)
        
    def handle_card_changed(self, index, showing_front):
        """Handle card changed event from flashcard display"""
        # Reset feedback state for new card
        self.stats_manager.reset_feedback_state()
        
        # Get the current card
        card = self.flashcard_display.get_current_card()
        
        # Update stats display
        self.stats_manager.update_feedback_buttons(showing_front, card)
        
        # Update notes panel for new card
        self.notes_manager.update_notes_panel(
            self.current_deck, 
            index, 
            showing_front, 
            self.flashcard_display.notes_visible
        )
        
        # Update toggle notes button
        self.notes_manager.update_toggle_notes_button(
            self.toggle_notes_btn,
            showing_front,
            self.flashcard_display.notes_visible
        )

    def toggle_notes(self):
        notes_visible = self.flashcard_display.toggle_notes_visibility()
        self.notes_manager.toggle_notes_visibility(notes_visible)
        self.notes_manager.update_toggle_notes_button(
            self.toggle_notes_btn,
            self.flashcard_display.showing_front,
            notes_visible
        )

    def save_notes(self):
        if self.notes_manager.save_notes() and self.current_deck:
            self.data_manager.save_deck(self.current_deck)
            QMessageBox.information(self, "Success", "Notes saved successfully.")

    def handle_card_flip(self, is_showing_answer):
        self.notes_manager.handle_card_flip(
            is_showing_answer, 
            self.flashcard_display.notes_visible
        )

    def add_flashcard(self):
        if not self.current_deck:
            QMessageBox.warning(self, "Warning", "Please select a deck first.")
            return

        dialog = AddCardDialog(self)
        if dialog.exec():
            card_data = dialog.get_card_data()
            if not card_data["front"] or not card_data["back"]:
                QMessageBox.warning(
                    self, "Warning", "Front and back of the card cannot be empty."
                )
                return

            self.current_deck.add_flashcard(
                card_data["front"], card_data["back"], card_data["notes"]
            )

            # Update the display and save
            card = self.flashcard_display.update_card_display()
            self.stats_manager.update_feedback_buttons(
                self.flashcard_display.showing_front, 
                card
            )
            self.data_manager.save_deck(self.current_deck)

    def manage_flashcards(self):
        if not self.current_deck:
            QMessageBox.warning(self, "Warning", "Please select a deck first.")
            return
            
        dialog = ManageCardsDialog(self.current_deck, self)
        if dialog.exec():
            # Jika perubahan dilakukan pada dialog, perbarui tampilan dan simpan
            card = self.flashcard_display.update_card_display()
            
            # Update stats and notes
            self.stats_manager.reset_feedback_state()
            self.stats_manager.update_feedback_buttons(
                self.flashcard_display.showing_front, 
                card
            )
            
            self.notes_manager.update_notes_panel(
                self.current_deck,
                self.flashcard_display.current_index,
                self.flashcard_display.showing_front,
                self.flashcard_display.notes_visible
            )
            
            self.data_manager.save_deck(self.current_deck)

    def mark_card_feedback(self, is_right):
        """Mark the current card as right or wrong"""
        self.stats_manager.mark_card_feedback(
            is_right, 
            self.flashcard_display.current_index
        )
        card = self.flashcard_display.get_current_card()
        dialog = RateDifficultyDialog(self)
        dialog.exec()  # No need to check dialog result since it always saves
        card.difficulty = dialog.get_difficulty()
        self.scheduler.schedule_card(card, is_right)
        self.data_manager.save_deck(self.current_deck)
        self.stats_manager.update_feedback_buttons(
            self.flashcard_display.showing_front,
            card
        )
       

    def handle_card_feedback(self, card_index, is_right):
        """Handle the card feedback signal"""
        success = self.stats_manager.process_feedback(
            self.current_deck, 
            card_index, 
            is_right
        )
            
        if success and self.current_deck:
            card = self.current_deck.get_flashcard(card_index)
            self.scheduler.schedule_card(card, is_right)
            self.data_manager.save_deck(self.current_deck)

    def show_stats(self):
        """Show statistics for current card"""
        if self.current_deck and self.flashcard_display.get_current_card():
            current_card = self.flashcard_display.get_current_card()
            stats_window = StatsPage(
                card=current_card,
                last_session_score=self.calculate_session_score(),
                total_study_time=self.stats_manager.get_elapsed_time()
            )
            stats_window.exec()  # Use exec() instead of show() for modal dialog
            
            # Update display after potential reset
            self.data_manager.save_deck(self.current_deck)
            self.flashcard_display.update_card_display()
    
    def calculate_session_score(self):
        """Calculate score for current session"""
        if not self.current_deck or not self.current_deck.flashcards:
            return 0
            
        total_right = sum(card.right_count for card in self.current_deck.flashcards)
        total_attempts = sum(card.right_count + card.wrong_count 
                           for card in self.current_deck.flashcards)
        
        return (total_right / total_attempts * 100) if total_attempts > 0 else 0

    def closeEvent(self, event):
        """Save study time when closing app"""
        if self.current_deck:
            self.stats_manager.stop_timer()
            self.data_manager.save_deck(self.current_deck)
        event.accept()