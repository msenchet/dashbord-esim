"""Formatage d'un montant en euros."""


def euro(value: float) -> str:
    """Formate un montant à la française : 1234.5 → « 1 234,50 € ».

    Args:
        value: montant en euros.

    Returns:
        Le montant formaté avec l'espace des milliers et la virgule décimale.
    """
    return f"{value:,.2f} €".replace(",", " ").replace(".", ",")
