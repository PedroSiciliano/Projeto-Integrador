# perfect_acqua_system/ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QFrame, QLabel, QListWidget, QListWidgetItem

from ui.dashboard_widget import Dashboard
from ui.financeiro_widget import Financeiro
from ui.alunos_widgets import ListaAlunos, NovoAluno
from ui.ponto_widgets import FolhaDePonto
from ui.condicao_fisica_widget import CondicaoFisica
from ui.agenda_aulas_widget import AgendaAulas
from ui.instrutores_widget import ListaInstrutores, NovoInstrutor
from ui.despesas_widget import Despesas

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
        self.sidebar_layout.addWidget(self.menu)

        self.content_frame = QFrame()
        self.content_frame.setObjectName("ContentFrame")
        content_layout = QVBoxLayout(self.content_frame)
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        main_layout.addWidget(sidebar_frame)
        main_layout.addWidget(self.content_frame, 1)

        self.dashboard_page = Dashboard()
        self.alunos_page = ListaAlunos()
        self.novo_aluno_page = NovoAluno()
        self.instrutores_page = ListaInstrutores()
        self.novo_instrutor_page = NovoInstrutor()
        self.condicao_fisica_page = CondicaoFisica()
        self.agenda_page = AgendaAulas()
        self.ponto_page = FolhaDePonto()
        self.financeiro_page = Financeiro()
        self.despesas_page = Despesas()

        self.pages = {
            "Dashboard": self.stack.addWidget(self.dashboard_page),
            "Alunos": self.stack.addWidget(self.alunos_page),
            "Instrutores": self.stack.addWidget(self.instrutores_page),
            "Condições de Saúde": self.stack.addWidget(self.condicao_fisica_page),
            "Agenda de Aulas": self.stack.addWidget(self.agenda_page),
            "Folha de Ponto": self.stack.addWidget(self.ponto_page),
            "Financeiro": self.stack.addWidget(self.financeiro_page),
            "Despesas": self.stack.addWidget(self.despesas_page),
        }

        self.stack.addWidget(self.novo_aluno_page)
        self.stack.addWidget(self.novo_instrutor_page)

        self.populate_menu()
        self.menu.currentItemChanged.connect(self.change_page)

        self.alunos_page.btn_cadastrar_clicked.connect(lambda: self.stack.setCurrentWidget(self.novo_aluno_page))
        self.instrutores_page.btn_cadastrar_clicked.connect(lambda: self.stack.setCurrentWidget(self.novo_instrutor_page))

        self.novo_aluno_page.back_requested.connect(lambda: self.stack.setCurrentWidget(self.alunos_page))
        self.novo_instrutor_page.back_requested.connect(lambda: self.stack.setCurrentWidget(self.instrutores_page))

        # --- Conexões Definitivas para Atualização Automática ---
        self.novo_aluno_page.aluno_salvo.connect(self.alunos_page.popular_tabela)
        self.novo_aluno_page.aluno_salvo.connect(self.financeiro_page.popular_tabela)
        self.novo_aluno_page.aluno_salvo.connect(self.dashboard_page.refresh_data)
        self.novo_aluno_page.aluno_salvo.connect(self.condicao_fisica_page.popular_lista_alunos)

        self.novo_instrutor_page.instrutor_salvo.connect(self.instrutores_page.popular_tabela)
        
        self.despesas_page.despesa_salva.connect(self.dashboard_page.refresh_data)
        
        self.financeiro_page.mensalidade_paga.connect(self.dashboard_page.refresh_data)
        self.financeiro_page.mensalidade_paga.connect(self.financeiro_page.popular_tabela)
        
        self.ponto_page.ponto_registrado.connect(self.ponto_page.aplicar_filtros)
        
        self.agenda_page.aula_salva.connect(self.agenda_page.popular_tabela)

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
                if self.stack.widget(index) == self.dashboard_page:
                    self.dashboard_page.refresh_data()
                self.stack.setCurrentIndex(index)