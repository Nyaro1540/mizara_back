# Utiliser une image de base Python
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source dans l'image
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Définir la commande pour exécuter le serveur Django avec gunicorn
CMD ["gunicorn", "mizara.wsgi:application", "--bind", "0.0.0.0:8000"]
