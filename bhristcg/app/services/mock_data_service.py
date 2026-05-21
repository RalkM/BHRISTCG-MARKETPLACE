#The mock data 
"""Mock card data and database seeding. Used when no API key is set or API is unavailable."""

MOCK_CARDS = [
    {
        'id': 'sv3pt5-201', 'name': 'Charizard ex', 'set_name': '151',
        'set_id': 'sv3pt5', 'number': '201', 'rarity': 'Special Illustration Rare',
        'types': 'Fire', 'supertype': 'Pokémon', 'subtypes': 'Basic,ex', 'hp': '330',
        'image_url': 'https://images.pokemontcg.io/sv3pt5/201.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv3pt5/201_hires.png',
        'market_price': 85.0, 'low_price': 65.0, 'high_price': 120.0, 'game': 'pokemon',
    },
    {
        'id': 'sv4-197', 'name': 'Umbreon ex', 'set_name': 'Paradox Rift',
        'set_id': 'sv4', 'number': '197', 'rarity': 'Special Illustration Rare',
        'types': 'Darkness', 'supertype': 'Pokémon', 'subtypes': 'Basic,ex', 'hp': '310',
        'image_url': 'https://images.pokemontcg.io/sv4/197.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv4/197_hires.png',
        'market_price': 55.0, 'low_price': 42.0, 'high_price': 75.0, 'game': 'pokemon',
    },
    {
        'id': 'sv6-180', 'name': 'Pikachu ex', 'set_name': 'Twilight Masquerade',
        'set_id': 'sv6', 'number': '180', 'rarity': 'Special Illustration Rare',
        'types': 'Lightning', 'supertype': 'Pokémon', 'subtypes': 'Basic,ex', 'hp': '240',
        'image_url': 'https://images.pokemontcg.io/sv6/180.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv6/180_hires.png',
        'market_price': 38.0, 'low_price': 28.0, 'high_price': 55.0, 'game': 'pokemon',
    },
    {
        'id': 'sv2-193', 'name': 'Gardevoir ex', 'set_name': 'Paldea Evolved',
        'set_id': 'sv2', 'number': '193', 'rarity': 'Special Illustration Rare',
        'types': 'Psychic', 'supertype': 'Pokémon', 'subtypes': 'Stage 2,ex', 'hp': '310',
        'image_url': 'https://images.pokemontcg.io/sv2/193.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv2/193_hires.png',
        'market_price': 28.0, 'low_price': 20.0, 'high_price': 42.0, 'game': 'pokemon',
    },
    {
        'id': 'sv4-182', 'name': 'Roaring Moon ex', 'set_name': 'Paradox Rift',
        'set_id': 'sv4', 'number': '182', 'rarity': 'Special Illustration Rare',
        'types': 'Darkness', 'supertype': 'Pokémon', 'subtypes': 'Basic,ex', 'hp': '230',
        'image_url': 'https://images.pokemontcg.io/sv4/182.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv4/182_hires.png',
        'market_price': 32.0, 'low_price': 22.0, 'high_price': 48.0, 'game': 'pokemon',
    },
    {
        'id': 'sv3pt5-6', 'name': 'Charizard', 'set_name': '151',
        'set_id': 'sv3pt5', 'number': '6', 'rarity': 'Rare Holo',
        'types': 'Fire', 'supertype': 'Pokémon', 'subtypes': 'Stage 2', 'hp': '170',
        'image_url': 'https://images.pokemontcg.io/sv3pt5/6.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv3pt5/6_hires.png',
        'market_price': 7.5, 'low_price': 5.0, 'high_price': 12.0, 'game': 'pokemon',
    },
    {
        'id': 'sv1-198', 'name': 'Miraidon ex', 'set_name': 'Scarlet & Violet',
        'set_id': 'sv1', 'number': '198', 'rarity': 'Special Illustration Rare',
        'types': 'Lightning', 'supertype': 'Pokémon', 'subtypes': 'Basic,ex', 'hp': '220',
        'image_url': 'https://images.pokemontcg.io/sv1/198.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv1/198_hires.png',
        'market_price': 22.0, 'low_price': 15.0, 'high_price': 35.0, 'game': 'pokemon',
    },
    {
        'id': 'sv1-197', 'name': 'Koraidon ex', 'set_name': 'Scarlet & Violet',
        'set_id': 'sv1', 'number': '197', 'rarity': 'Special Illustration Rare',
        'types': 'Fighting', 'supertype': 'Pokémon', 'subtypes': 'Basic,ex', 'hp': '230',
        'image_url': 'https://images.pokemontcg.io/sv1/197.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv1/197_hires.png',
        'market_price': 20.0, 'low_price': 14.0, 'high_price': 30.0, 'game': 'pokemon',
    },
    {
        'id': 'sv5-191', 'name': 'Terapagos ex', 'set_name': 'Temporal Forces',
        'set_id': 'sv5', 'number': '191', 'rarity': 'Special Illustration Rare',
        'types': 'Normal', 'supertype': 'Pokémon', 'subtypes': 'Basic,ex', 'hp': '330',
        'image_url': 'https://images.pokemontcg.io/sv5/191.png',
        'image_url_hi': 'https://images.pokemontcg.io/sv5/191_hires.png',
        'market_price': 42.0, 'low_price': 30.0, 'high_price': 60.0, 'game': 'pokemon',
    },
    {
        'id': 'swsh12pt5-GG47', 'name': 'Lugia V', 'set_name': 'Crown Zenith',
        'set_id': 'swsh12pt5', 'number': 'GG47', 'rarity': 'Ultra Rare',
        'types': 'Colorless', 'supertype': 'Pokémon', 'subtypes': 'Basic,V', 'hp': '220',
        'image_url': 'https://images.pokemontcg.io/swsh12pt5/GG47.png',
        'image_url_hi': 'https://images.pokemontcg.io/swsh12pt5/GG47_hires.png',
        'market_price': 15.0, 'low_price': 10.0, 'high_price': 25.0, 'game': 'pokemon',
    },
]

