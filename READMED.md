# fastApi_learning

Projeto de estudos baseado no curso **FastAPI do Zero**, usando o pacote `fast_zero`. Construído com FastAPI, SQLAlchemy, Alembic e Poetry para gerenciamento de dependências.

## 🧱 Stack

- **Python** 3.12.6
- **FastAPI** (extra `standard`)
- **SQLAlchemy** — ORM
- **Alembic** — migrations
- **Pydantic Settings** — configuração via `.env`
- **Poetry** — gerenciamento de dependências e ambiente virtual
- **Ruff** — lint e formatação
- **Pytest** + **pytest-cov** — testes e cobertura
- **Taskipy** — atalhos de tasks

## 📋 Pré-requisitos

- Python 3.12.6 (recomendado via `pyenv`)
- Poetry instalado
- Git

## 🚀 Setup rápido (Debian/Ubuntu)

Este repositório inclui um script que automatiza toda a instalação do ambiente no Debian:

```bash
chmod +x setup-debian.sh
./setup-debian.sh
```

O script instala dependências de sistema, `pyenv`, a versão correta do Python, o `Poetry`, e as dependências do projeto.

## 🔧 Setup manual

1. Clone o repositório:
   ```bash
   git clone https://github.com/LucasMateus-2/fastApi_learning.git
   cd fastApi_learning
   ```

2. Instale a versão correta do Python (via `pyenv`):
   ```bash
   pyenv install 3.12.6
   pyenv local 3.12.6
   ```

3. Instale o Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

4. Instale as dependências do projeto:
   ```bash
   poetry install
   ```

5. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```

6. Configure o arquivo `.env` na raiz do projeto (ajuste conforme seu banco):
   ```
   DATABASE_URL="sqlite+aiosqlite:///database.db"
   ```

7. Rode as migrations:
   ```bash
   poetry run alembic upgrade head
   ```

## ▶️ Rodando a aplicação

```bash
poetry run task run
```

Isso executa `fastapi dev fast_zero/app.py`, subindo o servidor com reload automático em `http://127.0.0.1:8000`.

- Documentação Swagger: `http://127.0.0.1:8000/docs`
- Documentação Redoc: `http://127.0.0.1:8000/redoc`

## 🧪 Tasks disponíveis

| Comando                 | Descrição                                  |
| ------------------------ | ------------------------------------------- |
| `poetry run task run`    | Sobe o servidor em modo dev                 |
| `poetry run task lint`   | Roda o `ruff check` no projeto              |
| `poetry run task format` | Formata o código com `ruff`                 |
| `poetry run task test`   | Roda os testes com `pytest` e cobertura     |

## 📁 Estrutura do projeto

```
fastApi_learning/
├── fast_zero/       # Código da aplicação
├── migrations/      # Migrations do Alembic
├── tests/           # Testes automatizados
├── alembic.ini      # Configuração do Alembic
├── pyproject.toml   # Dependências e configuração do Poetry/Ruff/Pytest
└── setup-debian.sh  # Script de setup automático para Debian
```

## 📄 Licença

Este projeto está sob a licença MIT.
