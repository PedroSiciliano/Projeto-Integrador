# perfect_acqua_system/ui/dashboard_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QListWidget
)
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

        # linha de baixo: próximas aulas (full width) + tarefas + balanço
        main_grid.addWidget(self._create_upcoming_classes_table(), 1, 0, 1, 2)
        main_grid.addWidget(self._create_tasks_list(), 2, 0)
        main_grid.addWidget(self._create_monthly_balance_card(), 2, 1)

        layout.addLayout(main_grid)

        self.refresh_data()

    # ----------------------------------------------------------
    # Atualizar dados principais
    # ----------------------------------------------------------

    def refresh_data(self):
        # alunos ativos
        try:
            self.total_alunos = database.contar_alunos_ativos() or 0
        except Exception:
            self.total_alunos = 0

        # receita e despesas do mês (financeiro)
        try:
            self.receita_mes = float(database.calcular_receita_mes_atual() or 0.0)
        except Exception:
            self.receita_mes = 0.0

        try:
            self.despesas_mes = float(database.calcular_despesas_mes_atual() or 0.0)
        except Exception:
            self.despesas_mes = 0.0

        # limpa cards antigos
        for i in reversed(range(self.cards_grid.count())):
            item = self.cards_grid.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        # cards de resumo
        self.cards_grid.addWidget(
            self._create_summary_card("👥", "Alunos Ativos", str(self.total_alunos), "#5eead4"),
            0, 0
        )
        self.cards_grid.addWidget(
            self._create_summary_card("💰", "Receita do Mês", f"R$ {self.receita_mes:,.2f}", "#67e8f9"),
            0, 1
        )
        self.cards_grid.addWidget(
            self._create_summary_card("💸", "Despesas do Mês", f"R$ {self.despesas_mes:,.2f}", "#f87171"),
            0, 2
        )

        self.update_balance_card()
        self.popular_tabela_aulas()

    # ----------------------------------------------------------
    # Cards superiores
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # Tarefas rápidas
    # ----------------------------------------------------------

    def _create_tasks_list(self):
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        layout = QVBoxLayout(frame)
        title = QLabel("Tarefas Rápidas")
        title.setObjectName("ListCardTitle")
        layout.addWidget(title)
        task_list = QListWidget()
        task_list.addItems([
            "✔ Confirmar pagamentos pendentes",
            "📋 Cadastrar novas despesas",
            "📅 Agendar próximas aulas",
        ])
        layout.addWidget(task_list)
        return frame

    # ----------------------------------------------------------
    # Balanço do mês (entradas x saídas)
    # ----------------------------------------------------------

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
        # remove widgets atuais
        for i in reversed(range(self.balance_grid.count())):
            item = self.balance_grid.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)

        total = (self.receita_mes or 0.0) + (self.despesas_mes or 0.0)
        total_for_bar = total if total > 0 else 1.0

        self.balance_grid.addWidget(
            self._create_progress_indicator("Entradas", self.receita_mes or 0.0, total_for_bar, "#22c55e"),
            0, 0
        )
        self.balance_grid.addWidget(
            self._create_progress_indicator("Saídas", self.despesas_mes or 0.0, total_for_bar, "#ef4444"),
            0, 1
        )

    def _create_progress_indicator(self, title, value, total, color):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        value_label = QLabel(f"R$ {float(value):,.2f}")
        value_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")

        progress_bar = QProgressBar()
        try:
            max_int = int(total) if total and total > 0 else 100
        except Exception:
            max_int = 100
        try:
            val_int = int(value) if value and value > 0 else 0
        except Exception:
            val_int = 0
        progress_bar.setMaximum(max_int)
        progress_bar.setValue(min(val_int, max_int))
        progress_bar.setTextVisible(False)
        progress_bar.setStyleSheet(f"""
            QProgressBar {{ border: none; background-color: #334155; height: 6px; border-radius: 3px; }}
            QProgressBar::chunk {{ background-color: {color}; border-radius: 3px; }}
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(progress_bar)
        return frame

    # ----------------------------------------------------------
    # Próximas aulas
    # ----------------------------------------------------------

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
        """
        Usa database.buscar_proximas_aulas() para preencher:
        Coluna 0: Horário (data + hora ou apenas hora)
        Coluna 1: Turma/Descrição
        Coluna 2: Instrutor
        """
        try:
            dados = database.buscar_proximas_aulas() or []
        except Exception as e:
            print(f"[dashboard] erro ao buscar proximas aulas: {e}")
            dados = []

        self.table_aulas.setColumnCount(3)
        self.table_aulas.setHorizontalHeaderLabels(["Horário", "Turma", "Instrutor"])
        self.table_aulas.verticalHeader().setVisible(False)

        self.table_aulas.setRowCount(len(dados))

        for row, rec in enumerate(dados):
            horario = ""
            turma = ""
            instrutor = ""

            try:
                if isinstance(rec, dict):
                    # esperado de database.buscar_proximas_aulas:
                    # {id_aula,data,horario,observacoes,id_instrutor,nome_instrutor,...}
                    data_val = rec.get("data") or ""
                    hora_val = rec.get("horario") or rec.get("hora") or ""
                    if data_val and hora_val:
                        horario = f"{data_val} {hora_val}"
                    else:
                        horario = hora_val or data_val

                    turma = rec.get("observacoes") or rec.get("nivel") or rec.get("descricao") or ""
                    instrutor = rec.get("nome_instrutor") or rec.get("instrutor") or ""
                elif isinstance(rec, (list, tuple)):
                    seq = list(rec) + [""] * 5
                    # heurística: (id_aula, data, horario, observacoes, nome_instrutor, ...)
                    data_val = seq[1]
                    hora_val = seq[2]
                    if data_val and hora_val:
                        horario = f"{data_val} {hora_val}"
                    else:
                        horario = hora_val or data_val
                    turma = seq[3] or ""
                    instrutor = seq[4] or ""
                else:
                    s = str(rec)
                    parts = [p.strip() for p in s.split(" - ")]
                    horario = parts[0] if parts else s
                    turma = parts[1] if len(parts) > 1 else ""
                    instrutor = parts[2] if len(parts) > 2 else ""
            except Exception as e:
                print(f"[dashboard] erro normalizando registro de aula (linha {row}): {e}")
                horario = str(rec)
                turma = ""
                instrutor = ""

            horario = "" if horario is None else str(horario)
            turma = "" if turma is None else str(turma)
            instrutor = "" if instrutor is None else str(instrutor)

            try:
                self.table_aulas.setItem(row, 0, QTableWidgetItem(horario))
                self.table_aulas.setItem(row, 1, QTableWidgetItem(turma))
                self.table_aulas.setItem(row, 2, QTableWidgetItem(instrutor))
            except Exception as e:
                print(f"[dashboard] erro ao inserir célula (linha {row}): {e}")
