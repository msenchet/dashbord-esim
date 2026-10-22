"""Construction de la page HTML finale."""
import json
from datetime import date

import pandas as pd

from esim import compute_stats

from .build_payload import build_payload
from .bundle_scripts import bundle_scripts
from .config import REPO_URL, STYLES, TEMPLATE


def render_html(offers: pd.DataFrame) -> str:
    """Remplit le gabarit site/index.html avec les styles, les scripts et les données.

    Args:
        offers: offres nettoyées à intégrer dans la page.

    Returns:
        Le HTML complet et autonome de docs/index.html.
    """
    stats = compute_stats(offers)
    # payload : offres au format compact ; repo_link : lien « code source » facultatif.
    payload = json.dumps(build_payload(offers), ensure_ascii=False, separators=(",", ":"))
    repo_link = f' · <a href="{REPO_URL}">code source</a>' if REPO_URL else ""
    page = (TEMPLATE.read_text(encoding="utf-8")
            .replace("__STYLES__", STYLES.read_text(encoding="utf-8").strip())
            .replace("__SCRIPT__", bundle_scripts()))
    return (page
            .replace("__DATA__", payload)
            .replace("__TOTAL__", f"{stats['total_offers']:,}".replace(",", " "))
            .replace("__PROVIDERS__", str(stats["providers"]))
            .replace("__FILES__", str(offers["source_file"].nunique()))
            .replace("__BUILT__", date.today().strftime("%d/%m/%Y"))
            .replace("__REPO_LINK__", repo_link))
