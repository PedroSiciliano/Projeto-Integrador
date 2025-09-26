-- Arquivo: schema.sql (Versão Definitiva)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS plano (
    id_plano INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_plano TEXT NOT NULL UNIQUE,
    valor_mensal REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS aluno (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    data_nascimento TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    telefone TEXT,
    email TEXT,
    endereco TEXT,
    status TEXT NOT NULL,
    responsavel_nome TEXT,
    responsavel_cpf TEXT,
    responsavel_telefone TEXT,
    id_plano INTEGER,
    FOREIGN KEY (id_plano) REFERENCES plano (id_plano)
);

CREATE TABLE IF NOT EXISTS aluno_condicao_fisica (
    id_condicao INTEGER PRIMARY KEY AUTOINCREMENT,
    condicao_medica TEXT,
    alergias TEXT,
    medicamentos TEXT,
    restricoes TEXT,
    contato_emergencia TEXT,
    telefone_emergencia TEXT,
    id_aluno INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (id_aluno) REFERENCES aluno (id_aluno)
);

CREATE TABLE IF NOT EXISTS instrutor (
    id_instrutor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    data_nascimento TEXT,
    cpf TEXT UNIQUE NOT NULL,
    email TEXT,
    telefone TEXT,
    especialidade TEXT
);

CREATE TABLE IF NOT EXISTS registro_ponto (
    id_ponto INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    hora_entrada TEXT,
    hora_saida TEXT,
    id_instrutor INTEGER NOT NULL,
    FOREIGN KEY (id_instrutor) REFERENCES instrutor (id_instrutor)
);

CREATE TABLE IF NOT EXISTS aula (
    id_aula INTEGER PRIMARY KEY AUTOINCREMENT,
    data_aula TEXT NOT NULL,
    horario_inicio TEXT NOT NULL,
    horario_fim TEXT NOT NULL,
    nivel TEXT NOT NULL,
    id_instrutor INTEGER,
    FOREIGN KEY (id_instrutor) REFERENCES instrutor (id_instrutor)
);

CREATE TABLE IF NOT EXISTS aluno_aula (
    id_aluno INTEGER,
    id_aula INTEGER,
    PRIMARY KEY (id_aluno, id_aula),
    FOREIGN KEY (id_aluno) REFERENCES aluno (id_aluno),
    FOREIGN KEY (id_aula) REFERENCES aula (id_aula)
);

CREATE TABLE IF NOT EXISTS mensalidade (
    id_mensalidade INTEGER PRIMARY KEY AUTOINCREMENT,
    data_vencimento TEXT NOT NULL,
    valor REAL NOT NULL,
    status TEXT NOT NULL,
    id_aluno INTEGER NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES aluno (id_aluno)
);

CREATE TABLE IF NOT EXISTS despesas (
    id_despesa INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    descricao TEXT NOT NULL,
    categoria TEXT,
    valor REAL NOT NULL
);

INSERT OR IGNORE INTO plano (id_plano, nome_plano, valor_mensal) VALUES
(1, 'Mensal', 160.00),
(2, 'Trimestral', 450.00),
(3, 'Anual', 1600.00);