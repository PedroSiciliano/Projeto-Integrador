# perfect_acqua_system/ui/dashboard_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFrame, 
    QGridLayout, QListWidgetItem, QTableWidget, QTableWidgetItem, 
    QHeaderView, QProgressBar
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        title_layout = QVBoxLayout()
        title = QLabel("Dashboard")
        title.setObjectName("Title")
        
        subtitle = QLabel("Visão geral do sistema Perfect Acqua")
        subtitle.setObjectName("Subtitle")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)

        cards_grid = QGridLayout()
        cards_grid.setSpacing(20)
        cards_grid.addWidget(self._create_summary_card("👥", "Total de Alunos", "4", "#5eead4"), 0, 0)
        cards_grid.addWidget(self._create_summary_card("👔", "Funcionários", "3", "#67e8f9"), 0, 1)
        cards_grid.addWidget(self._create_summary_card("⏰", "Pontos Hoje", "0", "#facc15"), 0, 2)
        cards_grid.addWidget(self._create_summary_card("⚠️", "Pendências", "3", "#f87171"), 0, 3)
        layout.addLayout(cards_grid)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        data_container = QVBoxLayout()
        data_container.setSpacing(20)
        data_container.addWidget(self._create_movimentacoes_panel())
        data_container.addWidget(self._create_lucros_table())
        bottom_layout.addLayout(data_container, 3)

        lists_container = QVBoxLayout()
        lists_container.setSpacing(20)
        lists_container.addWidget(self._create_list_card("📝 Atividade Recente", ["👩‍💼 Maria Silva - 10h", "👨‍💼 João Santos - 10h"]))
        lists_container.addWidget(self._create_list_card("💰 Pendências Financeiras", ["👨‍🎓 Pedro Oliveira - R$ 850,00", "👦 Lucas Ferreira - R$ 750,00"]))
        bottom_layout.addLayout(lists_container, 2)
        
        layout.addLayout(bottom_layout)
        layout.addStretch()

    def _create_summary_card(self, icon, title_text, value, color):
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        frame.setMinimumHeight(120)

        layout = QHBoxLayout(frame)
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 30))
        
        text_layout = QVBoxLayout()
        title_label = QLabel(title_text)
        title_label.setObjectName("SummaryCardTitle")
        value_label = QLabel(value)
        value_label.setObjectName("SummaryCardValue")
        value_label.setStyleSheet(f"color: {color};")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        return frame

    def _create_list_card(self, title, items):
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        
        vbox = QVBoxLayout(frame)
        lbl = QLabel(title)
        lbl.setObjectName("ListCardTitle")
        vbox.addWidget(lbl)
        
        list_widget = QListWidget()
        list_widget.setObjectName("DashboardList")
        for item_text in items:
            list_widget.addItem(QListWidgetItem(item_text))
        vbox.addWidget(list_widget)
        return frame

    def _create_lucros_table(self):
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        layout = QVBoxLayout(frame)

        title = QLabel("Resumo Mensal")
        title.setObjectName("ListCardTitle")
        layout.addWidget(title)
        
        tabela = QTableWidget()
        tabela.setColumnCount(3)
        tabela.setHorizontalHeaderLabels(["Mês", "Lucro", "Variação"])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabela.verticalHeader().setVisible(False)
        
        dados_lucro = [
            ("Junho/25", 8500, 1200), ("Julho/25", 9200, 700),
            ("Agosto/25", 11500, 2300), ("Setembro/25", 10800, -700)
        ]
        
        tabela.setRowCount(len(dados_lucro))
        for row, data in enumerate(dados_lucro):
            mes, lucro, variacao = data
            tabela.setItem(row, 0, QTableWidgetItem(mes))
            tabela.setItem(row, 1, QTableWidgetItem(f"R$ {lucro:,.2f}"))
            
            item_variacao = QTableWidgetItem(f"{'+' if variacao > 0 else ''} R$ {variacao:,.2f}")
            item_variacao.setForeground(QColor("#5eead4" if variacao > 0 else "#f87171"))
            tabela.setItem(row, 2, item_variacao)

        layout.addWidget(tabela)
        return frame

    def _create_movimentacoes_panel(self):
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)

        title = QLabel("Movimentações Financeiras (Mês)")
        title.setObjectName("ListCardTitle")
        layout.addWidget(title)
        
        entradas = 85000
        saidas = 32000
        total = entradas + saidas if entradas > saidas else saidas * 1.2 # Garante que a barra maior não preencha 100%

        grid = QGridLayout()
        grid.addWidget(self._create_progress_indicator("Entradas", entradas, total, "#22c55e"), 0, 0)
        grid.addWidget(self._create_progress_indicator("Saídas", saidas, total, "#ef4444"), 0, 1)
        layout.addLayout(grid)
        
        return frame

    def _create_progress_indicator(self, title, value, total, color):
        indicator_frame = QFrame()
        layout = QVBoxLayout(indicator_frame)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        
        value_label = QLabel(f"R$ {value:,.2f}")
        value_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        
        progress_bar = QProgressBar()
        progress_bar.setMaximum(int(total))
        progress_bar.setValue(int(value))
        progress_bar.setTextVisible(False)
        # Estilo da barra de progresso agora está no style.py
        
        # Adiciona uma folha de estilo específica para a cor da barra (chunk)
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none; background-color: #334155; height: 8px; border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {color}; border-radius: 4px;
            }}
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(progress_bar)
        
        return indicator_frame