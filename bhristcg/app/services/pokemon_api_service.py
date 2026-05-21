#Pokemon api service
"""
Pokemon TCG API service.
Strategy: cache → API (if key set) → mock fallback.
Never crashes on API failure.
"""
import requests
from flask import current_app
from app.services import cache_service
from app.services.mock_data_service import get_mock_cards, search_mock_cards, get_mock_card_by_id

BASE_URL = 'https://api.pokemontcg.io/v2'
TIMEOUT = 8


def _key():
    return current_app.config.get('POKEMON_TCG_API_KEY', '')


def _headers():
    h = {'Content-Type': 'application/json'}
    if _key():
        h['X-Api-Key'] = _key()
    return h


def _api_available():
    return bool(_key())


def search_cards(query='', set_name='', rarity='', game='pokemon', page=1, page_size=20):
    cache_key = f'search:{query}:{set_name}:{rarity}:{game}:{page}'
    cached = cache_service.get(cache_key)
    if cached:
        return cached

    if _api_available():
        try:
            result = _api_search(query, set_name, rarity, page, page_size)
            cache_service.set(cache_key, result, ttl=current_app.config['CACHE_TTL'])
            return result
        except Exception as e:
            current_app.logger.warning(f'Pokemon API error: {e}. Using mock.')

    cards = search_mock_cards(query, set_name, rarity, game)
    result = {'cards': cards, 'total': len(cards), 'source': 'mock'}
    cache_service.set(cache_key, result, ttl=300)
    return result


def get_card_by_id(card_id: str):
    cache_key = f'card:{card_id}'
    cached = cache_service.get(cache_key)
    if cached:
        return cached

    if _api_available():
        try:
            result = _api_get_card(card_id)
            if result:
                cache_service.set(cache_key, result, ttl=current_app.config['CACHE_TTL'])
                return result
        except Exception as e:
            current_app.logger.warning(f'Pokemon API error fetching {card_id}: {e}')

    result = get_mock_card_by_id(card_id)
    if result:
        cache_service.set(cache_key, result, ttl=300)
    return result


def get_featured_cards(limit=10):
    cache_key = f'featured:{limit}'
    cached = cache_service.get(cache_key)
    if cached:
        return cached

    if _api_available():
        try:
            result = _api_featured(limit)
            cache_service.set(cache_key, result, ttl=current_app.config['CACHE_TTL'])
            return result
        except Exception as e:
            current_app.logger.warning(f'Pokemon API featured error: {e}')

    result = get_mock_cards()[:limit]
    cache_service.set(cache_key, result, ttl=300)
    return result


def sync_card_to_db(card_data: dict):
    """Upsert API card data into local DB."""
    from app import db
    from app.models.card import Card
    from app.services.pricing_service import usd_to_nzd

    card = Card.query.get(card_data.get('id'))
    prices = card_data.get('tcgplayer', {}).get('prices', {})
    p = prices.get('normal') or prices.get('holofoil') or {}

    market = p.get('market') or card_data.get('market_price')
    low = p.get('low') or card_data.get('low_price')
    high = p.get('high') or card_data.get('high_price')

    images = card_data.get('images', {})
    types = card_data.get('types', [])
    set_info = card_data.get('set', {})

    if not card:
        card = Card(id=card_data['id'])
        db.session.add(card)

    card.name = card_data.get('name', '')
    card.set_name = set_info.get('name', '') if isinstance(set_info, dict) else card_data.get('set_name', '')
    card.set_id = set_info.get('id', '') if isinstance(set_info, dict) else card_data.get('set_id', '')
    card.number = card_data.get('number', '')
    card.rarity = card_data.get('rarity', '')
    card.types = ','.join(types) if isinstance(types, list) else types
    card.supertype = card_data.get('supertype', '')
    card.subtypes = ','.join(card_data.get('subtypes', [])) if isinstance(card_data.get('subtypes'), list) else ''
    card.hp = card_data.get('hp', '')
    card.image_url = images.get('small', '') if isinstance(images, dict) else card_data.get('image_url', '')
    card.image_url_hi = images.get('large', '') if isinstance(images, dict) else card_data.get('image_url_hi', '')
    card.market_price = usd_to_nzd(market) if market else None
    card.low_price = usd_to_nzd(low) if low else None
    card.high_price = usd_to_nzd(high) if high else None

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()


def _api_search(query, set_name, rarity, page, page_size):
    q_parts = []
    if query:
        q_parts.append(f'name:"{query}*"')
    if set_name:
        q_parts.append(f'set.name:"{set_name}"')
    if rarity:
        q_parts.append(f'rarity:"{rarity}"')
    if not q_parts:
        q_parts.append('supertype:Pokémon')

    params = {'q': ' '.join(q_parts), 'pageSize': page_size, 'page': page}
    resp = requests.get(f'{BASE_URL}/cards', headers=_headers(), params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    cards = data.get('data', [])
    for c in cards:
        try:
            sync_card_to_db(c)
        except Exception:
            pass
    return {'cards': cards, 'total': data.get('totalCount', len(cards)), 'source': 'api'}


def _api_get_card(card_id):
    resp = requests.get(f'{BASE_URL}/cards/{card_id}', headers=_headers(), timeout=TIMEOUT)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    data = resp.json().get('data')
    if data:
        try:
            sync_card_to_db(data)
        except Exception:
            pass
    return data


def _api_featured(limit):
    params = {'q': 'rarity:"Special Illustration Rare"', 'pageSize': limit}
    resp = requests.get(f'{BASE_URL}/cards', headers=_headers(), params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json().get('data', [])
