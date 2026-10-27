# 📶 Dashboard eSIM

Tableau de bord interactif qui compare **5 056 offres eSIM de 18 fournisseurs** (Airalo, Holafly, Saily, Ubigi…), construit en Python avec **Pandas**, **Plotly** et **Streamlit**.

🔗 **Démo en ligne :** https://msenchet.github.io/dashboard-esim/

📐 **Documentation technique** (architecture, flux de données, choix techniques, schémas) : [README_TECHNIQUE.md](README_TECHNIQUE.md)

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

## Graphiques interactifs

Un clic sur une barre ouvre un **résumé** dans un panneau latéral :
- **Fournisseur** (offres par fournisseur, €/Go) : prix min/moyen/max, €/Go comparé à la moyenne, part d'illimité, de 5G et de recharge, principales destinations, offres les moins chères et meilleur prix au Go.
- **Tranche de prix** (histogramme) et **volume de data** : le même résumé, avec les principaux fournisseurs.

« Voir les offres dans la liste ↓ » filtre « Toutes les offres » sur cette sélection et y fait défiler la page. Pour un fournisseur, « Filtrer tout le dashboard » applique aussi le filtre aux indicateurs et aux graphiques.

## Recherche multicritère

Dans la liste « Toutes les offres », la barre de recherche combine plusieurs critères séparés par des espaces. Une offre doit les remplir tous :

| Exemple | Signification |
|---|---|
| `japon`, `"afrique du sud"` | texte (fournisseur, offre, destination…), sans tenir compte des accents |
| `<20€`, `10-30€`, `20€` | prix inférieur à 20 €, entre 10 et 30 €, au plus 20 € |
| `>=5go`, `500mo`, `illimité`, `limité` | volume de data |
| `30j`, `<15j` | validité |
| `5g`, `4g`, `recharge` | réseau, offre rechargeable |
| `japon,corée` | l'un ou l'autre |
| `-holafly` | exclure |

Exemple : `japon,corée >=10go 30j <40€ -airalo`

On peut aussi **cliquer sur une valeur** du tableau (fournisseur, destination, data, validité, réseau, recharge) ou sur un fournisseur dans la « Répartition » pour l'ajouter comme filtre. Deux valeurs de la même colonne se combinent en « ou », des colonnes différentes en « et ». Les critères actifs s'affichent en pastilles : clique sur ✕ pour en retirer un. L'export CSV reprend la liste filtrée.

## Méthode de nettoyage (paquet `esim/`)

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

GitHub Pages ne sert que des fichiers statiques et ne peut pas exécuter Python. `build_site.py` nettoie donc les données avec le paquet `esim/`. Il assemble ensuite le gabarit `site/index.html`, les styles `site/styles.css` et les scripts de `site/js/` en une seule page. Les filtres et les indicateurs sont recalculés dans le navigateur, avec les mêmes formules que la version Python.

Après une modification des CSV ou de `site/`, régénère la page :

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
- Lien direct vers une source : `https://<ton-pseudo>.github.io/dashboard-esim/?source=<url-de-l-api>`. La page affiche un avertissement et ne charge les données qu'après un clic sur « Charger ces données ».

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

### API REST dynamique (paquet `esim_api/`, FastAPI)
Elle permet d'importer par programme et de filtrer côté serveur. GitHub Pages ne peut pas l'exécuter : lance-la en local ou héberge-la (Render, voir plus bas).

```bash
# Sur ton ordinateur : écriture sans clé et import d'URL locales autorisés
ESIM_OPEN_WRITE=1 ESIM_ALLOW_PRIVATE_URLS=1 uvicorn api:app --reload
# Sur un serveur : une clé est obligatoire pour importer
ESIM_API_KEY="une-longue-cle-secrete" uvicorn api:app --host 0.0.0.0
# documentation interactive : http://localhost:8000/docs
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
curl -H "X-API-Key: $ESIM_API_KEY" -F "files=@mes_offres.csv" \
     "http://localhost:8000/api/import/file?mode=append"
curl -X POST http://localhost:8000/api/import/json -H "X-API-Key: $ESIM_API_KEY" \
     -H "Content-Type: application/json" \
     -d '[{"provider":"MonOp","country_name":"Japon","data_gb":10,"validity_days":15,"price":19.9}]'
```

