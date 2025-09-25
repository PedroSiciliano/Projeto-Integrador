# perfect_acqua_system/database.py

import sqlite3
from datetime import datetime, timedelta

DATABASE_FILE = "perfect_acqua.db"

def conectar():
    """Cria uma conexão com o banco de dados."""
    return sqlite3.connect(DATABASE_FILE)

def criar_tabelas():
    """Cria as tabelas do banco de dados se não existirem."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        conexao.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conexao.close()

# --- Funções de Alunos ---
def adicionar_aluno(nome, data_nasc, cpf, tel, email, end, status, resp_nome, resp_cpf, resp_tel, id_plano):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO aluno (nome_completo, data_nascimento, cpf, telefone, email, endereco, status, 
                           responsavel_nome, responsavel_cpf, responsavel_telefone, id_plano)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, data_nasc, cpf, tel, email, end, status, resp_nome, resp_cpf, resp_tel, id_plano))
    
    id_aluno_novo = cursor.lastrowid
    
    cursor.execute("SELECT valor_mensal FROM plano WHERE id_plano = ?", (id_plano,))
    plano = cursor.fetchone()
    if plano:
        valor_mensalidade = plano[0]
        vencimento = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            INSERT INTO mensalidade (id_aluno, data_vencimento, valor, status)
            VALUES (?, ?, ?, 'Pendente')
        """, (id_aluno_novo, vencimento, valor_mensalidade))

    conexao.commit()
    conexao.close()

def buscar_alunos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT a.id_aluno, a.nome_completo, p.nome_plano, a.responsavel_nome, a.responsavel_telefone, a.status
        FROM aluno a LEFT JOIN plano p ON a.id_plano = p.id_plano
    """)
    return cursor.fetchall()

# --- Funções de Planos ---
def buscar_planos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_plano, nome_plano, valor_mensal FROM plano")
    return cursor.fetchall()

# --- Funções de Condição de Saúde ---
def buscar_condicao_aluno(id_aluno):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT condicao_medica, alergias, medicamentos, restricoes, contato_emergencia, telefone_emergencia FROM aluno_condicao_fisica WHERE id_aluno = ?", (id_aluno,))
    return cursor.fetchone()

def salvar_ou_atualizar_condicao(id_aluno, cond_med, alerg, med, restr, cont, tel):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_condicao FROM aluno_condicao_fisica WHERE id_aluno = ?", (id_aluno,))
    existe = cursor.fetchone()
    if existe:
        cursor.execute("""
            UPDATE aluno_condicao_fisica SET condicao_medica=?, alergias=?, medicamentos=?, restricoes=?,
            contato_emergencia=?, telefone_emergencia=? WHERE id_aluno=?
        """, (cond_med, alerg, med, restr, cont, tel, id_aluno))
    else:
        cursor.execute("""
            INSERT INTO aluno_condicao_fisica (id_aluno, condicao_medica, alergias, medicamentos, restricoes, contato_emergencia, telefone_emergencia)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_aluno, cond_med, alerg, med, restr, cont, tel))
    conexao.commit()
    conexao.close()

# --- Funções de Instrutores ---
def adicionar_instrutor(nome, data_nasc, cpf, email, telefone, especialidade):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO instrutor (nome_completo, data_nascimento, cpf, email, telefone, especialidade)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, data_nasc, cpf, email, telefone, especialidade))
    conexao.commit()
    conexao.close()

def buscar_instrutores():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_instrutor, nome_completo, especialidade, email, telefone FROM instrutor")
    return cursor.fetchall()

def buscar_instrutor_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_instrutor, nome_completo FROM instrutor WHERE nome_completo = ?", (nome,))
    return cursor.fetchone()

# --- Funções de Ponto ---
def registrar_ponto(id_instrutor, data, hora, tipo):
    conexao = conectar()
    cursor = conexao.cursor()
    if tipo == "Entrada":
        cursor.execute("SELECT id_ponto FROM registro_ponto WHERE id_instrutor = ? AND data = ? AND hora_saida IS NULL", (id_instrutor, data))
        if cursor.fetchone():
            return "Já existe um registro de entrada aberto para este instrutor hoje."
        cursor.execute("INSERT INTO registro_ponto (id_instrutor, data, hora_entrada) VALUES (?, ?, ?)",
                       (id_instrutor, data, hora))
    elif tipo == "Saída":
        cursor.execute("UPDATE registro_ponto SET hora_saida = ? WHERE id_instrutor = ? AND data = ? AND hora_saida IS NULL",
                       (hora, id_instrutor, data))
        if cursor.rowcount == 0:
            return "Nenhum registro de entrada aberto encontrado para registrar a saída."
    conexao.commit()
    conexao.close()
    return "Sucesso"

