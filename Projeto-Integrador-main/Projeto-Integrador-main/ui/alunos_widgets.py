# perfect_acqua_system/ui/alunos_widgets.py
import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QHeaderView, QTableWidgetItem, QFrame, QGridLayout,
    QDateEdit, QComboBox, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, QDate
from PyQt6.QtGui import QColor

# ==========================================================
# NORMALIZADOR DE REGISTROS DE ALUNO
# ==========================================================

def _normalize_aluno_record(rec):
    """
    Normaliza um registro vindo de database.buscar_alunos.
    Campos usados na UI: id, nome, telefone_responsavel, cpf, valor_mensalidade, status.
    """
    out = {
        "id": "",
        "nome": "",
        "telefone_responsavel": "",
        "cpf": "",
        "valor_mensalidade": "",
        "status": "",
    }

    if not rec:
        return out

    if isinstance(rec, dict):
        out["id"] = rec.get("id_aluno") or rec.get("id") or ""
        out["nome"] = rec.get("nome_completo") or rec.get("nome") or ""
        out["telefone_responsavel"] = rec.get("telefone_responsavel") or ""
        out["cpf"] = rec.get("cpf") or ""
        out["valor_mensalidade"] = rec.get("valor_mensalidade") or ""
        out["status"] = rec.get("status") or ""
        return out

    if isinstance(rec, (list, tuple)):
        seq = list(rec)
        if len(seq) > 0:
            out["id"] = seq[0]
        if len(seq) > 1:
            out["nome"] = seq[1]
        if len(seq) > 2:
            out["telefone_responsavel"] = seq[2]
        if len(seq) > 3:
            out["cpf"] = seq[3]
        if len(seq) > 4:
            out["valor_mensalidade"] = seq[4]
        if len(seq) > 5:
            out["status"] = seq[5]
        return out

    out["nome"] = str(rec)
    return out


# ==========================================================
# LISTA DE ALUNOS
# ==========================================================

class ListaAlunos(QWidget):
    btn_cadastrar_clicked = pyqtSignal()
    ver_ficha_requested = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Header
        title = QLabel("Lista de Alunos")
        title.setObjectName("Title")
        subtitle = QLabel("Gerencie os alunos cadastrados no sistema")
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # Filtro + botões
        top_layout = QHBoxLayout()
        self.filtro_alunos = QLineEdit(placeholderText="Digite o nome do aluno...")
        self.filtro_alunos.textChanged.connect(self._filtrar_por_texto)
        top_layout.addWidget(self.filtro_alunos)
        top_layout.addStretch()

        btn_ficha = QPushButton("👁 Ver Ficha")
        btn_ficha.setProperty("class", "secondary")
        btn_ficha.clicked.connect(self._on_ver_ficha_clicked)
        top_layout.addWidget(btn_ficha)

        btn_add = QPushButton("➕ Cadastrar Aluno")
        btn_add.setProperty("class", "success")
        btn_add.clicked.connect(self.btn_cadastrar_clicked.emit)
        top_layout.addWidget(btn_add)

        layout.addLayout(top_layout)

        # Tabela: ID oculto + Nome, Nº resp, CPF, Valor, Status
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Aluno", "Nº Responsável", "CPF", "Valor Mensalidade", "Status"]
        )
        self.tabela.setColumnHidden(0, True)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabela)

        self.popular_tabela()

    def _filtrar_por_texto(self, txt):
        txt = (txt or "").lower().strip()
        for r in range(self.tabela.rowCount()):
            item = self.tabela.item(r, 1)
            if item:
                self.tabela.setRowHidden(r, txt not in item.text().lower())
            else:
                self.tabela.setRowHidden(r, True)

    def _on_ver_ficha_clicked(self):
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um aluno.")
            return

        id_item = self.tabela.item(row, 0)
        if not id_item:
            QMessageBox.warning(self, "Erro", "ID não encontrado.")
            return

        self.ver_ficha_requested.emit(id_item.text())

    def popular_tabela(self):
        try:
            dados = database.buscar_alunos() or []
        except Exception:
            dados = []

        self.tabela.setRowCount(len(dados))

        for row, rec in enumerate(dados):
            norm = _normalize_aluno_record(rec)

            id_val = str(norm.get("id") or "")
            nome = str(norm.get("nome") or "")
            fone_resp = str(norm.get("telefone_responsavel") or "")
            cpf = str(norm.get("cpf") or "")
            valor = norm.get("valor_mensalidade")
            try:
                valor_txt = f"R$ {float(valor):.2f}" if valor not in (None, "") else ""
            except Exception:
                valor_txt = str(valor or "")
            status = str(norm.get("status") or "")

            self.tabela.setItem(row, 0, QTableWidgetItem(id_val))
            self.tabela.setItem(row, 1, QTableWidgetItem(nome))
            self.tabela.setItem(row, 2, QTableWidgetItem(fone_resp))
            self.tabela.setItem(row, 3, QTableWidgetItem(cpf))
            self.tabela.setItem(row, 4, QTableWidgetItem(valor_txt))

            item_status = QTableWidgetItem(status)
            if status.lower() in ("ativo", "true", "1", "sim", "yes"):
                item_status.setForeground(QColor("#5eead4"))
            self.tabela.setItem(row, 5, item_status)


# ==========================================================
# CADASTRO DE NOVO ALUNO
# ==========================================================

