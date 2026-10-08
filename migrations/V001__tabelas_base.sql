-- Qorvus - V001: Criação das tabelas base
-- Baseado no Dicionário de Dados (MySQL 8.0)


CREATE DATABASE IF NOT EXISTS qorvus
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE qorvus;
-- Tabela: empresa

CREATE TABLE empresa (
id           INT          NOT NULL AUTO_INCREMENT,
nome_empresa VARCHAR(150) NOT NULL,
cnpj         VARCHAR(18)  NOT NULL UNIQUE,
PRIMARY KEY (id)
) ENGINE=InnoDB;

-- Tabela: categoria

CREATE TABLE categoria (
id           INT         NOT NULL AUTO_INCREMENT,
empresa_id   INT         NOT NULL,
nome         VARCHAR(50) NOT NULL,
descricao    VARCHAR(255),
status_ativo BOOLEAN     NOT NULL DEFAULT TRUE,
PRIMARY KEY (id),
UNIQUE KEY uq_categoria_empresa_nome (empresa_id, nome),
UNIQUE KEY uq_categoria_id_empresa (id, empresa_id),
KEY ix_categoria_empresa_id (empresa_id),
CONSTRAINT fk_categoria_empresa
FOREIGN KEY (empresa_id) REFERENCES empresa (id)
) ENGINE=InnoDB;

-- Tabela: marca

CREATE TABLE marca (
id           INT         NOT NULL AUTO_INCREMENT,
empresa_id   INT         NOT NULL,
nome         VARCHAR(50) NOT NULL,
descricao    VARCHAR(255),
status_ativo BOOLEAN     NOT NULL DEFAULT TRUE,
PRIMARY KEY (id),
UNIQUE KEY uq_marca_empresa_nome (empresa_id, nome),
UNIQUE KEY uq_marca_id_empresa (id, empresa_id),
KEY ix_marca_empresa_id (empresa_id),
CONSTRAINT fk_marca_empresa
FOREIGN KEY (empresa_id) REFERENCES empresa (id)
) ENGINE=InnoDB;

-- Tabela: usuario

CREATE TABLE usuario (
id            INT                                 NOT NULL AUTO_INCREMENT,
nome_completo VARCHAR(100)                        NOT NULL,
cpf           VARCHAR(14)                         NOT NULL UNIQUE,
cargo         ENUM('ADMINISTRADOR','FUNCIONARIO') NOT NULL,
data_admissao DATE                                NOT NULL,
empresa_id    INT                                 NOT NULL,
email         VARCHAR(70)                         NOT NULL UNIQUE,
telefone      VARCHAR(20)                         NOT NULL,
senha_hash    VARCHAR(255)                        NOT NULL,
perfil        ENUM('ADMINISTRADOR','FUNCIONARIO') NOT NULL,
status_ativo  BOOLEAN                             NOT NULL DEFAULT TRUE,
PRIMARY KEY (id),
UNIQUE KEY uq_usuario_id_empresa (id, empresa_id),
CONSTRAINT fk_usuario_empresa
FOREIGN KEY (empresa_id) REFERENCES empresa (id)
) ENGINE=InnoDB;

-- Tabela: item

CREATE TABLE item (
id              INT           NOT NULL AUTO_INCREMENT,
empresa_id      INT           NOT NULL,
nome            VARCHAR(100)  NOT NULL,
quantidade      INT           NOT NULL DEFAULT 0,
categoria_id    INT           NOT NULL,
marca_id        INT,
preco_venda     DECIMAL(10,2) NOT NULL,
preco_custo     DECIMAL(10,2) NOT NULL,
limite_minimo   INT           NOT NULL DEFAULT 0,
status_removido BOOLEAN       NOT NULL DEFAULT FALSE,
descricao       VARCHAR(255),
imagem_item     VARCHAR(255),
PRIMARY KEY (id),
UNIQUE KEY uq_item_id_empresa (id, empresa_id),
KEY ix_item_empresa_id (empresa_id),
CONSTRAINT fk_item_empresa
FOREIGN KEY (empresa_id) REFERENCES empresa (id),
CONSTRAINT fk_item_categoria_empresa
FOREIGN KEY (categoria_id, empresa_id) REFERENCES categoria (id, empresa_id),
CONSTRAINT fk_item_marca_empresa
FOREIGN KEY (marca_id, empresa_id) REFERENCES marca (id, empresa_id)
) ENGINE=InnoDB;

-- Tabela: movimentacao

CREATE TABLE movimentacao (
id         INT                     NOT NULL AUTO_INCREMENT,
empresa_id INT                     NOT NULL,
item_id    INT                     NOT NULL,
usuario_id INT                     NOT NULL,
tipo       ENUM('ENTRADA','SAIDA') NOT NULL,
quantidade INT                     NOT NULL,
data_hora  TIMESTAMP               NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (id),
KEY ix_movimentacao_empresa_id (empresa_id),
CONSTRAINT fk_movimentacao_empresa
FOREIGN KEY (empresa_id) REFERENCES empresa (id),
CONSTRAINT fk_mov_item_empresa
FOREIGN KEY (item_id, empresa_id) REFERENCES item (id, empresa_id),
CONSTRAINT fk_mov_usuario_empresa
FOREIGN KEY (usuario_id, empresa_id) REFERENCES usuario (id, empresa_id),
CONSTRAINT ck_mov_quantidade
CHECK (quantidade > 0)
) ENGINE=InnoDB;