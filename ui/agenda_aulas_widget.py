# perfect_acqua_system/ui/agenda_aulas_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, 
    QHeaderView, QTableWidgetItem, QDateEdit, QDialog, QComboBox, 
    QTimeEdit, QSpinBox, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QDate

class AgendarAulaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agendar Nova Aula")
        self.setFixedSize(450, 350)

        # --- ALTERAÇÃO AQUI: Define fundo escuro e texto branco para os campos ---
        self.setStyleSheet("""
            /* Define fundo escuro, texto branco e bordas para os campos */
            QComboBox, QDateEdit, QTimeEdit, QSpinBox {
                background-color: #2b3a4a;
                color: white;
                border: 1px solid #4f6987;
                border-radius: 4px;
                padding: 4px;
            }
            /* Estilo da lista suspensa (fundo branco, texto preto) */
            QComboBox QAbstractItemView {
                color: black;
                background-color: white;
                selection-background-color: #0078d7;
                border: 1px solid lightgray;
            }
            /* Rótulos com texto branco */
            QLabel {
                color: white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Detalhes da Nova Aula")
        title.setObjectName("Title")
        layout.addWidget(title)
        
        form_layout = QGridLayout()
        form_layout.setSpacing(10)

        form_layout.addWidget(QLabel("Instrutor:"), 0, 0)
        self.combo_instrutor = QComboBox()
        self.combo_instrutor.addItems(["Carlos Souza", "Fernanda Lima", "Ana Costa"])
        form_layout.addWidget(self.combo_instrutor, 0, 1)

        form_layout.addWidget(QLabel("Data da Aula:"), 1, 0)
        self.date_aula = QDateEdit(calendarPopup=True)
        self.date_aula.setDate(QDate.currentDate())
        form_layout.addWidget(self.date_aula, 1, 1)

        form_layout.addWidget(QLabel("Horário de Início:"), 2, 0)
        self.time_inicio = QTimeEdit()
        form_layout.addWidget(self.time_inicio, 2, 1)

        form_layout.addWidget(QLabel("Horário de Fim:"), 3, 0)
        self.time_fim = QTimeEdit()
        form_layout.addWidget(self.time_fim, 3, 1)

        form_layout.addWidget(QLabel("Nível:"), 4, 0)
        self.combo_nivel = QComboBox()
        self.combo_nivel.addItems(["Iniciante Infantil", "Iniciante Adulto", "Intermediário", "Avançado", "Hidroginástica"])
        form_layout.addWidget(self.combo_nivel, 4, 1)

        form_layout.addWidget(QLabel("Vagas:"), 5, 0)
        self.spin_vagas = QSpinBox()
        self.spin_vagas.setMinimum(1)
        self.spin_vagas.setMaximum(20)
        form_layout.addWidget(self.spin_vagas, 5, 1)

        layout.addLayout(form_layout)
        layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancelar)

        btn_salvar = QPushButton("Salvar Agendamento")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.accept)
        button_layout.addWidget(btn_salvar)

        layout.addLayout(button_layout)


class AgendaAulas(QWidget):
    # ... (código da classe AgendaAulas permanece o mesmo) ...
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()
        title = QLabel("Agenda de Aulas")
        title.setObjectName("Title")
        subtitle = QLabel("Gerencie as aulas agendadas por data")
        subtitle.setObjectName("Subtitle")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        btn_agendar = QPushButton("➕ Agendar Nova Aula")
        btn_agendar.setProperty("class", "primary")
        btn_agendar.clicked.connect(self.abrir_dialog_agendamento)
        header_layout.addWidget(btn_agendar)
        layout.addLayout(header_layout)

        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Selecione a data:"))
        date_edit = QDateEdit(calendarPopup=True)
        date_edit.setDate(QDate.fromString("2025-09-11", "yyyy-MM-dd"))
        filtro_layout.addWidget(date_edit)
        filtro_layout.addStretch()
        layout.addLayout(filtro_layout)

        self.tabela_aulas = QTableWidget()
        self.tabela_aulas.setColumnCount(5)
        self.tabela_aulas.setHorizontalHeaderLabels(["Horário Início", "Horário Fim", "Nível", "Instrutor", "Vagas"])
        self.tabela_aulas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.popular_tabela()
        layout.addWidget(self.tabela_aulas)

    def abrir_dialog_agendamento(self):
        dialog = AgendarAulaDialog(self)
        if dialog.exec():
            QMessageBox.information(self, "Sucesso", "Nova aula agendada com sucesso!")

    def popular_tabela(self):
        dados_aulas = [
            ("08:00", "09:00", "Iniciante Infantil", "Carlos Souza", "5/8"),
            ("10:00", "11:00", "Avançado Adulto", "Fernanda Lima", "10/10"),
            ("14:00", "15:00", "Hidroginástica", "Ana Costa", "12/12"),
        ]
        
        self.tabela_aulas.setRowCount(len(dados_aulas))
        for row, data in enumerate(dados_aulas):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela_aulas.setItem(row, col, item)