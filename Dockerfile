# Image de base Python
FROM python:3.11-slim

# Installer ffmpeg pour yt-dlp
RUN apt-get install -y ffmpeg

# Créer un répertoire de travail
WORKDIR /app

# Copier requirements et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY . .

# Lancer ton bot (si ton fichier principal s'appelle bot.py)
CMD ["python", "telegram.py"]
