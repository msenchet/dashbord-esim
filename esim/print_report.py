"""Affichage des statistiques dans le terminal."""
from pathlib import Path

from .compute_stats import compute_stats
from .config import DATA_DIR
from .load_offers import load_offers
from .provider_breakdown import provider_breakdown


def print_report(folder: Path | str = DATA_DIR) -> None:
    """Charge les CSV d'un dossier et affiche les statistiques globales et par fournisseur.

    Args:
        folder: dossier contenant les fichiers CSV (par défaut, les données d'origine).
    """
    # offers : toutes les offres nettoyées ; stats : les indicateurs globaux calculés dessus.
    offers = load_offers(folder)
    stats = compute_stats(offers)
    print("=== Statistiques globales ===")
    print(f"Cartes eSIM         : {stats['total_offers']}")
    print(f"Offres > 100 €      : {stats['offers_over_100']}")
    print(f"Prix min / max / moy: {stats['price_min']:.2f} € / {stats['price_max']:.2f} € "
          f"/ {stats['price_mean']:.2f} €")
    print(f"Data moyenne        : {stats['data_mean_gb']:.2f} Go "
          f"(hors {stats['unlimited_offers']} illimités)")
    print(f"Prix moyen au Go    : {stats['price_per_gb_mean']:.2f} €/Go")
    print("\n=== Par fournisseur ===")
    print(provider_breakdown(offers).round(2).to_string())
