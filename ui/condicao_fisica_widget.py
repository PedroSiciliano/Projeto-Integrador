# perfect_acqua_system/ui/condicao_fisica_widget.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFrame, 
    QGridLayout, QListWidgetItem, QTableWidget, QTableWidgetItem, 
    QHeaderView, QPushButton, QTextEdit, QLineEdit, QDialog, QComboBox,
    QCheckBox
)
from PyQt6.QtCore import Qt, QDate

class CondicaoFisica(QWidget):
    # ... (código da classe CondicaoFisica permanece o mesmo) ...
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Condições de Saúde do Aluno")
        title.setObjectName("Title")
        subtitle = QLabel("Consulte e registre as condições de saúde, restrições e contatos de emergência")
        subtitle.setObjectName("Subtitle")
        
        header_layout = QVBoxLayout()
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.setSpacing(5)
        layout.addLayout(header_layout)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        # --- Coluna da Esquerda: Lista de Alunos ---
        left_panel = QFrame()
        left_panel.setProperty("class", "CardFrame")
        left_panel.setFixedWidth(250)
        left_layout = QVBoxLayout(left_panel)
        
        label_alunos = QLabel("Alunos")
        label_alunos.setObjectName("ListCardTitle")
        
        self.filtro_alunos = QLineEdit()
        self.filtro_alunos.setPlaceholderText("Buscar aluno...")
        self.filtro_alunos.textChanged.connect(self.filtrar_lista_alunos)
        
        self.lista_alunos = QListWidget()
        self.lista_alunos.setObjectName("DashboardList")
        self.lista_alunos.addItems([
            "Pedro Oliveira", "Julia Mendes", "Marcos Andrade", 
            "Lívia Costa", "Rafael Souza", "Ana Clara"
        ])
        
        left_layout.addWidget(label_alunos)
        left_layout.addWidget(self.filtro_alunos)
        left_layout.addWidget(self.lista_alunos)
        
        # --- Painel da Direita: Detalhes do Aluno ---
        right_panel = QFrame()
        right_panel.setProperty("class", "CardFrame")
        right_layout = QVBoxLayout(right_panel)
        
        tabela_condicoes = QTableWidget()
        tabela_condicoes.setColumnCount(4)
        tabela_condicoes.setHorizontalHeaderLabels(["Tipo", "Descrição", "Severidade", "Data de Atualização"])
        tabela_condicoes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        dados = [("Condição Médica", "Asma leve, controlada com Ventolin", "Leve", "10/02/2025")]
        tabela_condicoes.setRowCount(len(dados))
        for row, data_row in enumerate(dados):
            for col, data_cell in enumerate(data_row):
                tabela_condicoes.setItem(row, col, QTableWidgetItem(data_cell))
        
        right_layout.addWidget(tabela_condicoes)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_nova_condicao = QPushButton("➕ Registrar Nova Condição")
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
            nome_aluno = item.text().lower()
            item.setHidden(texto_filtro not in nome_aluno)

    def abrir_dialog_registro(self):
        dialog = RegistrarCondicaoDialog(self)
        dialog.exec()


class RegistrarCondicaoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Condição de Saúde")
        self.setFixedSize(500, 450)
        
        # --- ALTERAÇÃO AQUI: Define fundo escuro e texto branco para os campos ---
        self.setStyleSheet("""
            /* Define fundo escuro, texto branco e bordas para os campos */
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2b3a4a;
                color: white;
                border: 1px solid #4f6987;
                border-radius: 4px;
                padding: 4px;
            }
            /* Estilo da lista suspensa (fundo branco, texto preto) */
            QComboBox QAbstractItemView {
                color: black;
                background-color: white;
                selection-background-color: #0078d7;
                border: 1px solid lightgray;
            }
            /* Rótulos e checkboxes com texto branco */
            QLabel, QCheckBox {
                color: white;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("Nova Condição de Saúde")
        title.setObjectName("Subtitle")
        layout.addWidget(title)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(QLabel("Tipo:"), 0, 0)
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Condição Médica", "Alergia", "Lesão", "Outro"])
        grid.addWidget(self.tipo_combo, 0, 1)
        
        grid.addWidget(QLabel("Severidade:"), 1, 0)
        self.severidade_combo = QComboBox()
        self.severidade_combo.addItems(["Leve", "Moderada", "Grave"])
        grid.addWidget(self.severidade_combo, 1, 1)

        grid.addWidget(QLabel("Descrição:"), 2, 0)
        self.descricao_edit = QTextEdit()
        grid.addWidget(self.descricao_edit, 2, 1)

        grid.addWidget(QLabel("Medicamentos:"), 3, 0)
        self.medicamentos_edit = QLineEdit(placeholderText="Ex: Ventolin, se necessário")
        grid.addWidget(self.medicamentos_edit, 3, 1)
        
        grid.addWidget(QLabel("Contato de Emergência:"), 4, 0)
        self.contato_edit = QLineEdit(placeholderText="Nome do contato")
        grid.addWidget(self.contato_edit, 4, 1)
        
        grid.addWidget(QLabel("Telefone de Emergência:"), 5, 0)
        self.telefone_edit = QLineEdit(placeholderText="(00) 00000-0000")
        grid.addWidget(self.telefone_edit, 5, 1)

        self.restricao_check = QCheckBox("Possui restrição para atividades físicas?")
        grid.addWidget(self.restricao_check, 6, 0, 1, 2)
        
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
        
        layout.addLayout(button_layout)