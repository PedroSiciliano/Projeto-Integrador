# perfect_acqua_system/ui/agenda_aulas_widget.py

import database

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QHeaderView, QTableWidgetItem, QDateEdit, QDialog, QComboBox, QTimeEdit,
    QGridLayout, QMessageBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate, QTime, pyqtSignal


class GerenciarAlunosAula(QDialog):
    def __init__(self, id_aula, parent=None):
        super().__init__(parent)
        self.id_aula = id_aula

        self.setWindowTitle("Gerenciar Alunos na Aula")
        self.setMinimumSize(600, 400)

        layout = QHBoxLayout(self)

        # Painel esquerdo – alunos disponíveis
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Alunos Disponíveis"))
        self.lista_disponiveis = QListWidget()
        left_panel.addWidget(self.lista_disponiveis)

        # Painel central – botões
        mid_panel = QVBoxLayout()
        mid_panel.addStretch()
        btn_adicionar = QPushButton(">>")
        btn_remover = QPushButton("<<")
        btn_adicionar.clicked.connect(self.adicionar_aluno)
        btn_remover.clicked.connect(self.remover_aluno)
        mid_panel.addWidget(btn_adicionar)
        mid_panel.addWidget(btn_remover)
        mid_panel.addStretch()

        # Painel direito – alunos matriculados
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Alunos Matriculados"))
        self.lista_matriculados = QListWidget()
        right_panel.addWidget(self.lista_matriculados)

        layout.addLayout(left_panel)
        layout.addLayout(mid_panel)
        layout.addLayout(right_panel)

        # Botão salvar
        button_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(btn_salvar)
        right_panel.addLayout(button_layout)

        self.popular_listas()

    def popular_listas(self):
        self.lista_disponiveis.clear()
        self.lista_matriculados.clear()

        # alunos já na aula
        try:
            alunos_na_aula = database.buscar_alunos_da_aula(self.id_aula) or []
        except Exception as e:
            print(f"[GerenciarAlunosAula] erro buscar_alunos_da_aula: {e}")
            alunos_na_aula = []

        for rec in (alunos_na_aula or []):
            try:
                if isinstance(rec, dict):
                    id_aluno = rec.get("id_aluno") or rec.get("id")
                    nome = rec.get("nome_completo") or rec.get("nome") or str(id_aluno)
                elif isinstance(rec, (list, tuple)):
                    id_aluno = rec[0]
                    nome = rec[1] if len(rec) > 1 else str(id_aluno)
                else:
                    id_aluno = rec
                    nome = str(rec)

                item = QListWidgetItem(str(nome))
                item.setData(Qt.ItemDataRole.UserRole, id_aluno)
                self.lista_matriculados.addItem(item)
            except Exception:
                continue

        # alunos disponíveis (fora da aula)
        try:
            alunos_fora = database.buscar_alunos_fora_da_aula(self.id_aula) or []
        except Exception as e:
            print(f"[GerenciarAlunosAula] erro buscar_alunos_fora_da_aula: {e}")
            alunos_fora = []

        for rec in (alunos_fora or []):
            try:
                if isinstance(rec, dict):
                    id_aluno = rec.get("id_aluno") or rec.get("id")
                    nome = rec.get("nome_completo") or rec.get("nome") or str(id_aluno)
                elif isinstance(rec, (list, tuple)):
                    id_aluno = rec[0]
                    nome = rec[1] if len(rec) > 1 else str(id_aluno)
                else:
                    id_aluno = rec
                    nome = str(rec)

                # evitar duplicados
                already = False
                for i in range(self.lista_matriculados.count()):
                    if str(self.lista_matriculados.item(i).data(Qt.ItemDataRole.UserRole)) == str(id_aluno):
                        already = True
                        break
                if already:
                    continue

                item = QListWidgetItem(str(nome))
                item.setData(Qt.ItemDataRole.UserRole, id_aluno)
                self.lista_disponiveis.addItem(item)
            except Exception:
                continue

    def adicionar_aluno(self):
        item = self.lista_disponiveis.currentItem()
        if item:
            self.lista_disponiveis.takeItem(self.lista_disponiveis.row(item))
            self.lista_matriculados.addItem(item)

    def remover_aluno(self):
        item = self.lista_matriculados.currentItem()
        if item:
            self.lista_matriculados.takeItem(self.lista_matriculados.row(item))
            self.lista_disponiveis.addItem(item)

    def get_ids_matriculados(self):
        ids = []
        for i in range(self.lista_matriculados.count()):
            item = self.lista_matriculados.item(i)
            ids.append(item.data(Qt.ItemDataRole.UserRole))
        return ids


