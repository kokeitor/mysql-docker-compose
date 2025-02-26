# Usa Python 3.12 con Alpine Linux como base
FROM python:3.12.9-alpine3.21

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

# EXPOSE 80

ENTRYPOINT ["python"] 
CMD ["main.py"]
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]