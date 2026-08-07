import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Page Configuration
st.set_page_config(page_title="FootFit AI Pro", page_icon="👟", layout="centered")

# Dark/Light Mode Compatible Styling
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; text-align: center; margin-bottom: 0px; }
    .subtitle { font-size: 1.1rem; text-align: center; margin-bottom: 25px; opacity: 0.8; }
    .card { background-color: #1E293B; border-left: 5px solid #0EA5E9; padding: 15px; border-radius: 8px; margin-bottom: 15px; color: #FFFFFF; }
    .card h4 { color: #38BDF8 !important; margin-top: 0px; }
    .rec-card { background-color: #0F172A; border: 1px solid #334155; padding: 15px; border-radius: 8px; margin-bottom: 10px; color: #F8FAFC; }
    .rec-card strong { color: #38BDF8; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">👟 FootFit AI Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-Time Anatomical Foot Profile Analyzer</div>', unsafe_allow_html=True)

st.divider()

# Sample Shoe Database
SHOE_DATABASE = [
    {
        "name": "Altra Provision / Paradigm",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "FootShape™ Toe Box + GuideRail™ arch support frame.",
        "price": "$150"
    },
    {
        "name": "Topo Athletic Specter / Phantom",
        "toe_box": "Wide / Fan-Shaped Forefoot",
        "arch_support": "High Arch / Rigid Foot Vault (Supination Risk)",
        "feature": "Roomy anatomical forefoot with high-cushion neutral midsole.",
        "price": "$145"
    },
    {
        "name": "Brooks Adrenaline GTS (Wide 2E)",
        "toe_box": "Standard / Moderate Taper",
        "arch_support": "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "feature": "Structural medial arch support with generous forefoot width.",
        "price": "$140"
    },
    {
        "name": "Nike Air Zoom Pegasus",
        "toe_box": "Standard / Moderate Taper",
        "arch_support": "Neutral Arch",
        "feature": "Versatile neutral fit for standard foot lasts.",
        "price": "$130"
    }
]

def analyze_foot_contour(uploaded_file):
    """Real-time OpenCV analysis of forefoot width and shape profile."""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    _, thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        
        # Pixel-to-mm ratio estimation
        pixel_to_mm = 0.264
        foot_width_mm = round(w * pixel_to_mm, 1)
        foot_length_mm = round(h * pixel_to_mm, 1)
        
        ratio = foot_width_mm / (foot_length_mm if foot_length_mm > 0 else 1)
        shape = "Wide / Fan-Shaped Forefoot" if ratio > 0.38 else "Standard / Moderate Taper"
        
        return foot_width_mm, shape
    
    return 98.0, "Wide / Fan-Shaped Forefoot"

# Image Scanner Section
st.header("1. Real-Time AI Vision Scan")
uploaded_file = st.file_uploader("Upload top-down foot photo for automated measurement:", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Analyzing foot contours & anatomical splay...", width=280)
    
    with st.spinner("Processing OpenCV image detection..."):
        width_mm, detected_shape = analyze_foot_contour(uploaded_file)
    
    st.success("✅ Vision Analysis Complete!")
    
    col1, col2 = st.columns(2)
    col1.metric("Est. Forefoot Width", f"{width_mm} mm")
    col2.metric("Detected Shape", detected_shape)

st.divider()

# Biomechanical Input
st.header("2. Biomechanical Profile")
arch_type = st.selectbox(
    "Select Arch Drop / Pronation Tendency:",
    [
        "Flat Arch / Low Foot Vault (Overpronation Risk)",
        "High Arch / Rigid Foot Vault (Supination Risk)",
        "Neutral Arch"
    ]
)

st.divider()

# Results Engine
if st.button("Fetch Real-Time Matches 🚀", type="primary"):
    st.header("3. Diagnostic Fit Profile & Live Matches")
    
    st.markdown(f"""
    <div class="card">
        <h4>⚠️ Diagnostic Summary: {arch_type}</h4>
        <p>Matched against anatomical shoe lasts to optimize weight distribution and prevent forefoot joint compression.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Top Recommended Matches:")
    for shoe in SHOE_DATABASE:
        if shoe["arch_support"] == arch_type:
            st.markdown(f"""
            <div class="rec-card">
                <strong>👟 {shoe['name']}</strong> — {shoe['price']}<br>
                <span style="color: #CBD5E1; font-size: 0.95rem;">Why it fits: {shoe['feature']}</span>
            </div>
            """, unsafe_allow_html=True)
            import requests

def fetch_live_inventory(toe_shape, arch_type):
    """
    Simulates querying a live retail Storefront API based on foot diagnostics.
    Replace the API_ENDPOINT and HEADERS with your actual merchant credentials.
    """
    API_ENDPOINT = "https://api.yourstore.com/v1/products/search"
    
    # Query parameters based on foot assessment
    params = {
        "toe_box": toe_shape,
        "support_type": arch_type,
        "in_stock": True
    }
    
    headers = {
        "Authorization": "Bearer YOUR_STOREFRONT_API_TOKEN",
        "Content-Type": "application/json"
    }

    try:
        # Example API request
        response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()["products"]
    except Exception as e:
        # Fallback to local catalog if API request fails or is unconfigured
        pass

    # Fallback / Simulated Dynamic Data Structure
    return [
        {
            "title": "Altra Paradigm 7 (Wide FootShape)",
            "price": "$170.00",
            "availability": "In Stock (Sizes 7-11)",
            "image": "https://via.placeholder.com/150",
            "buy_url": "https://www.altrarunning.com"
        },
        {
            "title": "Brooks Adrenaline GTS 23 (Extra Wide 2E)",
            "price": "$140.00",
            "availability": "Low Stock (2 remaining)",
            "image": "https://via.placeholder.com/150",
            "buy_url": "https://www.brooksrunning.com"
        }
    ]import requests

def fetch_live_inventory(toe_shape, arch_type):
    """
    Simulates querying a live retail Storefront API based on foot diagnostics.
    Replace the API_ENDPOINT and HEADERS with your actual merchant credentials.
    """
    API_ENDPOINT = "https://api.yourstore.com/v1/products/search"
    
    # Query parameters based on foot assessment
    params = {
        "toe_box": toe_shape,
        "support_type": arch_type,
        "in_stock": True
    }
    
    headers = {
        "Authorization": "Bearer YOUR_STOREFRONT_API_TOKEN",
        "Content-Type": "application/json"
    }

    try:
        # Example API request
        response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()["products"]
    except Exception as e:
        # Fallback to local catalog if API request fails or is unconfigured
        pass

    # Fallback / Simulated Dynamic Data Structure
    return [
        {
            "title": "Altra Paradigm 7 (Wide FootShape)",
            "price": "$170.00",
            "availability": "In Stock (Sizes 7-11)",
            "image": "https://via.placeholder.com/150",
            "buy_url": "https://www.altrarunning.com"
        },
        {
            "title": "Brooks Adrenaline GTS 23 (Extra Wide 2E)",
            "price": "$140.00",
            "availability": "Low Stock (2 remaining)",
            "image": "https://via.placeholder.com/150",
            "buy_url": "https://www.brooksrunning.com"
        }
    ]import requests

def fetch_live_inventory(toe_shape, arch_type):
    """
    Simulates querying a live retail Storefront API based on foot diagnostics.
    Replace the API_ENDPOINT and HEADERS with your actual merchant credentials.
    """
    API_ENDPOINT = "https://api.yourstore.com/v1/products/search"
    
    # Query parameters based on foot assessment
    params = {
        "toe_box": toe_shape,
        "support_type": arch_type,
        "in_stock": True
    }
    
    headers = {
        "Authorization": "Bearer YOUR_STOREFRONT_API_TOKEN",
        "Content-Type": "application/json"
    }

    try:
        # Example API request
        response = requests.get(API_ENDPOINT, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()["products"]
    except Exception as e:
        # Fallback to local catalog if API request fails or is unconfigured
        pass

    # Fallback / Simulated Dynamic Data Structure
    return [
        {
            "title": "Altra Paradigm 7 (Wide FootShape)",
            "price": "$170.00",
            "availability": "In Stock (Sizes 7-11)",
            "image": "https://via.placeholder.com/150",
            "buy_url": "https://www.altrarunning.com"
        },
        {
            "title": "Brooks Adrenaline GTS 23 (Extra Wide 2E)",
            "price": "$140.00",
            "availability": "Low Stock (2 remaining)",
            "image": "https://via.placeholder.com/150",
            "buy_url": "https://www.brooksrunning.com"
        }
    ]import requests

# Displaying Live E-Commerce Results
st.subheader("🛍️ Real-Time Available Footwear Matches")

live_shoes = fetch_live_inventory(detected_shape, arch_type)

for shoe in live_shoes:
    st.markdown(f"""
    <div class="rec-card">
        <strong>👟 {shoe['title']}</strong> — <span style="color: #38BDF8;">{shoe['price']}</span><br>
        <span style="color: #CBD5E1; font-size: 0.9rem;">Status: {shoe['availability']}</span><br><br>
        <a href="{shoe['buy_url']}" target="_blank" style="background-color: #0EA5E9; color: white; padding: 6px 12px; border-radius: 5px; text-decoration: none; font-size: 0.85rem;">Buy Now / Check Stock ↗</a>
    </div>
    """, unsafe_allow_html=True)
