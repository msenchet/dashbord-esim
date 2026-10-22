"""Point d'entrée de l'API REST, pour pouvoir lancer :  uvicorn api:app --reload

Tout le code de l'API se trouve dans le paquet esim_api/ (un fichier par route).
"""
from esim_api import app

# Nom rendu disponible pour uvicorn (« api:app »).
__all__ = ["app"]
