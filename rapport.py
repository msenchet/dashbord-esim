"""Affiche les statistiques des offres eSIM dans le terminal.

Usage : python rapport.py [dossier_csv]
Sans argument, le dossier des données d'origine (donnees-test-mybestsim/) est utilisé.
"""
import sys

from esim import DATA_DIR, print_report

if __name__ == "__main__":
    # folder : dossier passé en argument, sinon les données d'origine.
    folder = sys.argv[1] if len(sys.argv) > 1 else DATA_DIR
    print_report(folder)
