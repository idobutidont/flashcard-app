import os
import json
import hashlib
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
from Virli_241524062 import FlashcardApp

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(500,120)

        layout = QGridLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(QLabel("Username:"), 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(QLabel("Password:"), 1, 0)
        layout.addWidget(self.password_input, 1, 1)

        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        self.exit_button = QPushButton("Exit")

        layout.addWidget(self.login_button, 2, 0, 1, 2)
        layout.addWidget(self.register_button, 3, 0, 1, 2)
        layout.addWidget(self.exit_button, 4, 0, 1, 2)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
        self.exit_button.clicked.connect(self.close)

        self.login_button.setEnabled(False)
        self.register_button.setEnabled(False)

        self.username_input.textChanged.connect(self.check_input)
        self.password_input.textChanged.connect(self.check_input)

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
        else:
            QMessageBox.warning(self, "Login", "Invalid username or password.")

        self.username_input.clear()
        self.password_input.clear()

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
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
            

        self.username_input.clear()
        self.password_input.clear()
