# perfect_acqua_system/ui/main_window.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, 
    QFrame, QLabel, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import QSize

# Importando as telas (widgets)
from ui.dashboard_widget import Dashboard
from ui.financeiro_widget import Financeiro
from ui.alunos_widgets import ListaAlunos, NovoAluno
from ui.ponto_widgets import FolhaDePonto
# Widgets atualizados e novos
from ui.condicao_fisica_widget import CondicaoFisica
from ui.agenda_aulas_widget import AgendaAulas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perfect Acqua System")
        self.setGeometry(100, 100, 1280, 720)
        self.setObjectName("MainWindow")

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setCentralWidget(main_widget)

        # --- Sidebar (Menu Lateral) ---
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("Sidebar")
        sidebar_frame.setFixedWidth(220)
        self.sidebar_layout = QVBoxLayout(sidebar_frame)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Perfect Acqua")
        title.setObjectName("SidebarTitle")
        self.sidebar_layout.addWidget(title)

        self.menu = QListWidget()
        self.menu.setObjectName("SidebarMenu")
        self.menu.setIconSize(QSize(20, 20))
        self.sidebar_layout.addWidget(self.menu)

        # --- Área de Conteúdo (Stacked Widget) ---
        self.content_frame = QFrame()
        self.content_frame.setObjectName("ContentFrame")
        content_layout = QVBoxLayout(self.content_frame)
        
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)

        main_layout.addWidget(sidebar_frame)
        main_layout.addWidget(self.content_frame, 1)

        # --- Páginas ---
        self.dashboard_page = Dashboard()
        self.alunos_page = ListaAlunos()
        self.novo_aluno_page = NovoAluno()
        self.financeiro_page = Financeiro()
        self.ponto_page = FolhaDePonto()
        self.condicao_fisica_page = CondicaoFisica()
        self.agenda_page = AgendaAulas()

        # Dicionário de páginas atualizado com os nomes corretos
        self.pages = {
            "Dashboard": self.stack.addWidget(self.dashboard_page),
            "Alunos": self.stack.addWidget(self.alunos_page),
            "Condições de Saúde": self.stack.addWidget(self.condicao_fisica_page),
            "Agenda de Aulas": self.stack.addWidget(self.agenda_page),
            "Folha de Ponto": self.stack.addWidget(self.ponto_page),
            "Financeiro": self.stack.addWidget(self.financeiro_page),
        }
        
        # Página de "Novo Aluno" não fica no menu principal
        self.stack.addWidget(self.novo_aluno_page)

        # --- Conexões de Sinais ---
        self.populate_menu()
        self.menu.currentItemChanged.connect(self.change_page)
        
        self.alunos_page.btn_cadastrar.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.novo_aluno_page)
        )

        self.novo_aluno_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.alunos_page)
        )

        self.menu.setCurrentRow(0)

    def populate_menu(self):
        for name in self.pages.keys():
            item = QListWidgetItem(name)
            self.menu.addItem(item)
    
    def change_page(self, current_item, previous_item):
        if current_item:
            page_name = current_item.text()
            index = self.pages.get(page_name)
            if index is not None:
                self.stack.setCurrentIndex(index)