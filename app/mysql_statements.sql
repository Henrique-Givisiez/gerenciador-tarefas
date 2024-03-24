-- Arquivo .sql para criar o banco de dados e as tabelas necessárias
-- Executar o comando: source seu_caminho\mysql_statements.sql

-- Cria o banco de dados
CREATE DATABASE bd_gerenciador_de_tarefas;

-- Conecta ao banco de dados
USE bd_gerenciador_de_tarefas;

-- Cria as tabelas das contas
CREATE TABLE contas(
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	usuario VARCHAR(50) NOT NULL,
	senha VARCHAR(255) NOT NULL,
	email VARCHAR(100) NOT NULL
);

-- Cria as tabelas das tarefas
CREATE TABLE tarefas(
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    usuario_id INT NOT NULL,
    categoria_tarefa VARCHAR(100),
    descricao_tarefa VARCHAR(1000),
    data_tarefa DATE,
    status_tarefa VARCHAR(50) NOT NULL,
    FOREIGN KEY(usuario_id) REFERENCES contas(id)
);



