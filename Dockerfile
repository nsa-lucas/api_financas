# Usa imagem base com Python
FROM python:3.10

# Define diretório de trabalho
WORKDIR /app

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta usada pelo app (Flask costuma usar 5000)
EXPOSE 5000

# Variáveis de ambiente do Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Comando para iniciar o app
CMD ["flask", "run"]
