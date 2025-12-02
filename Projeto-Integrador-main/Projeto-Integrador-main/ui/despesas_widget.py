# perfect_acqua_system/ui/despesas_widget.py

import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QDialog, QLineEdit, QDoubleSpinBox,
    QDateEdit, QGridLayout, QMessageBox
)
from PyQt6.QtCore import QDate, pyqtSignal


class Despesas(QWidget):
    despesa_salva = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # ======================================================
        # HEADER
        # ======================================================

        header_layout = QHBoxLayout()
        title_box = QVBoxLayout()

        title = QLabel("Controle de Despesas")
        title.setObjectName("Title")

        subtitle = QLabel("Registre e acompanhe as saídas e custos da academia")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        btn_add = QPushButton("➕ Adicionar Despesa")
        btn_add.setProperty("class", "primary")
        btn_add.clicked.connect(self.abrir_dialog_despesa)
        header_layout.addWidget(btn_add)

        layout.addLayout(header_layout)

        # ======================================================
        # TABELA
        # ======================================================

        self.tabela = QTableWidget()
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "Categoria", "Valor (R$)"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.tabela)

        self.popular_tabela()

    # ======================================================
    # FORMATADOR DE VALOR
    # ======================================================

    def _format_valor(self, valor):
        """
        Converte qualquer tipo de entrada para "R$ 1.234,56".
        Aceita float, int, string, formatos mistos.
        """
        try:
            if valor is None:
                return "R$ 0,00"

            if isinstance(valor, (int, float)):
                v = float(valor)
            else:
                s = str(valor).strip().replace("R$", "").replace(" ", "")
                if "," in s and "." in s:
                    s = s.replace(".", "").replace(",", ".")
                else:
                    s = s.replace(",", ".")
                v = float(s)

            return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return "R$ 0,00"

    # ======================================================
    # POPULAR TABELA
    # ======================================================

    def popular_tabela(self):
        """
        Carrega as despesas usando database.listar_despesas(),
        que é a função definida em database.py.
        """
        try:
            dados = database.listar_despesas() or []
        except Exception as e:
            print("DEBUG DESPESAS - erro ao listar:", e)
            dados = []

        print("DEBUG DESPESAS - dados:", dados)

        self.tabela.setRowCount(len(dados))

        for row, rec in enumerate(dados):
            # listar_despesas() retorna dict com:
            # id_despesa, data, descricao, categoria, valor, client_id, created_at, updated_at
            data = rec.get("data", "")
            descricao = rec.get("descricao", "")
            categoria = rec.get("categoria", "")
            valor = rec.get("valor", 0.0)

            self.tabela.setItem(row, 0, QTableWidgetItem(str(data)))
            self.tabela.setItem(row, 1, QTableWidgetItem(str(descricao)))
            self.tabela.setItem(row, 2, QTableWidgetItem(str(categoria)))
            self.tabela.setItem(row, 3, QTableWidgetItem(self._format_valor(valor)))

    # ======================================================
    # ABRIR MODAL
    # ======================================================

    def abrir_dialog_despesa(self):
        dialog = NovaDespesaDialog(self)

        if not dialog.exec():
            return

        data = dialog.data_edit.date().toString("yyyy-MM-dd")
        descricao = dialog.desc_edit.text().strip()
        categoria = dialog.cat_edit.text().strip()
        valor = float(dialog.valor_spin.value())

        if not descricao:
            QMessageBox.warning(self, "Atenção", "Descrição é obrigatória.")
            return

        if valor <= 0:
            QMessageBox.warning(self, "Atenção", "O valor deve ser maior que zero.")
            return

        try:
            # Em database.py, a função é adicionar_despesa
            database.adicionar_despesa(data, descricao, categoria, valor)

            QMessageBox.information(self, "Sucesso", "Despesa registrada com sucesso!")

            self.popular_tabela()
            self.despesa_salva.emit()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar a despesa:\n{e}")


# ======================================================
# DIALOG – NOVA DESPESA
# ======================================================

class NovaDespesaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Registrar Nova Despesa")

        layout = QVBoxLayout(self)
        grid = QGridLayout()

        grid.addWidget(QLabel("Data:"), 0, 0)
        self.data_edit = QDateEdit(calendarPopup=True)
        self.data_edit.setDate(QDate.currentDate())
        grid.addWidget(self.data_edit, 0, 1)

        grid.addWidget(QLabel("Descrição:"), 1, 0)
        self.desc_edit = QLineEdit()
        grid.addWidget(self.desc_edit, 1, 1)

        grid.addWidget(QLabel("Categoria:"), 2, 0)
        self.cat_edit = QLineEdit()
        grid.addWidget(self.cat_edit, 2, 1)

        grid.addWidget(QLabel("Valor (R$):"), 3, 0)
        self.valor_spin = QDoubleSpinBox()
        self.valor_spin.setRange(0, 99999.99)
        self.valor_spin.setPrefix("R$ ")
        self.valor_spin.setDecimals(2)
        grid.addWidget(self.valor_spin, 3, 1)

        layout.addLayout(grid)

        # Botões
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_salvar = QPushButton("Salvar")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.accept)

        button_layout.addWidget(btn_cancelar)
        button_layout.addWidget(btn_salvar)

        layout.addLayout(button_layout)
