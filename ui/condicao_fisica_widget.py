# perfect_acqua_system/ui/condicao_fisica_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFrame, 
    QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, 
    QPushButton, QTextEdit, QDialog, QLineEdit
)

class CondicaoFisica(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Condições de Saúde do Aluno")
        title.setObjectName("Title")
        subtitle = QLabel("Consulte e registre as condições de saúde, restrições e contatos de emergência")
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addLayout(header_layout)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        left_panel = QFrame()
        left_panel.setProperty("class", "CardFrame")
        left_panel.setFixedWidth(280)
        left_layout = QVBoxLayout(left_panel)
        
        filtro_label = QLabel("Buscar Aluno:")
        self.filtro_alunos = QLineEdit()
        self.filtro_alunos.setPlaceholderText("Digite o nome do aluno...")
        self.filtro_alunos.setStyleSheet("""
            QLineEdit {
                background-color: #2b3a4a; color: #e2e8f0;
                border: 1px solid #4f6987; border-radius: 5px; padding: 5px;
            }
            QLineEdit:focus { border: 1px solid #7dd3fc; }
        """)
        self.filtro_alunos.textChanged.connect(self.filtrar_lista_alunos)
        
        left_layout.addWidget(filtro_label)
        left_layout.addWidget(self.filtro_alunos)
        
        self.lista_alunos = QListWidget()
        self.lista_alunos.addItems(["Pedro Oliveira", "Julia Mendes", "Marcos Andrade", "Beatriz Costa"])
        self.lista_alunos.setStyleSheet("""
            QListWidget {
                background-color: #2b3a4a; color: #e2e8f0;
                border: 1px solid #4f6987; border-radius: 5px; padding: 5px;
            }
            QListWidget::item:hover { background-color: #3e526a; }
            QListWidget::item:selected { background-color: #38bdf8; color: #ffffff; }
        """)
        left_layout.addWidget(self.lista_alunos)
        
        right_panel = QFrame()
        right_panel.setProperty("class", "CardFrame")
        right_layout = QVBoxLayout(right_panel)
        
        tabela_condicoes = QTableWidget()
        
        # --- CORREÇÃO DEFINITIVA AQUI ---
        # Removidos todos os estilos anteriores e substituídos por este bloco único e completo
        tabela_condicoes.setStyleSheet("""
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
        
        tabela_condicoes.setColumnCount(4)
        tabela_condicoes.setHorizontalHeaderLabels(["Condição Médica", "Alergias", "Restrições", "Contato de Emergência"])
        tabela_condicoes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabela_condicoes.setAlternatingRowColors(True) # Ativa a cor de fundo alternada
        
        dados = [("Asma leve", "Poeira", "Evitar esforço excessivo", "Maria (mãe) - 9999-8888")]
        tabela_condicoes.setRowCount(len(dados))
        for row, data_row in enumerate(dados):
            for col, data_cell in enumerate(data_row):
                tabela_condicoes.setItem(row, col, QTableWidgetItem(data_cell))
        
        right_layout.addWidget(tabela_condicoes)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_nova_condicao = QPushButton("➕ Registrar/Atualizar Ficha")
        btn_nova_condicao.setProperty("class", "primary")
        btn_nova_condicao.clicked.connect(self.abrir_dialog_registro)
        btn_layout.addWidget(btn_nova_condicao)
        right_layout.addLayout(btn_layout)
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        layout.addLayout(main_layout)

    def filtrar_lista_alunos(self):
        texto_filtro = self.filtro_alunos.text().lower()
        for i in range(self.lista_alunos.count()):
            item = self.lista_alunos.item(i)
            item.setHidden(texto_filtro not in item.text().lower())

    def abrir_dialog_registro(self):
        dialog = RegistrarCondicaoDialog(self)
        dialog.exec()

# O código do pop-up (RegistrarCondicaoDialog) não foi alterado.
class RegistrarCondicaoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ficha de Saúde do Aluno")
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: #1e2b3a;")
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel("Atualizar Ficha de Saúde")
        title.setObjectName("Subtitle")
        layout.addWidget(title)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(QLabel("Condições Médicas:"), 0, 0)
        self.condicao_edit = QTextEdit(placeholderText="Ex: Asma, Hipertensão, Diabetes...")
        grid.addWidget(self.condicao_edit, 1, 0)
        grid.addWidget(QLabel("Alergias Conhecidas:"), 0, 1)
        self.alergias_edit = QTextEdit(placeholderText="Ex: Poeira, Cloro, Dipirona...")
        grid.addWidget(self.alergias_edit, 1, 1)
        grid.addWidget(QLabel("Medicamentos em Uso:"), 2, 0)
        self.medicamentos_edit = QTextEdit(placeholderText="Ex: Ventolin, se necessário...")
        grid.addWidget(self.medicamentos_edit, 3, 0)
        grid.addWidget(QLabel("Restrições de Atividade:"), 2, 1)
        self.restricoes_edit = QTextEdit(placeholderText="Ex: Evitar mergulhos, sem atividades de impacto...")
        grid.addWidget(self.restricoes_edit, 3, 1)
        grid.addWidget(QLabel("Contato de Emergência:"), 4, 0)
        self.contato_edit = QLineEdit(placeholderText="Nome do contato")
        grid.addWidget(self.contato_edit, 5, 0)
        grid.addWidget(QLabel("Telefone de Emergência:"), 4, 1)
        self.telefone_edit = QLineEdit(placeholderText="(00) 00000-0000")
        grid.addWidget(self.telefone_edit, 5, 1)
        layout.addLayout(grid)
        layout.addStretch()
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setProperty("class", "secondary")
        btn_cancelar.clicked.connect(self.reject)
        button_layout.addWidget(btn_cancelar)
        btn_salvar = QPushButton("Salvar Ficha")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.accept)
        button_layout.addWidget(btn_salvar)
        layout.addLayout(button_layout)