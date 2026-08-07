"""
database.py
Handles all persistence for the FooFit AI shoe catalog.

Why SQLite:
- It's a real relational database (proper querying, filtering, indexing).
- It's a single file (foofit.db) — no server, no credentials, no extra
  infrastructure. Works out of the box on Streamlit Community Cloud.
- If the catalog outgrows a single file (multiple editors, high write volume),
  swapping this module for a hosted Postgres client (e.g. via SQLAlchemy)
  is a small, contained change — nothing in app.py has to know the difference.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent / "foofit.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS shoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    toe_box TEXT NOT NULL,       -- 'Wide / Fan-Shaped Forefoot' | 'Standard / Tapered Forefoot'
    arch_support TEXT NOT NULL,  -- 'High Arch...' | 'Flat Arch...' | 'Neutral Arch'
    feature TEXT NOT NULL,
    price_usd TEXT,
    price_gbp TEXT,
    price_pkr TEXT,
    url_us TEXT,
    url_uk TEXT,
    url_pk TEXT,
    active INTEGER NOT NULL DEFAULT 1
);
"""

# Seed data ports over the original hardcoded catalog so nothing is lost.
SEED_SHOES = [
    dict(
        name="Altra Provision 7 / Paradigm",
        toe_box="Wide / Fan-Shaped Forefoot",
        arch_support="Flat Arch / Low Foot Vault (Overpronation Risk)",
        feature="FootShape™ wide toe box paired with GuideRail™ stability for flat arch pronation control.",
        price_usd="$150", price_gbp="£135", price_pkr="Rs. 42,000",
        url_us="https://www.altrarunning.com", url_uk="https://www.altrarunning.eu", url_pk="https://www.altrarunning.com",
    ),
    dict(
        name="Topo Athletic Specter 2",
        toe_box="Wide / Fan-Shaped Forefoot",
        arch_support="High Arch / Rigid Foot Vault (Supination Risk)",
        feature="Roomy anatomical forefoot chamber with thick, high-rebound cushioning for rigid high arches.",
        price_usd="$165", price_gbp="£150", price_pkr="Rs. 46,000",
        url_us="https://www.topoathletic.com", url_uk="https://www.topoathletic.co.uk", url_pk="https://www.topoathletic.com",
    ),
    dict(
        name="Asics Gel-Nimbus 26 (Wide Edition)",
        toe_box="Wide / Fan-Shaped Forefoot",
        arch_support="Neutral Arch",
        feature="Plush maximum-cushion platform with extra forefoot volume for neutral, non-constricting gait.",
        price_usd="$160", price_gbp="£180", price_pkr="Rs. 45,000",
        url_us="https://www.asics.com", url_uk="https://www.asics.com", url_pk="https://www.asics.com",
    ),
    dict(
        name="Brooks Adrenaline GTS 23",
        toe_box="Standard / Tapered Forefoot",
        arch_support="Flat Arch / Low Foot Vault (Overpronation Risk)",
        feature="Structured medial GuideRails for flat arches in a classic, streamlined standard fit.",
        price_usd="$140", price_gbp="£130", price_pkr="Rs. 39,000",
        url_us="https://www.brooksrunning.com", url_uk="https://www.brooksrunning.com", url_pk="https://www.brooksrunning.com",
    ),
    dict(
        name="Mizuno Wave Rider 27",
        toe_box="Standard / Tapered Forefoot",
        arch_support="High Arch / Rigid Foot Vault (Supination Risk)",
        feature="Wave plate technology offers energetic shock attenuation tailored for rigid, high-arched feet.",
        price_usd="$140", price_gbp="£135", price_pkr="Rs. 38,000",
        url_us="https://www.mizunousa.com", url_uk="https://www.mizuno.com", url_pk="https://www.mizunousa.com",
    ),
    dict(
        name="Nike Air Zoom Pegasus 40",
        toe_box="Standard / Tapered Forefoot",
        arch_support="Neutral Arch",
        feature="Balanced neutral trainer built on a traditional performance contour for standard foot shapes.",
        price_usd="$130", price_gbp="£115", price_pkr="Rs. 36,000",
        url_us="https://www.nike.com", url_uk="https://www.nike.com", url_pk="https://www.nike.com",
    ),
]


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Create the table if needed and seed it the first time only."""
    with get_conn() as conn:
        conn.execute(SCHEMA)
        count = conn.execute("SELECT COUNT(*) AS c FROM shoes").fetchone()["c"]
        if count == 0:
            for s in SEED_SHOES:
                conn.execute(
                    """INSERT INTO shoes
                       (name, toe_box, arch_support, feature, price_usd, price_gbp, price_pkr, url_us, url_uk, url_pk)
                       VALUES (:name, :toe_box, :arch_support, :feature, :price_usd, :price_gbp, :price_pkr, :url_us, :url_uk, :url_pk)""",
                    s,
                )


def find_shoes(toe_box: str, arch_support: str, exact: bool = True):
    """
    Look up matching shoes.
    exact=True  -> match both toe_box AND arch_support (best match)
    exact=False -> match arch_support only (fallback when no exact combo exists)
    """
    with get_conn() as conn:
        if exact:
            rows = conn.execute(
                "SELECT * FROM shoes WHERE active = 1 AND toe_box = ? AND arch_support = ?",
                (toe_box, arch_support),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM shoes WHERE active = 1 AND arch_support = ?",
                (arch_support,),
            ).fetchall()
        return [dict(r) for r in rows]


def search_shoes(query: str = "", max_price_usd: float = None):
    """Free-text search across name/feature, optional USD price ceiling. Used by the browse/search tab."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM shoes WHERE active = 1 AND (name LIKE ? OR feature LIKE ?)",
            (f"%{query}%", f"%{query}%"),
        ).fetchall()
    results = [dict(r) for r in rows]
    if max_price_usd is not None:
        def price_num(s):
            try:
                return float(s["price_usd"].replace("$", "").replace(",", ""))
            except (ValueError, AttributeError, TypeError):
                return float("inf")
        results = [r for r in results if price_num(r) <= max_price_usd]
    return results


def add_shoe(**fields):
    """Insert a new shoe. Lets the catalog grow without editing app code."""
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO shoes
               (name, toe_box, arch_support, feature, price_usd, price_gbp, price_pkr, url_us, url_uk, url_pk)
               VALUES (:name, :toe_box, :arch_support, :feature, :price_usd, :price_gbp, :price_pkr, :url_us, :url_uk, :url_pk)""",
            fields,
        )


def all_shoes():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM shoes WHERE active = 1 ORDER BY name").fetchall()
        return [dict(r) for r in rows]
