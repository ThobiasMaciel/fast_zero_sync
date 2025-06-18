FROM python:3.11-slim

# Instalar dependências do sistema (para compilar libs como uvicorn, psycopg2, etc)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Comando para iniciar FastAPI com uvicorn
CMD ["uvicorn", "src.fast_zero.app:app", "--host", "0.0.0.0", "--port", "8000"]