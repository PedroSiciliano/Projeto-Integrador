# perfect_acqua_system/ui/alunos_widgets.py
import database
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame, QGridLayout, QDateEdit, QComboBox, QSpacerItem, QSizePolicy, QMessageBox
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
        self.filtro_alunos = QLineEdit(placeholderText="Digite o nome do aluno...")
        top_layout.addWidget(self.filtro_alunos)
        top_layout.addStretch()
        self.btn_cadastrar = QPushButton("➕ Cadastrar Aluno")
        self.btn_cadastrar.setProperty("class", "success")
        self.btn_cadastrar.clicked.connect(self.btn_cadastrar_clicked.emit)
        top_layout.addWidget(self.btn_cadastrar)
        layout.addLayout(top_layout)

        self.tabela = QTableWidget()
        self.tabela.setAlternatingRowColors(True)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["ID", "Aluno", "Plano", "Responsável", "Contato Resp.", "Status"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela.setColumnHidden(0, True)
        self.popular_tabela()
        layout.addWidget(self.tabela)

    def popular_tabela(self):
        dados = database.buscar_alunos()
        self.tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                item = QTableWidgetItem(str(text or "-"))
                if col == 5:
                    color = "#5eead4" if str(text) == "Ativo" else "#f87171"
                    item.setForeground(QColor(color))
                self.tabela.setItem(row, col, item)

class NovoAluno(QWidget):
    back_requested = pyqtSignal()
    aluno_salvo = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Cadastro de Aluno")
        title.setObjectName("Title")
        layout.addWidget(title)

        form_frame = QFrame()
        form_frame.setProperty("class", "CardFrame")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        
        form_layout.addWidget(self._create_section_header("Dados Pessoais"))
        grid_pessoais = QGridLayout()
        self.nome_input = QLineEdit()
        self.data_nasc_input = QDateEdit(calendarPopup=True)
        self.cpf_input = QLineEdit(placeholderText="000.000.000-00")
        self.tel_input = QLineEdit(placeholderText="(00) 00000-0000")
        self.email_input = QLineEdit()
        self.end_input = QLineEdit()
        grid_pessoais.addWidget(QLabel("Nome Completo:"), 0, 0)
        grid_pessoais.addWidget(self.nome_input, 1, 0, 1, 2)
        grid_pessoais.addWidget(QLabel("Data de Nascimento:"), 0, 2)
        grid_pessoais.addWidget(self.data_nasc_input, 1, 2)
        grid_pessoais.addWidget(QLabel("CPF:"), 2, 0)
        grid_pessoais.addWidget(self.cpf_input, 3, 0)
        grid_pessoais.addWidget(QLabel("Telefone:"), 2, 1)
        grid_pessoais.addWidget(self.tel_input, 3, 1)
        grid_pessoais.addWidget(QLabel("E-mail:"), 2, 2)
        grid_pessoais.addWidget(self.email_input, 3, 2)
        grid_pessoais.addWidget(QLabel("Endereço:"), 4, 0)
        grid_pessoais.addWidget(self.end_input, 5, 0, 1, 3)
        form_layout.addLayout(grid_pessoais)
        
        form_layout.addWidget(self._create_section_header("Dados do Responsável (se menor de idade)"))
        grid_responsavel = QGridLayout()
        self.resp_nome_input = QLineEdit()
        self.resp_cpf_input = QLineEdit(placeholderText="000.000.000-00")
        self.resp_tel_input = QLineEdit(placeholderText="(00) 00000-0000")
        grid_responsavel.addWidget(QLabel("Nome do Responsável:"), 0, 0)
        grid_responsavel.addWidget(self.resp_nome_input, 1, 0)
        grid_responsavel.addWidget(QLabel("CPF do Responsável:"), 0, 1)
        grid_responsavel.addWidget(self.resp_cpf_input, 1, 1)
        grid_responsavel.addWidget(QLabel("Telefone do Responsável:"), 0, 2)
        grid_responsavel.addWidget(self.resp_tel_input, 1, 2)
        form_layout.addLayout(grid_responsavel)

        form_layout.addWidget(self._create_section_header("Dados da Matrícula"))
        grid_matricula = QGridLayout()
        self.combo_plano = QComboBox()
        self.planos = {f"{nome} - R$ {valor:.2f}": id_ for id_, nome, valor in database.buscar_planos()}
        self.combo_plano.addItems(self.planos.keys())
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Ativo", "Inativo"])
        grid_matricula.addWidget(QLabel("Plano:"), 0, 0)
        grid_matricula.addWidget(self.combo_plano, 1, 0)
        grid_matricula.addWidget(QLabel("Status:"), 0, 1)
        grid_matricula.addWidget(self.combo_status, 1, 1)
        form_layout.addLayout(grid_matricula)
        
        form_layout.addStretch()
        
        button_layout = QHBoxLayout()
        btn_voltar = QPushButton("Voltar")
        btn_voltar.setProperty("class", "secondary")
        btn_voltar.clicked.connect(self.back_requested.emit)
        save_button = QPushButton("Salvar Cadastro")
        save_button.setProperty("class", "success")
        save_button.clicked.connect(self.salvar_aluno)
        button_layout.addStretch()
        button_layout.addWidget(btn_voltar)
        button_layout.addWidget(save_button)
        form_layout.addLayout(button_layout)
        
        layout.addWidget(form_frame)
        layout.addStretch()

    def salvar_aluno(self):
        nome = self.nome_input.text().strip()
        cpf = self.cpf_input.text().strip()
        resp_nome = self.resp_nome_input.text().strip()
        resp_cpf = self.resp_cpf_input.text().strip()

        if not nome or not cpf:
            QMessageBox.warning(self, "Erro de Validação", "Nome e CPF do aluno são campos obrigatórios.")
            return
        
        if resp_nome and not resp_cpf:
            QMessageBox.warning(self, "Erro de Validação", "Se o nome do responsável for preenchido, o CPF dele também é obrigatório.")
            return

        try:
            database.adicionar_aluno(
                nome, self.data_nasc_input.date().toString("yyyy-MM-dd"), cpf,
                self.tel_input.text(), self.email_input.text(), self.end_input.text(),
                self.combo_status.currentText(), resp_nome, resp_cpf, self.resp_tel_input.text(),
                self.planos[self.combo_plano.currentText()]
            )
            QMessageBox.information(self, "Sucesso", "Aluno cadastrado com sucesso!")
            self.aluno_salvo.emit()
            self.back_requested.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível salvar.\nErro: {e}")

    def _create_section_header(self, text):
        label = QLabel(text)
        label.setObjectName("SectionHeader")
        return label