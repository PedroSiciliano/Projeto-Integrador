# perfect_acqua_system/ui/agenda_aulas_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, 
    QHeaderView, QTableWidgetItem, QDateEdit, QDialog, QComboBox, 
    QTimeEdit, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, QTime

# ... (código da classe AgendarAulaDialog permanece o mesmo) ...
class AgendarAulaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agendar Nova Aula")
        self.setFixedSize(450, 400)
        self.setStyleSheet("""
            QDialog { background-color: #1e293b; }
            QComboBox, QDateEdit, QTimeEdit {
                background-color: #2b3a4a; color: #e2e8f0;
                border: 1px solid #4f6987; border-radius: 5px; padding: 5px;
            }
            QComboBox:focus, QDateEdit:focus, QTimeEdit:focus { border: 1px solid #7dd3fc; }
            QComboBox QAbstractItemView {
                background-color: #f8fafc; color: #0f172a;
                selection-background-color: #38bdf8; selection-color: #f8fafc;
                border: 1px solid #94a3b8;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel("Agendar Nova Aula")
        title.setObjectName("Title")
        layout.addWidget(title)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(QLabel("Instrutor:"), 0, 0)
        self.instrutor_combo = QComboBox()
        self.instrutor_combo.addItems(["Carlos Souza", "Fernanda Lima", "Ana Costa"])
        grid.addWidget(self.instrutor_combo, 0, 1)
        grid.addWidget(QLabel("Data da Aula:"), 1, 0)
        self.data_edit = QDateEdit(calendarPopup=True)
        self.data_edit.setDate(QDate.currentDate())
        grid.addWidget(self.data_edit, 1, 1)
        grid.addWidget(QLabel("Horário de Início:"), 2, 0)
        self.inicio_edit = QTimeEdit()
        self.inicio_edit.setTime(QTime(8, 0))
        grid.addWidget(self.inicio_edit, 2, 1)
        grid.addWidget(QLabel("Horário de Fim:"), 3, 0)
        self.fim_edit = QTimeEdit()
        self.fim_edit.setTime(QTime(9, 0))
        grid.addWidget(self.fim_edit, 3, 1)
        grid.addWidget(QLabel("Nível da Turma:"), 4, 0)
        self.nivel_combo = QComboBox()
        self.nivel_combo.addItems(["Iniciante", "Intermediário", "Avançado", "Hidroginástica"])
        grid.addWidget(self.nivel_combo, 4, 1)
        layout.addLayout(grid)
        layout.addStretch()
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancelar)
        btn_salvar = QPushButton("Salvar")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.accept)
        button_layout.addWidget(btn_salvar)
        layout.addLayout(button_layout)

class AgendaAulas(QWidget):
    def __init__(self):
        super().__init__()
        # ... (código do layout e filtros permanece o mesmo) ...
        self.setStyleSheet("""
            QDateEdit {
                background-color: #2b3a4a; color: #e2e8f0;
                border: 1px solid #4f6987; border-radius: 5px; padding: 5px;
                min-width: 120px;
            }
            QDateEdit:focus { border: 1px solid #7dd3fc; }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()
        title = QLabel("Agenda de Aulas")
        title.setObjectName("Title")
        subtitle = QLabel("Gerencie as aulas agendadas por data")
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
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        filtro_layout.addWidget(self.date_edit)
        filtro_layout.addStretch()
        layout.addLayout(filtro_layout)

        self.tabela_aulas = QTableWidget()

        # --- ESTILO DA TABELA APLICADO AQUI ---
        self.tabela_aulas.setStyleSheet("""
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
        self.tabela_aulas.setAlternatingRowColors(True)

        self.tabela_aulas.setColumnCount(5)
        self.tabela_aulas.setHorizontalHeaderLabels(["Horário Início", "Horário Fim", "Nível", "Instrutor", "Vagas"])
        self.tabela_aulas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.popular_tabela()
        layout.addWidget(self.tabela_aulas)

    def abrir_dialog_agendamento(self):
        # ... (código da função permanece o mesmo) ...
        dialog = AgendarAulaDialog(self)
        if dialog.exec():
            QMessageBox.information(self, "Sucesso", "Nova aula agendada com sucesso!")
            self.popular_tabela() 

    def popular_tabela(self):
        # ... (código da função permanece o mesmo) ...
        dados_aulas = [
            ("08:00", "09:00", "Iniciante Infantil", "Carlos Souza", "5/8"),
            ("10:00", "11:00", "Avançado Adulto", "Fernanda Lima", "10/10"),
        ]
        self.tabela_aulas.setRowCount(len(dados_aulas))
        for row, data in enumerate(dados_aulas):
            for col, text in enumerate(data):
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela_aulas.setItem(row, col, item)