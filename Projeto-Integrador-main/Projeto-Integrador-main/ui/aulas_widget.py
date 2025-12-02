# perfect_acqua_system/ui/aulas_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import database


class Aulas(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Título
        title = QLabel("Agenda de Aulas")
        title.setObjectName("Title")
        subtitle = QLabel("Visualize e gerencie as aulas programadas")
        subtitle.setObjectName("Subtitle")

        header = QVBoxLayout()
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["Instrutor", "Data", "Horário", "Observações", "Qtd. Alunos"]
        )
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.tabela)

        # Preencher dados
        self.popular_tabela()

    # =====================================================================
    # 👉 BUSCAR AULAS REAIS NO SUPABASE
    # =====================================================================
    def popular_tabela(self):
        try:
            aulas = database.buscar_todas_aulas() or []
        except Exception:
            aulas = []

        self.tabela.setRowCount(len(aulas))

        for row, rec in enumerate(aulas):

            # Rec é dicionário vindo do Supabase
            instrutor = rec.get("instrutor_nome") or ""
            data = rec.get("data") or ""
            horario = rec.get("horario") or ""
            observacoes = rec.get("observacoes") or ""
            qtd_alunos = rec.get("qtd_alunos") or 0

            self.tabela.setItem(row, 0, QTableWidgetItem(str(instrutor)))
            self.tabela.setItem(row, 1, QTableWidgetItem(str(data)))
            self.tabela.setItem(row, 2, QTableWidgetItem(str(horario)))
            self.tabela.setItem(row, 3, QTableWidgetItem(str(observacoes)))

            qtd_item = QTableWidgetItem(str(qtd_alunos))
            qtd_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # cor verde quando há alunos
            if qtd_alunos > 0:
                qtd_item.setForeground(QColor("#4ade80"))
            self.tabela.setItem(row, 4, qtd_item)
