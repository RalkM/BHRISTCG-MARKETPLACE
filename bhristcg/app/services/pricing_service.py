#pricing services
"""Condition-adjusted price suggestions in NZD. All pricing logic lives here."""

CONDITION_MULTIPLIERS = {
    'mint': 1.2,
    'near_mint': 1.0,
    'light_played': 0.85,
    'played': 0.65,
    'damaged': 0.5,
}

CONDITION_LABELS = {
    'mint': 'Mint',
    'near_mint': 'Near Mint',
    'light_played': 'Light Played',
    'played': 'Played',
    'damaged': 'Damaged',
}

USD_TO_NZD = 1.63


def get_condition_multiplier(condition: str) -> float:
    return CONDITION_MULTIPLIERS.get(condition, 1.0)


def usd_to_nzd(amount: float) -> float:
    return round(amount * USD_TO_NZD, 2)


def get_price_suggestion(card, condition: str) -> dict:
    multiplier = get_condition_multiplier(condition)
    label = CONDITION_LABELS.get(condition, condition)

    if not card or not card.market_price:
        return {
            'suggested_price': None, 'low': None, 'high': None,
            'multiplier': multiplier, 'condition': label,
            'explanation': 'No market data available.', 'has_data': False,
        }

    suggested = round(card.market_price * multiplier, 2)
    low = round(card.low_price * multiplier, 2) if card.low_price else None
    high = round(card.high_price * multiplier, 2) if card.high_price else None

    return {
        'suggested_price': suggested,
        'low': low,
        'high': high,
        'market_base': card.market_price,
        'multiplier': multiplier,
        'condition': label,
        'explanation': (
            f'Market NZ${card.market_price:.2f} × {multiplier} ({label}) = NZ${suggested:.2f}'
        ),
        'has_data': True,
    }
