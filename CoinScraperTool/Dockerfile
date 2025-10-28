From python:3.10-bookworm

# ✅ Setting the working dierctory 
WORKDIR /app

# ✅ Installing the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt 

# ✅ Copying the Djnago app (CoinScraperTool) Project Files
COPY . .

# ✅ Exposing port
EXPOSE 8000

# ✅ Runnning migrations and starting server
CMD [ "sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000" ]

