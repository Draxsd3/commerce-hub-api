# API Flask + Flasgger

API REST completa em Python utilizando Flask, SQLAlchemy e Flasgger, organizada por camadas e pronta para execução em desenvolvimento com PostgreSQL.

## Tecnologias utilizadas

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flasgger
- PostgreSQL
- Docker Compose
- python-dotenv
- Dockerfile para subir a API em container

## Estrutura do projeto

```text
api-flasgger/
├── app/
│   ├── blueprints/
│   │   ├── auth/
│   │   ├── orders/
│   │   ├── products/
│   │   └── users/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   ├── extensions.py
│   └── __init__.py
├── db/
│   └── seed.sql
├── .env.example
├── docker-compose.yml
├── requirements.txt
├── run.py
└── README.md
```

## Recursos implementados

- App Factory para criação da aplicação
- 4 Blueprints independentes: autenticação, usuários, produtos e pedidos
- CRUD REST para cada domínio
- Models com SQLAlchemy
- Respostas padronizadas para sucesso e erro
- Tratamento global de exceções
- Swagger UI com documentação automática em todas as rotas
- Seed inicial para banco PostgreSQL

## Como rodar o banco com Docker

1. Certifique-se de ter Docker e Docker Compose instalados.
2. Copie o arquivo de ambiente:

```bash
copy .env.example .env
```

3. Suba o PostgreSQL:

```bash
docker compose up -d
```

4. O banco ficará disponível em `localhost:5432` com:

- Database: `api_flasgger`
- User: `postgres`
- Password: `postgres`

## Como executar a API

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Copie o arquivo de ambiente:

```bash
copy .env.example .env
```

4. Inicie a aplicação:

```bash
python run.py
```

## Como acessar a documentação Swagger

- Swagger UI: `http://localhost:5000/docs/`
- OpenAPI JSON: `http://localhost:5000/apispec.json`

## Como subir a API com Docker

```bash
docker compose up --build
```

Com esse comando, a API sobe em `http://localhost:5000` e o PostgreSQL em `localhost:5432`.

## Principais endpoints

- `GET /api/auth/`
- `POST /api/auth/`
- `PUT /api/auth/`
- `DELETE /api/auth/`
- `GET /api/users/`
- `POST /api/users/`
- `PUT /api/users/{id}`
- `DELETE /api/users/{id}`
- `GET /api/products/`
- `POST /api/products/`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`
- `GET /api/orders/`
- `POST /api/orders/`
- `PUT /api/orders/{id}`
- `DELETE /api/orders/{id}`

## Boas práticas adotadas

- Separação por camadas: `routes`, `services`, `models` e `config`
- Uso de variáveis sensíveis via `.env`
- Uso de Blueprints para modularização
- Padrão REST nas rotas
- Tratamento centralizado de erros
- Serialização consistente nas respostas

## Observações

- Em desenvolvimento, a aplicação executa `db.create_all()` ao subir a app.
- O seed SQL é aplicado automaticamente quando o container PostgreSQL sobe pela primeira vez.
- A autenticação foi modelada de forma simples para ambiente de desenvolvimento, com token fictício para facilitar testes.
