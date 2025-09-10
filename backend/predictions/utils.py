def implied_prob_from_american(odds: int) -> float:
    if odds > 0:
        return 100.0 / (odds + 100.0)
    return (-odds) / ((-odds) + 100.0)


def fair_american_from_prob(p: float) -> int:
    p = max(min(p, 0.999999), 1e-6)
    dec = 1.0 / p
    return int(round((dec - 1) * 100)) if dec >= 2 else int(round(-100 / (dec - 1)))
