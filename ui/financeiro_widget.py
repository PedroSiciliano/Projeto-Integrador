# perfect_acqua_system/ui/financeiro_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QColor

class Financeiro(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Controle Financeiro")
        # ... (código do cabeçalho permanece o mesmo) ...
        title.setObjectName("Title")
        subtitle = QLabel("Acompanhe as mensalidades e o status de pagamento dos alunos")
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)

        table = QTableWidget()

        # --- ESTILO DA TABELA APLICADO AQUI ---
        table.setStyleSheet("""
            QTableWidget {
                background-color: #1e293b;
                alternate-background-color: #2b3a4a;
                border: none;
                gridline-color: #4f6987;
            }
            QTableWidget::viewport {
                background-color: #1e293b;
                border: none;
            }
            QHeaderView::section {
                background-color: #2b3a4a;
                color: #94a3b8;
                padding: 4px;
                border: none;
                border-bottom: 1px solid #4f6987;
            }
            QHeaderView::section:horizontal {
                border-right: 1px solid #4f6987;
            }
            QTableCornerButton::section {
                background-color: #2b3a4a;
            }
        """)
        table.setAlternatingRowColors(True)

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
            # ... (código de preenchimento da tabela permanece o mesmo) ...
            table.setItem(i, 0, QTableWidgetItem(aluno))
            table.setItem(i, 1, QTableWidgetItem(plano))
            table.setItem(i, 2, QTableWidgetItem(valor))
            table.setItem(i, 3, QTableWidgetItem(venc))
            status_item = QTableWidgetItem(status)
            if status == "Pago":
                status_item.setForeground(QColor("#22c55e"))
            elif status == "Atrasado":
                status_item.setForeground(QColor("#ef4444"))
            else:
                status_item.setForeground(QColor("#facc15"))
            table.setItem(i, 4, status_item)
            
        layout.addWidget(table)