import os
import json
import hashlib
import re
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QHBoxLayout
from Virli_241524062 import FlashcardApp

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
        self.setWindowTitle("Login")
        self.resize(500,120)

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
        layout.addWidget(info_label, 0, 0, 1, 2)

        # input username
        self.username_input = QLineEdit()
        layout.addWidget(QLabel("Username:"), 1, 0)
        layout.addWidget(self.username_input, 1, 1)

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
        button_style = """
            QPushButton {
                background-color: #FF5733;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #FF6F4D;
            }
            QPushButton:disabled {
                background-color: #FFB399;
                color: #EEE;
            }
        """
        self.login_button.setStyleSheet(button_style)
        self.register_button.setStyleSheet(button_style)

        layout.addWidget(self.login_button, 3, 0, 1, 2)
        layout.addWidget(self.register_button, 4, 0, 1, 2)
        layout.addWidget(self.exit_button, 5, 0, 1, 2)

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
        password_hash = hash_password(password)

        if not os.path.exists("data/users.json"):
            QMessageBox.warning(self, "Error", "No users found.")
            return

        with open("data/users.json", "r") as f:
            users = json.load(f)

        if users.get(username) == password_hash:
            QMessageBox.information(self, "Login", "Login successful!")
            window = FlashcardApp()
            window.setHidden(False)
            self.close()
        else:
            QMessageBox.warning(self, "Login", "Invalid username or password.")

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

        password_hash = hash_password(password)

        if os.path.exists("data/users.json"):
            with open("data/users.json", "r") as f:
                users = json.load(f)
        else:
            users = {}

        if username in users:
            QMessageBox.warning(self, "Register", "Username already exists.")
        else:
            users[username] = password_hash
            with open("data/users.json", "w") as f:
                json.dump(users, f)
            QMessageBox.information(self, "Register", "Registration successful.")
            window = FlashcardApp()
            window.setHidden(False)
            window.setHidden(False)
            self.close()
            

        self.username_input.clear()
        self.password_input.clear()
        self.toggle_password_button.setChecked(False)
        self.toggle_password_visibility()
