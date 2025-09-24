# perfect_acqua_system/ui/alunos_widgets.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame, 
    QGridLayout, QDateEdit, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtGui import QColor

class ListaAlunos(QWidget):
    btn_cadastrar_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Lista de Alunos")
        title.setObjectName("Title")
        subtitle = QLabel("Gerencie os alunos cadastrados no sistema")
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        top_layout = QHBoxLayout()
        filtro_label = QLabel("Buscar Aluno:")
        self.filtro_alunos = QLineEdit()
        self.filtro_alunos.setPlaceholderText("Digite o nome ou CPF do aluno...")
        self.filtro_alunos.textChanged.connect(self.aplicar_filtro)
        top_layout.addWidget(filtro_label)
        top_layout.addWidget(self.filtro_alunos)
        top_layout.addStretch()
        self.btn_cadastrar = QPushButton("➕ Cadastrar Aluno")
        self.btn_cadastrar.setProperty("class", "success")
        self.btn_cadastrar.clicked.connect(self.btn_cadastrar_clicked.emit)
        top_layout.addWidget(self.btn_cadastrar)
        layout.addLayout(top_layout)

        self.tabela = QTableWidget()
        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: #1e293b; alternate-background-color: #2b3a4a;
                border: none; gridline-color: #4f6987;
            }
            QTableWidget::viewport { background-color: #1e293b; border: none; }
            QHeaderView::section {
                background-color: #2b3a4a; color: #94a3b8; padding: 4px;
                border: none; border-bottom: 1px solid #4f6987;
            }
            QHeaderView::section:horizontal { border-right: 1px solid #4f6987; }
            QTableCornerButton::section { background-color: #2b3a4a; }
        """)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["Aluno", "Plano", "Responsável", "CPF", "Contato", "Status"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.popular_tabela()
        layout.addWidget(self.tabela)

    def popular_tabela(self):
        dados = [
            ("Pedro Oliveira", "Anual", "Ele mesmo", "111.111.111-11", "(11) 98888-1111", "Ativo"),
            ("Julia Mendes (menor)", "Mensal", "Fernanda Mendes", "222.222.222-22", "(11) 98888-2222", "Ativo"),
            ("Marcos Andrade", "Trimestral", "Ele mesmo", "333.333.333-33", "(21) 97777-6666", "Inativo"),
        ]
        self.tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                if col == 5: 
                    color = "#5eead4" if text == "Ativo" else "#f87171"
                    item.setForeground(QColor(color))
                self.tabela.setItem(row, col, item)

    def aplicar_filtro(self):
        texto_filtro = self.filtro_alunos.text().lower()
        for row in range(self.tabela.rowCount()):
            nome_aluno = self.tabela.item(row, 0).text().lower()
            cpf_aluno = self.tabela.item(row, 3).text().lower()
            if texto_filtro in nome_aluno or texto_filtro in cpf_aluno:
                self.tabela.setRowHidden(row, False)
            else:
                self.tabela.setRowHidden(row, True)

class NovoAluno(QWidget):
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # --- CORREÇÃO FINAL AQUI ---
        # Estilo completo para todos os campos do formulário de cadastro
        self.setStyleSheet("""
            QLineEdit, QDateEdit, QComboBox {
                background-color: #2b3a4a;
                color: #e2e8f0;
                border: 1px solid #4f6987;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border: 1px solid #7dd3fc;
            }
            QComboBox QAbstractItemView {
                background-color: #f8fafc;
                color: #0f172a;
                selection-background-color: #38bdf8;
            }
        """)

        layout = QVBoxLayout(self)
        title = QLabel("Cadastro de Aluno")
        title.setObjectName("Title")
        subtitle = QLabel("Preencha os dados do novo aluno")
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        form_frame = QFrame()
        form_frame.setProperty("class", "CardFrame")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(20)
        
        form_layout.addWidget(self._create_section_header("Dados Pessoais"))
        grid_pessoais = QGridLayout()
        grid_pessoais.setSpacing(15)
        grid_pessoais.addWidget(QLabel("Nome Completo:"), 0, 0)
        grid_pessoais.addWidget(QLineEdit(), 1, 0, 1, 2)
        grid_pessoais.addWidget(QLabel("Data de Nascimento:"), 0, 2)
        grid_pessoais.addWidget(QDateEdit(calendarPopup=True), 1, 2)
        grid_pessoais.addWidget(QLabel("CPF:"), 2, 0)
        grid_pessoais.addWidget(QLineEdit(placeholderText="000.000.000-00"), 3, 0)
        grid_pessoais.addWidget(QLabel("Telefone:"), 2, 1)
        grid_pessoais.addWidget(QLineEdit(placeholderText="(00) 00000-0000"), 3, 1)
        grid_pessoais.addWidget(QLabel("E-mail:"), 2, 2)
        grid_pessoais.addWidget(QLineEdit(), 3, 2)
        grid_pessoais.addWidget(QLabel("Endereço:"), 4, 0)
        grid_pessoais.addWidget(QLineEdit(), 5, 0, 1, 3)
        form_layout.addLayout(grid_pessoais)
        
        form_layout.addSpacerItem(QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        form_layout.addWidget(self._create_section_header("Dados do Responsável (se aluno for menor de idade)"))
        grid_responsavel = QGridLayout()
        grid_responsavel.setSpacing(15)
        grid_responsavel.addWidget(QLabel("Nome do Responsável:"), 0, 0)
        grid_responsavel.addWidget(QLineEdit(), 1, 0)
        grid_responsavel.addWidget(QLabel("CPF do Responsável:"), 0, 1)
        grid_responsavel.addWidget(QLineEdit(placeholderText="000.000.000-00"), 1, 1)
        grid_responsavel.addWidget(QLabel("Telefone do Responsável:"), 0, 2)
        grid_responsavel.addWidget(QLineEdit(placeholderText="(00) 00000-0000"), 1, 2)
        form_layout.addLayout(grid_responsavel)

        form_layout.addSpacerItem(QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        form_layout.addWidget(self._create_section_header("Dados da Matrícula"))
        grid_matricula = QGridLayout()
        grid_matricula.setSpacing(15)
        grid_matricula.addWidget(QLabel("Plano:"), 0, 0)
        self.combo_plano = QComboBox()
        self.combo_plano.addItems(["Selecione o Plano", "Mensal", "Trimestral", "Quadrimestral", "Anual"])
        grid_matricula.addWidget(self.combo_plano, 1, 0)
        grid_matricula.addWidget(QLabel("Status:"), 0, 1)
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Ativo", "Inativo"])
        grid_matricula.addWidget(self.combo_status, 1, 1)
        form_layout.addLayout(grid_matricula)
        
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

    def _create_section_header(self, text):
        label = QLabel(text)
        label.setObjectName("SectionHeader")
        return label