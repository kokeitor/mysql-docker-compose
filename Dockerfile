# Usa Python 3.12 con Alpine Linux como base
FROM python:3.12.9-alpine3.21

# Establece el directorio de trabajo
WORKDIR /app

# Luego copia el resto del código
COPY . .

# Instala dependencias de Python sin usar caché
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python"] 
CMD ["main.py"]
