-- Active: 1661208283003@@127.0.0.1@3306@analise_risco
--  Arquivo SQL com os scripts utilizados para tratar os dados no banco.

--  Tradução de colunas e normalização dos dados da tabela ID identificada como tabela de FATOS.
--  Foi identificado que o tipo de dado que estava como TEXTO deveria ir para VARCHAR(16).
--  Permitindo assim a Chave Estrangeira com outras tabelas.

ALTER TABLE ids 
    CHANGE COLUMN person_id pessoa_id VARCHAR(16) NOT NULL 
    ,CHANGE COLUMN loan_id emprestimo_id VARCHAR(16) NOT NULL
    ,CHANGE COLUMN cb_id hst_id VARCHAR(16) NOT NULL
;

--  Tradução de colunas e normalização dos dados da tabela DADOS_MUTUARIOS identificada como tabela de CADASTRO.
--  Alterados alguns tipos de dados numericos para melhor desempenho de banco.

ALTER TABLE dados_mutuarios
    CHANGE COLUMN person_id pessoa_id VARCHAR(16) NULL
    ,CHANGE COLUMN person_age pessoa_idade INT NULL
    ,CHANGE COLUMN person_income salario_ano INT NULL
    ,CHANGE COLUMN person_home_ownership propriedade_sit VARCHAR(12)
    ,CHANGE COLUMN person_emp_length ano_trabalhado NUMERIC(4,1)
;

--  Tradução de conteudo da tabela.
UPDATE analise_risco.dados_mutuarios
SET propriedade_sit  =
    CASE
        WHEN propriedade_sit = 'Rent' THEN 'Alugada'
        WHEN propriedade_sit = 'Own' THEN 'Própria'
        WHEN propriedade_sit = 'Mortgage' THEN 'Hipotecada'
        WHEN propriedade_sit = 'Other' THEN 'Outros'
        WHEN propriedade_sit = '' THEN '-'
        END
;

--  Tradução de colunas e normalização dos dados da tabela EMPRESTIMOS identificada como tabela de CADASTRO.
--  Alterados alguns tipos de dados numericos/boleanos para melhor desempenho de banco.

ALTER TABLE emprestimos
    CHANGE COLUMN loan_id emprestimo_id VARCHAR(16) NULL
    ,CHANGE COLUMN loan_intent motivo_emprestimo VARCHAR(32)
    ,CHANGE COLUMN loan_grade pontuacao_emprestimos VARCHAR(1)
    ,CHANGE COLUMN loan_amnt vl_total NUMERIC(10,2) NULL
    ,CHANGE COLUMN loan_int_rate tx_juros NUMERIC(10,2) NULL
    ,CHANGE COLUMN loan_status inadimplencia BIT NULL
    ,CHANGE COLUMN loan_percent_income tx_renda_divida NUMERIC(3,2)
;

--  Tradução de conteudo da tabela.
UPDATE analise_risco.emprestimos
SET motivo_emprestimo = 
    CASE
        WHEN motivo_emprestimo = 'Homeimprovement' THEN 'Melhora do lar'
        WHEN motivo_emprestimo = 'Venture'    THEN 'Empreendimento'
        WHEN motivo_emprestimo = 'Personal'THEN 'Pessoal'
        WHEN motivo_emprestimo = 'Medical'THEN 'Médico'
        WHEN motivo_emprestimo = 'Education'THEN'Educativo'
        WHEN motivo_emprestimo = 'Debtconsolidation'THEN 'Pagamento de débitos'
        WHEN motivo_emprestimo =  ''THEN '-'
    END
;

--  Tradução de colunas e normalização dos dados da tabela EMPRESTIMOS identificada como tabela de CADASTRO.
--  Nesta tabela é necessário traduzir os dados anterior a tradução da tabela por conta do texto sendo transformado para boleano.
UPDATE analise_risco.historicos_banco
    SET cb_person_default_on_file = 
        CASE 
        WHEN cb_person_default_on_file = 'Y' THEN '1'
        WHEN cb_person_default_on_file = 'N' THEN '0'
    END
;
ALTER TABLE historicos_banco
    CHANGE COLUMN cb_id hst_id VARCHAR(16)
    ,CHANGE COLUMN cb_person_default_on_file hst_inadimplencia BIT NULL
    ,CHANGE COLUMN cb_person_cred_hist_length hst_primeiro_credito INT NULL
;


--  TRATAMENTO NECESSARIO PARA AS CHAVES SEREM CRIADAS.
--  Encontrar Chave Primaria Duplicada com intuito de analisar o melhor tipo de tratamento. 
SELECT pessoa_id, pessoa_idade, salario_ano, propriedade_sit, ano_trabalhado, COUNT(*)  
FROM dados_mutuarios GROUP BY pessoa_id HAVING COUNT(pessoa_id) > 1;
--  Remover as linhas duplicadas ja que não eram relevantes pois o id estava vazio.
DELETE FROM dados_mutuarios WHERE pessoa_id = "";


SELECT pessoa_id, emprestimo_id, hst_id, COUNT(*)  
FROM ids GROUP BY pessoa_id HAVING COUNT(pessoa_id) > 1;

DELETE FROM ids WHERE pessoa_id = "";

--  CHAVES PRIMARIAS
--  Chave Primaria da tabela Pessoas.
ALTER TABLE dados_mutuarios ADD CONSTRAINT PK_Pessoa PRIMARY KEY (pessoa_id);
--  Chave Primaria da tabela Emprestimos.
ALTER Table emprestimos ADD CONSTRAINT PK_Emprestimos PRIMARY KEY (emprestimo_id);
--  Chave Primaria da tabela de historicos.
ALTER TABLE historicos_banco ADD CONSTRAINT PK_historicos PRIMARY KEY (hst_id);



--Não Funcionando - Veririicar porque do dados estar incomativel.
--  CHAVE ESTRANGEIRAS 
--  Chave Estrangeira entre Fato e Cadastro.
ALTER TABLE ids ADD FOREIGN KEY (pessoa_id) REFERENCES dados_mutuarios(pessoa_id);
--  Chave Estrangeira entre Fato e Cadastro.
ALTER TABLE ID ADD FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(emprestimo_id);
--  Chave Estrangeira entre Fato e Historico.
ALTER TABLE ID ADD FOREIGN KEY (hst_id) REFERENCES historicos_banco(hst_id);

CREATE TABLE dados_modelo_ml AS SELECT 

dm.pessoa_id,
dm.pessoa_idade,
dm.salario_ano,
dm.propriedade_sit,
dm.ano_trabalhado,
e.motivo_emprestimo,
e.pontuacao_emprestimos,
e.vl_total,
e.tx_juros,
e.inadimplencia,
e.tx_renda_divida,
hb.hst_inadimplencia,
hb.hst_primeiro_credito

FROM ids i

JOIN dados_mutuarios dm ON dm.pessoa_id = i.pessoa_id 

JOIN emprestimos e ON e.emprestimo_id = i.emprestimo_id 

JOIN historicos_banco hb on hb.hst_id = i.hst_id