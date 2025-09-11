# perfect_acqua_system/ui/login_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QFrame, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Perfect Acqua System")
        self.setFixedSize(400, 450)
        self.setObjectName("LoginDialog")

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Frame para o conteúdo
        login_frame = QFrame()
        login_frame.setObjectName("LoginFrame")
        login_frame.setFixedWidth(350)
        
        frame_layout = QVBoxLayout(login_frame)
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
        frame_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Campos de entrada
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuário")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Senha")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        frame_layout.addWidget(QLabel("Usuário:"))
        frame_layout.addWidget(self.user_input)
        frame_layout.addWidget(QLabel("Senha:"))
        frame_layout.addWidget(self.pass_input)

        # Mensagem de erro (inicialmente oculta)
        self.error_label = QLabel("Usuário ou senha incorretos.")
        self.error_label.setObjectName("ErrorMessage")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        frame_layout.addWidget(self.error_label)
        
        frame_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Botão de login
        self.login_button = QPushButton("Entrar")
        self.login_button.setProperty("class", "primary")
        self.login_button.clicked.connect(self.check_login)
        self.pass_input.returnPressed.connect(self.check_login)

        frame_layout.addWidget(self.login_button)
        
        main_layout.addWidget(login_frame)

        # Mock de usuário e senha
        self.valid_user = "admin"
        self.valid_pass = "123"

    def check_login(self):
        """Verifica as credenciais de login."""
        user = self.user_input.text()
        password = self.pass_input.text()

        if user == self.valid_user and password == self.valid_pass:
            self.accept()
        else:
            self.error_label.show()