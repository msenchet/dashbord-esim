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

## Import et export des données

### Dans le dashboard (GitHub Pages, sans serveur)
Panneau **Données** en haut de la page :
- **Importer un fichier** CSV ou JSON (bouton ou glisser-déposer). Le fichier est lu dans le navigateur, rien n'est envoyé.
- **Charger une API** : colle l'URL d'une API qui renvoie du JSON ou du CSV. L'API doit autoriser CORS.
- Mode **Ajouter** (une offre avec un SKU déjà présent est mise à jour) ou **Remplacer**.
- **Exporter JSON / CSV** : exporte les offres filtrées, dans le même format que l'API.
- Lien direct vers une source : `https://<ton-pseudo>.github.io/dashboard-esim/?source=<url-de-l-api>`

Formats acceptés : CSV avec `,` ou `;`, ou JSON (liste d'offres, ou `{"offers": [...]}`). Seule la colonne `price` / `prix` est obligatoire. Les colonnes en français (fournisseur, destination, data, validité, réseau, recharge) sont reconnues, ainsi que `12,45 €`, `500 Mo` et `Illimité`.

### API statique (GitHub Pages, lecture seule)
`python build_site.py` génère ces fichiers, que GitHub Pages sert avec CORS ouvert :

| Route | Contenu |
|---|---|
| `api/offers.json` | `{total, offers: [...]}` |
| `api/offers.csv` | toutes les offres en CSV |
| `api/stats.json` | les 6 statistiques + KPIs bonus |
| `api/providers.json` | répartition par fournisseur + €/Go |
| `api/index.json` | description des routes |

### API REST dynamique (`api.py`, FastAPI)
Elle permet d'importer par programme et de filtrer côté serveur. GitHub Pages ne peut pas l'exécuter : lance-la en local ou héberge-la (Render, voir plus bas).

```bash
uvicorn api:app --reload      # documentation interactive : http://localhost:8000/docs
```

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/api/offers` | offres en JSON : filtres `provider`, `country`, `validity`, `network`, `kind`, `min_price`, `max_price`, `q` ; pagination `limit`/`offset` ; tri `sort`/`order` |
| GET | `/api/offers.csv` | même chose, en CSV |
| GET | `/api/stats` | statistiques (mêmes filtres) |
| GET | `/api/providers` | répartition par fournisseur |
| GET | `/api/sources` | sources chargées |
| POST | `/api/import/file` | import de fichiers CSV/JSON (multipart, `mode=append|replace`) |
| POST | `/api/import/json` | import d'offres envoyées en JSON |
| POST | `/api/import/url` | import depuis une URL `{"url": "...", "mode": "append"}` |
| DELETE | `/api/import` | retour aux données d'origine |

```bash
curl "http://localhost:8000/api/stats?provider=Holafly&kind=unlimited"
curl -F "files=@mes_offres.csv" "http://localhost:8000/api/import/file?mode=append"
curl -X POST http://localhost:8000/api/import/json -H "Content-Type: application/json"      -d '[{"provider":"MonOp","country_name":"Japon","data_gb":10,"validity_days":15,"price":19.9}]'
```

Si la variable `ESIM_API_KEY` est définie, les routes d'écriture exigent l'en-tête `X-API-Key`. Les imports sont gardés en mémoire : ils disparaissent au redémarrage du serveur.

Le dashboard en ligne peut afficher les données de l'API : `…github.io/dashboard-esim/?source=https://esim-api.onrender.com/api/offers?limit=10000`

**Héberger l'API sur Render (gratuit)** : New + → Blueprint → choisis ce dépôt. `render.yaml` configure le service et génère la clé API.

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Pour obtenir les statistiques dans le terminal : `python esim_data.py`

La version Streamlit accepte aussi l'import de fichiers et d'URL d'API (barre latérale), ainsi que l'export CSV et JSON.

## Structure

```
docs/index.html         # dashboard statique (GitHub Pages)
docs/api/                # API statique en lecture seule (générée)
api.py                  # API REST FastAPI (import + export)
render.yaml             # déploiement de l'API sur Render
build_site.py           # génère docs/index.html
site_template.html      # gabarit HTML/JS de la version statique
app.py                  # interface Streamlit
esim_data.py            # nettoyage (toutes sources) + statistiques
donnees-test-mybestsim/ # 18 fichiers CSV sources
requirements.txt
```
