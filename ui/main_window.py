# perfect_acqua_system/ui/main_window.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QFrame, QStackedWidget, QListWidgetItem, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QPointF

# Importa as classes das telas que criamos
from .dashboard_widget import Dashboard
from .ponto_widgets import FolhaDePonto
from .alunos_widgets import ListaAlunos, NovoAluno
from .financeiro_widget import Financeiro

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Perfect Acqua System")
        self.setGeometry(100, 50, 1400, 850)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(250)
        shadow1 = QGraphicsDropShadowEffect(blurRadius=30, color=QColor(0,0,0,90), offset=QPointF(0,0))
        sidebar.setGraphicsEffect(shadow1)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 15, 10, 15)

        title = QLabel("💧 Perfect Acqua")
        title.setObjectName("SidebarTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        sidebar_layout.addWidget(title)

        self.menu = QListWidget()
        self.menu.setObjectName("SidebarMenu")
        self.items = [
            ("📊 Dashboard", 0), ("🕒 Folha de Ponto", 1), ("👨‍🎓 Alunos", 2),
            ("➕ Novo Aluno", 3), ("💲 Financeiro", 4),
        ]
        for text, _ in self.items:
            self.menu.addItem(QListWidgetItem(text))
        
        self.menu.setCurrentRow(0)
        sidebar_layout.addWidget(self.menu)
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        content_frame = QFrame()
        content_frame.setObjectName("ContentFrame")
        shadow2 = QGraphicsDropShadowEffect(blurRadius=30, color=QColor(0,0,0,90), offset=QPointF(0,0))
        content_frame.setGraphicsEffect(shadow2)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(25, 25, 25, 25)

        self.stack = QStackedWidget()
        self.dashboard = Dashboard()
        self.folha = FolhaDePonto()
        self.alunos = ListaAlunos()
        self.novo_aluno = NovoAluno()
        self.financeiro = Financeiro()

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.folha)
        self.stack.addWidget(self.alunos)
        self.stack.addWidget(self.novo_aluno)
        self.stack.addWidget(self.financeiro)
        
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_frame, 1)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.alunos.btn_cadastrar.clicked.connect(self.show_novo_aluno_page)

    def show_novo_aluno_page(self):
        for text, index in self.items:
            if "Novo Aluno" in text:
                self.menu.setCurrentRow(index)
                break