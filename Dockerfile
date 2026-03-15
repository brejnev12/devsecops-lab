# Dockerfile-builder
FROM python:3.11-slim

WORKDIR /workspace

# Copier juste le requirements pour installer les dépendances
COPY app/requirements.txt .

# Installer toutes les dépendances nécessaires pour l'app et les tests
RUN pip install --no-cache-dir -r requirements.txt pytest bandit

# Copier le code source
COPY app/ .

# Exposer le port de l'application
EXPOSE 5000

# Commande par défaut pour démarrer l'app
CMD ["python", "app.py"]