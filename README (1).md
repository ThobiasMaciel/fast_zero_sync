# Gerenciador de Tarefas
##### Alunos: Lucas Machado, Thobias Maciel, Pedro Scott
### Engenharia de Software: Arquitetura e Padrões - 2025/01
##### Professor Guilherme Lacerda
                   
## 1. Visão Geral

### Objetivo do Sistema 
Esta API RESTful foi desenvolvida para gerenciar tarefas colaborativas entre usuários. Ela permite a criação, atribuição, edição e finalização de tarefas, além de controlar o acesso via autenticação com JWT.

### Contexto de Uso
Ideal para equipes pequenas e médias que desejam gerenciar atividades de forma organizada e colaborativa. A API pode ser integrada a frontends web ou mobile para aplicações de produtividade.

### Instruções de instalação
# Clonar o repositório
git clone https://github.com/usuario/api-tarefas.git
cd api-tarefas

# Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
uvicorn app.main:app --reload

## 2. Ferramentas Utilizadas

Python e Fast API

Swagger

Optamos pela Clean Architecture, separando responsabilidades em camadas bem definidas:

Domain: Entidades e regras de negócio

Use Cases: Casos de uso da aplicação

Infrastructure: Banco de dados, JWT, dependências externas

Interface: FastAPI com os endpoints REST

#### Padrões Aplicados
Inversão de dependência via injeção de dependências do FastAPI

Repositórios abstratos

Validação com Pydantic

Autenticação com JWT

Testes com Pytest

## 3. Modelagem de Dados

#### Diagrama Entidade-Relacionamento (ER)
+------------+       +-----------+
|   User     |       |  Task     |
+------------+       +-----------+
| id (PK)    |<----->| id (PK)   |
| name       |       | title     |
| email      |       | desc      |
| password   |       | status    |
| is_active  |       | priority  |
+------------+       | due_date  |
                     | assigned_to (FK -> User.id)
                     +-----------+

#### Descrição das Tabelas
#### users
Campo	  | Tipo	 | Descrição
----------------------------------------
id	      | Integer	 | Identificador único (PK)
name	  | Text	 | Nome do usuário
email	  | Text	 | Email do usuário (único)
password  | Text	 | Hash da senha
is_active | Boolean	 | Soft delete (true = ativo)

#### tasks
Campo	    | Tipo	    | Descrição
-------------------------------------------
id	        | Integer	| Identificador da tarefa
title	    | Text	    | Título da tarefa
desc	    | Text	    | Descrição detalhada
status	    | Text	    | Estado da tarefa (e.g., pending)
priority	| Text	    | Prioridade (low, medium, high)
due_date	| Date	    | Data limite para conclusão
assigned_to	| Integer	| ID do usuário responsável (FK)

## 5.Fluxo de Requisições
#### Autenticação
POST /auth/login
Recebe {email, password} e retorna JWT.

POST /auth/logout
Invalida o token (se implementado como blacklist ou client-side).

#### Usuários
POST /users
Cria um novo usuário.
Exemplo:
{
  "name": "João",
  "email": "joao@email.com",
  "password": "senha123"
}
GET /users/{id}
Retorna dados de um usuário.

PUT /users/{id}
Atualiza nome/email.

DELETE /users/{id}
Soft delete: marca is_active = false.

#### Tarefas
POST /tasks
Cria uma tarefa nova.

GET /tasks/{id}
Retorna os detalhes da tarefa.

GET /tasks?assignedTo=3
Retorna todas as tarefas do usuário 3.

GET /tasks?status=done&priority=high&dueBefore=2025-06-01
Filtro avançado.

PUT /tasks/{id}
Atualiza os campos da tarefa.

DELETE /tasks/{id}
Remove uma tarefa.

#### Configuração e Deploy
#### Dependências Principais
Python 3.11+

FastAPI

Uvicorn

SQLite

SQLAlchemy

Pydantic

PyJWT

passlib

pytest

#### Execução Local
uvicorn app.main:app --reload

#### Variáveis de Ambiente
JWT_SECRET=secreto123
JWT_ALGORITHM=HS256

#### Deploy com Docker
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

## 6. Testes Automatizados

#### Estratégia
Testes unitários dos casos de uso (camada de domínio)

Testes de integração dos endpoints com a lib httpx

Mock de dependências com pytest-mock

#### Cobertura
Cobertura total acima de 60%

Testes para:

Criação de usuários e tarefas

Login com JWT

Filtros de busca

Validações de dados

#### Ferramentas de testes utilizadas:
* pytest --cov=app