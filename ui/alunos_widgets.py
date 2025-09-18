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

        # --- ALTERAÇÃO AQUI: Adicionada folha de estilo para corrigir as cores ---
        self.setStyleSheet("""
            /* Define fundo escuro e texto branco para os campos de entrada */
            QLineEdit, QDateEdit, QComboBox {
                background-color: #2b3a4a;
                color: white;
                border: 1px solid #4f6987;
                border-radius: 4px;
                padding: 4px;
            }
            /* Define fundo branco e texto PRETO para a lista suspensa */
            QComboBox QAbstractItemView {
                color: black;
                background-color: white;
                selection-background-color: #0078d7;
                border: 1px solid lightgray;
            }
        """)
        
        # --- Cabeçalho ---
        title = QLabel("Cadastro de Aluno")
        title.setObjectName("Title")
        subtitle = QLabel("Preencha todos os dados para a matrícula do aluno")
        subtitle.setObjectName("Subtitle")
        
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)

        # --- Frame principal do formulário ---
        form_frame = QFrame()
        form_frame.setProperty("class", "CardFrame") 
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(20)

        def create_section_title(text):
            label = QLabel(text)
            label.setObjectName("Subtitle")
            label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
            return label

        # --- Seção: Dados Pessoais ---
        form_layout.addWidget(create_section_title("Dados Pessoais"))
        pessoais_grid = QGridLayout()
        pessoais_grid.setSpacing(15)
        
        pessoais_grid.addWidget(QLabel("Nome Completo:"), 0, 0, 1, 2)
        pessoais_grid.addWidget(QLineEdit(placeholderText="Nome completo do aluno"), 1, 0, 1, 2)
        
        pessoais_grid.addWidget(QLabel("CPF:"), 2, 0)
        pessoais_grid.addWidget(QLineEdit(placeholderText="000.000.000-00"), 3, 0)

        pessoais_grid.addWidget(QLabel("RG:"), 2, 1)
        pessoais_grid.addWidget(QLineEdit(placeholderText="00.000.000-0"), 3, 1)
        
        pessoais_grid.addWidget(QLabel("Telefone:"), 4, 0)
        pessoais_grid.addWidget(QLineEdit(placeholderText="(00) 00000-0000"), 5, 0)
        
        pessoais_grid.addWidget(QLabel("E-mail:"), 4, 1)
        pessoais_grid.addWidget(QLineEdit(placeholderText="email@dominio.com"), 5, 1)

        pessoais_grid.addWidget(QLabel("Data de Nascimento:"), 0, 2)
        date_nasc = QDateEdit(calendarPopup=True)
        date_nasc.setDate(QDate.fromString("2000-01-01", "yyyy-MM-dd"))
        pessoais_grid.addWidget(date_nasc, 1, 2)
        
        pessoais_grid.addWidget(QLabel("Gênero:"), 2, 2)
        combo_genero = QComboBox()
        combo_genero.addItems(["Masculino", "Feminino", "Outro"])
        pessoais_grid.addWidget(combo_genero, 3, 2)

        form_layout.addLayout(pessoais_grid)

        # --- Seção: Endereço ---
        form_layout.addWidget(create_section_title("Endereço"))
        endereco_grid = QGridLayout()
        endereco_grid.setSpacing(15)

        endereco_grid.addWidget(QLabel("CEP:"), 0, 0)
        endereco_grid.addWidget(QLineEdit(placeholderText="00000-000"), 1, 0)

        endereco_grid.addWidget(QLabel("Logradouro (Rua, Av.):"), 0, 1)
        endereco_grid.addWidget(QLineEdit(), 1, 1)

        endereco_grid.addWidget(QLabel("Número:"), 2, 0)
        endereco_grid.addWidget(QLineEdit(), 3, 0)
        
        endereco_grid.addWidget(QLabel("Bairro:"), 2, 1)
        endereco_grid.addWidget(QLineEdit(), 3, 1)

        endereco_grid.addWidget(QLabel("Cidade:"), 2, 2)
        endereco_grid.addWidget(QLineEdit(), 3, 2)

        endereco_grid.addWidget(QLabel("UF:"), 2, 3)
        combo_uf = QComboBox()
        combo_uf.addItems(["SP", "RJ", "MG", "BA", "DF", "GO", "PR", "SC", "RS"])
        endereco_grid.addWidget(combo_uf, 3, 3)

        endereco_grid.setColumnStretch(1, 1)
        form_layout.addLayout(endereco_grid)

        # --- Seção: Dados do Responsável ---
        form_layout.addWidget(create_section_title("Dados do Responsável (se menor de idade)"))
        responsavel_grid = QGridLayout()
        responsavel_grid.setSpacing(15)

        responsavel_grid.addWidget(QLabel("Nome do Responsável:"), 0, 0)
        responsavel_grid.addWidget(QLineEdit(), 1, 0)

        responsavel_grid.addWidget(QLabel("CPF do Responsável:"), 0, 1)
        responsavel_grid.addWidget(QLineEdit(placeholderText="000.000.000-00"), 1, 1)

        responsavel_grid.addWidget(QLabel("Telefone do Responsável:"), 0, 2)
        responsavel_grid.addWidget(QLineEdit(placeholderText="(00) 00000-0000"), 1, 2)
        
        responsavel_grid.setColumnStretch(0, 2)
        responsavel_grid.setColumnStretch(1, 1)
        responsavel_grid.setColumnStretch(2, 1)
        form_layout.addLayout(responsavel_grid)
        
        # --- Seção: Dados da Matrícula ---
        form_layout.addWidget(create_section_title("Dados da Matrícula"))
        matricula_grid = QGridLayout()
        matricula_grid.setSpacing(15)

        matricula_grid.addWidget(QLabel("Plano / Turma:"), 0, 0)
        combo_plano = QComboBox()
        # --- ALTERAÇÃO AQUI: Atualiza os itens da lista de planos ---
        combo_plano.addItems(["mensal", "trimestral", "semestral"])
        matricula_grid.addWidget(combo_plano, 1, 0)

        matricula_grid.addWidget(QLabel("Data da Matrícula:"), 0, 1)
        date_matricula = QDateEdit(calendarPopup=True)
        date_matricula.setDate(QDate.fromString("2025-09-11", "yyyy-MM-dd"))
        matricula_grid.addWidget(date_matricula, 1, 1)
        
        matricula_grid.addWidget(QLabel("Status:"), 0, 2)
        combo_status = QComboBox()
        # --- ALTERAÇÃO AQUI: Atualiza os itens da lista de status ---
        combo_status.addItems(["ativo", "inativo"])
        matricula_grid.addWidget(combo_status, 1, 2)
        
        matricula_grid.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), 1, 3)
        form_layout.addLayout(matricula_grid)
        
        # --- Botões de Ação ---
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