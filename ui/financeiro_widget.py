# perfect_acqua_system/ui/financeiro_widget.py
<<<<<<< HEAD
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QComboBox, QLineEdit, QGridLayout, QMessageBox, QFrame
from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSignal
import database

class Financeiro(QWidget):
    mensalidade_paga = pyqtSignal()

=======

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QComboBox, QLineEdit, QGridLayout, QFrame
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class Financeiro(QWidget):
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Controle Financeiro")
        title.setObjectName("Title")
        subtitle = QLabel("Acompanhe e gerencie as mensalidades dos alunos")
<<<<<<< HEAD
        
=======

>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

<<<<<<< HEAD
        # (Restante do __init__ igual...)
        top_panel = QFrame()
        top_panel.setProperty("class", "CardFrame")
        top_layout = QVBoxLayout(top_panel)
        grid_layout = QGridLayout()
=======
        # Painel superior (filtros e resumo)
        top_panel = QFrame()
        top_panel.setProperty("class", "CardFrame")
        top_layout = QVBoxLayout(top_panel)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6

        grid_layout.addWidget(QLabel("Filtrar por Status:"), 0, 0)
        self.filtro_status = QComboBox()
        self.filtro_status.addItems(["Todos", "Pendente", "Pago", "Atrasado"])
        grid_layout.addWidget(self.filtro_status, 0, 1)
<<<<<<< HEAD
        grid_layout.addWidget(QLabel("Mês/Ano:"), 0, 2)
        self.filtro_data = QLineEdit(placeholderText="Ex: 09/2025")
        grid_layout.addWidget(self.filtro_data, 0, 3)
=======

        grid_layout.addWidget(QLabel("Mês/Ano:"), 0, 2)
        self.filtro_data = QLineEdit(placeholderText="Ex: 09/2025")
        grid_layout.addWidget(self.filtro_data, 0, 3)

>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
        btn_filtrar = QPushButton("🔎 Filtrar")
        btn_filtrar.setProperty("class", "primary")
        grid_layout.addWidget(btn_filtrar, 0, 4)

<<<<<<< HEAD
        top_layout.addLayout(grid_layout)
        layout.addWidget(top_panel)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
=======
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(3, 1)

        self.label_recebido = QLabel("Total Recebido (Mês): R$ 350,00")
        self.label_recebido.setObjectName("SuccessText")
        self.label_a_receber = QLabel("Total a Receber (Mês): R$ 400,00")
        self.label_a_receber.setObjectName("WarningText")

        top_layout.addLayout(grid_layout)

        summary_layout = QHBoxLayout()
        summary_layout.addStretch()
        summary_layout.addWidget(self.label_recebido)
        summary_layout.addWidget(self.label_a_receber)
        top_layout.addLayout(summary_layout)

        layout.addWidget(top_panel)

        # Tabela
        self.table = QTableWidget()
        self.setup_table_style()
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Aluno", "Plano", "Valor", "Vencimento", "Status", "Ações"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

<<<<<<< HEAD
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
            
=======
        self.popular_tabela()
        layout.addWidget(self.table)

    def setup_table_style(self):
        self.table.setStyleSheet("""
            QTableWidget { background-color: #1e293b; alternate-background-color: #2b3a4a;
                           border: none; gridline-color: #4f6987; }
            QTableWidget::viewport { background-color: #1e293b; border: none; }
            QHeaderView::section { background-color: #2b3a4a; color: #94a3b8; padding: 4px;
                                   border: none; border-bottom: 1px solid #4f6987; }
            QHeaderView::section:horizontal { border-right: 1px solid #4f6987; }
            QTableCornerButton::section { background-color: #2b3a4a; }
        """)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

    def popular_tabela(self):
        dados = [
            (1, "Maria Silva", "Plano trimestral", "R$ 350,00", "10/09/2025", "Pago"),
            (2, "João Santos", "Plano mensal", "R$ 250,00", "05/09/2025", "Pendente"),
            (3, "Lucas Ferreira", "Plano semestral", "R$ 150,00", "02/09/2025", "Atrasado"),
        ]

        self.table.setRowCount(len(dados))
        for i, (id_mensalidade, aluno, plano, valor, venc, status) in enumerate(dados):
            self.table.setItem(i, 0, QTableWidgetItem(aluno))
            self.table.setItem(i, 1, QTableWidgetItem(plano))
            self.table.setItem(i, 2, QTableWidgetItem(valor))
            self.table.setItem(i, 3, QTableWidgetItem(venc))

>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
            status_item = QTableWidgetItem(status)
            if status == "Pago":
                status_item.setForeground(QColor("#22c55e"))
            elif status == "Atrasado":
                status_item.setForeground(QColor("#ef4444"))
            else:
                status_item.setForeground(QColor("#facc15"))
<<<<<<< HEAD
            self.table.setItem(i, 4, status_item)

            self.table.setCellWidget(i, 5, None)
            if status in ["Pendente", "Atrasado"]:
                btn_pagar = QPushButton("✔ Marcar como Pago")
                btn_pagar.setProperty("class", "success")
=======
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 4, status_item)

            # Ajusta altura da linha
            self.table.setRowHeight(i, 40)

            if status in ["Pendente", "Atrasado"]:
                btn_pagar = QPushButton("✔ Marcar como Pago")
                btn_pagar.setProperty("class", "success-outline")
                btn_pagar.setStyleSheet("""
                    QPushButton {
                        padding: 4px 10px;
                        border: 1px solid #22c55e;
                        border-radius: 6px;
                        color: #22c55e;
                        background-color: transparent;
                    }
                    QPushButton:hover {
                        background-color: #22c55e;
                        color: white;
                    }
                """)
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
                btn_pagar.clicked.connect(lambda _, mid=id_mensalidade: self.marcar_como_pago(mid))
                self.table.setCellWidget(i, 5, btn_pagar)

    def marcar_como_pago(self, mensalidade_id):
<<<<<<< HEAD
        # ... (código da função igual à versão anterior)
        database.marcar_mensalidade_paga(mensalidade_id)
        QMessageBox.information(self, "Sucesso", f"Mensalidade marcada como paga!")
        self.popular_tabela()
        self.mensalidade_paga.emit()
=======
        """Atualiza o status na própria tabela em vez de abrir mensagem torta."""
        for row in range(self.table.rowCount()):
            if row + 1 == mensalidade_id:
                # Atualiza a célula de status
                status_item = QTableWidgetItem("Pago ✅")
                status_item.setForeground(QColor("#22c55e"))
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 4, status_item)

                # Remove o botão de ação
                self.table.removeCellWidget(row, 5)
                break
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
