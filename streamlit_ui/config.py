"""Réglages de l'application Streamlit (aucune fonction ici)."""

# Couleur des barres des graphiques (bleu de la palette du dashboard).
BLUE = "#2a78d6"

# Couleur de la ligne de référence pointillée « 100 € » de l'histogramme.
GRAY = "#a3a29c"

# Hauteur (pixels) des graphiques par fournisseur et des autres graphiques.
TALL_CHART = 520
CHART_HEIGHT = 420

# Nombre de tranches de l'histogramme des prix.
HIST_BINS = 40

# Choix du filtre « Type de forfait ».
KIND_ALL = "Tous"
KIND_LIMITED = "Volume limité"
KIND_UNLIMITED = "Illimité"
KIND_CHOICES = [KIND_ALL, KIND_LIMITED, KIND_UNLIMITED]

# Durée (secondes) pendant laquelle une réponse d'URL est gardée en cache, et délai d'appel.
URL_CACHE_SECONDS = 300
URL_TIMEOUT_SECONDS = 20

# Colonnes affichées dans le tableau « Toutes les offres », dans cet ordre.
OFFER_COLUMNS = ["provider", "product_name", "country_name", "data_display", "validity_days",
                 "price", "price_per_gb", "network", "top_up"]

# Colonnes dans lesquelles la recherche cherche les mots tapés.
SEARCH_COLUMNS = ["provider", "product_name", "country_name", "network"]
