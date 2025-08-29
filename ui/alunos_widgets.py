# perfect_acqua_system/ui/alunos_widgets.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame, QGridLayout, QDateEdit
)
from PyQt6.QtGui import QColor

class ListaAlunos(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Lista de Alunos")
        title.setObjectName("Title")
        subtitle = QLabel("Gerencie os alunos cadastrados")
        subtitle.setObjectName("Subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        top_layout = QHBoxLayout()
        filtros = QHBoxLayout()
        filtros.setSpacing(10)
        filtros.addWidget(QLabel("Nome:"))
        filtros.addWidget(QLineEdit())
        filtros.addStretch()
        top_layout.addLayout(filtros)
        
        self.btn_cadastrar = QPushButton("➕ Cadastrar aluno")
        self.btn_cadastrar.setProperty("class", "success")
        top_layout.addWidget(self.btn_cadastrar)
        layout.addLayout(top_layout)

        tabela = QTableWidget()
        tabela.verticalHeader().setVisible(False)
        tabela.setColumnCount(5)
        tabela.setHorizontalHeaderLabels(["Aluno", "Turma", "Responsável", "Contato", "Status"])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        dados = [
            ("Pedro Oliveira", "Piscina Adulta", "Ele mesmo", "(11) 98888-1111", "Ativo"),
            ("Julia Mendes", "Piscina Infantil", "Fernanda Mendes", "(11) 98888-2222", "Ativo"),
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
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Cadastro de Aluno")
        title.setObjectName("Title")
        subtitle = QLabel("Preencha os dados do novo aluno")
        subtitle.setObjectName("Subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #1e293b; border-radius: 12px; padding: 25px; border: 1px solid #334155; margin-top: 15px;")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        section1 = QLabel("Dados Pessoais")
        section1.setObjectName("SectionHeader")
        form_layout.addWidget(section1)
        grid_pessoais = QGridLayout()
        grid_pessoais.setSpacing(15)
        grid_pessoais.addWidget(QLabel("Nome Completo *"), 0, 0)
        grid_pessoais.addWidget(QLineEdit(placeholderText="Digite o nome completo"), 1, 0)
        grid_pessoais.addWidget(QLabel("Data de Nascimento *"), 0, 1)
        grid_pessoais.addWidget(QDateEdit(calendarPopup=True), 1, 1)
        grid_pessoais.addWidget(QLabel("CPF"), 2, 0)
        grid_pessoais.addWidget(QLineEdit(inputMask="000.000.000-00", placeholderText="000.000.000-00"), 3, 0)
        grid_pessoais.addWidget(QLabel("Telefone"), 2, 1)
        grid_pessoais.addWidget(QLineEdit(inputMask="(00) 00000-0000", placeholderText="(00) 00000-0000"), 3, 1)
        form_layout.addLayout(grid_pessoais)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        save_button = QPushButton("Salvar Cadastro")
        save_button.setProperty("class", "success")
        save_button.setMinimumHeight(45)
        button_layout.addWidget(save_button)
        form_layout.addStretch()
        form_layout.addLayout(button_layout)
        layout.addWidget(form_frame)