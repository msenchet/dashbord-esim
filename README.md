# 📶 Dashboard eSIM

Tableau de bord interactif qui compare **5 056 offres eSIM de 18 fournisseurs** (Airalo, Holafly, Saily, Ubigi…), construit en Python avec **Pandas**, **Plotly** et **Streamlit**.

🔗 **Démo en ligne :** https://&lt;ton-pseudo&gt;.github.io/dashboard-esim/

## Indicateurs

| Indicateur | Valeur (jeu complet) |
|---|---|
| Nombre total de cartes eSIM | 5 056 |
| Offres à plus de 100 € | 56 |
| Prix minimum / maximum / moyen | 5,36 € / 154,63 € / 29,30 € |
| Data moyenne par carte (hors illimité) | 14,5 Go |
| Forfaits illimités | 653 |
| Prix moyen au Go (bonus) | 3,17 €/Go |

Le dashboard affiche aussi la répartition par fournisseur, le prix moyen au Go par fournisseur, la distribution des prix, le prix médian selon le volume et un tableau consultable avec recherche et export CSV. Tous les indicateurs se recalculent selon les filtres (fournisseur, destination, durée, réseau, prix, type de forfait).

## Méthode de nettoyage (`esim_data.py`)

- Lecture automatique de tous les `.csv` du dossier, avec détection du séparateur (`,` ou `;`).
- Nom du fournisseur pris dans la colonne `provider`, ou à défaut dans le nom du fichier.
- Prix convertis en `float` (gère `12,45 €`, `€12.45`, `1 234,50`).
- Volumes standardisés en Go (`500 Mo` → 0,5 Go, `1 To` → 1 000 Go).
- Forfaits **illimités** repérés (`Illimité`, `unlimited`) et **exclus** des moyennes de data et de €/Go, pour ne pas les fausser.
- Le prix au Go est calculé pour chaque offre (`prix / Go`), puis moyenné.
- Les doublons de SKU sont supprimés.

## Deux versions du dashboard

| Version | Fichier | Hébergement |
|---|---|---|
| **Statique** (HTML + Plotly.js) | `docs/index.html`, généré par `build_site.py` | **GitHub Pages** |
| Streamlit | `app.py` | local ou Streamlit Community Cloud |

GitHub Pages ne sert que des fichiers statiques et ne peut pas exécuter Python. `build_site.py` nettoie donc les données avec `esim_data.py`, puis les injecte dans `site_template.html`. Les filtres et les indicateurs sont recalculés dans le navigateur, avec les mêmes formules que la version Python.

Après une modification des CSV ou du gabarit, régénère la page :

```bash
python build_site.py
```

### Publier sur GitHub Pages
1. Pousse le dépôt sur GitHub.
2. **Settings → Pages → Build and deployment** : Source *Deploy from a branch*, branche `main`, dossier `/docs`, puis **Save**.
3. Au bout d'une minute environ, le site est en ligne à l'adresse `https://<ton-pseudo>.github.io/<nom-du-depot>/`.

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Pour obtenir les statistiques dans le terminal : `python esim_data.py`

## Structure

```
docs/index.html         # dashboard statique (GitHub Pages)
build_site.py           # génère docs/index.html
site_template.html      # gabarit HTML/JS de la version statique
app.py                  # interface Streamlit
esim_data.py            # nettoyage + statistiques
donnees-test-mybestsim/ # 18 fichiers CSV sources
requirements.txt
```
