import streamlit as st

# ====================
# CONFIG PAGE
# ====================
st.set_page_config
    page_title="Sistem Gudang",
    page_icon="📦",
    layout="wide"

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #ff9a9e,
        #fecfef,
        #fcb69f
    );
    color: #4a4a4a;
}

h1, h2, h3 {
    color: white !important;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.2);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffdde1,
        #ee9ca7
    );
}

.stButton>button {
    width: 100%;
    border-radius: 15px;
    border: none;
    padding: 12px;
    font-weight: bold;
    font-size: 15px;
    background: linear-gradient(
        90deg,
        #ff758c,
        #ff7eb3
    );
    color: white;
    transition: 0.3s;
    box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(
        90deg,
        #ff5f95,
        #ffb6c1
    );
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.25);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
}

div[data-testid="stDataFrame"] {
    background-color: rgba(255,255,255,0.15);
    border-radius: 15px;
    padding: 10px;
}

.block-container {
    padding-top: 2rem;
}

input, textarea {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)