MOCK_SETS = ['151', 'Paradox Rift', 'Temporal Forces', 'Twilight Masquerade',
             'Paldea Evolved', 'Crown Zenith', 'Scarlet & Violet']

MOCK_RARITIES = ['Common', 'Uncommon', 'Rare', 'Rare Holo', 'Double Rare',
                 'Ultra Rare', 'Special Illustration Rare', 'Hyper Rare']

MOCK_FINISHES = ['Non-Holo', 'Holo', 'Reverse Holo', 'Foil', 'SIR', 'Alt Art']


def get_mock_cards():
    return MOCK_CARDS


def get_mock_card_by_id(card_id: str):
    return next((c for c in MOCK_CARDS if c['id'] == card_id), None)


def search_mock_cards(query='', set_name='', rarity='', game=''):
    results = MOCK_CARDS
    if query:
        q = query.lower()
        results = [c for c in results if q in c['name'].lower()]
    if set_name:
        results = [c for c in results if c['set_name'] == set_name]
    if rarity:
        results = [c for c in results if c['rarity'] == rarity]
    if game:
        results = [c for c in results if c.get('game') == game]
    return results


def seed_if_empty():
    from app.models.card import Card
    from app.models.user import User
    from app.models.listing import Listing
    from app.models.collection import Collection, CollectionItem
    from app import db

    if Card.query.count() > 0:
        return

    # Seed cards
    for d in MOCK_CARDS:
        card = Card(
            id=d['id'], name=d['name'], set_name=d['set_name'],
            set_id=d.get('set_id'), number=d.get('number'),
            rarity=d.get('rarity'), types=d.get('types'),
            supertype=d.get('supertype'), subtypes=d.get('subtypes'),
            hp=d.get('hp'), image_url=d.get('image_url'),
            image_url_hi=d.get('image_url_hi'),
            market_price=d.get('market_price'), low_price=d.get('low_price'),
            high_price=d.get('high_price'), game=d.get('game', 'pokemon'),
        )
        db.session.add(card)

    # Seed demo users
    users_data = [
        {'username': 'User_21231', 'email': 'user21231@bhristcg.nz', 'password': 'demo1234',
         'store_name': "User_21231's Store"},
        {'username': 'sarah_j', 'email': 'sarah@bhristcg.nz', 'password': 'demo1234',
         'store_name': "Sarah's Card Shop"},
        {'username': 'alex_t', 'email': 'alex@bhristcg.nz', 'password': 'demo1234',
         'store_name': "Alex's TCG Store"},
    ]
    users = []
    for ud in users_data:
        u = User(username=ud['username'], email=ud['email'],
                 store_name=ud.get('store_name'))
        u.set_password(ud['password'])
        db.session.add(u)
        users.append(u)
    db.session.flush()

    # Seed listings
    listings_seed = [
        ('sv3pt5-201', users[1], 189.90, 'near_mint', 'sir', 'Pack fresh, sleeved immediately.'),
        ('sv4-197', users[1], 339.90, 'near_mint', 'holo', 'Beautiful card, top condition.'),
        ('sv6-180', users[2], 420.0, 'near_mint', 'sir', 'Mint condition, shipped with toploader.'),
        ('sv2-193', users[1], 500.0, 'mint', 'sir', 'Pulled from sealed box.'),
        ('sv4-182', users[2], 639.80, 'near_mint', 'holo', 'Great card, fast shipping.'),
        ('sv3pt5-6', users[0], 75.0, 'light_played', 'holo', 'Minor edge wear only.'),
        ('sv1-198', users[0], 125.0, 'near_mint', 'sir', 'Fresh from pack.'),
        ('sv1-197', users[2], 98.0, 'near_mint', 'sir', 'Stored in binder, excellent.'),
        ('sv5-191', users[1], 210.0, 'mint', 'sir', 'Sealed condition.'),
        ('swsh12pt5-GG47', users[0], 55.0, 'near_mint', 'holo', 'Great Gengar card.'),
    ]
    for card_id, seller, price, cond, finish, notes in listings_seed:
        l = Listing(card_id=card_id, seller_id=seller.id, price=price,
                    condition=cond, finish=finish, notes=notes,
                    status='active', delivery_type='both', shipping_cost=10.0)
        db.session.add(l)

    # Seed collections for User_21231
    db.session.flush()
    coll1 = Collection(owner_id=users[0].id, name='My First Collection',
                       total_cards_needed=9,
                       cover_image='https://images.pokemontcg.io/sv3pt5/201.png')
    coll2 = Collection(owner_id=users[0].id, name='My Second Collection',
                       total_cards_needed=50,
                       cover_image='https://images.pokemontcg.io/sv4/197.png')
    db.session.add(coll1)
    db.session.add(coll2)
    db.session.flush()

    collection_items = [
        (users[0].id, coll1.id, 'sv3pt5-201', 'near_mint', 1, 85.0),
        (users[0].id, coll1.id, 'sv6-180', 'near_mint', 1, 38.0),
        (users[0].id, coll2.id, 'sv4-197', 'near_mint', 2, 55.0),
        (users[0].id, coll2.id, 'sv2-193', 'near_mint', 1, 28.0),
    ]
    for owner_id, coll_id, card_id, cond, qty, pprice in collection_items:
        ci = CollectionItem(owner_id=owner_id, collection_id=coll_id,
                            card_id=card_id, condition=cond,
                            quantity=qty, purchase_price=pprice)
        db.session.add(ci)

    db.session.commit()
