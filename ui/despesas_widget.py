# perfect_acqua_system/ui/despesas_widget.py

<<<<<<< HEAD
import database
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QDialog, QLineEdit, QDoubleSpinBox,
    QDateEdit, QGridLayout, QMessageBox
)
# --- CORREÇÃO: Importar pyqtSignal ---
from PyQt6.QtCore import QDate, pyqtSignal

class Despesas(QWidget):
    # --- CORREÇÃO: Adicionar o sinal que estava faltando ---
    despesa_salva = pyqtSignal()

=======
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QDialog, QLineEdit, QDoubleSpinBox,
    QDateEdit, QGridLayout, QMessageBox, QFrame
)
from PyQt6.QtCore import QDate

class Despesas(QWidget):
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()
        title = QLabel("Controle de Despesas")
        title.setObjectName("Title")
        subtitle = QLabel("Registre e acompanhe as saídas e custos da academia")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        btn_adicionar = QPushButton("➕ Adicionar Despesa")
        btn_adicionar.setProperty("class", "primary")
        btn_adicionar.clicked.connect(self.abrir_dialog_despesa)
        header_layout.addWidget(btn_adicionar)
        layout.addLayout(header_layout)

        self.tabela = QTableWidget()
<<<<<<< HEAD
        self.tabela.setAlternatingRowColors(True)
=======
        self.setup_table_style()
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Data", "Descrição", "Categoria", "Valor"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        
        self.popular_tabela()
        layout.addWidget(self.tabela)

<<<<<<< HEAD
    def popular_tabela(self):
        dados = database.buscar_despesas()
        self.tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            data_formatada = list(data)
            data_formatada[3] = f"R$ {data[3]:.2f}"
            for col, text in enumerate(data_formatada):
                self.tabela.setItem(row, col, QTableWidgetItem(str(text)))
=======
    def setup_table_style(self):
        self.tabela.setStyleSheet("""
            QTableWidget { background-color: #1e293b; alternate-background-color: #2b3a4a;
                           border: none; gridline-color: #4f6987; }
            QTableWidget::viewport { background-color: #1e293b; border: none; }
            QHeaderView::section { background-color: #2b3a4a; color: #94a3b8; padding: 4px;
                                   border: none; border-bottom: 1px solid #4f6987; }
            QHeaderView::section:horizontal { border-right: 1px solid #4f6987; }
            QTableCornerButton::section { background-color: #2b3a4a; }
        """)
        self.tabela.setAlternatingRowColors(True)

    def popular_tabela(self):
        # Esta função buscaria os dados do banco de dados
        dados = [
            ("15/09/2025", "Salário Instrutor Carlos", "Recursos Humanos", "R$ 1.500,00"),
            ("10/09/2025", "Conta de Luz", "Infraestrutura", "R$ 350,70"),
            ("05/09/2025", "Material de Limpeza", "Manutenção", "R$ 120,00"),
        ]
        
        self.tabela.setRowCount(len(dados))
        for row, data in enumerate(dados):
            for col, text in enumerate(data):
                self.tabela.setItem(row, col, QTableWidgetItem(text))
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6

    def abrir_dialog_despesa(self):
        dialog = NovaDespesaDialog(self)
        if dialog.exec():
<<<<<<< HEAD
            data = dialog.data_edit.date().toString("yyyy-MM-dd")
            desc = dialog.desc_edit.text()
            cat = dialog.cat_edit.text()
            valor = dialog.valor_spin.value()

            if not desc or valor == 0:
                QMessageBox.warning(self, "Erro", "Descrição e Valor são obrigatórios.")
                return

            try:
                database.adicionar_despesa(data, desc, cat, valor)
                QMessageBox.information(self, "Sucesso", "Despesa registrada!")
                self.popular_tabela()
                # --- CORREÇÃO: Emitir o sinal para o Dashboard atualizar ---
                self.despesa_salva.emit()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível salvar a despesa.\nErro: {e}")
=======
            # Aqui iria a lógica para salvar a despesa no banco
            QMessageBox.information(self, "Sucesso", "Despesa registrada!")
            self.popular_tabela()
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6

class NovaDespesaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Nova Despesa")
<<<<<<< HEAD
=======
        
        # Estilo para os campos do formulário
        self.setStyleSheet("""
            QLineEdit, QDateEdit, QDoubleSpinBox {
                background-color: #2b3a4a; color: #e2e8f0;
                border: 1px solid #4f6987; border-radius: 5px; padding: 5px;
            }
        """)
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6

        layout = QVBoxLayout(self)
        grid = QGridLayout()
        
        grid.addWidget(QLabel("Data:"), 0, 0)
        self.data_edit = QDateEdit(calendarPopup=True)
        self.data_edit.setDate(QDate.currentDate())
        grid.addWidget(self.data_edit, 0, 1)

        grid.addWidget(QLabel("Descrição:"), 1, 0)
        self.desc_edit = QLineEdit()
        grid.addWidget(self.desc_edit, 1, 1)

        grid.addWidget(QLabel("Categoria:"), 2, 0)
        self.cat_edit = QLineEdit()
        grid.addWidget(self.cat_edit, 2, 1)

        grid.addWidget(QLabel("Valor (R$):"), 3, 0)
        self.valor_spin = QDoubleSpinBox()
        self.valor_spin.setRange(0, 99999.99)
        self.valor_spin.setPrefix("R$ ")
        grid.addWidget(self.valor_spin, 3, 1)

        layout.addLayout(grid)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
<<<<<<< HEAD
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancelar)
        
=======
>>>>>>> b5fde65adc1279d3f005b38aa1643af8c14e1ce6
        btn_salvar = QPushButton("Salvar")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.accept)
        button_layout.addWidget(btn_salvar)
        layout.addLayout(button_layout)