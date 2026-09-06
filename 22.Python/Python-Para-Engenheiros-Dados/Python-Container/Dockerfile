FROM python:3.12-slim

WORKDIR /app

# Copia e instala as dependências primeiro (aproveita o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY main.py .

CMD ["python", "main.py"]