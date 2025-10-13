# 💰 API Controle de Finanças Pessoais

Uma API simples para controle de finanças pessoais, desenvolvida em **Python** com **Flask** e **PostgreSQL**.  
Permite o gerenciamento de usuários, transações e categorias de forma segura e organizada.

---

## 📘 Descrição

Esta API permite que cada usuário crie uma conta e gerencie suas próprias transações financeiras.  
As transações podem ser do tipo **receita** ou **despesa**, e cada uma delas possui:

- Categoria  
- Descrição  
- Tipo
- Data  
- Valor  
- ID do usuário (chave estrangeira)  
- ID da categoria (chave estrangeira)

Ao cadastrar uma transação, o sistema verifica se a categoria informada já existe.  
Caso **não exista**, uma nova categoria é automaticamente criada.  

Os usuários também podem **criar, atualizar e deletar** categorias manualmente.  
Cada usuário possui suas **próprias categorias** e **transações**.  

Na rota de usuário, é possível:
- Atualizar dados pessoais (nome, email, senha)
- Deletar completamente a conta e todos os dados relacionados  

> ⚠️ Todas as rotas, com exceção da criação de usuário, requerem autenticação por login.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Flask**
- **PostgreSQL**
- **SQLAlchemy**
- **Werkzeug** (para hash de senhas)
- **Flask-Login** (autenticação)

---

## 🚀 Como Rodar Localmente

1. **Clone o repositório**

   ```bash
   git clone https://github.com/nsa-lucas/api_financas.git
   cd api_financas
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**

   Crie uma base de dados de sua preferência e informe o link, com usuário e senha no arquivo .env.
   Crie e edite o arquivo `.env` (ou a variável de ambiente) com as credenciais do seu PostgreSQL ou banco de dados de sua preferência e informe a SECRET_KEY, por exemplo:

   ```
   SECRET_KEY=minha-secret-key
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/financas_db
   ```
   A importação do arquivo .env é feito de forma automática com python-dotenv


5. **Crie as tabelas do banco de dados inicie o servidor**

   ```bash
   flask shell
   >>>db.create_all()
   >>>db.session.commit()
   >>>exit()
   flask run
   ```

6. **Testando as rotas com o Postman**

   Todas as rotas da API devem ser testadas através do **Postman**.  
   Um arquivo `.json` será disponibilizado no repositório contendo a **coleção completa de requisições**, pronta para importação.

   ### 🧪 Como testar no Postman

   1. Abra o **Postman**  
   2. Clique em **Importar** (ícone no canto superior esquerdo ou utilizando o atalho Ctrl+O)  
   3. Selecione o arquivo `api_financas.postman_collection.json` disponível no repositório  
   4. Após importar, a coleção com todas as rotas aparecerá no painel lateral  
   5. Execute as requisições conforme desejar — lembre-se de realizar o **login** antes de acessar as rotas protegidas

   > ⚠️ As rotas da API só podem ser testadas via Postman, pois não há interface web.

---

## 🔐 Autenticação

A API utiliza **autenticação baseada em login de usuário**.  
Após o login, o token ou sessão deve ser incluído em todas as requisições às rotas protegidas.

---

## 📂 Estrutura Básica das Rotas

| Rota | Método | Descrição |
|------|---------|-----------|
| `/api/user/add` | `POST` | Cria um novo usuário |
| `/api/user/login` | `POST` | Realiza login e autentica o usuário |
| `/api/user/logout` | `POST` | Realiza logout do usuário |
| `/api/user/update` | `PUT` | Atualiza os dados do usuário logado |
| `/api/user/delete` | `DELETE` | Deleta o usuário e todos os dados associados (necessário informar a senha) |
| `/api/transactions` | `GET` | Lista as transações do usuário |
| `/api/transactions/add` | `POST` | Cria uma nova transação |
| `/api/transactions/update/<id>` | `PUT` | Atualiza os dados da transação (description, amount, type, date, category) |
| `/api/transactions/delete/<id>` | `DELETE` | Deleta uma transação |
| `/api/categories` | `GET` | Lista categorias do usuário |
| `/api/categories/add` | `POST` | Cria uma nova categoria |
| `/api/categories/update/<id>` | `PUT` | Atualiza o nome da categoria |
| `/api/categories/delete/<id>` | `DELETE` | Deleta uma categoria (caso não esteja em uso) |

---

## 📦 Dependências Principais

```
Flask
Flask-SQLAlchemy
Flask-Login
Werkzeug
psycopg2
python-dotenv
```

---

## 🧾 Licença

Este projeto **não possui licença** definida.  
Sinta-se à vontade para utilizá-lo e modificá-lo para fins de estudo ou aprendizado.

---

## ✨ Autor

**Lucas Nunes**  
📧 https://github.com/nsa-lucas
