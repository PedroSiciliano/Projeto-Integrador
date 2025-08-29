# perfect_acqua_system/main.py

import sys
from PyQt6.QtWidgets import QApplication

# Importa os componentes principais
from style import STYLESHEET
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    
    login = LoginDialog()
    
    # Mostra a tela de login. Se o login for bem-sucedido (login.exec() retorna True)...
    if login.exec():
        # ...cria e mostra a janela principal.
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
    else:
        # Se o usuário fechar a tela de login, o programa encerra.
        sys.exit(0)