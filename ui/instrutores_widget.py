# perfect_acqua_system/ui/instrutores_widget.py
import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame,
    QGridLayout, QDateEdit, QMessageBox
)
from PyQt6.QtCore import pyqtSignal

class ListaInstrutores(QWidget):
    btn_cadastrar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Gerenciamento de Instrutores")
        title.setObjectName("Title")
        # ... (Resto do __init__ igual)
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
        
        self.tabela = QTableWidget()
        self.tabela.setAlternatingRowColors(True)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "Especialidade", "E-mail", "Telefone"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela.setColumnHidden(0, True)

        self.popular_tabela()
        layout.addWidget(self.tabela)

    def popular_tabela(self):
        dados = database.buscar_instrutores()
        self.tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                self.tabela.setItem(row, col, QTableWidgetItem(str(text)))

class NovoInstrutor(QWidget):
    back_requested = pyqtSignal()
    instrutor_salvo = pyqtSignal() # --- CORREÇÃO: Sinal para avisar que salvou ---

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Cadastro de Instrutor")
        # ... (Layout do formulário igual ao anterior, mas com nomes para os inputs)
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
        self.nome_input = QLineEdit(placeholderText="Nome do instrutor")
        grid.addWidget(self.nome_input, 1, 0, 1, 2)
        grid.addWidget(QLabel("Data de Nascimento:"), 0, 2)
        self.data_nasc_input = QDateEdit(calendarPopup=True)
        grid.addWidget(self.data_nasc_input, 1, 2)
        
        grid.addWidget(QLabel("CPF:"), 2, 0)
        self.cpf_input = QLineEdit(placeholderText="000.000.000-00")
        grid.addWidget(self.cpf_input, 3, 0)
        grid.addWidget(QLabel("Telefone:"), 2, 1)
        self.tel_input = QLineEdit(placeholderText="(00) 00000-0000")
        grid.addWidget(self.tel_input, 3, 1)
        grid.addWidget(QLabel("E-mail:"), 2, 2)
        self.email_input = QLineEdit(placeholderText="email@dominio.com")
        grid.addWidget(self.email_input, 3, 2)
        
        grid.addWidget(QLabel("Especialidade(s):"), 4, 0)
        self.esp_input = QLineEdit(placeholderText="Ex: Natação Infantil, Hidroginástica")
        grid.addWidget(self.esp_input, 5, 0, 1, 3)
        
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
        
        # --- CORREÇÃO: Botão conectado ---
        save_button.clicked.connect(self.salvar_instrutor)
        
        button_layout.addWidget(save_button)
        form_layout.addLayout(button_layout)
        layout.addWidget(form_frame)
        layout.addStretch()

    def salvar_instrutor(self):
        nome = self.nome_input.text()
        data_nasc = self.data_nasc_input.date().toString("yyyy-MM-dd")
        cpf = self.cpf_input.text()
        email = self.email_input.text()
        tel = self.tel_input.text()
        esp = self.esp_input.text()

        if not nome or not cpf:
            QMessageBox.warning(self, "Erro de Validação", "Nome e CPF são campos obrigatórios.")
            return

        try:
            database.adicionar_instrutor(nome, data_nasc, cpf, email, tel, esp)
            QMessageBox.information(self, "Sucesso", "Instrutor cadastrado com sucesso!")
            self.instrutor_salvo.emit()
            self.back_requested.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro no Banco de Dados", f"Não foi possível salvar o instrutor.\nErro: {e}")