# Use uma imagem oficial leve do Python
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie apenas requirements para aproveitar cache de camadas
COPY requirements.txt .

# Instale dependências sem cache
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código fonte
COPY src/ ./src/

# Exponha a porta que o Uvicorn usará
EXPOSE 8000

# Comando de inicialização padrão
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