class NovoAluno(QWidget):
    back_requested = pyqtSignal()
    aluno_salvo = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Título
        title = QLabel("Cadastro de Aluno")
        title.setObjectName("Title")
        layout.addWidget(title)

        # Card
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        f = QVBoxLayout(frame)

        # --------------------------
        # Dados pessoais
        # --------------------------
        f.addWidget(self._sec("Dados Pessoais"))
        grid_p = QGridLayout()

        self.nome_input = QLineEdit()
        self.data_nasc_input = QDateEdit(calendarPopup=True)
        self.data_nasc_input.setDate(QDate.currentDate())
        self.cpf_input = QLineEdit()
        self.end_input = QLineEdit()

        grid_p.addWidget(QLabel("Nome Completo:"), 0, 0)
        grid_p.addWidget(self.nome_input, 1, 0, 1, 3)

        grid_p.addWidget(QLabel("Data de Nascimento:"), 2, 0)
        grid_p.addWidget(self.data_nasc_input, 3, 0)

        grid_p.addWidget(QLabel("CPF:"), 2, 1)
        grid_p.addWidget(self.cpf_input, 3, 1)

        grid_p.addWidget(QLabel("Endereço:"), 4, 0)
        grid_p.addWidget(self.end_input, 5, 0, 1, 3)

        f.addLayout(grid_p)

        # --------------------------
        # Responsável (opcional)
        # --------------------------
        f.addWidget(self._sec("Responsável (se menor de idade)"))
        grid_r = QGridLayout()

        self.nome_resp_input = QLineEdit()
        self.tel_resp_input = QLineEdit()
        self.cpf_resp_input = QLineEdit()

        grid_r.addWidget(QLabel("Nome do Responsável:"), 0, 0)
        grid_r.addWidget(self.nome_resp_input, 1, 0, 1, 3)

        grid_r.addWidget(QLabel("Telefone do Responsável:"), 2, 0)
        grid_r.addWidget(self.tel_resp_input, 3, 0)

        grid_r.addWidget(QLabel("CPF do Responsável:"), 2, 1)
        grid_r.addWidget(self.cpf_resp_input, 3, 1)

        f.addLayout(grid_r)

        # --------------------------
        # Dados do plano / financeiro
        # --------------------------
        f.addWidget(self._sec("Plano / Financeiro"))
        grid_m = QGridLayout()

        self.combo_tipo_plano = QComboBox()
        self.combo_tipo_plano.addItems(["Mensal", "Trimestral", "Anual"])

        grid_m.addWidget(QLabel("Plano:"), 0, 0)
        grid_m.addWidget(self.combo_tipo_plano, 1, 0)

        grid_m.addWidget(QLabel("Valor que vai pagar:"), 0, 1)
        self.valor_pagar_input = QLineEdit()
        grid_m.addWidget(self.valor_pagar_input, 1, 1)

        # Status do aluno
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Ativo", "Inativo"])
        grid_m.addWidget(QLabel("Status do Aluno:"), 2, 0)
        grid_m.addWidget(self.combo_status, 3, 0)

        f.addLayout(grid_m)
        f.addStretch()

        # Botões
        buttons = QHBoxLayout()
        btn_voltar = QPushButton("Voltar")
        btn_voltar.setProperty("class", "secondary")
        btn_voltar.clicked.connect(self.back_requested.emit)

        btn_salvar = QPushButton("Salvar Cadastro")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.salvar_aluno)

        buttons.addStretch()
        buttons.addWidget(btn_voltar)
        buttons.addWidget(btn_salvar)

        f.addLayout(buttons)

        layout.addWidget(frame)
        layout.addStretch()

    # ==========================================================
    # SALVAR ALUNO
    # ==========================================================

    def salvar_aluno(self):
        nome = self.nome_input.text().strip()
        data_nasc = self.data_nasc_input.date().toString("yyyy-MM-dd")
        cpf = self.cpf_input.text().strip()
        endereco = self.end_input.text().strip()

        nome_resp = self.nome_resp_input.text().strip()
        tel_resp = self.tel_resp_input.text().strip()
        cpf_resp = self.cpf_resp_input.text().strip()

        tipo_plano = self.combo_tipo_plano.currentText()
        status = self.combo_status.currentText()

        if not nome or not cpf:
            QMessageBox.warning(self, "Erro", "Nome e CPF são obrigatórios.")
            return

        valor_txt = self.valor_pagar_input.text().strip()
        if not valor_txt:
            QMessageBox.warning(self, "Erro", "Informe o valor que o aluno vai pagar.")
            return

        try:
            valor_pagar = float(valor_txt.replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Valor da mensalidade inválido.")
            return

        try:
            # grava aluno
            res = database.adicionar_aluno(
                nome_completo=nome,
                data_nascimento=data_nasc,
                cpf=cpf,
                telefone=None,
                email=None,
                endereco=endereco,
                id_plano=None,  # se quiser ligar com tabela plano depois
                valor_mensalidade=valor_pagar,
                nome_responsavel=nome_resp or None,
                telefone_responsavel=tel_resp or None,
                cpf_responsavel=cpf_resp or None,
                status=status,
            )

            # recuperar id do aluno inserido
            if isinstance(res, list) and res:
                r0 = res[0]
            elif isinstance(res, dict):
                r0 = res
            else:
                r0 = {}

            id_aluno = r0.get("id_aluno") or r0.get("id")

            # cria mensalidade pendente
            if id_aluno is not None:
                try:
                    database.criar_mensalidade_inicial_para_aluno(
                        id_aluno=id_aluno,
                        valor_praticado=valor_pagar,
                        tipo_plano=tipo_plano,
                    )
                except Exception as e:
                    # não bloqueia o cadastro, só avisa
                    print(f"[NovoAluno] erro ao criar mensalidade inicial: {e}")

            QMessageBox.information(self, "Sucesso", "Aluno cadastrado com sucesso!")
            self.aluno_salvo.emit()
            self.back_requested.emit()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar aluno:\n{e}")

    # ==========================================================

    def _sec(self, txt):
        l = QLabel(txt)
        l.setObjectName("SectionHeader")
        return l
