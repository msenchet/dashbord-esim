"""Route POST /api/import/file : import de fichiers CSV ou JSON."""
from fastapi import File, HTTPException, UploadFile

from esim import MAX_IMPORT_BYTES, read_any

from .config import MAX_FILES, Mode
from .merge_offers import merge_offers
from .parse_import import parse_import


async def import_file(files: list[UploadFile] = File(...), mode: Mode = "append") -> dict:
    """Importe un ou plusieurs fichiers envoyés en multipart (champ « files »).

    Args:
        files: fichiers CSV ou JSON envoyés par le client.
        mode: « append » pour ajouter, « replace » pour remplacer les données.

    Returns:
        Le bilan de l'import (voir merge_offers).

    Raises:
        HTTPException: 413 si trop de fichiers ou si un fichier dépasse 20 Mo,
            422 s'il est illisible.
    """
    if len(files) > MAX_FILES:
        raise HTTPException(413, f"Au plus {MAX_FILES} fichiers par import")
    # frames : un couple (tableau brut, nom du fichier) par fichier reçu.
    frames = []
    for upload in files:
        # Lecture limitée à 20 Mo + 1 octet : un fichier plus gros est refusé sans tout lire.
        content = await upload.read(MAX_IMPORT_BYTES + 1)
        name = upload.filename or "import.csv"
        if len(content) > MAX_IMPORT_BYTES:
            raise HTTPException(413, f"{upload.filename} dépasse 20 Mo")
        try:
            frames.append((read_any(content, name), name))
        except Exception as exc:
            raise HTTPException(422, f"{upload.filename} : fichier illisible ({exc})") from exc
    return merge_offers(parse_import(frames), mode, ", ".join(name for _, name in frames))
