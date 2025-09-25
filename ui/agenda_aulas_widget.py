# perfect_acqua_system/ui/agenda_aulas_widget.py
<<<<<<< HEAD
import database
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QDateEdit, QDialog, QComboBox, QTimeEdit, QGridLayout, QMessageBox, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QDate, QTime, pyqtSignal

class GerenciarAlunosAulaDialog(QDialog):
    def __init__(self, id_aula, parent=None):
        super().__init__(parent)
        self.id_aula = id_aula
        self.setWindowTitle("Gerenciar Alunos na Aula")
        self.setMinimumSize(600, 400)
        
        layout = QHBoxLayout(self)
        
        # Painel da esquerda: Alunos disponíveis
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Alunos Disponíveis"))
        self.lista_disponiveis = QListWidget()
        left_panel.addWidget(self.lista_disponiveis)
        
        # Painel central: Botões de ação
        mid_panel = QVBoxLayout()
        mid_panel.addStretch()
        btn_adicionar = QPushButton(">>")
        btn_remover = QPushButton("<<")
        btn_adicionar.clicked.connect(self.adicionar_aluno)
        btn_remover.clicked.connect(self.remover_aluno)
        mid_panel.addWidget(btn_adicionar)
        mid_panel.addWidget(btn_remover)
        mid_panel.addStretch()
        
        # Painel da direita: Alunos na aula
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Alunos Matriculados"))
        self.lista_matriculados = QListWidget()
        right_panel.addWidget(self.lista_matriculados)
        
        layout.addLayout(left_panel)
        layout.addLayout(mid_panel)
        layout.addLayout(right_panel)
        
        # Botões de salvar/cancelar
        button_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(btn_salvar)
        
        right_panel.addLayout(button_layout)
        
        self.popular_listas()

    def popular_listas(self):
        self.lista_disponiveis.clear()
        self.lista_matriculados.clear()
        
        alunos_na_aula = database.buscar_alunos_da_aula(self.id_aula)
        for id_aluno, nome in alunos_na_aula:
            item = QListWidgetItem(nome)
            item.setData(Qt.ItemDataRole.UserRole, id_aluno)
            self.lista_matriculados.addItem(item)
            
        alunos_fora_da_aula = database.buscar_alunos_fora_da_aula(self.id_aula)
        for id_aluno, nome in alunos_fora_da_aula:
            item = QListWidgetItem(nome)
            item.setData(Qt.ItemDataRole.UserRole, id_aluno)
            self.lista_disponiveis.addItem(item)

    def adicionar_aluno(self):
        item_selecionado = self.lista_disponiveis.currentItem()
        if item_selecionado:
            self.lista_disponiveis.takeItem(self.lista_disponiveis.row(item_selecionado))
            self.lista_matriculados.addItem(item_selecionado)

    def remover_aluno(self):
        item_selecionado = self.lista_matriculados.currentItem()
        if item_selecionado:
            self.lista_matriculados.takeItem(self.lista_matriculados.row(item_selecionado))
            self.lista_disponiveis.addItem(item_selecionado)

    def get_ids_matriculados(self):
        ids = []
        for i in range(self.lista_matriculados.count()):
            item = self.lista_matriculados.item(i)
            ids.append(item.data(Qt.ItemDataRole.UserRole))
        return ids

