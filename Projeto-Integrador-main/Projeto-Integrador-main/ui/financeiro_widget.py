# perfect_acqua_system/ui/financeiro_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QComboBox, QLineEdit, QGridLayout, QMessageBox,
    QFrame, QInputDialog
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import pyqtSignal
import database
import re


def _parse_valor_text(text: str) -> float:
    """Converte 'R$ 120,00', '120.00', '120,00' em float."""
    if not text:
        raise ValueError("Vazio")
    s = text.strip().replace("R$", "").replace(" ", "").replace(".", "")
    s = s.replace(",", ".")
    if not re.match(r"^[0-9]*\.?[0-9]+$", s):
        raise ValueError("Formato inválido")
    return float(s)


class Financeiro(QWidget):
    mensalidade_paga = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Controle Financeiro")
        title.setObjectName("Title")

        subtitle = QLabel("Acompanhe e gerencie as mensalidades dos alunos")

        header = QVBoxLayout()
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # =====================  FILTROS  =========================

        top_panel = QFrame()
        top_panel.setProperty("class", "CardFrame")
        top_layout = QVBoxLayout(top_panel)
        grid = QGridLayout()

        grid.addWidget(QLabel("Status:"), 0, 0)
        self.filtro_status = QComboBox()
        self.filtro_status.addItems(["Todos", "Pendente", "Pago", "Atrasado"])
        grid.addWidget(self.filtro_status, 0, 1)

        grid.addWidget(QLabel("Mês/Ano (mes_referencia):"), 0, 2)
        self.filtro_data = QLineEdit(placeholderText="Ex: 2025-09")
        grid.addWidget(self.filtro_data, 0, 3)

        btn_filtrar = QPushButton("🔎 Filtrar")
        btn_filtrar.setProperty("class", "primary")
        btn_filtrar.clicked.connect(self.popular_tabela)
        grid.addWidget(btn_filtrar, 0, 4)

        top_layout.addLayout(grid)
        layout.addWidget(top_panel)

        # =====================  TABELA  =========================

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Aluno", "Plano", "Valor", "Vencimento", "Status", "Ações"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        dummy = QPushButton("✔ Marcar como Pago")
        self.table.verticalHeader().setDefaultSectionSize(dummy.sizeHint().height() + 10)

        layout.addWidget(self.table)

        self.popular_tabela()

    # ============================================================
    #  AUXILIARES
    # ============================================================

    def _format_valor(self, valor) -> str:
        try:
            if valor is None:
                return "R$ 0,00"
            v = float(valor)
            return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return "R$ 0,00"

    # ============================================================
    #  POPULAR TABELA DE MENSALIDADES
    # ============================================================

    def popular_tabela(self):
        """
        Usa database.listar_mensalidades(), que retorna:
        id_mensalidade, id_aluno, mes_referencia, valor_praticado,
        valor_pago, data_vencimento, data_pagamento, status, ...
        """
        try:
            dados = database.listar_mensalidades() or []
        except Exception as e:
            print("DEBUG FINANCEIRO - erro ao listar:", e)
            dados = []

        # enriquecer com nome do aluno (opcional)
        alunos_map = {}
        try:
            alunos = database.buscar_alunos(1000)
            for a in alunos:
                aid = a.get("id_aluno") or a.get("id")
                alunos_map[str(aid)] = a.get("nome_completo") or a.get("nome") or ""
        except Exception:
            pass

        # FILTRO STATUS
        fs = self.filtro_status.currentText()
        if fs != "Todos":
            dados = [d for d in dados if str(d.get("status") or "").lower() == fs.lower()]

        # FILTRO MÊS/ANO usando mes_referencia (ex: "2025-09")
        mesano = self.filtro_data.text().strip()
        if mesano:
            dados = [d for d in dados if mesano in str(d.get("mes_referencia", ""))]

        self.table.setRowCount(len(dados))

        for row, rec in enumerate(dados):
            id_mens = rec.get("id_mensalidade")
            id_aluno = rec.get("id_aluno")
            aluno_nome = alunos_map.get(str(id_aluno), str(id_aluno) if id_aluno is not None else "")
            plano_nome = ""  # não vem direto do banco; pode ser preenchido depois se você ligar com planos

            valor = rec.get("valor_praticado", 0.0)
            venc = rec.get("data_vencimento", "")
            status = rec.get("status", "") or ""

            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(id_mens) if id_mens is not None else ""))

            # ALUNO
            self.table.setItem(row, 1, QTableWidgetItem(str(aluno_nome)))

            # PLANO (placeholder)
            self.table.setItem(row, 2, QTableWidgetItem(str(plano_nome)))

            # VALOR formatado
            self.table.setItem(row, 3, QTableWidgetItem(self._format_valor(valor)))

            # VENCIMENTO
            self.table.setItem(row, 4, QTableWidgetItem(str(venc)))

            # STATUS com cor
            st_item = QTableWidgetItem(str(status))
            st = status.lower().strip()

            if st == "pago":
                st_item.setForeground(QColor("#22c55e"))
            elif st == "atrasado":
                st_item.setForeground(QColor("#ef4444"))
            else:  # pendente ou qualquer outro
                st_item.setForeground(QColor("#facc15"))

            self.table.setItem(row, 5, st_item)

            # BOTÃO "PAGAR"
            if st in ["pendente", "atrasado"]:
                btn = QPushButton("✔ Marcar como Pago")
                btn.setProperty("class", "success")
                btn.clicked.connect(lambda _, mid=id_mens: self.marcar_como_pago(mid))
                self.table.setCellWidget(row, 6, btn)
            else:
                self.table.setCellWidget(row, 6, QLabel("✓"))

    # ============================================================
    #  MARCAR MENSALIDADE COMO PAGA
    # ============================================================

    def marcar_como_pago(self, id_mensalidade):
        if not id_mensalidade:
            QMessageBox.warning(self, "Erro", "ID inválido.")
            return

        # PERGUNTA VALOR
        txt, ok = QInputDialog.getText(
            self,
            "Valor pago",
            "Informe o valor pago (ex: 120,00):"
        )
        if not ok:
            return

        try:
            valor_pago = _parse_valor_text(txt)
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Valor inválido: {e}")
            return

        # CONFIRMAÇÃO
        c = QMessageBox.question(
            self,
            "Confirmar",
            f"Confirmar pagamento no valor de {self._format_valor(valor_pago)} ?"
        )
        if c != QMessageBox.StandardButton.Yes:
            return

        try:
            database.marcar_mensalidade_paga(
                id_mensalidade=id_mensalidade,
                valor_pago=valor_pago
            )
            QMessageBox.information(self, "Sucesso", "Mensalidade paga!")
            self.popular_tabela()
            self.mensalidade_paga.emit()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao registrar pagamento:\n{e}")
