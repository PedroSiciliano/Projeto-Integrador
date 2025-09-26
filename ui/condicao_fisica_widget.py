# perfect_acqua_system/ui/condicao_fisica_widget.py
import database
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QFrame, QGridLayout, QPushButton, QTextEdit, QLineEdit, QMessageBox, QListWidgetItem
from PyQt6.QtCore import Qt

class CondicaoFisica(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Condições de Saúde do Aluno")
        title.setObjectName("Title")
        layout.addWidget(title)
        
        main_layout = QHBoxLayout()
        
        left_panel = QFrame()
        left_panel.setProperty("class", "CardFrame")
        left_layout = QVBoxLayout(left_panel)
        
        # CORREÇÃO: Adicionado filtro de busca
        self.filtro_aluno = QLineEdit(placeholderText="Buscar aluno...")
        self.filtro_aluno.textChanged.connect(self.filtrar_lista_alunos)
        left_layout.addWidget(self.filtro_aluno)

        self.lista_alunos = QListWidget()
        self.lista_alunos.currentItemChanged.connect(self.carregar_ficha_aluno)
        left_layout.addWidget(self.lista_alunos)
        
        right_panel = QFrame()
        right_panel.setProperty("class", "CardFrame")
        right_layout = QVBoxLayout(right_panel)
        self.aluno_selecionado_label = QLabel("Nenhum aluno selecionado")
        self.aluno_selecionado_label.setObjectName("Subtitle")
        right_layout.addWidget(self.aluno_selecionado_label)
        
        grid = QGridLayout()
        self.condicao_edit = QTextEdit(placeholderText="Ex: Asma, Hipertensão...")
        self.alergias_edit = QTextEdit(placeholderText="Ex: Poeira, Cloro...")
        self.medicamentos_edit = QTextEdit(placeholderText="Ex: Ventolin, se necessário...")
        self.restricoes_edit = QTextEdit(placeholderText="Ex: Evitar mergulhos...")
        self.contato_edit = QLineEdit(placeholderText="Nome do contato")
        self.telefone_edit = QLineEdit(placeholderText="(00) 00000-0000")
        
        grid.addWidget(QLabel("Condições Médicas:"), 0, 0)
        grid.addWidget(self.condicao_edit, 1, 0)
        grid.addWidget(QLabel("Alergias:"), 0, 1)
        grid.addWidget(self.alergias_edit, 1, 1)
        grid.addWidget(QLabel("Medicamentos em Uso:"), 2, 0)
        grid.addWidget(self.medicamentos_edit, 3, 0)
        grid.addWidget(QLabel("Restrições de Atividade:"), 2, 1)
        grid.addWidget(self.restricoes_edit, 3, 1)
        grid.addWidget(QLabel("Contato de Emergência:"), 4, 0)
        grid.addWidget(self.contato_edit, 5, 0)
        grid.addWidget(QLabel("Telefone de Emergência:"), 4, 1)
        grid.addWidget(self.telefone_edit, 5, 1)
        right_layout.addLayout(grid)
        
        btn_salvar = QPushButton("Salvar Ficha")
        btn_salvar.setProperty("class", "success")
        btn_salvar.clicked.connect(self.salvar_ficha)
        right_layout.addWidget(btn_salvar, 0, Qt.AlignmentFlag.AlignRight)
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 3)
        layout.addLayout(main_layout)
        
        self.popular_lista_alunos()

    def filtrar_lista_alunos(self):
        texto_filtro = self.filtro_aluno.text().lower()
        for i in range(self.lista_alunos.count()):
            item = self.lista_alunos.item(i)
            item.setHidden(texto_filtro not in item.text().lower())

    def popular_lista_alunos(self):
        # (código da função igual à versão anterior)
        current_selection = self.lista_alunos.currentItem()
        current_id = current_selection.data(Qt.ItemDataRole.UserRole) if current_selection else None
        
        self.lista_alunos.clear()
        alunos = database.buscar_alunos()
        for id_aluno, nome, _, _, _, _ in alunos:
            item = QListWidgetItem(nome)
            item.setData(Qt.ItemDataRole.UserRole, id_aluno)
            self.lista_alunos.addItem(item)
            if id_aluno == current_id:
                self.lista_alunos.setCurrentItem(item)

    def carregar_ficha_aluno(self, current_item, previous_item):
        # (código da função igual à versão anterior)
        if not current_item:
            self.limpar_campos()
            return
            
        id_aluno = current_item.data(Qt.ItemDataRole.UserRole)
        self.aluno_selecionado_label.setText(f"Editando ficha de: {current_item.text()}")
        
        dados_ficha = database.buscar_condicao_aluno(id_aluno)
        if dados_ficha:
            self.condicao_edit.setText(dados_ficha[0] or "")
            self.alergias_edit.setText(dados_ficha[1] or "")
            self.medicamentos_edit.setText(dados_ficha[2] or "")
            self.restricoes_edit.setText(dados_ficha[3] or "")
            self.contato_edit.setText(dados_ficha[4] or "")
            self.telefone_edit.setText(dados_ficha[5] or "")
        else:
            self.limpar_campos()

    def salvar_ficha(self):
        # (código da função igual à versão anterior)
        current_item = self.lista_alunos.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Atenção", "Selecione um aluno para salvar a ficha.")
            return
            
        id_aluno = current_item.data(Qt.ItemDataRole.UserRole)
        try:
            database.salvar_ou_atualizar_condicao(
                id_aluno,
                self.condicao_edit.toPlainText(), self.alergias_edit.toPlainText(),
                self.medicamentos_edit.toPlainText(), self.restricoes_edit.toPlainText(),
                self.contato_edit.text(), self.telefone_edit.text()
            )
            QMessageBox.information(self, "Sucesso", "Ficha de saúde salva com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível salvar a ficha.\nErro: {e}")

    def limpar_campos(self):
        # (código da função igual à versão anterior)
        self.aluno_selecionado_label.setText("Nenhum aluno selecionado")
        self.condicao_edit.clear()
        self.alergias_edit.clear()
        self.medicamentos_edit.clear()
        self.restricoes_edit.clear()
        self.contato_edit.clear()
        self.telefone_edit.clear()
