# perfect_acqua_system/ui/instrutores_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame, 
    QGridLayout, QDateEdit
)
from PyQt6.QtCore import pyqtSignal, QDate

class ListaInstrutores(QWidget):
    btn_cadastrar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Gerenciamento de Instrutores")
        # ... (código do cabeçalho e botão permanece o mesmo) ...
        title.setObjectName("Title")
        subtitle = QLabel("Cadastre e gerencie os instrutores da academia")
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        self.btn_cadastrar = QPushButton("➕ Cadastrar Instrutor")
        self.btn_cadastrar.setProperty("class", "success")
        self.btn_cadastrar.clicked.connect(self.btn_cadastrar_clicked.emit)
        top_layout.addWidget(self.btn_cadastrar)
        layout.addLayout(top_layout)
        
        tabela = QTableWidget()

        # --- ESTILO DA TABELA APLICADO AQUI ---
        tabela.setStyleSheet("""
            QTableWidget {
                background-color: #1e293b;
                alternate-background-color: #2b3a4a;
                border: none;
                gridline-color: #4f6987;
            }
            QTableWidget::viewport {
                background-color: #1e293b;
                border: none;
            }
            QHeaderView::section {
                background-color: #2b3a4a;
                color: #94a3b8;
                padding: 4px;
                border: none;
                border-bottom: 1px solid #4f6987;
            }
            QHeaderView::section:horizontal {
                border-right: 1px solid #4f6987;
            }
            QTableCornerButton::section {
                background-color: #2b3a4a;
            }
        """)
        tabela.setAlternatingRowColors(True)

        tabela.verticalHeader().setVisible(False)
        tabela.setColumnCount(4)
        tabela.setHorizontalHeaderLabels(["Nome", "Especialidade", "E-mail", "Telefone"])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        dados = [
            ("Carlos Souza", "Natação Infantil", "carlos.souza@email.com", "(11) 91111-2222"),
            ("Fernanda Lima", "Hidroginástica, Avançado", "fernanda.lima@email.com", "(21) 93333-4444"),
        ]
        
        tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                tabela.setItem(row, col, QTableWidgetItem(text))
        layout.addWidget(tabela)

# A classe NovoInstrutor não foi alterada.
class NovoInstrutor(QWidget):
    # ... (código da classe NovoInstrutor permanece o mesmo) ...
    back_requested = pyqtSignal()
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Cadastro de Instrutor")
        title.setObjectName("Title")
        subtitle = QLabel("Preencha os dados do novo instrutor")
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)
        form_frame = QFrame()
        form_frame.setProperty("class", "CardFrame")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(20)
        grid = QGridLayout()
        grid.setSpacing(15)
        grid.addWidget(QLabel("Nome Completo:"), 0, 0)
        grid.addWidget(QLineEdit(placeholderText="Nome do instrutor"), 1, 0, 1, 2)
        grid.addWidget(QLabel("Data de Nascimento:"), 0, 2)
        grid.addWidget(QDateEdit(calendarPopup=True), 1, 2)
        grid.addWidget(QLabel("CPF:"), 2, 0)
        grid.addWidget(QLineEdit(placeholderText="000.000.000-00"), 3, 0)
        grid.addWidget(QLabel("Telefone:"), 2, 1)
        grid.addWidget(QLineEdit(placeholderText="(00) 00000-0000"), 3, 1)
        grid.addWidget(QLabel("E-mail:"), 2, 2)
        grid.addWidget(QLineEdit(placeholderText="email@dominio.com"), 3, 2)
        grid.addWidget(QLabel("Especialidade(s):"), 4, 0)
        grid.addWidget(QLineEdit(placeholderText="Ex: Natação Infantil, Hidroginástica"), 5, 0, 1, 3)
        form_layout.addLayout(grid)
        form_layout.addStretch()
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        btn_voltar = QPushButton("Voltar")
        btn_voltar.setProperty("class", "secondary")
        btn_voltar.clicked.connect(self.back_requested.emit)
        button_layout.addWidget(btn_voltar)
        save_button = QPushButton("Salvar Cadastro")
        save_button.setProperty("class", "success")
        button_layout.addWidget(save_button)
        form_layout.addLayout(button_layout)
        layout.addWidget(form_frame)
        layout.addStretch()