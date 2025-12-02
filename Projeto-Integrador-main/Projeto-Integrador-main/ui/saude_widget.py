# ui/saude_widget.py

import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


def _normalizar_condicao(rec):
    """
    Recebe um registro vindo do Supabase (dict ou tuple) e
    retorna um dicionário padronizado para exibição.
    """
    out = {
        "aluno": "",
        "condicao": "",
        "severidade": "",
        "medicamentos": "",
        "restricoes": ""
    }

    if rec is None:
        return out

    # dicionário (forma típica do Supabase)
    if isinstance(rec, dict):
        out["aluno"] = rec.get("nome_aluno") or rec.get("aluno") or ""
        out["condicao"] = rec.get("condicoes") or rec.get("condicao") or ""
        out["severidade"] = rec.get("severidade") or ""
        out["medicamentos"] = rec.get("medicamentos") or ""
        out["restricoes"] = rec.get("restricoes") or ""
        return out

    # tupla/lista
    if isinstance(rec, (list, tuple)):
        seq = list(rec) + [""] * 5
        out["aluno"], out["condicao"], out["severidade"], out["medicamentos"], out["restricoes"] = seq[:5]
        return out

    # fallback: string
    out["aluno"] = str(rec)
    return out


class SaudeAluno(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Saúde dos Alunos")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Aluno", "Condição", "Severidade", "Medicamentos", "Restrições"]
        )
        layout.addWidget(self.table)

        self.popular_tabela()

    def popular_tabela(self):
        """Carrega dados reais da tabela de saúde, se existir."""
        try:
            # Tenta função oficial do seu projeto
            if hasattr(database, "buscar_todas_condicoes"):
                dados = database.buscar_todas_condicoes()
            elif hasattr(database, "listar_condicoes"):
                dados = database.listar_condicoes()
            else:
                # como fallback, usa dados de condicao individual
                dados = database.buscar_condicao_aluno_todos() if hasattr(database, "buscar_condicao_aluno_todos") else []
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha ao carregar fichas de saúde:\n{e}")
            dados = []

        dados = dados or []

        self.table.setRowCount(len(dados))

        for i, rec in enumerate(dados):
            norm = _normalizar_condicao(rec)

            self.table.setItem(i, 0, QTableWidgetItem(norm["aluno"]))
            self.table.setItem(i, 1, QTableWidgetItem(norm["condicao"]))
            self.table.setItem(i, 2, QTableWidgetItem(norm["severidade"]))
            self.table.setItem(i, 3, QTableWidgetItem(norm["medicamentos"]))
            self.table.setItem(i, 4, QTableWidgetItem(norm["restricoes"]))
