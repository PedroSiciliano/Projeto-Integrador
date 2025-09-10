-- === Academia de Natação — Esquema completo ===
CREATE DATABASE IF NOT EXISTS academia_natacao
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE academia_natacao;

SET NAMES utf8mb4;
SET time_zone = '+00:00';

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS registro_ponto, aluno_aula, mensalidade, aula, instrutor, aluno_condicao_fisica, plano, aluno, login;
SET FOREIGN_KEY_CHECKS = 1;

-- LOGIN
CREATE TABLE login (
  id_login  INT AUTO_INCREMENT PRIMARY KEY,
  username  VARCHAR(50)  NOT NULL UNIQUE,
  senha     VARCHAR(255) NOT NULL,
  tipo      ENUM('aluno','instrutor','admin') NOT NULL,
  criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_login_tipo (tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ALUNO
CREATE TABLE aluno (
  id_aluno INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  cpf  CHAR(11) NOT NULL,
  data_nascimento DATE NOT NULL,
  telefone VARCHAR(15),
  email VARCHAR(100),
  endereco VARCHAR(255),
  status ENUM('ativo','inativo') NOT NULL DEFAULT 'ativo',
  CONSTRAINT uq_aluno_cpf UNIQUE (cpf),
  CONSTRAINT uq_aluno_email UNIQUE (email),
  CONSTRAINT ck_aluno_cpf_digits CHECK (cpf REGEXP '^[0-9]{11}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- INSTRUTOR
CREATE TABLE instrutor (
  id_instrutor INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  cpf  CHAR(11) NOT NULL,
  telefone VARCHAR(15),
  email VARCHAR(100),
  especialidade VARCHAR(50),
  status ENUM('ativo','inativo') NOT NULL DEFAULT 'ativo',
  CONSTRAINT uq_instrutor_cpf UNIQUE (cpf),
  CONSTRAINT uq_instrutor_email UNIQUE (email),
  CONSTRAINT ck_instrutor_cpf_digits CHECK (cpf REGEXP '^[0-9]{11}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- AULA
CREATE TABLE aula (
  id_aula INT AUTO_INCREMENT PRIMARY KEY,
  id_instrutor INT NOT NULL,
  data_aula DATE NOT NULL,
  hora_inicio TIME NOT NULL,
  hora_fim    TIME NOT NULL,
  nivel ENUM('iniciante','intermediario','avancado') NOT NULL,
  vagas INT NOT NULL,
  CONSTRAINT fk_aula_instrutor
    FOREIGN KEY (id_instrutor) REFERENCES instrutor(id_instrutor)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT uq_aula_slot UNIQUE (id_instrutor, data_aula, hora_inicio, hora_fim),
  CONSTRAINT ck_aula_horas CHECK (hora_fim > hora_inicio),
  CONSTRAINT ck_aula_vagas CHECK (vagas > 0),
  INDEX idx_aula_instrutor_data (id_instrutor, data_aula)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- MATRÍCULA 
CREATE TABLE aluno_aula (
  id_aluno INT NOT NULL,
  id_aula  INT NOT NULL,
  presenca TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id_aluno, id_aula),
  CONSTRAINT fk_aa_aluno FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_aa_aula  FOREIGN KEY (id_aula)  REFERENCES aula(id_aula)
    ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_aa_aula (id_aula)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- MENSALIDADE
CREATE TABLE mensalidade (
  id_mensalidade INT AUTO_INCREMENT PRIMARY KEY,
  id_aluno INT NOT NULL,
  valor DECIMAL(10,2) NOT NULL,
  data_vencimento DATE NOT NULL,
  status_pagamento ENUM('pago','pendente','atrasado') NOT NULL DEFAULT 'pendente',
  data_pagamento DATE NULL,
  CONSTRAINT fk_mensalidade_aluno
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT uq_mensalidade_unica UNIQUE (id_aluno, data_vencimento),
  INDEX idx_mensalidade_status (status_pagamento),
  INDEX idx_mensalidade_aluno (id_aluno, data_vencimento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- REGISTRO DE PONTO 
CREATE TABLE registro_ponto (
  id_folha INT AUTO_INCREMENT PRIMARY KEY,
  id_instrutor INT NOT NULL,
  data_ponto DATE NOT NULL,
  hora_entrada TIME NOT NULL,
  hora_saida   TIME NOT NULL,
  CONSTRAINT fk_fp_instrutor
    FOREIGN KEY (id_instrutor) REFERENCES instrutor(id_instrutor)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT ck_fp_horas CHECK (hora_saida > hora_entrada),
  CONSTRAINT uq_fp_dia UNIQUE (id_instrutor, data_ponto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- PLANO 
CREATE TABLE plano (
  id_plano INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(50) NOT NULL,
  descricao VARCHAR(255),
  valor DECIMAL(10,2) NOT NULL,
  duracao_meses INT NOT NULL DEFAULT 1,
  aulas_semanais TINYINT NOT NULL DEFAULT 1,
  status ENUM('ativo','inativo') NOT NULL DEFAULT 'ativo',
  CONSTRAINT uq_plano_nome UNIQUE (nome),
  CONSTRAINT ck_plano_valor CHECK (valor >= 0),
  CONSTRAINT ck_plano_duracao CHECK (duracao_meses > 0),
  CONSTRAINT ck_plano_aulas CHECK (aulas_semanais BETWEEN 1 AND 7)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE aluno
  ADD COLUMN id_plano INT NULL,
  ADD CONSTRAINT fk_aluno_plano
    FOREIGN KEY (id_plano) REFERENCES plano(id_plano)
    ON UPDATE CASCADE ON DELETE SET NULL;

-- CONDIÇÕES FÍSICAS DO ALUNO
CREATE TABLE aluno_condicao_fisica (
  id_condicao INT AUTO_INCREMENT PRIMARY KEY,
  id_aluno INT NOT NULL,
  tipo ENUM('alergia','cardiaco','respiratorio','ortopedico','neurologico','outros') NOT NULL DEFAULT 'outros',
  descricao VARCHAR(255) NOT NULL,
  severidade ENUM('leve','moderada','grave') DEFAULT 'leve',
  medicamentos VARCHAR(255),
  contato_emergencia VARCHAR(100),
  telefone_emergencia VARCHAR(20),
  restricao_atividade TINYINT(1) NOT NULL DEFAULT 0,
  data_atualizacao DATE NOT NULL DEFAULT (CURRENT_DATE),
  CONSTRAINT fk_acf_aluno FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno)
    ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_acf_aluno (id_aluno),
  INDEX idx_acf_tipo (tipo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- VIEWS úteis
CREATE OR REPLACE VIEW vw_agenda_instrutor AS
SELECT a.id_aula, i.nome AS instrutor, a.data_aula, a.hora_inicio, a.hora_fim, a.nivel, a.vagas,
       (SELECT COUNT(*) FROM aluno_aula aa WHERE aa.id_aula = a.id_aula) AS inscritos
FROM aula a JOIN instrutor i ON i.id_instrutor = a.id_instrutor;

CREATE OR REPLACE VIEW vw_aluno_plano AS
SELECT a.id_aluno, a.nome, p.nome AS plano, p.valor, p.duracao_meses, p.aulas_semanais
FROM aluno a LEFT JOIN plano p ON p.id_plano = a.id_plano;

CREATE OR REPLACE VIEW vw_condicoes_aluno AS
SELECT a.nome AS aluno, c.tipo, c.descricao, c.severidade, c.restricao_atividade, c.data_atualizacao
FROM aluno a JOIN aluno_condicao_fisica c ON c.id_aluno = a.id_aluno;
