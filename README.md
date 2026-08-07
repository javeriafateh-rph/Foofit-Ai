# FootFit AI Pro

## What changed from the original version

**Structure** — split one 228-line file into four focused ones:
- `app.py` — UI only
- `database.py` — the shoe catalog, now a real SQLite database
- `vision.py` — foot photo analysis
- `styles.py` — CSS

This matters mainly for *you and future AI-assisted edits*: when something breaks or you want to change one piece (say, add a new region), the AI helping you only needs to look at one small, relevant file instead of untangling everything at once.

**Catalog → real database** — `foofit.db` (SQLite) replaces the hardcoded Python list. It supports:
- Filtering by exact shape + arch match (the recommendation engine)
- Free-text search + price filtering (new "Browse Catalog" tab)
- Adding shoes via `database.add_shoe(...)` without touching `app.py`

**Accurate measurement (calibrated)** — the old version invented a width in millimeters from a made-up formula. Now:
- If you place a standard ID/credit/debit card next to your foot in the photo, the app detects it and uses its known real-world size (85.6mm × 53.98mm) to convert pixels → real millimeters. This gives an actual calibrated measurement.
- If no card is detected, you can manually enter your foot length (measured with a ruler) instead.
- If neither is available, the app clearly labels the result as a **shape estimate only** — it will never silently show a fake number as if it were real. Look for the green "Calibrated measurement" badge vs. the amber "Shape estimate only" badge.

**Fixed a deployment bug** — swapped `opencv-python` for `opencv-python-headless` in requirements. The former needs system GUI libraries that often aren't installed on cloud servers and can cause deploy failures; the headless version is built for exactly this use case.

**Theming** — added `.streamlit/config.toml` so the app uses a consistent dark theme by default instead of Streamlit's default look.

## Running locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
The first run creates `foofit.db` automatically and seeds it with the original 6 shoes.

## Adding shoes to the catalog
Don't edit `app.py`. Instead, from a Python shell in the project folder:
```python
import database
database.add_shoe(
    name="New Shoe Name",
    toe_box="Wide / Fan-Shaped Forefoot",       # must exactly match existing values
    arch_support="Neutral Arch",                 # must exactly match existing values
    feature="One sentence on what makes it fit this profile.",
    price_usd="$120", price_gbp="£110", price_pkr="Rs. 34,000",
    url_us="https://...", url_uk="https://...", url_pk="https://...",
)
```
Valid `toe_box` values: `"Wide / Fan-Shaped Forefoot"`, `"Standard / Tapered Forefoot"`
Valid `arch_support` values: `"High Arch / Rigid Foot Vault (Supination Risk)"`, `"Flat Arch / Low Foot Vault (Overpronation Risk)"`, `"Neutral Arch"`

As the catalog grows past a few dozen shoes, or if you want to add a proper admin screen for editing shoes without Python, that's a natural next step — just ask.

## Deploying
Same as before — push to GitHub, deploy via Streamlit Community Cloud pointing at `app.py`. `foofit.db` will be created fresh on first run on the server (the seed data ships with the code, not the database file itself).

**Note on Streamlit Cloud + SQLite:** Streamlit Cloud's filesystem is not permanently persistent across app restarts/redeploys — any shoes you add via `add_shoe()` directly on the deployed app could be lost on redeploy. For now that's fine since the catalog is edited by you, not by end users. If you later want end users' data (like saved measurements) to persist reliably, that's the point where moving to a small hosted database (e.g. free-tier Supabase Postgres) makes sense — happy to wire that up when you're there.

## Honest limitations that remain
- Shape classification (wide vs. standard) is still a heuristic based on aspect ratio, not a trained model. It's a reasonable first pass but will misclassify some feet, especially at odd camera angles.
- Card detection can fail on cluttered backgrounds or poor lighting — the manual-length fallback exists for exactly this reason.
- This is not a medical device and shouldn't be treated as podiatric advice.
