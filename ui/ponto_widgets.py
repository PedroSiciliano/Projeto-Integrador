# perfect_acqua_system/ui/ponto_widgets.py
import database
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, QDateEdit, QPushButton, QDialog, QMessageBox, QLineEdit, QGridLayout, QTimeEdit
from PyQt6.QtCore import Qt, QDateTime, QDate, QTime, pyqtSignal

class PontoDialog(QDialog):
    def __init__(self, tipo_registro, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Registrar {tipo_registro}")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout(self)
        grid = QGridLayout()
        
        title = QLabel(f"Registrar {tipo_registro}")
        title.setObjectName("Title")
        layout.addWidget(title)
        
        grid.addWidget(QLabel("Instrutor:"), 0, 0)
        self.combo_instrutores = QComboBox()
        instrutores = database.buscar_instrutores()
        self.instrutores_map = {nome: id_ for id_, nome, _, _, _ in instrutores}
        self.combo_instrutores.addItems(self.instrutores_map.keys())
        grid.addWidget(self.combo_instrutores, 0, 1)

        # --- CORREÇÃO: Campos manuais de data e hora ---
        grid.addWidget(QLabel("Data:"), 1, 0)
        self.data_edit = QDateEdit(calendarPopup=True)
        self.data_edit.setDate(QDate.currentDate())
        grid.addWidget(self.data_edit, 1, 1)

        grid.addWidget(QLabel("Hora:"), 2, 0)
        self.hora_edit = QTimeEdit()
        self.hora_edit.setTime(QTime.currentTime())
        grid.addWidget(self.hora_edit, 2, 1)

        layout.addLayout(grid)
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancelar)
        btn_confirmar = QPushButton("Confirmar Registro")
        btn_confirmar.setProperty("class", "success")
        btn_confirmar.clicked.connect(self.accept)
        button_layout.addWidget(btn_confirmar)
        layout.addLayout(button_layout)

class FolhaDePonto(QWidget):
    ponto_registrado = pyqtSignal()

    def __init__(self):
        # ... (código do __init__ igual à versão anterior)
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Folha de Ponto")
        title.setObjectName("Title")
        layout.addWidget(title)
        
        top_layout = QHBoxLayout()
        action_layout = QHBoxLayout()
        btn_entrada = QPushButton("Registrar Entrada")
        btn_entrada.setProperty("class", "success")
        btn_entrada.clicked.connect(lambda: self.abrir_dialog("Entrada"))
        btn_saida = QPushButton("Registrar Saída")
        btn_saida.setProperty("class", "primary")
        btn_saida.clicked.connect(lambda: self.abrir_dialog("Saída"))
        top_layout.addStretch()
        top_layout.addWidget(btn_entrada)
        top_layout.addWidget(btn_saida)
        layout.addLayout(top_layout)

        self.tabela = QTableWidget()
        self.tabela.setAlternatingRowColors(True)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Instrutor", "Data", "Hora Entrada", "Hora Saída"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabela)
        self.aplicar_filtros()

    def aplicar_filtros(self):
        registros = database.buscar_registros_ponto()
        self.popular_tabela(registros)

    def popular_tabela(self, dados):
        self.tabela.setRowCount(0)
        self.tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            nome, data_str, entrada, saida = data
            data_formatada = QDate.fromString(data_str, "yyyy-MM-dd").toString("dd/MM/yyyy")
            self.tabela.setItem(row, 0, QTableWidgetItem(nome))
            self.tabela.setItem(row, 1, QTableWidgetItem(data_formatada))
            self.tabela.setItem(row, 2, QTableWidgetItem(entrada or "---"))
            self.tabela.setItem(row, 3, QTableWidgetItem(saida or "---"))

    def abrir_dialog(self, tipo):
        dialog = PontoDialog(tipo, self)
        if dialog.exec():
            nome_instrutor = dialog.combo_instrutores.currentText()
            id_instrutor = dialog.instrutores_map.get(nome_instrutor)
            
            # --- CORREÇÃO: Pega a data e hora do diálogo ---
            data_str = dialog.data_edit.date().toString("yyyy-MM-dd")
            hora_str = dialog.hora_edit.time().toString("HH:mm:ss")

            resultado = database.registrar_ponto(id_instrutor, data_str, hora_str, tipo)
            
            if resultado == "Sucesso":
                QMessageBox.information(self, "Sucesso", f"{tipo} registrada com sucesso!")
                self.ponto_registrado.emit()
            else:
                QMessageBox.warning(self, "Aviso", resultado)
