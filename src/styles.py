"""Original CSS for the Bias Heist Streamlit interface."""

import streamlit as st


CSS_BASE = r"""<style>

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: 3px;
    line-height: 1;
    margin: 0;
}

.subtitle {
    font-size: 1rem;
    color: #9aa8bd;
    margin-top: 4px;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.investigation-hint {
    background: #111b2e;
    border: 1px solid #263d62;
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 10px;
    color: #c9d7ee;
    font-size: 0.75rem;
}

.experiment-hint {
    background: #111c1a;
    border: 1px solid #28564c;
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 10px;
    color: #c8e4dc;
    font-size: 0.75rem;
}

.threshold-hint {
    background: #1b172d;
    border: 1px solid #4a3b78;
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 10px;
    color: #d9d0f5;
    font-size: 0.75rem;
}

</style>"""

CSS_INTERFACE = r"""<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 0.5rem;
}

.main-title {
    font-size: 2.65rem;
    font-weight: 800;
    letter-spacing: 3px;
    line-height: 1;
    margin: 0;
}

.main-title .accent {
    color: #8b5cf6;
}

.tagline {
    color: #7f8da3;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin-top: 7px;
    margin-bottom: 20px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 5px;
    margin-bottom: 2px;
}

.hero-title span {
    color: #8b5cf6;
}

.hero-text {
    color: #8d99aa;
    font-size: 0.82rem;
    margin-bottom: 12px;
}

.section-title {
    font-size: 1.05rem;
    font-weight: 750;
    margin-bottom: 2px;
}

.section-subtitle {
    color: #8995a8;
    font-size: 0.72rem;
    margin-bottom: 8px;
}

.result-title {
    font-size: 1.1rem;
    font-weight: 750;
}

.mission-text {
    font-size: 0.8rem;
    line-height: 1.35;
}

.mission-card {
    background: #101827;
    border: 1px solid #2b3b55;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 5px 0;
}

.mission-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 1rem;
    font-weight: 750;
    margin-bottom: 9px;
}

.mission-header span {
    color: #8b5cf6;
}

.mission-step {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    margin: 7px 0;
    font-size: 0.8rem;
    color: #d4dbea;
    line-height: 1.35;
}

.mission-number {
    min-width: 21px;
    height: 21px;
    border-radius: 50%;
    background: #211a46;
    border: 1px solid #5146a5;
    color: #a78bfa;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.68rem;
    font-weight: 700;
}

div[data-testid="stMetricValue"] {
    font-size: 1.65rem !important;
    font-weight: 700 !important;
}

.pro-tip {
    padding: 13px 14px;
    border-radius: 10px;
    background: #17133a;
    border: 1px solid #5146a5;
    color: #d9d5ff;
    font-size: 0.78rem;
    margin-top: 12px;
    min-height: 46px;
    box-sizing: border-box;
}

.probability-row {
    display: flex;
    align-items: center;
    gap: 22px;
    margin: 16px 0;
}

.probability-circle {
    width: 105px;
    height: 105px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    flex-shrink: 0;
}

.probability-circle::before {
    content: "";
    width: 82px;
    height: 82px;
    border-radius: 50%;
    background: #0d1524;
    position: absolute;
}

.probability-value {
    position: relative;
    font-size: 1.45rem;
    font-weight: 800;
}

.probability-label {
    color: #9aa4b2;
    font-size: 0.78rem;
}

.probability-number {
    font-size: 1.9rem;
    font-weight: 800;
}

div[data-testid="stForm"] {
    border: none;
    padding: 0;
}

div[data-testid="stNumberInput"] input {
    min-height: 34px;
}

div[data-baseweb="select"] > div {
    min-height: 34px;
}

div[data-testid="stFormSubmitButton"] button {
    min-height: 46px;
    font-weight: 750;
    letter-spacing: 0.6px;
    border-radius: 9px;
}

</style>"""


def apply_styles():
    """Apply the original styles in their original order."""
    st.markdown(CSS_BASE, unsafe_allow_html=True)
    st.markdown(CSS_INTERFACE, unsafe_allow_html=True)
