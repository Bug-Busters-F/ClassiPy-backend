# Usar uma imagem Python oficial como base
FROM python:3.11-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta que a aplicação vai usar
EXPOSE 8000

# Comando para iniciar a aplicação quando o container for executado
# Usamos --host 0.0.0.0 para permitir conexões de fora do container
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
