# perfect_acqua_system/ui/instrutores_widget.py

import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QFrame,
    QGridLayout, QMessageBox
)
from PyQt6.QtCore import pyqtSignal


def _normalize_instrutor_record(rec):
    """
    Normaliza o registro do instrutor conforme a tabela real do Supabase.
    Campos reais:
        - id_instrutor
        - nome_completo
        - cref
        - telefone
        - cpf
        - especialidade
    """
    out = {
        "id": None,
        "nome": "",
        "cref": "",
        "telefone": "",
        "cpf": "",
        "especialidade": "",
    }

    if rec is None:
        return out

    if isinstance(rec, dict):
        out["id"] = rec.get("id_instrutor") or rec.get("id")
        out["nome"] = rec.get("nome_completo") or rec.get("nome") or ""
        out["cref"] = rec.get("cref") or ""
        out["telefone"] = rec.get("telefone") or ""
        out["cpf"] = rec.get("cpf") or ""
        out["especialidade"] = rec.get("especialidade") or ""
        return out

    if isinstance(rec, (list, tuple)):
        seq = list(rec)
        out["id"] = seq[0] if len(seq) > 0 else None
        out["nome"] = seq[1] if len(seq) > 1 else ""
        out["cref"] = seq[2] if len(seq) > 2 else ""
        out["telefone"] = seq[3] if len(seq) > 3 else ""
        out["cpf"] = seq[4] if len(seq) > 4 else ""
        out["especialidade"] = seq[5] if len(seq) > 5 else ""
        return out

    out["nome"] = str(rec)
    return out


# =====================================================================
# LISTA DE INSTRUTORES
# =====================================================================
class ListaInstrutores(QWidget):
    btn_cadastrar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Gerenciamento de Instrutores")
        title.setObjectName("Title")

        subtitle = QLabel("Cadastre e gerencie os instrutores da academia")

        header = QVBoxLayout()
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # Botão cadastrar
        top = QHBoxLayout()
        top.addStretch()
        btn = QPushButton("➕ Cadastrar Instrutor")
        btn.setProperty("class", "success")
        btn.clicked.connect(self.btn_cadastrar_clicked.emit)
        top.addWidget(btn)
        layout.addLayout(top)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Nome", "CREF", "Telefone", "CPF", "Especialidade"]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela.setColumnHidden(0, True)

        layout.addWidget(self.tabela)

        self.popular_tabela()

    def popular_tabela(self):
        try:
            dados = database.buscar_instrutores()
        except Exception:
            dados = []

        self.tabela.setRowCount(len(dados))

        for row, rec in enumerate(dados):
            norm = _normalize_instrutor_record(rec)

            self.tabela.setItem(row, 0, QTableWidgetItem(str(norm["id"])))
            self.tabela.setItem(row, 1, QTableWidgetItem(norm["nome"]))
            self.tabela.setItem(row, 2, QTableWidgetItem(norm["cref"]))
            self.tabela.setItem(row, 3, QTableWidgetItem(norm["telefone"]))
            self.tabela.setItem(row, 4, QTableWidgetItem(norm["cpf"]))
            self.tabela.setItem(row, 5, QTableWidgetItem(norm["especialidade"]))


# =====================================================================
# CADASTRO DE INSTRUTOR
# =====================================================================
class NovoInstrutor(QWidget):
    back_requested = pyqtSignal()
    instrutor_salvo = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Cadastro de Instrutor")
        title.setObjectName("Title")

        subtitle = QLabel("Preencha os dados do novo instrutor")

        header = QVBoxLayout()
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # Card
        card = QFrame()
        card.setProperty("class", "CardFrame")
        form = QVBoxLayout(card)

        grid = QGridLayout()

        # Nome
        grid.addWidget(QLabel("Nome Completo:"), 0, 0)
        self.nome_input = QLineEdit()
        grid.addWidget(self.nome_input, 1, 0, 1, 3)

        # CREF
        grid.addWidget(QLabel("CREF:"), 2, 0)
        self.cref_input = QLineEdit()
        grid.addWidget(self.cref_input, 3, 0)

        # Telefone
        grid.addWidget(QLabel("Telefone:"), 2, 1)
        self.telefone_input = QLineEdit()
        grid.addWidget(self.telefone_input, 3, 1)

        # Email (opcional, não aparece na tabela)
        grid.addWidget(QLabel("Email:"), 2, 2)
        self.email_input = QLineEdit()
        grid.addWidget(self.email_input, 3, 2)

        # CPF
        grid.addWidget(QLabel("CPF:"), 4, 0)
        self.cpf_input = QLineEdit()
        grid.addWidget(self.cpf_input, 5, 0)

        # Especialidade
        grid.addWidget(QLabel("Especialidade:"), 4, 1)
        self.esp_input = QLineEdit()
        grid.addWidget(self.esp_input, 5, 1)

        form.addLayout(grid)

        # Botões
        btns = QHBoxLayout()
        btns.addStretch()

        btn_voltar = QPushButton("Voltar")
        btn_voltar.setProperty("class", "secondary")
        btn_voltar.clicked.connect(self.back_requested.emit)
        btns.addWidget(btn_voltar)

        btn_salvar = QPushButton("Salvar Cadastro")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.salvar_instrutor)
        btns.addWidget(btn_salvar)

        form.addLayout(btns)

        layout.addWidget(card)
        layout.addStretch()

    # ==========================================
    # SALVAR NO SUPABASE
    # ==========================================
    def salvar_instrutor(self):
        nome = self.nome_input.text().strip()
        cref = self.cref_input.text().strip()
        telefone = self.telefone_input.text().strip()
        email = self.email_input.text().strip()
        cpf = self.cpf_input.text().strip()
        especialidade = self.esp_input.text().strip()

        if not nome or not cref:
            QMessageBox.warning(self, "Erro", "Nome e CREF são obrigatórios.")
            return

        try:
            database.adicionar_instrutor(
                nome_completo=nome,
                cref=cref,
                telefone=telefone or None,
                email=email or None,
                cpf=cpf or None,
                especialidade=especialidade or None,
            )
            QMessageBox.information(self, "Sucesso", "Instrutor cadastrado!")
            self.instrutor_salvo.emit()
            self.back_requested.emit()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar instrutor:\n{e}")
