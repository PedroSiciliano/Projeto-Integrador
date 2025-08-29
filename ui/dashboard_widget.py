# perfect_acqua_system/ui/dashboard_widget.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFrame, QGridLayout, QListWidgetItem
from PyQt6.QtGui import QFont

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Título principal
        title = QLabel("Dashboard")
        title.setObjectName("Title")
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff; margin-bottom: 5px;")
        
        subtitle = QLabel("Gestão Perfect Acqua")
        subtitle.setObjectName("Subtitle")
        subtitle.setFont(QFont("Segoe UI", 18))
        subtitle.setStyleSheet("color: #94a3b8; margin-bottom: 20px;")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Cards resumo
        cards_grid = QGridLayout()
        cards_grid.setSpacing(20)
        cards_grid.addWidget(self._create_summary_card("👥", "Total de Alunos", "4", "#5eead4"), 0, 0)
        cards_grid.addWidget(self._create_summary_card("👔", "Funcionários", "3", "#67e8f9"), 0, 1)
        cards_grid.addWidget(self._create_summary_card("⏰", "Pontos Hoje", "0", "#facc15"), 0, 2)
        cards_grid.addWidget(self._create_summary_card("⚠️", "Pendências", "3", "#f87171"), 0, 3)
        layout.addLayout(cards_grid)

        # Parte inferior
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        bottom_layout.setContentsMargins(0, 20, 0, 0)
        bottom_layout.addWidget(
            self._create_list_card("📝 Atividade Recente", ["👩‍💼 Maria Silva - 10h", "👨‍💼 João Santos - 10h"]), 2
        )
        bottom_layout.addWidget(
            self._create_list_card("💰 Pendências Financeiras", ["👨‍🎓 Pedro Oliveira - R$ 850,00", "👦 Lucas Ferreira - R$ 750,00"]), 1
        )
        layout.addLayout(bottom_layout)
        
        layout.addStretch()

    def _create_summary_card(self, icon, title, value, color):
        frame = QFrame()
        frame.setStyleSheet(
            "background-color: #1e293b; "
            "border-radius: 12px; "
            "padding: 24px; "
            "border: 2px solid #475569;"  # borda mais grossa
        )
        
        layout = QHBoxLayout(frame)
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 30))
        
        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("color:#94a3b8; font-size: 16px; font-weight: 600;")
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        return frame

    def _create_list_card(self, title, items):
        frame = QFrame()
        frame.setStyleSheet(
            "background-color: #1e293b; "
            "border-radius: 12px; "
            "padding: 20px; "
            "border: 2px solid #475569;"  # borda mais grossa
        )
        vbox = QVBoxLayout(frame)

        # Título da seção
        lbl = QLabel(title)
        lbl.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        lbl.setStyleSheet("color: #ffffff; margin-bottom: 12px;")
        vbox.addWidget(lbl)
        
        # Lista customizada
        list_widget = QListWidget()
        list_widget.setStyleSheet(
            "border: none; "
            "background-color: #0f172a; "
            "border-radius: 8px; "
            "padding: 6px; "
            "font-size: 15px; "
            "color: #cbd5e1;"
        )
        
        for item_text in items:
            item = QListWidgetItem(item_text)
            item.setFont(QFont("Segoe UI", 14))
            list_widget.addItem(item)

        # Estilo das linhas dos itens
        list_widget.setStyleSheet(
            """
            QListWidget {
                background-color: #0f172a;
                border-radius: 8px;
                padding: 6px;
                font-size: 15px;
                color: #cbd5e1;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #475569;  /* linha mais forte */
            }
            QListWidget::item:last-child {
                border: none; /* remove linha do último */
            }
            """
        )

        vbox.addWidget(list_widget)
        return frame
