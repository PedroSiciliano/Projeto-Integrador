# perfect_acqua_system/ui/login_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFrame, QLabel, QLineEdit, QPushButton,
    QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QPointF, QPropertyAnimation, QRect

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Perfect Acqua System")
        self.setObjectName("LoginDialog")
        self.setFixedSize(400, 450)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        login_frame = QFrame()
        login_frame.setObjectName("LoginFrame")
        frame_layout = QVBoxLayout(login_frame)
        frame_layout.setSpacing(15)
        
        shadow = QGraphicsDropShadowEffect(blurRadius=30, color=QColor(0,0,0,90), offset=QPointF(0,0))
        login_frame.setGraphicsEffect(shadow)

        title = QLabel("💧 Perfect Acqua")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("Usuário")
        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("Senha")
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Entrar")
        self.login_button.setProperty("class", "primary")
        self.login_button.setFixedHeight(40)

        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorMessage")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        frame_layout.addWidget(title)
        frame_layout.addSpacing(20)
        frame_layout.addWidget(QLabel("Usuário"))
        frame_layout.addWidget(self.user_edit)
        frame_layout.addWidget(QLabel("Senha"))
        frame_layout.addWidget(self.pass_edit)
        frame_layout.addSpacing(10)
        frame_layout.addWidget(self.login_button)
        frame_layout.addWidget(self.error_label)
        
        main_layout.addWidget(login_frame)

        self.login_button.clicked.connect(self.handle_login)
        self.pass_edit.returnPressed.connect(self.handle_login)

    def handle_login(self):
        if self.user_edit.text() == "admin" and self.pass_edit.text() == "admin123":
            self.accept()
        else:
            self.error_label.setText("Usuário ou senha inválidos.")
            self.shake_window()

    def shake_window(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)
        start_pos = self.geometry()
        x = start_pos.x()
        for i in range(1, 10):
            pos = -10 if i % 2 == 0 else 10
            self.animation.setKeyValueAt(i/10, QRect(x + pos, start_pos.y(), start_pos.width(), start_pos.height()))
        self.animation.setKeyValueAt(1.0, start_pos)
        self.animation.start()