# Gerenciador de Tarefas

## Descrição
Gerenciador de tarefas que tem como estrutura semelhante a um Kanban. Primeiro projeto desenvolvido com objetivo de praticar os conhecimentos em web development. As tecnologias utilizadas no frontend foram JavaScript, CSS e HTML. Para o backend foi utilizado o framework flask e o SGBD MySQL

## Instalação
Para instalar o projeto siga os passos abaixo

1. Clone o repositório:
git clone "https://github.com/Henrique-Givisiez/gerenciador-tarefas.git"

2. Entre no diretório do projeto 
cd "caminho/do/local/do/projeto"

3. Instale as dependências (ATENÇÃO: pip 24.0 e python 3.11.2 64-bit já devem estar previamente instalados)
pip install -r "app/requirements.txt"

4. Crie as tabelas necessárias do banco de dados por meio do comando abaixo substituindo o caminho pelo local onde está o projeto (REQUISITO: MySQL):
mysql -u root -p
source "caminho/do/local/do/projeto/gerenciador-tarefas/app/mysql_statements.sql"

## Uso
Para utilizar o projeto rode o comando abaixo no terminal e abra o navegador na URL "http://127.0.0.1:5000":
python app/run.py

## Contato
Para mais informações entre em contato via e-mail: lucogds@gmail.com
