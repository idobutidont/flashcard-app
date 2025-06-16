import hashlib
import re
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QHBoxLayout
from Virli_241524062 import FlashcardApp
from Ido_241524047 import UserManager, DataManager

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Validasi username: minimal 5 karakter, hanya huruf/angka/underscore
def valid_username(username):
    return re.fullmatch(r'[A-Za-z0-9_]{5,}', username) is not None

# Validasi password: minimal 8 karakter, huruf besar/kecil, angka, simbol, tanpa spasi
def valid_password(password):
    if len(password) < 8:
        return False
    if ' ' in password:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()-_=+[]{};:',.<>?/\\|`~" for c in password)
    return has_upper and has_lower and has_digit and has_special

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()
        self.setWindowTitle("Login")
        self.resize(680,120)

        from PyQt6.QtGui import QIcon
        self.setWindowIcon(QIcon("images/icon.png"))

        layout = QGridLayout()

        # Informasi kriteria username & password
        info_label = QLabel(
            "<b>Username:</b> min 5 karakter (huruf/angka/_)<br>"
            "<b>Password:</b> min 8 karakter, kombinasi huruf besar, huruf kecil, angka, simbol, tanpa spasi"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #555;")
        # Add info_label below password input, row 3, col 0 spanning 2 columns
        layout.addWidget(info_label, 3, 0, 1, 2)

        # input username
        self.username_input = QLineEdit()
        layout.addWidget(QLabel("Username:"), 0, 0)
        layout.addWidget(self.username_input, 0, 1)

        # input password dengan ikon mata
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        password_layout = QHBoxLayout()
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.addWidget(self.password_input)

        self.toggle_password_button = QPushButton("👁️")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.setFixedWidth(30)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.toggle_password_button)
        layout.addWidget(QLabel("Password:"), 2, 0)
        layout.addLayout(password_layout, 2, 1)

        # Tombol login, register, dan exit
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        self.exit_button = QPushButton("Exit")

        # Set consistent styles for login and register buttons
        login_style = """
            QPushButton {
                background-color: #28a745; /* green */
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #a9d5a9;
                color: #EEE;
            }
        """
        register_style = """
            QPushButton {
                background-color: #007bff; /* blue */
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0069d9;
            }
            QPushButton:disabled {
                background-color: #a6c8ff;
                color: #EEE;
            }
        """
        exit_style = """
            QPushButton {
                background-color: #dc3545; /* red */
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:disabled {
                background-color: #f5a6aa;
                color: #EEE;
            }
        """
        self.login_button.setStyleSheet(login_style)
        self.register_button.setStyleSheet(register_style)
        self.exit_button.setStyleSheet(exit_style)

        layout.addWidget(self.login_button, 4, 0, 1, 2)
        layout.addWidget(self.register_button, 5, 0, 1, 2)
        layout.addWidget(self.exit_button, 6, 0, 1, 2)

        self.setLayout(layout)

        # Koneksi tombol
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
        self.exit_button.clicked.connect(self.close)

        # Tombol hanya aktif jika input tidak kosong
        self.login_button.setEnabled(False)
        self.register_button.setEnabled(False)

        self.username_input.textChanged.connect(self.check_input)
        self.password_input.textChanged.connect(self.check_input)

    # Melihat atau menyembunyikan password
    def toggle_password_visibility(self):
        if self.toggle_password_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password_button.setText("🚫")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password_button.setText("👁️")

    def check_input(self):
        if self.username_input.text() and self.password_input.text():
            self.login_button.setEnabled(True)
            self.register_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)
            self.register_button.setEnabled(False)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        success, message = self.user_manager.authenticate_user(username, password)

        if success:
            QMessageBox.information(self, "Login", "Login successful!")
            self.open_flashcard_app(username)
        else:
            QMessageBox.warning(self, "Login", message)

        self.username_input.clear()
        self.password_input.clear()
        self.toggle_password_button.setChecked(False)
        self.toggle_password_visibility()

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Validasi username
        if not valid_username(username):
            QMessageBox.warning(self, "Register", 
                "Username harus minimal 5 karakter dan hanya boleh mengandung huruf, angka, atau underscore (_).")
            return

        # Validasi password
        if not valid_password(password):
            QMessageBox.warning(self, "Register", 
                "Password harus minimal 8 karakter, mengandung huruf besar, huruf kecil, angka, dan simbol, serta tanpa spasi.")
            return

        success, message = self.user_manager.register_user(username, password)

        if success:
            QMessageBox.information(self, "Register", "Registration successful! You can now login.")
        else:
            QMessageBox.warning(self, "Register", message)
            
        self.username_input.clear()
        self.password_input.clear()
        self.toggle_password_button.setChecked(False)
        self.toggle_password_visibility()
    
    def open_flashcard_app(self, username):
        """Open the flashcard application for the logged-in user"""
        try:
            # Create user-specific data manager
            user_data_manager = DataManager(username)
            
            # Create and show flashcard app
            window = FlashcardApp(self)
            window.data_manager = user_data_manager
            window.set_user(username, self.user_manager)
            window.show()
            
            # Only close login window if flashcard app opened successfully
            self.hide()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open flashcard application: {str(e)}")
