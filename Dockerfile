# Imagem base oficial do Python slim para menor consumo de memória e inicialização rápida
FROM python:3.11-slim

# Configurações de ambiente para Python em containers
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências e instala as bibliotecas Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte da aplicação
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar a aplicação Starlette via Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
