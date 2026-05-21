# BhrisTCG Marketplace

New Zealand's dedicated Pokémon TCG marketplace — built for the 203 Cross-Platform Development assessment.

**Authors:** Brix Munsayac (270464698) 

---

## What It Does

BhrisTCG solves the gaps in eBay, TCGPlayer, and Facebook Marketplace for NZ Pokémon TCG traders:

- Browse and search card listings with condition/set/rarity filters
- Create and manage your own card listings
- Condition-adjusted price suggestions (market price × condition multiplier, in NZD)
- Personal collection tracking with estimated value
- Real-time buyer/seller chat via Flask-SocketIO
- Seller ratings and reviews
- Report system for fraud/misrepresentation

---

## Backend Tech Stack

| Component         | Technology                     |
|-------------------|-------------------------------|
| Framework         | Flask 3.0 (Python)            |
| ORM               | SQLAlchemy 2.0 + Flask-SQLAlchemy |
| Migrations        | Flask-Migrate (Alembic)       |
| Database          | SQLite (required)         |
| Authentication    | Flask-Login + Werkzeug hashing |
| Forms/Validation  | Flask-WTF + WTForms           |
| Real-time         | Flask-SocketIO + eventlet     |
| HTTP API          | Pokémon TCG API (optional)    |
| Architecture      | MVC + Service Layer           |

---

