CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500&display=swap');

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(14,165,233,0.25);
}
.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: white;
    margin: 0;
}
.hero-subtitle {
    color: #E0F2FE;
    font-size: 1.02rem;
    margin-top: 6px;
}

.step-badge {
    display: inline-block;
    background: linear-gradient(135deg, #0EA5E9, #6366F1);
    color: white;
    border-radius: 999px;
    width: 28px; height: 28px;
    text-align: center;
    line-height: 28px;
    font-weight: 700;
    margin-right: 8px;
    font-size: 0.85rem;
}
.step-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1.15rem;
}

.guide-box {
    background-color: #0F172A;
    border: 1px dashed #38BDF8;
    padding: 12px 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    color: #CBD5E1;
    font-size: 0.9rem;
}

.card {
    background-color: #1E293B;
    border-left: 5px solid #0EA5E9;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    color: #FFFFFF;
}
.card h4 { color: #38BDF8 !important; margin-top: 0px; font-family: 'Poppins', sans-serif; }

.rec-card {
    background: linear-gradient(180deg, #0F172A 0%, #111C33 100%);
    border: 1px solid #2B3A55;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 14px;
    color: #F8FAFC;
    transition: border-color 0.2s ease;
}
.rec-card:hover { border-color: #38BDF8; }
.rec-card strong { font-size: 1.15rem; color: #38BDF8; font-family: 'Poppins', sans-serif; }

.match-bar-track {
    background-color: #1E293B;
    border-radius: 999px;
    height: 8px;
    width: 100%;
    margin: 8px 0 10px 0;
    overflow: hidden;
}
.match-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #0EA5E9, #22D3EE);
}
.match-pct {
    font-size: 0.8rem;
    color: #7DD3FC;
    font-weight: 600;
}

.buy-btn {
    display: inline-block;
    background: linear-gradient(135deg, #0EA5E9, #6366F1);
    color: #FFFFFF !important;
    font-weight: 600;
    padding: 8px 18px;
    border-radius: 999px;
    text-decoration: none;
    margin-top: 10px;
    font-size: 0.9rem;
}
.buy-btn:hover { opacity: 0.9; }

.category-pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 8px;
}
.pill-everyday { background-color: #164E63; color: #A5F3FC; }
.pill-sports { background-color: #713F12; color: #FDE68A; }
.pill-medical { background-color: #14532D; color: #BBF7D0; }

.accuracy-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-left: 8px;
}
.accuracy-calibrated { background-color: #065F46; color: #D1FAE5; }
.accuracy-estimate { background-color: #78350F; color: #FEF3C7; }

.disclaimer {
    background-color: #1F2937;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #9CA3AF;
    margin-top: 24px;
}
</style>
"""

CATEGORY_PILL_CLASS = {
    "Everyday / Casual": "pill-everyday",
    "Sports & Training": "pill-sports",
    "Medical & Comfort": "pill-medical",
}
