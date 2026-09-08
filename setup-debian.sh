#!/usr/bin/env bash
#
# setup-debian.sh
#
# Automatiza a configuração do ambiente de desenvolvimento do projeto
# fastApi_learning em sistemas Debian/Ubuntu.
#
# O que este script faz:
#   1. Atualiza o apt e instala dependências de sistema (build tools,
#      libs necessárias para compilar o Python via pyenv, git, curl).
#   2. Instala o pyenv (se ainda não estiver instalado).
#   3. Instala a versão do Python exigida pelo projeto (3.12.6).
#   4. Instala o Poetry (se ainda não estiver instalado).
#   5. Instala as dependências do projeto via `poetry install`.
#   6. Cria um .env básico (se ainda não existir).
#
# Uso:
#   chmod +x setup-debian.sh
#   ./setup-debian.sh
#
set -euo pipefail

PYTHON_VERSION="3.12.6"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() {
    echo -e "\n\033[1;32m==>\033[0m $1"
}

warn() {
    echo -e "\n\033[1;33m[AVISO]\033[0m $1"
}

# ---------------------------------------------------------------------------
# 1. Dependências de sistema
# ---------------------------------------------------------------------------
log "Atualizando pacotes do sistema..."
sudo apt-get update -y

log "Instalando dependências de build necessárias para o pyenv/Python..."
sudo apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    ca-certificates

# ---------------------------------------------------------------------------
# 2. pyenv
# ---------------------------------------------------------------------------
if ! command -v pyenv >/dev/null 2>&1; then
    log "Instalando pyenv..."
    curl -fsSL https://pyenv.run | bash

    # Adiciona o pyenv ao shell atual (para uso imediato neste script)
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    # Persiste no .bashrc, caso ainda não esteja lá
    SHELL_RC="$HOME/.bashrc"
    if ! grep -q 'PYENV_ROOT' "$SHELL_RC" 2>/dev/null; then
        {
            echo ''
            echo '# pyenv'
            echo 'export PYENV_ROOT="$HOME/.pyenv"'
            echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
            echo 'eval "$(pyenv init -)"'
        } >> "$SHELL_RC"
        warn "Configuração do pyenv adicionada ao $SHELL_RC. Rode 'source $SHELL_RC' ou abra um novo terminal depois."
    fi
else
    log "pyenv já está instalado, pulando instalação."
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

# ---------------------------------------------------------------------------
# 3. Python via pyenv
# ---------------------------------------------------------------------------
if ! pyenv versions --bare | grep -q "^${PYTHON_VERSION}$"; then
    log "Instalando Python ${PYTHON_VERSION} via pyenv (pode demorar alguns minutos)..."
    pyenv install "${PYTHON_VERSION}"
else
    log "Python ${PYTHON_VERSION} já está instalado via pyenv."
fi

log "Definindo Python ${PYTHON_VERSION} como versão local do projeto..."
cd "$PROJECT_DIR"
pyenv local "${PYTHON_VERSION}"

# ---------------------------------------------------------------------------
# 4. Poetry
# ---------------------------------------------------------------------------
if ! command -v poetry >/dev/null 2>&1; then
    log "Instalando Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -

    export PATH="$HOME/.local/bin:$PATH"
    SHELL_RC="$HOME/.bashrc"
    if ! grep -q '.local/bin' "$SHELL_RC" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        warn "PATH do Poetry adicionado ao $SHELL_RC. Rode 'source $SHELL_RC' ou abra um novo terminal depois."
    fi
else
    log "Poetry já está instalado, pulando instalação."
fi

# ---------------------------------------------------------------------------
# 5. Dependências do projeto
# ---------------------------------------------------------------------------
log "Configurando Poetry para usar o Python correto..."
poetry env use "$(pyenv which python)"

log "Instalando dependências do projeto com Poetry..."
poetry install

# ---------------------------------------------------------------------------
# 6. Arquivo .env
# ---------------------------------------------------------------------------
if [ ! -f "$PROJECT_DIR/.env" ]; then
    log "Criando arquivo .env padrão..."
    cat > "$PROJECT_DIR/.env" <<EOF
DATABASE_URL="sqlite+aiosqlite:///database.db"
EOF
else
    log "Arquivo .env já existe, mantendo o atual."
fi

# ---------------------------------------------------------------------------
# 7. Migrations
# ---------------------------------------------------------------------------
log "Aplicando migrations do Alembic..."
poetry run alembic upgrade head

log "Setup concluído! ✅"
echo ""
echo "Para rodar o projeto:"
echo "  poetry run task run"
echo ""
echo "Depois acesse: http://127.0.0.1:8000/docs"
