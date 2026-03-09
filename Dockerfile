# Dockerfile complet DevSecOps
FROM python:3.11-slim

WORKDIR /app

# Copier le fichier requirements
COPY app/requirements.txt .

# Installer toutes les dépendances + outils de test
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest bandit pbr

# Copier le code source
COPY app/ .

# Exposer le port
EXPOSE 5000

# Lancer l'application par défaut
CMD ["python", "app.py"]