# perfect_acqua_system/ui/login_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt


class LoginDialog(QDialog):
    """
    Tela de login simples (mock).
    No futuro pode ser integrada ao Supabase Auth sem mudanças estruturais.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Login - Perfect Acqua System")
        self.setFixedSize(400, 450)
        self.setObjectName("LoginDialog")

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Frame
        frame = QFrame()
        frame.setObjectName("LoginFrame")
        frame.setFixedWidth(330)

        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(15)

        # Títulos
        title = QLabel("Bem-vindo de volta!")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Acesse o sistema com suas credenciais")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame_layout.addWidget(title)
        frame_layout.addWidget(subtitle)

        frame_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Inputs
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuário")
        self.user_input.setClearButtonEnabled(True)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Senha")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setClearButtonEnabled(True)

        frame_layout.addWidget(QLabel("Usuário:"))
        frame_layout.addWidget(self.user_input)
        frame_layout.addWidget(QLabel("Senha:"))
        frame_layout.addWidget(self.pass_input)

        # Erro
        self.error_label = QLabel("Usuário ou senha incorretos.")
        self.error_label.setObjectName("ErrorMessage")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        frame_layout.addWidget(self.error_label)

        frame_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botão login
        self.login_button = QPushButton("Entrar")
        self.login_button.setProperty("class", "primary")
        self.login_button.clicked.connect(self.check_login)

        # Enter pressionado = login
        self.pass_input.returnPressed.connect(self.check_login)

        frame_layout.addWidget(self.login_button)

        layout.addWidget(frame)

        # Mock de credenciais (pode ser substituído por Supabase Auth futuramente)
        self.valid_user = "admin"
        self.valid_pass = "123"

    # ==========================================================
    # VERIFICAÇÃO DE LOGIN
    # ==========================================================
    def check_login(self):
        """Valida as credenciais mockadas."""
        user = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if user == self.valid_user and password == self.valid_pass:
            self.error_label.hide()
            self.accept()
        else:
            self.error_label.show()
            self.pass_input.clear()
            self.pass_input.setFocus()
