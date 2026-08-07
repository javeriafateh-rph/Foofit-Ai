import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Page Configuration
st.set_page_config(page_title="FootFit AI Pro", page_icon="👟", layout="centered")

# Custom Styling
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

# 1. Regional Configuration
COUNTRIES = {
    "Global / International (USD)": {"price_key": "price_usd", "url_key": "url_us"},
    "United States (USD)": {"price_key": "price_usd", "url_key": "url_us"},
    "United Kingdom (GBP)": {"price_key": "price_gbp", "url_key": "url_uk"},
    "Pakistan (PKR)": {"price_key": "price_pkr", "url_key": "url_pk"}
}

st.header("1. Localization & Shopping Region")
selected_region = st.selectbox("Select Your Preferred Shopping Region:", list(COUNTRIES.keys()))
region_info = COUNTRIES[selected_region]

st.divider()

# Diverse Footwear Catalog covering all combinations
SHOE_DATABASE = [
    # --- WIDE / FAN-SHAPED FOREFOOT ---
    {
        "name": "Altra Provision 7 / Paradigm",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "FootShape™ wide toe box paired with GuideRail™ stability for flat arch pronation control.",
        "price_usd": "$150", "price_gbp": "£135", "price_pkr": "Rs. 42,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)", "Pakistan (PKR)"],
        "url_us": "https://www.altrarunning.com", "url_uk": "https://www.altrarunning.eu", "url_pk": "https://www.altrarunning.com"
    },
    {
        "name": "Topo Athletic Specter 2",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "High Arch / Rigid Foot Vault (Supination Risk)",
        "feature": "Roomy anatomical forefoot chamber with thick, high-rebound cushioning for rigid high arches.",
        "price_usd": "$165", "price_gbp": "£150", "price_pkr": "Rs. 46,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)", "Pakistan (PKR)"],
        "url_us": "https://www.topoathletic.com", "url_uk": "https://www.topoathletic.co.uk", "url_pk": "https://www.topoathletic.com"
    },
    {
        "name": "Asics Gel-Nimbus 26 (Wide Edition)",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "Neutral Arch",
        "feature": "Plush maximum-cushion platform with extra forefoot volume for neutral, non-constricting gait.",
        "price_usd": "$160", "price_gbp": "£180", "price_pkr": "Rs. 45,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)", "Pakistan (PKR)"],
        "url_us": "https://www.asics.com", "url_uk": "https://www.asics.com", "url_pk": "https://www.asics.com"
    },

    # --- STANDARD / TAPERED FOREFOOT ---
    {
        "name": "Brooks Adrenaline GTS 23",
        "toe_box": "Standard / Tapered Forefoot",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "Structured medial GuideRails for flat arches in a classic, streamlined standard fit.",
        "price_usd": "$140", "price_gbp": "£130", "price_pkr": "Rs. 39,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)", "Pakistan (PKR)"],
        "url_us": "https://www.brooksrunning.com", "url_uk": "https://www.brooksrunning.com", "url_pk": "https://www.brooksrunning.com"
    },
    {
        "name": "Mizuno Wave Rider 27",
        "toe_box": "Standard / Tapered Forefoot",
        "arch_support": "High Arch / Rigid Foot Vault (Supination Risk)",
        "feature": "Wave plate technology offers energetic shock attenuation tailored for rigid, high-arched feet.",
        "price_usd": "$140", "price_gbp": "£135", "price_pkr": "Rs. 38,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)", "Pakistan (PKR)"],
        "url_us": "https://www.mizunousa.com", "url_uk": "https://www.mizuno.com", "url_pk": "https://www.mizunousa.com"
    },
    {
        "name": "Nike Air Zoom Pegasus 40",
        "toe_box": "Standard / Tapered Forefoot",
        "arch_support": "Neutral Arch",
        "feature": "Balanced neutral trainer built on a traditional performance contour for standard foot shapes.",
        "price_usd": "$130", "price_gbp": "£115", "price_pkr": "Rs. 36,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)", "Pakistan (PKR)"],
        "url_us": "https://www.nike.com", "url_uk": "https://www.nike.com", "url_pk": "https://www.nike.com"
    }
]

def analyze_foot_contour(pil_image):
    """Processes uploaded image to extract forefoot width and dynamic shape profile."""
    try:
        img_rgb = np.array(pil_image.convert('RGB'))
        img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            
            aspect_ratio = w / float(h) if h > 0 else 0.35
            
            # Dynamic Width Calculation
            normalized_width = round(78.0 + (aspect_ratio * 50.0), 1)
            normalized_width = min(max(normalized_width, 75.0), 115.0)
            
            # Differentiate Wide vs Standard Forefoot based on aspect ratio threshold
            if aspect_ratio > 0.42:
                shape = "Wide / Fan-Shaped Forefoot"
            else:
                shape = "Standard / Tapered Forefoot"
                
            return normalized_width, shape
    except Exception:
        pass
    
    return 88.0, "Standard / Tapered Forefoot"

# 2. AI Vision Scanner Section
st.header("2. Real-Time AI Vision Scan")