def buscar_registros_ponto():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT i.nome_completo, r.data, r.hora_entrada, r.hora_saida
        FROM registro_ponto r JOIN instrutor i ON r.id_instrutor = i.id_instrutor
        ORDER BY r.data DESC, r.hora_entrada DESC
    """)
    return cursor.fetchall()

# --- Funções de Aulas ---
def adicionar_aula(data, inicio, fim, nivel, id_instrutor):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO aula (data_aula, horario_inicio, horario_fim, nivel, id_instrutor)
        VALUES (?, ?, ?, ?, ?)
    """, (data, inicio, fim, nivel, id_instrutor))
    conexao.commit()
    conexao.close()

def buscar_aulas_com_id_por_data(data_str):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT a.id_aula, a.horario_inicio, a.horario_fim, a.nivel, i.nome_completo,
               (SELECT COUNT(*) FROM aluno_aula WHERE id_aula = a.id_aula)
        FROM aula a LEFT JOIN instrutor i ON a.id_instrutor = i.id_instrutor
        WHERE a.data_aula = ? ORDER BY a.horario_inicio
    """, (data_str,))
    return cursor.fetchall()

def buscar_alunos_da_aula(id_aula):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT a.id_aluno, a.nome_completo FROM aluno a JOIN aluno_aula aa ON a.id_aluno = aa.id_aluno WHERE aa.id_aula = ?", (id_aula,))
    return cursor.fetchall()

def buscar_alunos_fora_da_aula(id_aula):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id_aluno, nome_completo FROM aluno WHERE status = 'Ativo' AND id_aluno NOT IN
        (SELECT id_aluno FROM aluno_aula WHERE id_aula = ?)
    """, (id_aula,))
    return cursor.fetchall()

def atualizar_alunos_na_aula(id_aula, ids_alunos_para_adicionar):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM aluno_aula WHERE id_aula = ?", (id_aula,))
    if ids_alunos_para_adicionar:
        dados = [(id_aluno, id_aula) for id_aluno in ids_alunos_para_adicionar]
        cursor.executemany("INSERT INTO aluno_aula (id_aluno, id_aula) VALUES (?, ?)", dados)
    conexao.commit()
    conexao.close()

# --- Funções de Despesas ---
def adicionar_despesa(data, descricao, categoria, valor):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO despesas (data, descricao, categoria, valor) VALUES (?, ?, ?, ?)",
                   (data, descricao, categoria, valor))
    conexao.commit()
    conexao.close()

def buscar_despesas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT data, descricao, categoria, valor FROM despesas ORDER BY data DESC")
    return cursor.fetchall()

# --- Funções Financeiro ---
def buscar_mensalidades():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT m.id_mensalidade, a.nome_completo, p.nome_plano, m.valor, m.data_vencimento, m.status
        FROM mensalidade m
        JOIN aluno a ON m.id_aluno = a.id_aluno
        JOIN plano p ON a.id_plano = p.id_plano
        ORDER BY m.data_vencimento DESC
    """)
    return cursor.fetchall()

def marcar_mensalidade_paga(id_mensalidade):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE mensalidade SET status = 'Pago' WHERE id_mensalidade = ?", (id_mensalidade,))
    conexao.commit()
    conexao.close()

# --- Funções do Dashboard ---
def contar_alunos_ativos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM aluno WHERE status = 'Ativo'")
    total = cursor.fetchone()[0]
    return total

def calcular_receita_mes_atual():
    conexao = conectar()
    cursor = conexao.cursor()
    mes_atual = datetime.now().strftime('%Y-%m')
    cursor.execute("""
        SELECT SUM(valor) FROM mensalidade WHERE status = 'Pago' AND strftime('%Y-%m', data_vencimento) = ?
    """, (mes_atual,))
    total = cursor.fetchone()[0]
    return total or 0.0

def calcular_despesas_mes_atual():
    conexao = conectar()
    cursor = conexao.cursor()
    mes_atual = datetime.now().strftime('%Y-%m')
    cursor.execute("SELECT SUM(valor) FROM despesas WHERE strftime('%Y-%m', data) = ?", (mes_atual,))
    total = cursor.fetchone()[0]
    return total or 0.0

def buscar_proximas_aulas():
    conexao = conectar()
    cursor = conexao.cursor()
    hoje = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT strftime('%d/%m', a.data_aula) || ' - ' || a.horario_inicio, a.nivel, i.nome_completo
        FROM aula a
        LEFT JOIN instrutor i ON a.id_instrutor = i.id_instrutor
        WHERE a.data_aula >= ?
        ORDER BY a.data_aula, a.horario_inicio
        LIMIT 5
    """, (hoje,))
    return cursor.fetchall()