"""Assemblage des fichiers JavaScript du site en un seul script."""
from .config import JS_DIR, JS_FUNCTIONS_DIR, JS_HEAD, JS_TAIL


def bundle_scripts() -> str:
    """Concatène les scripts dans l'ordre : données, config, état, fonctions, démarrage.

    Les fonctions sont déclarées avec « function » : elles sont donc utilisables partout
    dans le script final, quel que soit l'ordre de leurs fichiers.

    Returns:
        Le code JavaScript complet, chaque fichier précédé d'un commentaire indiquant sa source.
    """
    # paths : tous les fichiers à assembler, dans l'ordre d'exécution.
    paths = ([JS_DIR / name for name in JS_HEAD]
             + sorted(JS_FUNCTIONS_DIR.glob("*.js"))
             + [JS_DIR / name for name in JS_TAIL])
    parts = [f"/* ===== {path.relative_to(JS_DIR).as_posix()} ===== */\n"
             + path.read_text(encoding="utf-8").strip() for path in paths]
    return "\n\n".join(parts)
