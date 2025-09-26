# perfect_acqua_system/ui/financeiro_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QComboBox, QLineEdit, QGridLayout, QMessageBox, QFrame
from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSignal
import database

class Financeiro(QWidget):
    mensalidade_paga = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Controle Financeiro")
        title.setObjectName("Title")
        subtitle = QLabel("Acompanhe e gerencie as mensalidades dos alunos")
        
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        # (Restante do __init__ igual...)
        top_panel = QFrame()
        top_panel.setProperty("class", "CardFrame")
        top_layout = QVBoxLayout(top_panel)
        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("Filtrar por Status:"), 0, 0)
        self.filtro_status = QComboBox()
        self.filtro_status.addItems(["Todos", "Pendente", "Pago", "Atrasado"])
        grid_layout.addWidget(self.filtro_status, 0, 1)
        grid_layout.addWidget(QLabel("Mês/Ano:"), 0, 2)
        self.filtro_data = QLineEdit(placeholderText="Ex: 09/2025")
        grid_layout.addWidget(self.filtro_data, 0, 3)
        btn_filtrar = QPushButton("🔎 Filtrar")
        btn_filtrar.setProperty("class", "primary")
        grid_layout.addWidget(btn_filtrar, 0, 4)

        top_layout.addLayout(grid_layout)
        layout.addWidget(top_panel)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Aluno", "Plano", "Valor", "Vencimento", "Status", "Ações"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        # --- CORREÇÃO: Ajuste programático da altura da linha para caber o botão ---
        dummy_button = QPushButton("✔ Marcar como Pago")
        row_height = dummy_button.sizeHint().height() + 10
        self.table.verticalHeader().setDefaultSectionSize(row_height)

        self.popular_tabela()
        layout.addWidget(self.table)

    def popular_tabela(self):
        # ... (código da função igual à versão anterior)
        dados = database.buscar_mensalidades()
        self.table.setRowCount(len(dados))

        for i, (id_mensalidade, aluno, plano, valor, venc, status) in enumerate(dados):
            self.table.setItem(i, 0, QTableWidgetItem(aluno))
            self.table.setItem(i, 1, QTableWidgetItem(plano))
            self.table.setItem(i, 2, QTableWidgetItem(f"R$ {valor:,.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(venc))
            
            status_item = QTableWidgetItem(status)
            if status == "Pago":
                status_item.setForeground(QColor("#22c55e"))
            elif status == "Atrasado":
                status_item.setForeground(QColor("#ef4444"))
            else:
                status_item.setForeground(QColor("#facc15"))
            self.table.setItem(i, 4, status_item)

            self.table.setCellWidget(i, 5, None)
            if status in ["Pendente", "Atrasado"]:
                btn_pagar = QPushButton("✔ Marcar como Pago")
                btn_pagar.setProperty("class", "success")
                btn_pagar.clicked.connect(lambda _, mid=id_mensalidade: self.marcar_como_pago(mid))
                self.table.setCellWidget(i, 5, btn_pagar)

    def marcar_como_pago(self, mensalidade_id):
        # ... (código da função igual à versão anterior)
        database.marcar_mensalidade_paga(mensalidade_id)
        QMessageBox.information(self, "Sucesso", f"Mensalidade marcada como paga!")
        self.popular_tabela()
        self.mensalidade_paga.emit()
