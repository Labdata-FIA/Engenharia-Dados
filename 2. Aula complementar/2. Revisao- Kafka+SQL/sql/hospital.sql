-- Banco do pronto-socorro (dados fictícios)
CREATE SCHEMA IF NOT EXISTS prontosocorro;

-- Cadastro de pacientes
CREATE TABLE prontosocorro.pacientes (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    cpf             VARCHAR(14)  NOT NULL,
    data_nascimento DATE         NOT NULL,
    convenio        VARCHAR(50)  NOT NULL
);

-- Cadastro de médicos
CREATE TABLE prontosocorro.medicos (
    id            SERIAL PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    crm           VARCHAR(20)  NOT NULL,
    especialidade VARCHAR(50)  NOT NULL
);

-- Atendimentos do pronto-socorro (classificação de risco: Protocolo de Manchester)
CREATE TABLE prontosocorro.atendimentos (
    id                  SERIAL PRIMARY KEY,
    paciente_id         INT          NOT NULL REFERENCES prontosocorro.pacientes(id),
    medico_id           INT          NOT NULL REFERENCES prontosocorro.medicos(id),
    classificacao_risco VARCHAR(10)  NOT NULL
        CHECK (classificacao_risco IN ('VERMELHO','LARANJA','AMARELO','VERDE','AZUL')),
    queixa              VARCHAR(200),
    status              VARCHAR(20)  NOT NULL DEFAULT 'AGUARDANDO'
        CHECK (status IN ('AGUARDANDO','EM_ATENDIMENTO','ALTA')),
    aberto_em           TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Grava a linha "antiga" completa no WAL: o campo "before" do Debezium vem preenchido no UPDATE
ALTER TABLE prontosocorro.pacientes    REPLICA IDENTITY FULL;
ALTER TABLE prontosocorro.medicos      REPLICA IDENTITY FULL;
ALTER TABLE prontosocorro.atendimentos REPLICA IDENTITY FULL;

-- Dados iniciais
INSERT INTO prontosocorro.pacientes (nome, cpf, data_nascimento, convenio) VALUES
  ('Maria Silva',    '111.111.111-11', '1958-03-12', 'SUS'),
  ('Joao Santos',    '222.222.222-22', '1990-07-25', 'Unimed'),
  ('Ana Oliveira',   '333.333.333-33', '1975-11-02', 'Bradesco Saude'),
  ('Carlos Souza',   '444.444.444-44', '1983-01-30', 'SulAmerica'),
  ('Beatriz Lima',   '555.555.555-55', '2018-05-18', 'SUS');

INSERT INTO prontosocorro.medicos (nome, crm, especialidade) VALUES
  ('Dra. Fernanda Costa', 'CRM-SP 100001', 'Clinica Geral'),
  ('Dr. Ricardo Alves',   'CRM-SP 100002', 'Cardiologia'),
  ('Dra. Juliana Rocha',  'CRM-SP 100003', 'Pediatria'),
  ('Dr. Paulo Mendes',    'CRM-SP 100004', 'Ortopedia');

INSERT INTO prontosocorro.atendimentos (paciente_id, medico_id, classificacao_risco, queixa, status) VALUES
  (1, 2, 'LARANJA',  'Dor no peito',             'EM_ATENDIMENTO'),
  (2, 4, 'VERDE',    'Torcao no tornozelo',      'AGUARDANDO'),
  (3, 1, 'AMARELO',  'Febre e tosse ha 3 dias',  'AGUARDANDO');
