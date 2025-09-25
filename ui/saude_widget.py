# ui/saude_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont

class SaudeAluno(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Saúde do Aluno")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Aluno", "Condição", "Severidade", "Medicamentos", "Restrições"])

        dados = [
            ("Maria Silva", "Asma", "Leve", "Inalador", "Evitar treinos intensos"),
            ("Lucas Ferreira", "Problema cardíaco", "Moderado", "Remédio diário", "Restrição em atividades pesadas"),
            ("Ana Paula", "Nenhuma", "-", "-", "-"),
        ]

        table.setRowCount(len(dados))
        for i, (aluno, cond, sev, med, rest) in enumerate(dados):
            table.setItem(i, 0, QTableWidgetItem(aluno))
            table.setItem(i, 1, QTableWidgetItem(cond))
            table.setItem(i, 2, QTableWidgetItem(sev))
            table.setItem(i, 3, QTableWidgetItem(med))
            table.setItem(i, 4, QTableWidgetItem(rest))

        layout.addWidget(table)