Les routes d'écriture exigent l'en-tête `X-API-Key`, égal à la variable `ESIM_API_KEY` du serveur. Sans clé configurée, l'écriture est refusée (`ESIM_OPEN_WRITE=1` la rouvre, uniquement en local). Les imports sont gardés en mémoire (200 000 offres au plus) : ils disparaissent au redémarrage du serveur.

Le dashboard en ligne peut afficher les données de l'API : `…github.io/dashboard-esim/?source=https://esim-api.onrender.com/api/offers?limit=10000`

**Héberger l'API sur Render (gratuit)** : New + → Blueprint → choisis ce dépôt. `render.yaml` configure le service et génère la clé API.

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Pour obtenir les statistiques dans le terminal : `python rapport.py`

La version Streamlit accepte aussi l'import de fichiers et d'URL d'API (barre latérale), ainsi que l'export CSV et JSON.

## Sécurité

| Risque | Protection |
|---|---|
| Injection de code via des données importées | tout texte affiché est échappé ; les noms piégés (`<img onerror=…>`, `javascript:`) sont inoffensifs |
| SSRF : l'API ou Streamlit utilisés pour lire un service interne | l'import par URL refuse les adresses privées, locales et de métadonnées cloud, y compris après une redirection (`ESIM_ALLOW_PRIVATE_URLS=1` lève la restriction, uniquement en local) |
| Modification des données par un autre site | écriture refusée sans clé API ; la clé est comparée à temps constant |
| Formules Excel piégées dans les CSV exportés | les textes commençant par `= + - @` sont précédés d'une apostrophe |
| Fichiers ou réponses démesurés | 20 Mo par fichier (lecture interrompue au-delà), 20 fichiers par import, 200 000 offres en mémoire |
| Script Plotly modifié sur le CDN | empreinte `integrity` (SRI) : le navigateur refuse un fichier altéré |
| Lien `?source=` piégé | confirmation obligatoire avant de charger des données externes |

Aucun secret n'est stocké dans le dépôt : la clé API se définit dans l'environnement du serveur (Render la génère via `render.yaml`).

## Normes du code

Les fichiers de fonctions suivent trois règles : **une seule fonction nommée par fichier**, **80 lignes au maximum** et **100 caractères par ligne au maximum**. Chaque fichier porte le nom de sa fonction. Les fonctions anonymes passées en argument (`rows.map(o => …)`, gestionnaires d'événements) font partie de la fonction qui les contient.

Les autres fichiers (constantes, état, assemblage, HTML, CSS) ne contiennent aucune fonction. Toutes les variables y sont documentées en français. Pour tout vérifier :

```bash
python outils/verifier_normes.py
```

## Structure

```
esim/                   # moteur : nettoyage (toutes sources) + statistiques, 1 fonction par fichier
  config.py             #   constantes (chemins, seuil 100 €, alias de colonnes…)
esim_api/               # API REST FastAPI, une route par fichier
  app.py                #   création de l'application et déclaration des routes
  config.py, store.py, models.py   # réglages, données en mémoire, structures échangées
site/                   # sources du dashboard statique
  index.html            #   gabarit HTML
  styles.css            #   styles et couleurs (clair / sombre)
  js/donnees.js         #   données injectées au build
  js/config.js          #   constantes
  js/etat.js            #   état de la page
  js/fonctions/*.js     #   une fonction par fichier
  js/main.js            #   démarrage de la page
site_builder/           # génération de docs/ (1 fonction par fichier)
streamlit_ui/           # briques de l'application Streamlit (1 fonction par fichier)
outils/verifier_normes.py  # contrôle des normes du code
docs/index.html         # dashboard généré (GitHub Pages)
docs/api/               # API statique en lecture seule (générée)
app.py                  # application Streamlit
api.py                  # point d'entrée de l'API (uvicorn api:app)
build_site.py           # génère docs/
rapport.py              # statistiques dans le terminal
render.yaml             # déploiement de l'API sur Render
donnees-test-mybestsim/ # 18 fichiers CSV sources
requirements.txt
```
