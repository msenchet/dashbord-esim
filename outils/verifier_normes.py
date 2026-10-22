"""Vérifie les normes du code du projet.

Règles pour les fichiers de fonctions (Python avec « def », JavaScript de site/js/fonctions/) :
une seule fonction nommée par fichier, 80 lignes au maximum, 100 caractères par ligne au maximum.
Les autres fichiers (constantes, état, assemblage, HTML, CSS) ne doivent contenir aucune
fonction nommée ; leurs lignes de plus de 100 caractères sont signalées pour lisibilité.

Usage : python outils/verifier_normes.py      (code de sortie 1 en cas d'erreur)
"""
import ast
import re
import sys
from pathlib import Path

# ROOT : racine du projet ; MAX_LINES / MAX_WIDTH : limites des fichiers de fonctions.
ROOT = Path(__file__).resolve().parent.parent
MAX_LINES = 80
MAX_WIDTH = 100
# Dossiers et fichiers contrôlés.
PY_FILES = [p for d in ["esim", "esim_api", "site_builder", "streamlit_ui", "outils"]
            for p in sorted((ROOT / d).glob("*.py"))] + [
    ROOT / name for name in ["app.py", "api.py", "build_site.py", "rapport.py"]]
JS_FUNCTION_FILES = sorted((ROOT / "site" / "js" / "fonctions").glob("*.js"))
OTHER_FILES = sorted((ROOT / "site" / "js").glob("*.js")) + [
    ROOT / "site" / "styles.css", ROOT / "site" / "index.html"]
# JS_NAMED : déclaration « function nom » ou constante contenant une fonction fléchée nommée.
JS_NAMED = re.compile(r"\bfunction\s+[\w$]+|\b(?:const|let|var)\s+[\w$]+\s*=\s*"
                      r"(?:async\s*)?(?:function\b|\([^)]*\)\s*=>|[\w$]+\s*=>)")


def verifier_normes() -> int:
    """Contrôle tous les fichiers, affiche erreurs et avertissements, compte les erreurs.

    Returns:
        Le nombre d'erreurs trouvées (0 = toutes les normes sont respectées).
    """
    errors, warnings, function_files = [], [], 0
    for path in PY_FILES + JS_FUNCTION_FILES + OTHER_FILES:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        name = path.relative_to(ROOT).as_posix()
        if path.suffix == ".py":
            named = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                        for node in ast.walk(ast.parse(text)))
        else:
            named = len(JS_NAMED.findall(text))
        is_function_file = path in JS_FUNCTION_FILES or (path.suffix == ".py" and named > 0)
        long_lines = [i + 1 for i, line in enumerate(lines) if len(line) > MAX_WIDTH]
        if is_function_file:
            function_files += 1
            if named != 1:
                errors.append(f"{name} : {named} fonctions nommées (1 attendue)")
            if len(lines) > MAX_LINES:
                errors.append(f"{name} : {len(lines)} lignes (maximum {MAX_LINES})")
            if long_lines:
                errors.append(f"{name} : lignes > {MAX_WIDTH} caractères : {long_lines}")
        else:
            if named:
                errors.append(f"{name} : {named} fonction(s) dans un fichier sans fonction")
            if long_lines:
                warnings.append(f"{name} : lignes > {MAX_WIDTH} caractères : {long_lines}")
    for message in errors:
        print("ERREUR       ", message)
    for message in warnings:
        print("avertissement", message)
    print(f"{function_files} fichiers de fonctions, "
          f"{len(PY_FILES) + len(JS_FUNCTION_FILES) + len(OTHER_FILES)} fichiers contrôlés : "
          f"{len(errors)} erreur(s), {len(warnings)} avertissement(s)")
    return len(errors)


if __name__ == "__main__":
    sys.exit(1 if verifier_normes() else 0)
