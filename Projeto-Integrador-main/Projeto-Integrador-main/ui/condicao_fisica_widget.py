# perfect_acqua_system/ui/condicao_fisica_widget.py

import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFrame, QGridLayout,
    QPushButton, QTextEdit, QLineEdit, QMessageBox, QListWidgetItem
)
from PyQt6.QtCore import Qt


class CondicaoFisica(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Condições de Saúde do Aluno")
        title.setObjectName("Title")
        layout.addWidget(title)

        main_layout = QHBoxLayout()

        # ==========================================================
        # PAINEL ESQUERDO – LISTA DE ALUNOS
        # ==========================================================

        left_panel = QFrame()
        left_panel.setProperty("class", "CardFrame")
        left_layout = QVBoxLayout(left_panel)

        self.filtro_aluno = QLineEdit(placeholderText="Buscar aluno...")
        self.filtro_aluno.textChanged.connect(self.filtrar_lista_alunos)
        left_layout.addWidget(self.filtro_aluno)

        self.lista_alunos = QListWidget()
        self.lista_alunos.currentItemChanged.connect(self.carregar_ficha_aluno)
        left_layout.addWidget(self.lista_alunos)

        self.btn_ver_ficha = QPushButton("📄 Ver Ficha Completa")
        self.btn_ver_ficha.setProperty("class", "primary")
        self.btn_ver_ficha.clicked.connect(self.ver_ficha_completa)
        left_layout.addWidget(self.btn_ver_ficha)

        # ==========================================================
        # PAINEL DIREITO – FICHA DO ALUNO
        # ==========================================================

        right_panel = QFrame()
        right_panel.setProperty("class", "CardFrame")
        right_layout = QVBoxLayout(right_panel)

        self.aluno_selecionado_label = QLabel("Nenhum aluno selecionado")
        self.aluno_selecionado_label.setObjectName("Subtitle")
        right_layout.addWidget(self.aluno_selecionado_label)

        grid = QGridLayout()

        self.condicao_edit = QTextEdit()
        self.alergias_edit = QTextEdit()
        self.medicamentos_edit = QTextEdit()
        self.restricoes_edit = QTextEdit()
        self.contato_edit = QLineEdit()
        self.telefone_edit = QLineEdit()

        grid.addWidget(QLabel("Condições Médicas:"), 0, 0)
        grid.addWidget(self.condicao_edit, 1, 0)

        grid.addWidget(QLabel("Alergias:"), 0, 1)
        grid.addWidget(self.alergias_edit, 1, 1)

        grid.addWidget(QLabel("Medicamentos:"), 2, 0)
        grid.addWidget(self.medicamentos_edit, 3, 0)

        grid.addWidget(QLabel("Restrições:"), 2, 1)
        grid.addWidget(self.restricoes_edit, 3, 1)

        grid.addWidget(QLabel("Contato de Emergência:"), 4, 0)
        grid.addWidget(self.contato_edit, 5, 0)

        grid.addWidget(QLabel("Telefone:"), 4, 1)
        grid.addWidget(self.telefone_edit, 5, 1)

        right_layout.addLayout(grid)

        btn_salvar = QPushButton("Salvar Ficha")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.salvar_ficha)
        right_layout.addWidget(btn_salvar, 0, Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)
        layout.addLayout(main_layout)

        # Carregar alunos
        self.popular_lista_alunos()

    # ==========================================================
    # LISTA DE ALUNOS
    # ==========================================================

    def filtrar_lista_alunos(self):
        texto = (self.filtro_aluno.text() or "").lower()
        for i in range(self.lista_alunos.count()):
            item = self.lista_alunos.item(i)
            item.setHidden(texto not in item.text().lower())

    def popular_lista_alunos(self):
        try:
            alunos = database.buscar_alunos() or []
        except Exception:
            alunos = []

        self.lista_alunos.clear()

        for item in alunos:
            if isinstance(item, dict):
                id_aluno = item.get("id_aluno") or item.get("id")
                nome = item.get("nome_completo") or item.get("nome") or str(id_aluno)
            else:
                # fallback tupla/lista
                id_aluno = item[0]
                nome = item[1] if len(item) > 1 else str(id_aluno)

            lista_item = QListWidgetItem(str(nome))
            lista_item.setData(Qt.ItemDataRole.UserRole, id_aluno)
            self.lista_alunos.addItem(lista_item)

    # ==========================================================
    # CARREGAR FICHA DO ALUNO
    # ==========================================================

    def carregar_ficha_aluno(self, current_item, previous_item):
        if not current_item:
            self.limpar_campos()
            return

        id_aluno = current_item.data(Qt.ItemDataRole.UserRole)
        self.aluno_selecionado_label.setText(
            f"Editando ficha de: {current_item.text()}"
        )

        try:
            dados = database.buscar_condicao_aluno(id_aluno) or {}
        except Exception:
            dados = {}

        if not dados:
            # ficha ainda não existe → começa em branco
            self.limpar_campos(keep_label=True)
            return

        self.condicao_edit.setText(dados.get("condicoes", "") or "")
        self.alergias_edit.setText(dados.get("alergias", "") or "")
        self.medicamentos_edit.setText(dados.get("medicamentos", "") or "")
        self.restricoes_edit.setText(dados.get("restricoes", "") or "")
        self.contato_edit.setText(dados.get("contato", "") or "")
        self.telefone_edit.setText(dados.get("telefone", "") or "")

    # ==========================================================
    # SALVAR FICHA
    # ==========================================================

    def salvar_ficha(self):
        current_item = self.lista_alunos.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Atenção", "Selecione um aluno primeiro.")
            return

        id_aluno = current_item.data(Qt.ItemDataRole.UserRole)

        dados = {
            "condicoes": self.condicao_edit.toPlainText().strip(),
            "alergias": self.alergias_edit.toPlainText().strip(),
            "medicamentos": self.medicamentos_edit.toPlainText().strip(),
            "restricoes": self.restricoes_edit.toPlainText().strip(),
            "contato": self.contato_edit.text().strip(),
            "telefone": self.telefone_edit.text().strip(),
        }

        try:
            database.salvar_ou_atualizar_condicao(id_aluno, dados)
            QMessageBox.information(self, "Sucesso", "Ficha salva com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar a ficha:\n{e}")

    # ==========================================================
    # LIMPAR CAMPOS
    # ==========================================================

    def limpar_campos(self, keep_label: bool = False):
        if not keep_label:
            self.aluno_selecionado_label.setText("Nenhum aluno selecionado")
        self.condicao_edit.clear()
        self.alergias_edit.clear()
        self.medicamentos_edit.clear()
        self.restricoes_edit.clear()
        self.contato_edit.clear()
        self.telefone_edit.clear()

    # ==========================================================
    # VER FICHA COMPLETA
    # ==========================================================

    def ver_ficha_completa(self, id_aluno=None):
        if id_aluno is None:
            current_item = self.lista_alunos.currentItem()
            if not current_item:
                QMessageBox.warning(self, "Atenção", "Selecione um aluno.")
                return
            id_aluno = current_item.data(Qt.ItemDataRole.UserRole)
            nome_aluno = current_item.text()
        else:
            nome_aluno = str(id_aluno)

        try:
            dados = database.buscar_condicao_aluno(id_aluno) or {}
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao buscar ficha:\n{e}")
            return

        try:
            aluno = database.buscar_aluno_por_id(id_aluno) or {}
        except Exception:
            aluno = {}

        nome_cad = aluno.get("nome_completo") or aluno.get("nome") or nome_aluno

        texto = (
            f"Aluno: {nome_cad}\n"
            f"CPF: {aluno.get('cpf','')}\n"
            f"Endereço: {aluno.get('endereco','')}\n\n"
            f"Condições Médicas:\n{dados.get('condicoes','')}\n\n"
            f"Alergias:\n{dados.get('alergias','')}\n\n"
            f"Medicamentos:\n{dados.get('medicamentos','')}\n\n"
            f"Restrições:\n{dados.get('restricoes','')}\n\n"
            f"Contato de Emergência: {dados.get('contato','')} — {dados.get('telefone','')}"
        )

        QMessageBox.information(self, "Ficha Completa", texto)
