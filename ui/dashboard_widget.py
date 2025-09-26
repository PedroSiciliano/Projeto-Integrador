# perfect_acqua_system/ui/dashboard_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QListWidget
from PyQt6.QtGui import QFont
import database

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        title_layout = QVBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("Title")
        subtitle = QLabel("Visão geral do sistema Perfect Acqua")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)

        main_grid = QGridLayout()
        main_grid.setSpacing(20)

        self.cards_grid = QGridLayout()
        main_grid.addLayout(self.cards_grid, 0, 0, 1, 2)

        # --- CORREÇÃO: Novo layout com 3 painéis inferiores ---
        main_grid.addWidget(self._create_upcoming_classes_table(), 1, 0, 1, 2) # Próximas aulas ocupa a linha inteira
        main_grid.addWidget(self._create_tasks_list(), 2, 0) # Tarefas na coluna 0
        main_grid.addWidget(self._create_monthly_balance_card(), 2, 1) # Balanço na coluna 1
        
        layout.addLayout(main_grid)
        self.refresh_data()

    def refresh_data(self):
        self.total_alunos = database.contar_alunos_ativos()
        self.receita_mes = database.calcular_receita_mes_atual()
        self.despesas_mes = database.calcular_despesas_mes_atual()

        for i in reversed(range(self.cards_grid.count())): 
            self.cards_grid.itemAt(i).widget().setParent(None)

        self.cards_grid.addWidget(self._create_summary_card("👥", "Alunos Ativos", str(self.total_alunos), "#5eead4"), 0, 0)
        self.cards_grid.addWidget(self._create_summary_card("💰", "Receita do Mês", f"R$ {self.receita_mes:,.2f}", "#67e8f9"), 0, 1)
        self.cards_grid.addWidget(self._create_summary_card("💸", "Despesas do Mês", f"R$ {self.despesas_mes:,.2f}", "#f87171"), 0, 2)
        
        self.update_balance_card()
        self.popular_tabela_aulas()

    def _create_summary_card(self, icon, title, value, color):
        card = QFrame()
        card.setProperty("class", "CardFrame")
        layout = QHBoxLayout(card)
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", 24))
        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("Subtitle")
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        return card

    # --- CORREÇÃO: Método para criar a lista de Tarefas Rápidas ---
    def _create_tasks_list(self):
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        layout = QVBoxLayout(frame)
        title = QLabel("Tarefas Rápidas")
        title.setObjectName("ListCardTitle")
        layout.addWidget(title)
        task_list = QListWidget()
        task_list.addItems(["✔ Confirmar pagamentos pendentes", "📋 Cadastrar novas despesas", "📅 Agendar próximas aulas"])
        layout.addWidget(task_list)
        return frame

    def _create_monthly_balance_card(self):
        self.balance_frame = QFrame()
        self.balance_frame.setProperty("class", "CardFrame")
        layout = QVBoxLayout(self.balance_frame)
        title = QLabel("Balanço do Mês")
        title.setObjectName("ListCardTitle")
        layout.addWidget(title)
        self.balance_grid = QGridLayout()
        layout.addLayout(self.balance_grid)
        return self.balance_frame

    def update_balance_card(self):
        for i in reversed(range(self.balance_grid.count())): 
            self.balance_grid.itemAt(i).widget().setParent(None)
        
        total = self.receita_mes + self.despesas_mes
        self.balance_grid.addWidget(self._create_progress_indicator("Entradas", self.receita_mes, total, "#22c55e"), 0, 0)
        self.balance_grid.addWidget(self._create_progress_indicator("Saídas", self.despesas_mes, total, "#ef4444"), 0, 1)

    def _create_progress_indicator(self, title, value, total, color):
        indicator_frame = QFrame()
        layout = QVBoxLayout(indicator_frame)
        title_label = QLabel(title)
        value_label = QLabel(f"R$ {value:,.2f}")
        value_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        progress_bar = QProgressBar()
        progress_bar.setMaximum(int(total) if total > 0 else 100)
        progress_bar.setValue(int(value))
        progress_bar.setTextVisible(False)
        progress_bar.setStyleSheet(f"""
            QProgressBar {{ border: none; background-color: #334155; height: 6px; border-radius: 3px; }}
            QProgressBar::chunk {{ background-color: {color}; border-radius: 3px; }}
        """)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(progress_bar)
        return indicator_frame

    def _create_upcoming_classes_table(self):
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        layout = QVBoxLayout(frame)
        title = QLabel("Próximas Aulas")
        title.setObjectName("ListCardTitle")
        layout.addWidget(title)
        
        self.table_aulas = QTableWidget()
        self.table_aulas.setColumnCount(3)
        self.table_aulas.setHorizontalHeaderLabels(["Horário", "Turma", "Instrutor"])
        self.table_aulas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_aulas.verticalHeader().setVisible(False)
        layout.addWidget(self.table_aulas)
        return frame
        
    def popular_tabela_aulas(self):
        dados = database.buscar_proximas_aulas()
        self.table_aulas.setRowCount(len(dados))
        for row, data_row in enumerate(dados):
            for col, data_cell in enumerate(data_row):
                self.table_aulas.setItem(row, col, QTableWidgetItem(data_cell))
