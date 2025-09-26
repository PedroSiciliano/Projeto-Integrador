# perfect_acqua_system/ui/aulas_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView

class Aulas(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Agenda de Aulas")
        title.setObjectName("Title")
        subtitle = QLabel("Visualize e gerencie as aulas programadas")
        subtitle.setObjectName("Subtitle")

        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)

        table = QTableWidget()
        table.verticalHeader().setVisible(False)
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Instrutor", "Data", "Horário", "Nível", "Alunos"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        dados = [
            ("Carlos Souza", "12/09/2025", "08:00 - 09:00", "Iniciante", "Maria, João"),
            ("Fernanda Lima", "12/09/2025", "09:00 - 10:00", "Avançado", "Lucas, Pedro"),
            ("Carlos Souza", "13/09/2025", "08:00 - 09:00", "Intermediário", "Ana, Rafael"),
        ]

        table.setRowCount(len(dados))
        for i, (instrutor, data, horario, nivel, alunos) in enumerate(dados):
            table.setItem(i, 0, QTableWidgetItem(instrutor))
            table.setItem(i, 1, QTableWidgetItem(data))
            table.setItem(i, 2, QTableWidgetItem(horario))
            table.setItem(i, 3, QTableWidgetItem(nivel))
            table.setItem(i, 4, QTableWidgetItem(alunos))

        layout.addWidget(table)