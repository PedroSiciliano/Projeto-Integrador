# perfect_acqua_system/ui/agenda_aulas_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, 
    QHeaderView, QTableWidgetItem, QDateEdit, QDialog, QComboBox, 
    QTimeEdit, QSpinBox, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QDate

# NOVA CLASSE: Diálogo para agendar uma nova aula
class AgendarAulaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agendar Nova Aula")
        self.setFixedSize(450, 350)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Detalhes da Nova Aula")
        title.setObjectName("Title")
        layout.addWidget(title)
        
        form_layout = QGridLayout()
        form_layout.setSpacing(10)

        # Campos do formulário baseados na tabela `aula`
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

        # Botões de ação
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
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # --- Cabeçalho ---
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
        # CONEXÃO DO SINAL DO BOTÃO
        btn_agendar.clicked.connect(self.abrir_dialog_agendamento)
        header_layout.addWidget(btn_agendar)
        layout.addLayout(header_layout)

        # --- Filtro de Data ---
        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Selecione a data:"))
        date_edit = QDateEdit(calendarPopup=True)
        date_edit.setDate(QDate.fromString("2025-09-11", "yyyy-MM-dd"))
        filtro_layout.addWidget(date_edit)
        filtro_layout.addStretch()
        layout.addLayout(filtro_layout)

        # --- Tabela de Aulas do Dia ---
        self.tabela_aulas = QTableWidget()
        self.tabela_aulas.setColumnCount(5)
        self.tabela_aulas.setHorizontalHeaderLabels(["Horário Início", "Horário Fim", "Nível", "Instrutor", "Vagas"])
        self.tabela_aulas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.popular_tabela()
        layout.addWidget(self.tabela_aulas)

    # NOVO MÉTODO: Para abrir o diálogo de agendamento
    def abrir_dialog_agendamento(self):
        dialog = AgendarAulaDialog(self)
        # O método .exec() abre o diálogo e espera o usuário interagir
        if dialog.exec():
            # Se o usuário clicou em "Salvar" (accept), o .exec() retorna True
            # Aqui você adicionaria a lógica para salvar os dados no banco de dados.
            # Por enquanto, vamos apenas mostrar uma mensagem de sucesso.
            QMessageBox.information(self, "Sucesso", "Nova aula agendada com sucesso!")
            # Idealmente, aqui você também atualizaria a tabela de aulas.
            # self.popular_tabela() 

    def popular_tabela(self):
        """Popula a tabela com dados mock para o dia selecionado."""
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