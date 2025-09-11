# perfect_acqua_system/ui/alunos_widgets.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame, 
    QGridLayout, QDateEdit, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QDate, pyqtSignal

class ListaAlunos(QWidget):
    # (O código da ListaAlunos não precisa de alterações, mas é incluído para manter o arquivo completo)
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Lista de Alunos")
        title.setObjectName("Title")
        subtitle = QLabel("Gerencie os alunos cadastrados no sistema")
        subtitle.setObjectName("Subtitle")
        
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 10, 0, 0)
        
        filtros = QHBoxLayout()
        filtros.setSpacing(10)
        filtros.addWidget(QLabel("Filtrar por nome:"))
        filtros.addWidget(QLineEdit(placeholderText="Digite o nome do aluno..."))
        filtros.addStretch()
        top_layout.addLayout(filtros)
        
        self.btn_cadastrar = QPushButton("➕ Cadastrar Aluno")
        self.btn_cadastrar.setProperty("class", "success")
        top_layout.addWidget(self.btn_cadastrar)
        layout.addLayout(top_layout)

        tabela = QTableWidget()
        tabela.verticalHeader().setVisible(False)
        tabela.setColumnCount(5)
        tabela.setHorizontalHeaderLabels(["Aluno", "Plano", "Responsável", "Contato", "Status"])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        dados = [
            ("Pedro Oliveira", "Plano Ouro", "Ele mesmo", "(11) 98888-1111", "Ativo"),
            ("Julia Mendes", "Plano Infantil", "Fernanda Mendes", "(11) 98888-2222", "Ativo"),
        ]
        tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                if col == 4: 
                    color = "#5eead4" if text == "Ativo" else "#f87171"
                    item.setForeground(QColor(color))
                tabela.setItem(row, col, item)
        layout.addWidget(tabela)


class NovoAluno(QWidget):
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        title = QLabel("Cadastro de Aluno")
        title.setObjectName("Title")
        subtitle = QLabel("Preencha os dados de acordo com o modelo de dados")
        subtitle.setObjectName("Subtitle")
        
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)

        form_frame = QFrame()
        form_frame.setProperty("class", "CardFrame") 
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(20)
        
        # --- Formulário alinhado com a tabela `aluno` ---
        grid = QGridLayout()
        grid.setSpacing(15)
        
        grid.addWidget(QLabel("Nome Completo:"), 0, 0)
        grid.addWidget(QLineEdit(placeholderText="Nome do aluno"), 1, 0, 1, 2)
        
        grid.addWidget(QLabel("Data de Nascimento:"), 0, 2)
        grid.addWidget(QDateEdit(calendarPopup=True), 1, 2)
        
        grid.addWidget(QLabel("CPF:"), 2, 0)
        grid.addWidget(QLineEdit(placeholderText="000.000.000-00"), 3, 0)

        grid.addWidget(QLabel("Telefone:"), 2, 1)
        grid.addWidget(QLineEdit(placeholderText="(00) 00000-0000"), 3, 1)
        
        grid.addWidget(QLabel("E-mail:"), 2, 2)
        grid.addWidget(QLineEdit(placeholderText="email@dominio.com"), 3, 2)

        grid.addWidget(QLabel("Endereço:"), 4, 0)
        grid.addWidget(QLineEdit(placeholderText="Rua, número, bairro, cidade..."), 5, 0, 1, 3)

        grid.addWidget(QLabel("Plano:"), 6, 0)
        combo_plano = QComboBox()
        combo_plano.addItems(["Plano mensal", "Plano semestral", "Plano trimestral",])
        grid.addWidget(combo_plano, 7, 0)

        grid.addWidget(QLabel("Status:"), 6, 1)
        combo_status = QComboBox()
        combo_status.addItems(["Ativo", "Inativo"])
        grid.addWidget(combo_status, 7, 1)
        
        form_layout.addLayout(grid)
        form_layout.addStretch()
        
        # --- Botões ---
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