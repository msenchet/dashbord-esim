"""Jeu de données gardé en mémoire par l'API (aucune fonction ici).

Les fonctions merge_offers et reset_offers modifient ces variables. Les imports sont perdus
au redémarrage du serveur.
"""
import threading

from esim import load_offers

from .config import ORIGIN_LABEL

# Verrou : empêche deux imports simultanés de modifier les données en même temps.
lock = threading.Lock()

# Offres d'origine (les 18 CSV), chargées une seule fois au démarrage.
base = load_offers()

# Offres actuellement servies par l'API (origine + imports successifs).
offers = base

# Liste lisible des sources chargées, dans l'ordre d'import.
sources = [ORIGIN_LABEL]
