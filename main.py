# perfect_acqua_system/main.py

import sys
from PyQt6.QtWidgets import QApplication
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from style import STYLESHEET

def main():
    """Ponto de entrada principal da aplicação."""
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)  # Aplica o estilo globalmente

    login = LoginDialog()
    # A verificação de login é feita dentro da própria classe LoginDialog
    if login.exec():
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()