class AgendaAulas(QWidget):
    aula_salva = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Cabeçalho
        header_layout = QHBoxLayout()
        title = QLabel("Agenda de Aulas")
        title.setObjectName("Title")
        header_layout.addWidget(title)
        header_layout.addStretch()

        btn_agendar = QPushButton("➕ Agendar Nova Aula")
        btn_agendar.setProperty("class", "primary")
        btn_agendar.clicked.connect(self.abrir_dialog_agendamento)
        header_layout.addWidget(btn_agendar)
        layout.addLayout(header_layout)

        # Filtro por data
        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Selecione a data:"))
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.popular_tabela)
        filtro_layout.addWidget(self.date_edit)
        filtro_layout.addStretch()
        layout.addLayout(filtro_layout)

        # Tabela
        self.tabela_aulas = QTableWidget()
        self.tabela_aulas.setAlternatingRowColors(True)
        self.tabela_aulas.setColumnCount(7)
        self.tabela_aulas.setHorizontalHeaderLabels(
            ["ID", "Horário", "Data", "Nível", "Instrutor", "Alunos", "Ações"]
        )
        self.tabela_aulas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela_aulas.setColumnHidden(0, True)  # esconde ID, mas mantém na linha
        self.tabela_aulas.horizontalHeader().setSectionResizeMode(
            6, QHeaderView.ResizeMode.ResizeToContents
        )

        dummy_button = QPushButton("Ver Alunos")
        row_height = dummy_button.sizeHint().height() + 10
        self.tabela_aulas.verticalHeader().setDefaultSectionSize(row_height)

        layout.addWidget(self.tabela_aulas)

        self.popular_tabela()

    # ----------------------------------------------------------
    # Agendar nova aula
    # ----------------------------------------------------------

    def abrir_dialog_agendamento(self):
            dialog = AgendarAulaDialog(self)
            if not dialog.exec():
                return

            data = dialog.data_edit.date().toString("yyyy-MM-dd")
            hora = dialog.inicio_edit.time().toString("HH:mm:ss")
            horario_iso = f"{data} {hora}"  # ex: 2025-12-02 08:00:00

            nivel = dialog.nivel_combo.currentText()

            display_instrutor = dialog.instrutor_combo.currentText()
            id_instrutor = dialog.instrutores_map.get(display_instrutor)

            if id_instrutor is None:
                QMessageBox.warning(self, "Erro", "Não foi possível determinar o instrutor selecionado.")
                return

            try:
                res = database.adicionar_aula(
                    data_val=data,
                    horario=horario_iso,
                    id_instrutor=id_instrutor,
                    duracao_minutes=60,
                    sala=None,
                    descricao=nivel,
                )
                self.popular_tabela()
                self.aula_salva.emit()

                msg_id = None
                if isinstance(res, dict):
                    msg_id = res.get("id_aula") or res.get("id")
                elif isinstance(res, (list, tuple)) and res:
                    first = res[0]
                    if isinstance(first, dict):
                        msg_id = first.get("id_aula") or first.get("id")
                    else:
                        msg_id = str(first)
                else:
                    msg_id = str(res)

                QMessageBox.information(self, "Sucesso", f"Aula agendada com sucesso! (id: {msg_id})")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao agendar aula: {e}")


    # ----------------------------------------------------------
    # Preencher tabela
    # ----------------------------------------------------------

    def popular_tabela(self):
        self.tabela_aulas.setRowCount(0)
        data_selecionada = self.date_edit.date().toString("yyyy-MM-dd")

        try:
            dados_aulas = database.buscar_aulas_com_id_por_data(data_selecionada) or []
        except Exception as e:
            print(f"[AgendaAulas] erro ao chamar buscar_aulas_com_id_por_data: {e}")
            dados_aulas = []

        dados_aulas = list(dados_aulas or [])
        self.tabela_aulas.setRowCount(len(dados_aulas))

        for row, a in enumerate(dados_aulas):
            try:
                id_aula = str(a.get("id_aula") or a.get("id") or "")
                data_aula = str(a.get("data") or data_selecionada)
                horario = str(a.get("horario") or "")
                nivel = str(a.get("nivel") or a.get("observacoes") or "")
                instrutor = str(a.get("nome_instrutor") or "")
            except Exception:
                id_aula = ""
                data_aula = ""
                horario = ""
                nivel = ""
                instrutor = ""

            self.tabela_aulas.setItem(row, 0, QTableWidgetItem(id_aula))
            self.tabela_aulas.setItem(row, 1, QTableWidgetItem(horario))
            self.tabela_aulas.setItem(row, 2, QTableWidgetItem(data_aula))
            self.tabela_aulas.setItem(row, 3, QTableWidgetItem(nivel))
            self.tabela_aulas.setItem(row, 4, QTableWidgetItem(instrutor))

            # coluna "Alunos" (pode mostrar só contagem ou deixar em branco)
            self.tabela_aulas.setItem(row, 5, QTableWidgetItem(""))

            btn_ver_alunos = QPushButton("Ver Alunos")
            try:
                aid_for_cb = int(id_aula) if str(id_aula).isdigit() else id_aula
            except Exception:
                aid_for_cb = id_aula
            btn_ver_alunos.clicked.connect(
                lambda _, aid=aid_for_cb: self.gerenciar_alunos_aula(aid)
            )
            self.tabela_aulas.setCellWidget(row, 6, btn_ver_alunos)

    # ----------------------------------------------------------
    # Gerenciar alunos na aula
    # ----------------------------------------------------------

    def gerenciar_alunos_aula(self, id_aula):
        if id_aula is None or str(id_aula) == "":
            QMessageBox.warning(self, "Erro", "ID da aula não informado.")
            return

        try:
            dialog = GerenciarAlunosAula(id_aula, self)
            if dialog.exec():
                ids_para_salvar = dialog.get_ids_matriculados()
                try:
                    database.atualizar_alunos_na_aula(id_aula, ids_para_salvar)
                    self.popular_tabela()
                    QMessageBox.information(self, "Sucesso", "Lista de alunos atualizada!")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Falha ao atualizar alunos da aula: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir gerenciador de alunos: {e}")


class AgendarAulaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Agendar Nova Aula")
        self.setFixedSize(450, 400)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Agendar Nova Aula")
        title.setObjectName("Title")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(10)

        # Instrutor
        grid.addWidget(QLabel("Instrutor:"), 0, 0)
        self.instrutor_combo = QComboBox()

        try:
            instrutores = database.buscar_instrutores() or []
        except Exception:
            instrutores = []

        self.instrutores_map = {}
        itens = []

        for ins in instrutores:
            try:
                if isinstance(ins, dict):
                    nome = ins.get("nome") or ins.get("nome_completo") or str(ins.get("id") or "")
                    id_ = ins.get("id_instrutor") or ins.get("id")
                elif isinstance(ins, (list, tuple)):
                    id_ = ins[0] if len(ins) > 0 else None
                    nome = ins[1] if len(ins) > 1 else str(id_)
                else:
                    nome = str(ins)
                    id_ = None

                display = nome if nome else str(id_)
                if display in self.instrutores_map:
                    display = f"{display} ({id_})"

                self.instrutores_map[display] = id_
                itens.append(display)
            except Exception:
                continue

        if not itens:
            itens = ["— Nenhum —"]
            self.instrutores_map[itens[0]] = None

        self.instrutor_combo.addItems(itens)
        grid.addWidget(self.instrutor_combo, 0, 1)

        # Data
        grid.addWidget(QLabel("Data da Aula:"), 1, 0)
        self.data_edit = QDateEdit(calendarPopup=True)
        self.data_edit.setDate(QDate.currentDate())
        grid.addWidget(self.data_edit, 1, 1)

        # Horário início
        grid.addWidget(QLabel("Horário de Início:"), 2, 0)
        self.inicio_edit = QTimeEdit()
        self.inicio_edit.setTime(QTime(8, 0))
        grid.addWidget(self.inicio_edit, 2, 1)

        # Horário fim (não usado no insert atual, mas mantido na UI)
        grid.addWidget(QLabel("Horário de Fim:"), 3, 0)
        self.fim_edit = QTimeEdit()
        self.fim_edit.setTime(QTime(9, 0))
        grid.addWidget(self.fim_edit, 3, 1)

        # Nível
        grid.addWidget(QLabel("Nível da Turma:"), 4, 0)
        self.nivel_combo = QComboBox()
        self.nivel_combo.addItems(["Iniciante", "Intermediário", "Avançado", "Hidroginástica"])
        grid.addWidget(self.nivel_combo, 4, 1)

        layout.addLayout(grid)
        layout.addStretch()

        # Botões
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancelar)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.accept)
        button_layout.addWidget(btn_salvar)

        layout.addLayout(button_layout)
