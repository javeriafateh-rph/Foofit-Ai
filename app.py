import streamlit as st
from PIL import Image

import database
import vision
from styles import CSS

# ---------- Page setup ----------
st.set_page_config(page_title="FootFit AI Pro", page_icon="👟", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)
database.init_db()

st.markdown('<div class="main-title">👟 FootFit AI Pro</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Anatomical Foot Profile & Regional Shoe Recommendation Engine</div>',
    unsafe_allow_html=True,
)

# ---------- Regions ----------
COUNTRIES = {
    "Global / International (USD)": {"price_key": "price_usd", "url_key": "url_us"},
    "United States (USD)": {"price_key": "price_usd", "url_key": "url_us"},
    "United Kingdom (GBP)": {"price_key": "price_gbp", "url_key": "url_uk"},
    "Pakistan (PKR)": {"price_key": "price_pkr", "url_key": "url_pk"},
}

tab_scan, tab_browse = st.tabs(["📸 Scan & Match", "🔎 Browse Catalog"])

# =====================================================================
# TAB 1 — Guided scan-and-match flow
# =====================================================================
with tab_scan:
    st.markdown('<span class="step-badge">1</span> **Shopping Region**', unsafe_allow_html=True)
    selected_region = st.selectbox(
        "Select your preferred shopping region:",
        list(COUNTRIES.keys()),
        label_visibility="collapsed",
    )
    region_info = COUNTRIES[selected_region]

    st.divider()
    st.markdown('<span class="step-badge">2</span> **Foot Scan**', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="guide-box">
        📸 <b>For an accurate measurement:</b><br>
        • Place a standard <b>ID / credit / debit card</b> flat next to your foot in the photo — it's used as a size reference.<br>
        • Take a <b>top-down photo</b> on a plain, contrasting background.<br>
        • No card handy? You can enter your foot length manually instead.
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload foot photo:", type=["jpg", "png", "jpeg"])

    use_manual = False
    manual_length_cm = 25.0
    if uploaded_file is not None:
        with st.expander("No card in photo? Enter a known foot length instead (optional)"):
            manual_length_cm = st.number_input(
                "Foot length in cm (heel to longest toe, measured with a ruler)",
                min_value=15.0, max_value=35.0, value=25.0, step=0.1,
            )
            use_manual = st.checkbox("Use this manual length instead of card detection")

    detected_width = None
    detected_length = None
    detected_shape = "Standard / Tapered Forefoot"
    calibrated = False

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Analyzing foot contours...", width=260)

        if use_manual:
            px_per_mm = None
            known_len = manual_length_cm * 10  # cm -> mm
        else:
            px_per_mm = vision.detect_reference_card(img)
            known_len = None

        result = vision.analyze_foot_contour(img, px_per_mm=px_per_mm, known_length_mm=known_len)
        detected_width = result["width_mm"]
        detected_length = result["length_mm"]
        detected_shape = result["shape"]
        calibrated = result["calibrated"]

        if calibrated:
            st.success("✅ Analysis complete — measurement calibrated.")
            badge = '<span class="accuracy-badge accuracy-calibrated">📏 Calibrated measurement</span>'
        else:
            st.warning("⚠️ No reference card detected and no manual length given — showing shape only, not a real measurement.")
            badge = '<span class="accuracy-badge accuracy-estimate">🔍 Shape estimate only</span>'

        st.markdown(badge, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Forefoot Width", f"{detected_width} mm" if detected_width else "—")
        c2.metric("Foot Length", f"{detected_length} mm" if detected_length else "—")
        approx_size = vision.mm_to_us_shoe_size(detected_length) if detected_length else None
        c3.metric("Est. US Size", f"{approx_size}" if approx_size else "—")
        st.caption(f"Detected shape profile: **{detected_shape}**")

    st.divider()
    st.markdown('<span class="step-badge">3</span> **Biomechanical Profile**', unsafe_allow_html=True)
    arch_type = st.selectbox(
        "Select your arch type / pronation tendency:",
        [
            "High Arch / Rigid Foot Vault (Supination Risk)",
            "Flat Arch / Low Foot Vault (Overpronation Risk)",
            "Neutral Arch",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown('<span class="step-badge">4</span> **Recommended Matches**', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="card">
        <h4>⚠️ Diagnostic Profile: {detected_shape} + {arch_type.split('(')[0].strip()}</h4>
        <p>Targeting shoes engineered for a <b>{detected_shape}</b> paired with <b>{arch_type}</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    matching_shoes = database.find_shoes(detected_shape, arch_type, exact=True)
    if not matching_shoes:
        matching_shoes = database.find_shoes(detected_shape, arch_type, exact=False)
    matching_shoes = [s for s in matching_shoes if selected_region in COUNTRIES]  # region always valid; kept for clarity

    if not matching_shoes:
        st.info("No matches found yet for this exact profile — try Browse Catalog to explore all shoes.")
    else:
        for shoe in matching_shoes:
            price = shoe.get(region_info["price_key"]) or shoe["price_usd"]
            product_url = shoe.get(region_info["url_key"]) or shoe["url_us"]
            st.markdown(
                f"""
                <div class="rec-card">
                <strong>👟 <a href="{product_url}" target="_blank" style="color:#38BDF8;text-decoration:underline;">{shoe['name']}</a></strong> — {price}<br>
                <span style="color:#CBD5E1;font-size:0.95rem;"><b>Anatomical Match:</b> {shoe['toe_box']} | {shoe['arch_support'].split('(')[0]}</span><br>
                <span style="color:#CBD5E1;font-size:0.90rem;"><b>Biomechanical Feature:</b> {shoe['feature']}</span><br>
                <a href="{product_url}" target="_blank" class="buy-btn">View Product Details ↗</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

# =====================================================================
# TAB 2 — Browse / search the full catalog
# =====================================================================
with tab_browse:
    st.subheader("Search the full catalog")
    col_a, col_b = st.columns([2, 1])
    with col_a:
        query = st.text_input("Search by name or feature", placeholder="e.g. 'wide' or 'cushion'")
    with col_b:
        max_price = st.number_input("Max price (USD)", min_value=0, value=0, step=10, help="0 = no limit")

    results = database.search_shoes(query, max_price_usd=max_price if max_price > 0 else None)
    st.caption(f"{len(results)} shoe(s) found")
    for shoe in results:
        st.markdown(
            f"""
            <div class="rec-card">
            <strong>👟 <a href="{shoe['url_us']}" target="_blank" style="color:#38BDF8;text-decoration:underline;">{shoe['name']}</a></strong> — {shoe['price_usd']}<br>
            <span style="color:#CBD5E1;font-size:0.95rem;">{shoe['toe_box']} | {shoe['arch_support'].split('(')[0]}</span><br>
            <span style="color:#CBD5E1;font-size:0.90rem;">{shoe['feature']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
