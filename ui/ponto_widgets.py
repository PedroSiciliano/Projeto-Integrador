# perfect_acqua_system/ui/ponto_widgets.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QHeaderView,
    QTableWidgetItem, QComboBox, QDateEdit, QPushButton, QDialog, QMessageBox
)
# CORREÇÃO: Adicionado QDate à importação
from PyQt6.QtCore import Qt, QDateTime, QDate

class PontoDialog(QDialog):
    def __init__(self, tipo_registro, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Registrar {tipo_registro}")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        title = QLabel(f"Registrar {tipo_registro} de Instrutor")
        title.setObjectName("Title")
        layout.addWidget(title)

        layout.addWidget(QLabel("Selecione o Instrutor:"))
        self.combo_instrutores = QComboBox()
        self.combo_instrutores.addItems(["Carlos Souza", "Fernanda Lima", "Ana Costa"])
        layout.addWidget(self.combo_instrutores)
        
        horario_atual = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm:ss")
        layout.addWidget(QLabel(f"Horário do Registro: {horario_atual}"))
        layout.addStretch()

        button_layout = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)

        btn_confirmar = QPushButton("Confirmar Registro")
        btn_confirmar.setProperty("class", "success")
        btn_confirmar.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(btn_cancelar)
        button_layout.addWidget(btn_confirmar)
        layout.addLayout(button_layout)

class FolhaDePonto(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Folha de Ponto")
        title.setObjectName("Title")
        subtitle = QLabel("Controle de entrada e saída dos instrutores")
        subtitle.setObjectName("Subtitle")
        
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)

        top_layout = QHBoxLayout()
        filtros = QHBoxLayout()
        filtros.setSpacing(10)
        filtros.addWidget(QLabel("Data:"))
        date_edit = QDateEdit(calendarPopup=True)
        # Esta linha agora funciona porque QDate foi importado
        date_edit.setDate(QDate.currentDate())
        filtros.addWidget(date_edit)
        filtros.addStretch()
        top_layout.addLayout(filtros)
        
        btn_entrada = QPushButton("Registrar Entrada")
        btn_entrada.setProperty("class", "success")
        btn_entrada.clicked.connect(lambda: self.abrir_dialog("Entrada"))
        
        btn_saida = QPushButton("Registrar Saída")
        btn_saida.setProperty("class", "primary")
        btn_saida.clicked.connect(lambda: self.abrir_dialog("Saída"))
        
        top_layout.addWidget(btn_entrada)
        top_layout.addWidget(btn_saida)
        layout.addLayout(top_layout)

        tabela = QTableWidget()
        tabela.verticalHeader().setVisible(False)
        tabela.setColumnCount(4)
        tabela.setHorizontalHeaderLabels(["Instrutor", "Data", "Hora Entrada", "Hora Saída"])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        dados = [
            ("Carlos Souza", "11/09/2025", "07:58", "17:02"),
            ("Fernanda Lima", "11/09/2025", "09:30", ""),
        ]
        
        tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabela.setItem(row, col, item)
        layout.addWidget(tabela)

    def abrir_dialog(self, tipo):
        dialog = PontoDialog(tipo, self)
        if dialog.exec():
            QMessageBox.information(self, "Sucesso", f"{tipo} registrada com sucesso!")