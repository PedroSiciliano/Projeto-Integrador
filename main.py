<<<<<<< HEAD
# main.py
=======
# perfect_acqua_system/main.py

>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
import sys
from PyQt6.QtWidgets import QApplication
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from style import STYLESHEET
<<<<<<< HEAD
import database

def main():
    # Garante que as tabelas do banco de dados existam
    database.criar_tabelas()

    app = QApplication(sys.argv)

    # Aplica a folha de estilos importada do arquivo style.py
    app.setStyleSheet(STYLESHEET)

    login_dialog = LoginDialog()
    if login_dialog.exec():
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == '__main__':
=======

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
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
    main()