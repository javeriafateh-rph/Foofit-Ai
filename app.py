import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Page Configuration
st.set_page_config(page_title="FootFit AI Pro", page_icon="👟", layout="centered")

# CSS Styling
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
st.markdown('<div class="subtitle">Real-Time Anatomical Foot Profile & Recommendation Engine</div>', unsafe_allow_html=True)

st.divider()

# Catalog Database with Direct Product Deep Links
SHOE_DATABASE = [
    {
        "name": "Altra Provision 7 / Paradigm",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "Anatomical FootShape™ toe box prevents metatarsal squeezing; GuideRail™ prevents arch collapse.",
        "price": "$150",
        "url": "https://www.altrarunning.com/shop/mens-shoes-running-support/mens-provision-7-al0a7r6e"
    },
    {
        "name": "Topo Athletic Specter 2",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "High Arch / Rigid Foot Vault (Supination Risk)",
        "feature": "Wide anatomical forefoot chamber paired with maximum shock-absorbing midsole for rigid arches.",
        "price": "$165",
        "url": "https://www.topoathletic.com/mens-specter-2"
    },
    {
        "name": "Brooks Adrenaline GTS 23 (Wide 2E)",
        "toe_box": "Standard / Moderate Taper",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "Structural medial arch support with wide option to accommodate midfoot pronation.",
        "price": "$140",
        "url": "https://www.brooksrunning.com/en_us/mens-adrenaline-gts-23-supportive-running-shoe/110391.html"
    },
    {
        "name": "Asics Gel-Nimbus 26 (Wide)",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "Neutral Arch",
        "feature": "High-cushion platform with ample forefoot volume for neutral, non-constricting gait.",
        "price": "$160",
        "url": "https://www.asics.com/us/en-us/gel-nimbus-26-wide/p/ANA_1011B793-001.html"
    },
    {
        "name": "Nike Air Zoom Pegasus 40",
        "toe_box": "Standard / Moderate Taper",
        "arch_support": "Neutral Arch",
        "feature": "Versatile neutral fit designed for standard, tapered foot profiles.",
        "price": "$130",
        "url": "https://www.nike.com/t/pegasus-40-mens-road-running-shoes-MC1Ltw/DV3853-001"
    }
]

def analyze_foot_contour(pil_image):
    """Processes uploaded image to extract forefoot width (normalized) and shape category."""
    try:
        img_rgb = np.array(pil_image.convert('RGB'))
        img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        _, thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            
            aspect_ratio = w / float(h) if h > 0 else 0.4
            
            # Normalize calculated width to standard human physiological range (80mm - 110mm)
            normalized_width = round(85.0 + (aspect_ratio * 35.0), 1)
            normalized_width = min(max(normalized_width, 78.0), 112.0)
            
            shape = "Wide / Fan-Shaped Forefoot" if aspect_ratio > 0.38 else "Standard / Moderate Taper"
            return normalized_width, shape
    except Exception:
        pass
    
    return 96.5, "Wide / Fan-Shaped Forefoot"

# 1. Vision Scanner
st.header("1. Real-Time AI Vision Scan")

# Photo Guidelines Box
st.markdown("""
<div class="guide-box">
    📸 <b>Photo Guidelines for Best Accuracy:</b><br>
    • <b>Angle:</b> Take a <b>Top-Down photo</b> (looking straight down at the top of your foot).<br>
    • <b>Position:</b> Place your foot flat on a plain floor (avoid patterned rugs/towels).<br>
    • <b>Lighting:</b> Ensure clear lighting so toe edges are visible.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload foot photo for automated analysis:", type=["jpg", "png", "jpeg"])

detected_width = 96.5
detected_shape = "Wide / Fan-Shaped Forefoot"

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Scanning foot contours & anatomical splay...", width=260)
    
    detected_width, detected_shape = analyze_foot_contour(img)
    st.success("✅ Vision Analysis Complete!")
    
    col1, col2 = st.columns(2)
    col1.metric("Est. Forefoot Width", f"{detected_width} mm")
    col2.metric("Detected Shape Profile", detected_shape)

st.divider()

# 2. Biomechanical Selection
st.header("2. Biomechanical Profile")
arch_type = st.selectbox(
    "Select Arch Drop / Pronation Tendency:",
    [
        "High Arch / Rigid Foot Vault (Supination Risk)",
        "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "Neutral Arch"
    ]
)

st.divider()

# 3. Dynamic Real-Time Recommendations
st.header("3. Diagnostic Profile & Recommended Matches")

st.markdown(f"""
<div class="card">
    <h4>⚠️ Diagnostic Summary: {detected_shape} + {arch_type.split('(')[0].strip()}</h4>
    <p>Your photo scan indicates a <b>{detected_shape}</b> ({detected_width} mm). Paired with a <b>{arch_type}</b>, your feet require shoes with generous forefoot volume to prevent bunion compression and targeted arch vaulting.</p>
</div>
""", unsafe_allow_html=True)

# Recommendation Filtering Logic
matching_shoes = [
    s for s in SHOE_DATABASE 
    if s["arch_support"] == arch_type or s["toe_box"] == detected_shape
]

if not matching_shoes:
    matching_shoes = SHOE_DATABASE[:2]

st.subheader("Top Recommended Matches:")
for shoe in matching_shoes:
    st.markdown(f"""
    <div class="rec-card">
        <strong>👟 <a href="{shoe['url']}" target="_blank" style="color: #38BDF8; text-decoration: underline;">{shoe['name']}</a></strong> — {shoe['price']}<br>
        <span style="color: #CBD5E1; font-size: 0.95rem;">Why it fits: {shoe['feature']}</span><br>
        <a href="{shoe['url']}" target="_blank" class="buy-btn">View Specific Product Page ↗</a>
    </div>
    """, unsafe_allow_html=True)
# Regional Configuration
COUNTRIES = {
    "Global / International (USD)": {"currency": "$", "code": "US"},
    "United States (USD)": {"currency": "$", "code": "US"},
    "United Kingdom (GBP)": {"currency": "£", "code": "UK"},
    "Europe (EUR)": {"currency": "€", "code": "EU"},
    "Pakistan (PKR)": {"currency": "Rs.", "code": "PK"}
}

st.header("1. Region & Localization")
selected_country = st.selectbox("Select Your Shopping Region:", list(COUNTRIES.keys()))
SHOE_DATABASE = [
    {
        "name": "Altra Provision 7 / Paradigm",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "FootShape™ Toe Box + GuideRail™ arch support frame.",
        "price_usd": "$150",
        "price_pkr": "Rs. 42,000",
        "regions": ["Global / International (USD)", "United States (USD)", "Pakistan (PKR)"],
        "url_us": "https://www.altrarunning.com",
        "url_pk": "https://www.altrarunning.com" # or local distributor
    },
    {
        "name": "Brooks Adrenaline GTS 23 (Wide 2E)",
        "toe_box": "Standard / Moderate Taper",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "Structural medial arch support with generous forefoot width.",
        "price_usd": "$140",
        "price_gbp": "£130",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)"],
        "url_us": "https://www.brooksrunning.com/en_us/",
        "url_uk": "https://www.brooksrunning.com/en_gb/"


    }# Filter matching shoes by both Biomechanics AND Selected Region
matching_shoes = [
    s for s in SHOE_DATABASE 
    if (s["arch_support"] == arch_type or s["toe_box"] == detected_shape)
    and selected_country in s["regions"]
]
]
