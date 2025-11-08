# 💰 API Controle de Finanças Pessoais

API para controle de finanças pessoais, desenvolvida em **Python** com **Flask** e **PostgreSQL**.  
Permite o gerenciamento de transações e categorias de forma segura e organizada.

# User Route

- [x] Cadastro de usuários
- [x] Autenticação utilizando JWT
- [x] Atualização dos dados do usuário
- [x] Deletar usuário e todas as informações

# Transaction Route

- [x] Cadastro de transação e categoria pela mesma rota
- [x] Requisição de todas as transações
- [x] Requisição de transações com filtros
- [x] Requisição de resumo de gastos/receita baseados em categorias
- [x] Resumo de gastos/receita por mẽs, ano
- [x] Deletar transação
- [x] Atualizar dados de transação

# Category Route

- [x] Cadastro de categoria
- [x] Atualizar nome de categoria (Também altera as transações dessa categoria)
- [x] Listar categorias
- [x] Deletar categoria não utilizada

# Bibliotecas utilizadas

- Flask
- flask-cors
- Flask-Migrate
- Flask-SQLAlchemy
- python-dotenv
- Werkzeug
- flask-jwt-extended
- flask-marshmallow