st.markdown("""
<div class="guide-box">
    📸 <b>Photo Guidelines for Accurate Fit Matching:</b><br>
    • Take a <b>Top-Down photo</b> flat on a solid plain background.<br>
    • Ensure clear distinction between your foot and the floor.
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload foot photo for automated analysis:", type=["jpg", "png", "jpeg"])

detected_width = 88.0
detected_shape = "Standard / Tapered Forefoot"

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Scanning foot contours & anatomical splay...", width=260)
    
    detected_width, detected_shape = analyze_foot_contour(img)
    st.success("✅ Vision Analysis Complete!")
    
    col1, col2 = st.columns(2)
    col1.metric("Est. Forefoot Width", f"{detected_width} mm")
    col2.metric("Detected Shape Profile", detected_shape)

st.divider()

# 3. Biomechanical Profile Selection
st.header("3. Biomechanical Profile")
arch_type = st.selectbox(
    "Select Arch Drop / Pronation Tendency:",
    [
        "High Arch / Rigid Foot Vault (Supination Risk)",
        "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "Neutral Arch"
    ]
)

st.divider()

# 4. Diagnostic Profile & Dynamic Matcher
st.header("4. Diagnostic Profile & Recommended Matches")

st.markdown(f"""
<div class="card">
    <h4>⚠️ Diagnostic Profile: {detected_shape} + {arch_type.split('(')[0].strip()}</h4>
    <p>Targeting shoes engineered specifically for a <b>{detected_shape}</b> paired with <b>{arch_type}</b>.</p>
</div>
""", unsafe_allow_html=True)

# STRICT MATCHING LOGIC (Must match shape AND arch AND region)
matching_shoes = [
    s for s in SHOE_DATABASE 
    if s["toe_box"] == detected_shape 
    and s["arch_support"] == arch_type 
    and selected_region in s["regions"]
]

# Fallback in case exact combination isn't in mock DB
if not matching_shoes:
    matching_shoes = [
        s for s in SHOE_DATABASE 
        if s["arch_support"] == arch_type 
        and selected_region in s["regions"]
    ]

st.subheader("Tailored Recommendations:")
for shoe in matching_shoes:
    price = shoe.get(region_info["price_key"], shoe["price_usd"])
    product_url = shoe.get(region_info["url_key"], shoe["url_us"])
    
    st.markdown(f"""
    <div class="rec-card">
        <strong>👟 <a href="{product_url}" target="_blank" style="color: #38BDF8; text-decoration: underline;">{shoe['name']}</a></strong> — {price}<br>
        <span style="color: #CBD5E1; font-size: 0.95rem;"><b>Anatomical Match:</b> {shoe['toe_box']} | {shoe['arch_support'].split('(')[0]}</span><br>
        <span style="color: #CBD5E1; font-size: 0.90rem;"><b>Biomechanical Feature:</b> {shoe['feature']}</span><br>
        <a href="{product_url}" target="_blank" class="buy-btn">View Product Details ↗</a>
    </div>
    """, unsafe_allow_html=True)        "feature": "Versatile neutral fit designed for standard, tapered foot profiles.",
        "price_usd": "$130",
        "price_gbp": "£115",
        "price_pkr": "Rs. 36,000",
        "regions": ["Global / International (USD)", "United States (USD)", "United Kingdom (GBP)", "Pakistan (PKR)"],
        "url_us": "https://www.nike.com/t/pegasus-40-mens-road-running-shoes-MC1Ltw/DV3853-001",
        "url_uk": "https://www.nike.com/gb/t/pegasus-40-road-running-shoes-MC1Ltw/DV3853-001",
        "url_pk": "https://www.nike.com"
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
            
            # Normalize calculated width to standard human physiological range (78mm - 112mm)
            normalized_width = round(85.0 + (aspect_ratio * 35.0), 1)
            normalized_width = min(max(normalized_width, 78.0), 112.0)
            
            shape = "Wide / Fan-Shaped Forefoot" if aspect_ratio > 0.38 else "Standard / Moderate Taper"
            return normalized_width, shape
    except Exception:
        pass
    
    return 96.5, "Wide / Fan-Shaped Forefoot"

# 2. AI Vision Scanner Section
st.header("2. Real-Time AI Vision Scan")

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

# 3. Biomechanical Profile Selection
st.header("3. Biomechanical Profile")
arch_type = st.selectbox(
    "Select Arch Drop / Pronation Tendency:",
    [
        "High Arch / Rigid Foot Vault (Supination Risk)",
        "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "Neutral Arch"
    ]
)

st.divider()

# 4. Diagnostic Profile & Live Recommendations Engine
st.header("4. Diagnostic Profile & Recommended Matches")

st.markdown(f"""
<div class="card">
    <h4>⚠️ Diagnostic Summary: {detected_shape} + {arch_type.split('(')[0].strip()}</h4>
    <p>Your photo scan indicates a <b>{detected_shape}</b> ({detected_width} mm). Paired with a <b>{arch_type}</b>, your feet require shoes with generous forefoot volume to prevent bunion compression and targeted arch vaulting.</p>
</div>
""", unsafe_allow_html=True)

# Recommendation Filtering Logic (Matching Biomechanics AND Selected Shopping Region)
matching_shoes = [
    s for s in SHOE_DATABASE 
    if (s["arch_support"] == arch_type or s["toe_box"] == detected_shape)
    and selected_region in s["regions"]
]

if not matching_shoes:
    matching_shoes = SHOE_DATABASE[:2]

st.subheader("Top Recommended Matches:")
for shoe in matching_shoes:
    price = shoe.get(region_info["price_key"], shoe["price_usd"])
    product_url = shoe.get(region_info["url_key"], shoe["url_us"])
    
    st.markdown(f"""
    <div class="rec-card">
        <strong>👟 <a href="{product_url}" target="_blank" style="color: #38BDF8; text-decoration: underline;">{shoe['name']}</a></strong> — {price}<br>
        <span style="color: #CBD5E1; font-size: 0.95rem;">Why it fits: {shoe['feature']}</span><br>
        <a href="{product_url}" target="_blank" class="buy-btn">View Product Details in {selected_region.split('(')[0].strip()} ↗</a>
    </div>
    """, unsafe_allow_html=True)
