# Usa Python 3.12 con Alpine Linux como base
FROM python:3.12.9-alpine3.21

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo el archivo de dependencias primero (mejor caché en Docker)
COPY requirements.txt requirements.txt

# Instala dependencias de Python sin usar caché
RUN pip install --no-cache-dir -r requirements.txt

# Luego copia el resto del código
COPY . .

CMD ["python", "main.py"]
