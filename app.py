import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Page Configuration
st.set_page_config(page_title="FootFit AI Pro", page_icon="👟", layout="centered")

# Custom Styling (Dark & Light Mode Compatible)
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 0px; }
    .subtitle { font-size: 1.1rem; text-align: center; margin-bottom: 25px; opacity: 0.8; }
    .card { background-color: #1E293B; border-left: 5px solid #0EA5E9; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #FFFFFF; }
    .card h4 { color: #38BDF8 !important; margin-top: 0px; }
    .guide-box { background-color: #0F172A; border: 1px dashed #38BDF8; padding: 12px 15px; border-radius: 8px; margin-bottom: 15px; color: #CBD5E1; font-size: 0.9rem; }
    .rec-card { background-color: #0F172A; border: 1px solid #334155; padding: 16px; border-radius: 8px; margin-bottom: 12px; color: #F8FAFC; }
    .rec-card strong { font-size: 1.15rem; color: #38BDF8; }
    .buy-btn {
        display: inline-block;
        background-color: #0EA5E9;
        color: #FFFFFF !important;
        font-weight: 600;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        margin-top: 10px;
        font-size: 0.9rem;
    }
    .buy-btn:hover { background-color: #0284C7; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">👟 FootFit AI Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-Time Anatomical Foot Profile & Regional Recommendation Engine</div>', unsafe_allow_html=True)

st.divider()

# Regional Settings
COUNTRIES = {
    "Global / International (USD)": {"code": "US", "price_key": "price_usd", "url_key": "url_us"},
    "United States (USD)": {"code": "US", "price_key": "price_usd", "url_key": "url_us"},
    "United Kingdom (GBP)": {"code": "UK", "price_key": "price_gbp", "url_key": "url_uk"},
    "Pakistan (PKR)": {"code": "PK", "price_key": "price_pkr", "url_key": "url_pk"}
}

st.header("1. Localization & Region Selection")
selected_region = st.selectbox("Select Your Preferred Shopping Country:", list(COUNTRIES.keys()))
region_info = COUNTRIES[selected_region]

st.divider()

# Regional Footwear Catalog
SHOE_DATABASE = [
    {
        "name": "Altra Provision 7 / Paradigm",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "Anatomical FootShape™ toe box prevents metatarsal squeezing; GuideRail™ prevents arch collapse.",
        "price_usd": "$150",
        "price_gbp": "£135",
        "price_pkr": "Rs. 42,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)", "Pakistan (PKR)"],
        "url_us": "https://www.altrarunning.com/shop/mens-shoes-running-support/mens-provision-7-al0a7r6e",
        "url_uk": "https://www.altrarunning.eu/uk/provision-7.html",
        "url_pk": "https://www.altrarunning.com"
    },
    {
        "name": "Topo Athletic Specter 2",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "High Arch / Rigid Foot Vault (Supination Risk)",
        "feature": "Wide anatomical forefoot chamber paired with maximum shock-absorbing midsole for rigid arches.",
        "price_usd": "$165",
        "price_gbp": "£150",
        "price_pkr": "Rs. 46,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)"],
        "url_us": "https://www.topoathletic.com/mens-specter-2",
        "url_uk": "https://www.topoathletic.co.uk",
        "url_pk": "https://www.topoathletic.com"
    },
    {
        "name": "Brooks Adrenaline GTS 23 (
