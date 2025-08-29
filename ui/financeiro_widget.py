# perfect_acqua_system/ui/financeiro_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QHeaderView,
    QTableWidgetItem, QComboBox, QLineEdit, QPushButton, QFrame
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class Financeiro(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        header_layout = QHBoxLayout()
        header_text_layout = QVBoxLayout()
        title = QLabel("Gestão Financeira")
        title.setObjectName("Title")
        subtitle = QLabel("Controle de mensalidades e pendências")
        subtitle.setObjectName("Subtitle")
        header_text_layout.addWidget(title)
        header_text_layout.addWidget(subtitle)
        
        btn_nova_cobranca = QPushButton("➕ Nova Cobrança")
        btn_nova_cobranca.setProperty("class", "primary")
        
        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        header_layout.addWidget(btn_nova_cobranca)
        layout.addLayout(header_layout)

        filtros_frame = QFrame()
        filtros_frame.setStyleSheet("background-color: #1e293b; border-radius: 10px; padding: 15px; border: 1px solid #334155;")
        filtros_layout = QHBoxLayout(filtros_frame)
        filtros_layout.setSpacing(10)
        filtros_layout.addWidget(QLabel("Status:"))
        filtros_layout.addWidget(QComboBox())
        filtros_layout.addWidget(QLabel("Aluno:"))
        filtros_layout.addWidget(QLineEdit(placeholderText="Buscar por nome..."))
        filtros_layout.addStretch()
        layout.addWidget(filtros_frame)

        tabela = QTableWidget()
        tabela.verticalHeader().setVisible(False)
        tabela.setColumnCount(5)
        tabela.setHorizontalHeaderLabels(["Aluno", "Vencimento", "Valor", "Status", "Ações"])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        dados = [
            ("Lucas Ferreira", "14/08/2025", "R$ 750,00", "Atrasado"),
            ("Pedro Oliveira", "09/08/2025", "R$ 850,00", "Atrasado"),
        ]
        tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                if col == 3: 
                    item.setForeground(QColor("#f87171"))
                tabela.setItem(row, col, item)
            
            btn_pagar = QPushButton("Marcar como Pago")
            btn_pagar.setProperty("class", "table-success")
            btn_pagar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_pagar.clicked.connect(lambda checked, b=btn_pagar: self.marcar_como_pago(b))
            tabela.setCellWidget(row, 4, btn_pagar)
        layout.addWidget(tabela)

    def marcar_como_pago(self, button):
        button.setText("✅ Pago")
        button.setDisabled(True)