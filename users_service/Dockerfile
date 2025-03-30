# Usamos una imagen base de Python
FROM python:3.9

# Configuración del directorio de trabajo
WORKDIR /app

# Copiar los archivos al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del microservicio
EXPOSE 5001

# Comando de ejecución
CMD ["python", "app.py"]
