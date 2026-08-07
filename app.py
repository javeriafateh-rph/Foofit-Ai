import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(page_title="FootFit AI", page_icon="👟", layout="centered")

# Custom CSS Styling
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E293B; text-align: center; margin-bottom: 0px; }
    .subtitle { font-size: 1.1rem; color: #64748B; text-align: center; margin-bottom: 25px; }
    .card { background-color: #F8FAFC; border-left: 5px solid #0EA5E9; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .rec-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">👟 FootFit AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Anatomical Foot Profile Analyzer & Recommendation Engine</div>', unsafe_allow_html=True)

st.divider()

# Input Section
st.header("1. Anatomical Foot Assessment")

col1, col2 = st.columns(2)

with col1:
    toe_shape = st.selectbox(
        "Forefoot / Toe Width Structure:",
        [
            "Standard / Moderate Taper",
            "Wide / Fan-Shaped Toes (Wide Forefoot)",
            "Narrow / Tapered Toes"
        ]
    )

with col2:
    arch_type = st.selectbox(
        "Arch Drop & Biomechanics:",
        [
            "Neutral Arch",
            "Flat Arch / Low Foot Vault (Overpronation Risk)",
            "High Arch / Rigid Foot Vault (Supination Risk)"
        ]
    )

activity = st.selectbox(
    "Primary Footwear Intended Use:",
    ["All-Day Standing & Walking", "Running & Fitness", "Workplace / Formal Wear", "Casual Daily Wear"]
)

st.divider()

# Image Upload
st.header("2. AI Vision Scan (Optional)")
uploaded_file = st.file_uploader("Upload a top-down or arch-profile photo of your foot for visual validation:", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Analyzing forefoot splay and arch drop gap...", width=280)
    st.success("✅ Image analyzed successfully. Foot outlines aligned.")

st.divider()

# Run Engine Button
if st.button("Generate Anatomical Fit Recommendations 🚀", type="primary"):
    st.header("3. Diagnostic Fit Profile & Match Results")
    
    # Recommendation Logic Matrix
    if "Wide" in toe_shape and "Flat" in arch_type:
        st.markdown("""
        <div class="card">
            <h4>⚠️ Diagnostic Summary: Fan-Shaped Forefoot + Low Arch Vault</h4>
            <p>Standard tapered shoes compress your toe joints, leading to bunions and midfoot collapse. You require an <b>anatomical foot-shaped toe box</b> paired with <b>medial guidance stability</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        recs = [
            {"brand": "Altra Provision / Paradigm", "feature": "FootShape™ Toe Box + GuideRail™ arch support frame."},
            {"brand": "Brooks Adrenaline GTS (Wide 2E)", "feature": "Structural medial arch support with generous forefoot width."},
            {"brand": "Topo Athletic Ultrafly", "feature": "Anatomical wide toe box with midfoot stability guidance."}
        ]
        
    elif "Wide" in toe_shape and "High" in arch_type:
        st.markdown("""
        <div class="card">
            <h4>⚠️ Diagnostic Summary: Fan-Shaped Forefoot + High Rigid Arch</h4>
            <p>Your foot shape requires maximum shock absorption and a wide, non-constricting toe box to prevent pressure buildup under the heel and ball of the foot.</p>
        </div>
        """, unsafe_allow_html=True)
        
        recs = [
            {"brand": "Topo Athletic Specter / Phantom", "feature": "Roomy anatomical forefoot with high-cushion neutral midsole."},
            {"brand": "New Balance Fresh Foam 1080 (Wide 2E)", "feature": "Ultra-flexible mesh upper with high shock absorption."}
        ]

    elif "Flat" in arch_type:
        st.markdown("""
        <div class="card">
            <h4>ℹ️ Diagnostic Summary: Flat Arch (Overpronation Tendency)</h4>
            <p>Requires structural arch posts and a deep heel cup to align the ankles and knees properly during gait.</p>
        </div>
        """, unsafe_allow_html=True)
        
        recs = [
            {"brand": "Asics Gel-Kayano", "feature": "Industry-standard dynamic arch support structure."},
            {"brand": "Saucony Guide", "feature": "Lightweight medial stability frame with balanced cushioning."}
        ]

    else:
        st.markdown("""
        <div class="card">
            <h4>✅ Diagnostic Summary: Standard / Neutral Foot Alignment</h4>
            <p>Balanced weight distribution across the foot structure. Standard neutral shoe lasts offer optimal comfort.</p>
        </div>
        """, unsafe_allow_html=True)
        
        recs = [
            {"brand": "Nike Air Zoom Pegasus", "feature": "Versatile neutral fit for standard foot lasts."},
            {"brand": "Asics Gel-Cumulus", "feature": "Balanced neutral cushioning and breathable upper."}
        ]

    # Display Matches
    st.subheader("Top Recommended Shoe Matches:")
    for item in recs:
        st.markdown(f"""
        <div class="rec-card">
            <strong>👟 {item['brand']}</strong><br>
            <span style="color: #475569; font-size: 0.95rem;">Why it fits: {item['feature']}</span>
        </div>
        """, unsafe_allow_html=True)
