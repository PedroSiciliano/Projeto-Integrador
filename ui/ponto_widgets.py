# perfect_acqua_system/ui/ponto_widgets.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QHeaderView,
    QTableWidgetItem, QComboBox, QDateEdit, QPushButton, QDialog, QMessageBox,
    QLineEdit, QGridLayout  # QGridLayout adicionado aqui
)
from PyQt6.QtCore import Qt, QDateTime, QDate

class PontoDialog(QDialog):
    def __init__(self, tipo_registro, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Registrar {tipo_registro}")
        self.setFixedSize(400, 250)

        self.setStyleSheet("""
            QComboBox { color: white; }
            QComboBox QAbstractItemView { color: black; background-color: white; }
        """)

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
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QLineEdit, QDateEdit {
                background-color: #2b3a4a;
                color: #e2e8f0;
                border: 1px solid #4f6987;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 1px solid #7dd3fc;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Folha de Ponto")
        title.setObjectName("Title")
        subtitle = QLabel("Controle de entrada e saída dos instrutores")
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        top_layout = QHBoxLayout()
        filtros = QGridLayout()
        filtros.setSpacing(10)

        filtros.addWidget(QLabel("Filtrar por Instrutor:"), 0, 0)
        self.filtro_nome = QLineEdit(placeholderText="Digite o nome do instrutor...")
        filtros.addWidget(self.filtro_nome, 0, 1)

        filtros.addWidget(QLabel("Período:"), 0, 2)
        self.filtro_data_inicio = QDateEdit(calendarPopup=True)
        self.filtro_data_inicio.setDate(QDate.currentDate().addDays(-30))
        filtros.addWidget(self.filtro_data_inicio, 0, 3)
        filtros.addWidget(QLabel("até"), 0, 4)
        self.filtro_data_fim = QDateEdit(calendarPopup=True)
        self.filtro_data_fim.setDate(QDate.currentDate())
        filtros.addWidget(self.filtro_data_fim, 0, 5)

        self.btn_buscar = QPushButton("🔎 Buscar")
        self.btn_buscar.setProperty("class", "primary")
        filtros.addWidget(self.btn_buscar, 0, 6)
        
        filtros.setColumnStretch(1, 1)

        top_layout.addLayout(filtros)
        top_layout.addStretch()
        
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        btn_entrada = QPushButton("Registrar Entrada")
        btn_entrada.setProperty("class", "success")
        btn_entrada.clicked.connect(lambda: self.abrir_dialog("Entrada"))
        
        btn_saida = QPushButton("Registrar Saída")
        btn_saida.setProperty("class", "primary")
        btn_saida.clicked.connect(lambda: self.abrir_dialog("Saída"))
        
        action_layout.addWidget(btn_entrada)
        action_layout.addWidget(btn_saida)
        
        layout.addLayout(top_layout)
        layout.addLayout(action_layout)

        self.tabela = QTableWidget()
        self.tabela.setStyleSheet("""
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
        self.tabela.setAlternatingRowColors(True)
        
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Instrutor", "Data", "Hora Entrada", "Hora Saída"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.todos_os_registros = [
            ("Carlos Souza", "11/09/2025", "07:58", "17:02"),
            ("Fernanda Lima", "11/09/2025", "09:30", ""),
            ("Carlos Souza", "10/09/2025", "08:01", "17:05"),
            ("Ana Costa", "10/09/2025", "13:00", "21:00"),
            ("Fernanda Lima", "09/09/2025", "09:25", "18:30"),
        ]
        
        layout.addWidget(self.tabela)
        
        self.btn_buscar.clicked.connect(self.aplicar_filtros)
        self.filtro_nome.textChanged.connect(self.aplicar_filtros)

        self.aplicar_filtros()

    def aplicar_filtros(self):
        texto_filtro = self.filtro_nome.text().lower()
        data_inicio = self.filtro_data_inicio.date()
        data_fim = self.filtro_data_fim.date()

        registros_filtrados = []
        for nome, data_str, entrada, saida in self.todos_os_registros:
            data_registro = QDate.fromString(data_str, "dd/MM/yyyy")
            
            match_nome = texto_filtro in nome.lower()
            match_data = data_inicio <= data_registro <= data_fim
            
            if match_nome and match_data:
                registros_filtrados.append((nome, data_str, entrada, saida))
        
        self.popular_tabela(registros_filtrados)

    def popular_tabela(self, dados):
        self.tabela.setRowCount(0)
        self.tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row, col, item)

    def abrir_dialog(self, tipo):
        dialog = PontoDialog(tipo, self)
        if dialog.exec():
            QMessageBox.information(self, "Sucesso", f"{tipo} registrada com sucesso!")