class AgendaAulas(QWidget):
    aula_salva = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()
        title = QLabel("Agenda de Aulas")
        title.setObjectName("Title")
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
        self.date_edit.dateChanged.connect(self.popular_tabela)
        filtro_layout.addWidget(self.date_edit)
        filtro_layout.addStretch()
        layout.addLayout(filtro_layout)

        self.tabela_aulas = QTableWidget()
        self.tabela_aulas.setAlternatingRowColors(True)
        self.tabela_aulas.setColumnCount(7)
        self.tabela_aulas.setHorizontalHeaderLabels(["ID", "Início", "Fim", "Nível", "Instrutor", "Alunos", "Ações"])
        self.tabela_aulas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela_aulas.setColumnHidden(0, True)
        self.tabela_aulas.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        
        dummy_button = QPushButton("Ver Alunos")
        row_height = dummy_button.sizeHint().height() + 10
        self.tabela_aulas.verticalHeader().setDefaultSectionSize(row_height)

        layout.addWidget(self.tabela_aulas)
        self.popular_tabela()
        
    def abrir_dialog_agendamento(self):
        dialog = AgendarAulaDialog(self)
        if dialog.exec():
            data = dialog.data_edit.date().toString("yyyy-MM-dd")
            inicio = dialog.inicio_edit.time().toString("HH:mm")
            fim = dialog.fim_edit.time().toString("HH:mm")
            nivel = dialog.nivel_combo.currentText()
            nome_instrutor = dialog.instrutor_combo.currentText()
            
            instrutor = database.buscar_instrutor_por_nome(nome_instrutor)
            if not instrutor:
                QMessageBox.warning(self, "Erro", f"Instrutor '{nome_instrutor}' não encontrado.")
                return
            
            id_instrutor = instrutor[0]

            try:
                database.adicionar_aula(data, inicio, fim, nivel, id_instrutor)
                QMessageBox.information(self, "Sucesso", "Nova aula agendada!")
                self.aula_salva.emit() 
                self.popular_tabela()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível agendar.\nErro: {e}")

    def popular_tabela(self):
        self.tabela_aulas.setRowCount(0)
        data_selecionada = self.date_edit.date().toString("yyyy-MM-dd")
        dados_aulas = database.buscar_aulas_com_id_por_data(data_selecionada)
        
        self.tabela_aulas.setRowCount(len(dados_aulas))
        for row, data in enumerate(dados_aulas):
            id_aula, inicio, fim, nivel, instrutor, vagas = data
            self.tabela_aulas.setItem(row, 0, QTableWidgetItem(str(id_aula)))
            self.tabela_aulas.setItem(row, 1, QTableWidgetItem(inicio))
            self.tabela_aulas.setItem(row, 2, QTableWidgetItem(fim))
            self.tabela_aulas.setItem(row, 3, QTableWidgetItem(nivel))
            self.tabela_aulas.setItem(row, 4, QTableWidgetItem(instrutor or "N/A"))
            self.tabela_aulas.setItem(row, 5, QTableWidgetItem(f"{vagas} / 10"))

            btn_ver_alunos = QPushButton("Ver Alunos")
            btn_ver_alunos.clicked.connect(lambda _, r=row: self.gerenciar_alunos_aula(r))
            self.tabela_aulas.setCellWidget(row, 6, btn_ver_alunos)

    def gerenciar_alunos_aula(self, row):
        id_aula = int(self.tabela_aulas.item(row, 0).text())
        dialog = GerenciarAlunosAulaDialog(id_aula, self)
        if dialog.exec():
            ids_para_salvar = dialog.get_ids_matriculados()
            database.atualizar_alunos_na_aula(id_aula, ids_para_salvar)
            self.popular_tabela()
            QMessageBox.information(self, "Sucesso", "Lista de alunos atualizada!")

=======

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, 
    QHeaderView, QTableWidgetItem, QDateEdit, QDialog, QComboBox, 
    QTimeEdit, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, QTime

# ... (código da classe AgendarAulaDialog permanece o mesmo) ...
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
class AgendarAulaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agendar Nova Aula")
        self.setFixedSize(450, 400)
<<<<<<< HEAD
=======
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
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel("Agendar Nova Aula")
        title.setObjectName("Title")
        layout.addWidget(title)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(QLabel("Instrutor:"), 0, 0)
        self.instrutor_combo = QComboBox()
<<<<<<< HEAD
        
        instrutores = database.buscar_instrutores()
        self.instrutores = {nome: id_ for id_, nome, _, _, _ in instrutores}
        self.instrutor_combo.addItems(self.instrutores.keys())
        
=======
        self.instrutor_combo.addItems(["Carlos Souza", "Fernanda Lima", "Ana Costa"])
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
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
<<<<<<< HEAD
        layout.addLayout(button_layout)
=======
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
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
