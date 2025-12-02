# main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from style import STYLESHEET
import database

# inicia sync background
try:
    database.start_background_sync(interval_seconds=15)
except Exception as e:
    print("Warning: não foi possível iniciar background sync:", e)


def main():
    # Garante que as tabelas do banco de dados existam
    #database.criar_tabelas()

    app = QApplication(sys.argv)

    # Aplica a folha de estilos importada do arquivo style.py
    app.setStyleSheet(STYLESHEET)

    login_dialog = LoginDialog()
    if login_dialog.exec():
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    main()