# perfect_acqua_system/ui/ponto_widgets.py

import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QHeaderView,
    QTableWidgetItem, QComboBox, QDateEdit, QPushButton, QDialog, QMessageBox,
    QGridLayout, QTimeEdit
)
from PyQt6.QtCore import QDate, QTime, pyqtSignal


def _extract_id_and_name_from_instrutor(rec):
    """
    Extrai (id_instrutor, nome_completo) de qualquer formato.
    Compatível com estrutura da tabela 'instrutor'.
    """
    if rec is None:
        return (None, None)

    if isinstance(rec, dict):
        _id = rec.get("id_instrutor") or rec.get("id") or None
        _name = rec.get("nome_completo") or rec.get("nome") or rec.get("name") or None
        return (str(_id) if _id else None, str(_name) if _name else None)

    if isinstance(rec, (list, tuple)):
        seq = list(rec)
        _id = seq[0] if len(seq) > 0 else None
        _name = seq[1] if len(seq) > 1 else None
        return (str(_id) if _id else None, str(_name) if _name else None)

    return (None, str(rec))


def _parse_registro_ponto_row(row):
    """
    Normaliza linha vinda do Supabase → (nome_instrutor, yyyy-mm-dd, entrada, saída).
    Compatível com tabela 'ponto'.
    """
    if row is None:
        return ("", "", None, None)

    if isinstance(row, dict):
        nome = row.get("nome_instrutor") or row.get("instrutor") or ""
        data = row.get("data") or ""
        entrada = row.get("hora_entrada")
        saida = row.get("hora_saida")
        return (str(nome), str(data), entrada, saida)

    if isinstance(row, (list, tuple)):
        seq = list(row)
        while len(seq) < 4:
            seq.append(None)
        nome, data, entrada, saida = seq[:4]
        return (str(nome or ""), str(data or ""), entrada, saida)

    txt = str(row)
    parts = [p.strip() for p in txt.split(",")]
    if len(parts) >= 4:
        return (parts[0], parts[1], parts[2], parts[3])
    return (txt, "", None, None)


class PontoDialog(QDialog):
    def __init__(self, tipo_registro, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Registrar {tipo_registro}")
        self.setFixedSize(420, 260)

        layout = QVBoxLayout(self)
        grid = QGridLayout()

        title = QLabel(f"Registrar {tipo_registro}")
        title.setObjectName("Title")
        layout.addWidget(title)

        # Instrutor
        grid.addWidget(QLabel("Instrutor:"), 0, 0)
        self.combo_instrutores = QComboBox()

        try:
            instrutores_raw = database.buscar_instrutores() or []
        except Exception:
            try:
                instrutores_raw = database.listar_instrutores() or []
            except Exception:
                instrutores_raw = []

        self.instrutores_map = {}
        display_list = []

        for rec in instrutores_raw:
            _id, _name = _extract_id_and_name_from_instrutor(rec)
            if not _name:
                _name = f"Instrutor {_id}" if _id else "Desconhecido"
            display = _name
            if display in self.instrutores_map:
                display = f"{_name} ({_id})"
            self.instrutores_map[display] = _id
            display_list.append(display)

        if not display_list:
            display_list = ["— Nenhum instrutor cadastrado —"]
            self.instrutores_map[display_list[0]] = None

        self.combo_instrutores.addItems(display_list)
        grid.addWidget(self.combo_instrutores, 0, 1)

        # Data
        grid.addWidget(QLabel("Data:"), 1, 0)
        self.data_edit = QDateEdit(calendarPopup=True)
        self.data_edit.setDate(QDate.currentDate())
        grid.addWidget(self.data_edit, 1, 1)

        # Hora
        grid.addWidget(QLabel("Hora:"), 2, 0)
        self.hora_edit = QTimeEdit()
        self.hora_edit.setTime(QTime.currentTime())
        grid.addWidget(self.hora_edit, 2, 1)

        layout.addLayout(grid)
        layout.addStretch()

        # Botões
        buttons = QHBoxLayout()
        buttons.addStretch()

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)
        buttons.addWidget(btn_cancelar)

        btn_confirmar = QPushButton("Registrar")
        btn_confirmar.setProperty("class", "success")
        btn_confirmar.clicked.connect(self.accept)
        buttons.addWidget(btn_confirmar)

        layout.addLayout(buttons)


class FolhaDePonto(QWidget):
    ponto_registrado = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        title = QLabel("Folha de Ponto")
        title.setObjectName("Title")
        layout.addWidget(title)

        # Botões topo
        top = QHBoxLayout()
        btn_entrada = QPushButton("Registrar Entrada")
        btn_entrada.setProperty("class", "success")
        btn_entrada.clicked.connect(lambda: self.abrir_dialog("Entrada"))

        btn_saida = QPushButton("Registrar Saída")
        btn_saida.setProperty("class", "primary")
        btn_saida.clicked.connect(lambda: self.abrir_dialog("Saída"))

        top.addStretch()
        top.addWidget(btn_entrada)
        top.addWidget(btn_saida)
        layout.addLayout(top)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setAlternatingRowColors(True)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Instrutor", "Data", "Entrada", "Saída"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabela)

        self.aplicar_filtros()

    def aplicar_filtros(self):
        try:
            if hasattr(database, "buscar_registros_ponto"):
                registros = database.buscar_registros_ponto() or []
            else:
                registros = []
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar registros:\n{e}")
            registros = []

        self.popular_tabela(registros)

    def popular_tabela(self, dados):
        dados = dados or []
        self.tabela.setRowCount(len(dados))

        for row, raw in enumerate(dados):
            nome, data_str, entrada, saida = _parse_registro_ponto_row(raw)

            try:
                qd = QDate.fromString(data_str, "yyyy-MM-dd")
                data_fmt = qd.toString("dd/MM/yyyy") if qd.isValid() else data_str
            except Exception:
                data_fmt = data_str

            self.tabela.setItem(row, 0, QTableWidgetItem(nome or ""))
            self.tabela.setItem(row, 1, QTableWidgetItem(data_fmt))
            self.tabela.setItem(row, 2, QTableWidgetItem(entrada or "---"))
            self.tabela.setItem(row, 3, QTableWidgetItem(saida or "---"))

    def abrir_dialog(self, tipo):
        dialog = PontoDialog(tipo, self)

        if not dialog.exec():
            return

        instrutor_nome = dialog.combo_instrutores.currentText()
        instrutor_id = dialog.instrutores_map.get(instrutor_nome)

        data_str = dialog.data_edit.date().toString("yyyy-MM-dd")
        hora_str = dialog.hora_edit.time().toString("HH:mm:ss")

        try:
            # registrar_ponto(id_instrutor, hora_entrada, hora_saida, observacoes)
            if tipo == "Entrada":
                database.registrar_ponto(
                    id_instrutor=instrutor_id,
                    hora_entrada=hora_str,
                    hora_saida=None,
                    observacoes=f"Entrada em {data_str}",
                )
            else:  # Saída
                database.registrar_ponto(
                    id_instrutor=instrutor_id,
                    hora_entrada=None,
                    hora_saida=hora_str,
                    observacoes=f"Saída em {data_str}",
                )
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao registrar ponto:\n{e}")
            return

        QMessageBox.information(self, "Sucesso", "Ponto registrado com sucesso!")
        self.aplicar_filtros()
        self.ponto_registrado.emit()
