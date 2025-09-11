# perfect_acqua_system/ui/financeiro_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QColor

class Financeiro(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Controle Financeiro")
        title.setObjectName("Title")
        subtitle = QLabel("Acompanhe as mensalidades e o status de pagamento dos alunos")
        subtitle.setObjectName("Subtitle")

        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)

        table = QTableWidget()
        table.verticalHeader().setVisible(False)
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Aluno", "Plano", "Valor", "Vencimento", "Status"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        dados = [
            ("Maria Silva", "Plano trimestral", "R$ 350,00", "10/09/2025", "Pago"),
            ("João Santos", "Plano mensal", "R$ 250,00", "05/09/2025", "Pendente"),
            ("Lucas Ferreira", "Plano semestral", "R$ 150,00", "02/09/2025", "Atrasado"),
        ]

        table.setRowCount(len(dados))
        for i, (aluno, plano, valor, venc, status) in enumerate(dados):
            table.setItem(i, 0, QTableWidgetItem(aluno))
            table.setItem(i, 1, QTableWidgetItem(plano))
            table.setItem(i, 2, QTableWidgetItem(valor))
            table.setItem(i, 3, QTableWidgetItem(venc))
            
            status_item = QTableWidgetItem(status)
            if status == "Pago":
                status_item.setForeground(QColor("#5eead4"))
            elif status == "Atrasado":
                status_item.setForeground(QColor("#f87171"))
            elif status == "Pendente":
                status_item.setForeground(QColor("#facc15"))
            table.setItem(i, 4, status_item)

        layout.addWidget(table)