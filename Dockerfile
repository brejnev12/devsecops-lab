# Utiliser l'image Python officielle
FROM python:3.11-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances
COPY app/requirements.txt .

# Installer toutes les dépendances de l'application + outils de test
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest bandit

# Copier le code de l'application
COPY app/ .

# Exposer le port de l'application
EXPOSE 5000

# Commande par défaut : lancer l'application
CMD ["python", "app.py"]