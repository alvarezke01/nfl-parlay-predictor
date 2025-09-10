"""
Odds/probability conversions used across predictions/parlays.
"""


def implied_prob_from_american(odds: int) -> float:
    """Convert American odds to implied probability (0..1). +200 -> 0.3333, -150 -> 0.6"""
    if odds > 0:
        return 100.0 / (odds + 100.0)
    return (-odds) / ((-odds) + 100.0)


def fair_american_from_prob(p: float) -> int:
    """Convert probability (0..1) to 'fair' American odds (no vig)."""
    p = max(min(p, 0.999999), 1e-6)
    dec = 1.0 / p
    return int(round((dec - 1.0) * 100.0)) if dec >= 2.0 else int(round(-100.0 / (dec - 1.0)))


def american_to_decimal(odds: int) -> float:
    """Convert American odds to decimal odds."""
    return 1.0 + (odds / 100.0) if odds > 0 else 1.0 + (100.0 / -odds)


def decimal_to_american(dec: float) -> int:
    """Convert decimal odds to American odds."""
    return int(round((dec - 1.0) * 100.0)) if dec >= 2.0 else int(round(-100.0 / (dec - 1.0)))


