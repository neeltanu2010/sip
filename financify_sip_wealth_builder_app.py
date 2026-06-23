import math
from datetime import datetime
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =====================================================
# FINANCIFY - SIP + WEALTH BUILDER CALCULATOR
# Free premium hook tool for Financify blog
# =====================================================

st.set_page_config(
    page_title="Financify SIP + Wealth Builder Calculator",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SURECART_CHECKOUT_URL = "https://financify.blog/buy/financify-tools"
TOOLS_PAGE_URL = "https://financify.blog/tools"
BLOG_URL = "https://financify.blog"

# Mobile-friendly Plotly config
PLOTLY_MOBILE_CONFIG = {"responsive": True, "displayModeBar": False}

# -------------------------
# Premium CSS
# -------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 8%, rgba(255, 210, 31, 0.26), transparent 30%),
            radial-gradient(circle at 86% 18%, rgba(255, 159, 10, 0.18), transparent 28%),
            radial-gradient(circle at 85% 82%, rgba(255, 210, 31, 0.18), transparent 30%),
            linear-gradient(135deg, #fffaf0 0%, #fff8d8 44%, #fffdf6 100%);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.12;
        background-image:
          linear-gradient(30deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(150deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(30deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(150deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(60deg, rgba(0,0,0,0.18) 25%, transparent 25.5%, transparent 75%, rgba(0,0,0,0.18) 75%, rgba(0,0,0,0.18));
        background-size: 64px 112px;
        background-position: 0 0, 0 0, 32px 56px, 32px 56px, 0 0;
        z-index: -1;
    }

    .block-container {
        padding-top: 1.35rem;
        padding-bottom: 3rem;
        max-width: 1230px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050505 0%, #171100 52%, #241900 100%);
        border-right: 1px solid rgba(255, 210, 31, 0.25);
    }

    /* Sidebar readability fix: labels stay light, input text stays dark */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #fff8d8 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        color: #111111 !important;
        background: #fff8d8 !important;
        border-radius: 12px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] div,
    section[data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #111111 !important;
        background: #fff8d8 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        color: #111111 !important;
        background: #fff8d8 !important;
    }

    section[data-testid="stSidebar"] a {
        color: #FFD21F !important;
        font-weight: 900 !important;
    }

    .hero-card {
        background: linear-gradient(135deg, #050505 0%, #171100 52%, #3a2b00 100%);
        border: 1px solid rgba(255, 210, 31, 0.58);
        border-radius: 30px;
        padding: 34px 34px 30px 34px;
        box-shadow: 0 26px 85px rgba(0,0,0,0.23);
        position: relative;
        overflow: hidden;
        margin-bottom: 22px;
    }

    .hero-card:before {
        content: "";
        position: absolute;
        inset: -4px;
        background:
            radial-gradient(circle at 90% 20%, rgba(255,210,31,0.34), transparent 23%),
            radial-gradient(circle at 12% 90%, rgba(255,210,31,0.14), transparent 24%);
        pointer-events: none;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 210, 31, 0.15);
        color: #ffe680;
        border: 1px solid rgba(255, 210, 31, 0.45);
        padding: 8px 13px;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 900;
        letter-spacing: 0.02em;
    }

    .hero-title {
        color: #ffffff;
        font-size: clamp(2.05rem, 4vw, 4.08rem);
        line-height: 1.02;
        font-weight: 950;
        letter-spacing: -0.058em;
        margin-top: 18px;
        margin-bottom: 16px;
        max-width: 920px;
    }

    .hero-title span {
        color: #FFD21F;
    }

    .hero-subtitle {
        color: #fff4bd;
        font-size: 1.04rem;
        line-height: 1.7;
        max-width: 900px;
        margin-bottom: 20px;
    }

    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
    }

    .pill {
        background: rgba(255, 255, 255, 0.08);
        color: #fff7cf;
        border: 1px solid rgba(255, 210, 31, 0.28);
        border-radius: 999px;
        padding: 9px 13px;
        font-size: 0.88rem;
        font-weight: 800;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.86);
        border: 1px solid rgba(17, 17, 17, 0.08);
        border-radius: 25px;
        padding: 22px;
        box-shadow: 0 14px 44px rgba(20, 14, 0, 0.08);
        backdrop-filter: blur(12px);
        margin-bottom: 18px;
    }

    .dark-card {
        background: linear-gradient(135deg, #080808 0%, #211700 68%, #4a3800 100%);
        border: 1px solid rgba(255, 210, 31, 0.46);
        border-radius: 26px;
        padding: 24px;
        box-shadow: 0 18px 44px rgba(0,0,0,0.22);
        color: #fff8d8;
        margin-bottom: 18px;
    }

    .metric-card {
        background: linear-gradient(180deg, #ffffff 0%, #fff7d2 100%);
        border: 1px solid rgba(17, 17, 17, 0.08);
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 12px 30px rgba(17, 17, 17, 0.08);
        min-height: 145px;
    }

    .metric-label {
        color: #5c4a00;
        font-size: 0.82rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.055em;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #080808;
        font-size: 1.68rem;
        font-weight: 950;
        letter-spacing: -0.04em;
        margin-bottom: 6px;
    }

    .metric-help {
        color: #5a5a5a;
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 950;
        color: #111;
        letter-spacing: -0.035em;
        margin-bottom: 8px;
    }

    .section-title-light {
        font-size: 1.45rem;
        font-weight: 950;
        color: #FFD21F;
        letter-spacing: -0.035em;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #5b5b5b;
        font-size: 0.97rem;
        line-height: 1.55;
        margin-bottom: 18px;
    }

    .light-text {
        color: #fff7cf;
        line-height: 1.62;
        font-weight: 600;
    }

    .mini-badge {
        display: inline-block;
        background: #FFD21F;
        color: #111;
        padding: 7px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 950;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .soft-badge {
        display: inline-block;
        background: rgba(255, 210, 31, 0.18);
        border: 1px solid rgba(255, 210, 31, 0.35);
        color: #fff7cf;
        padding: 7px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 850;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .warning-box {
        background: #fff2bd;
        border-left: 6px solid #FFD21F;
        border-radius: 18px;
        padding: 16px 18px;
        color: #2f2600;
        line-height: 1.58;
        font-weight: 650;
        margin-bottom: 18px;
    }

    .cta-card {
        background: linear-gradient(135deg, #FFD21F 0%, #ffb800 100%);
        color: #111;
        border-radius: 27px;
        padding: 25px;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 18px 42px rgba(122, 91, 0, 0.18);
        margin-top: 18px;
    }

    .cta-card h3 {
        color: #111;
        font-size: 1.55rem;
        font-weight: 950;
        margin-bottom: 8px;
        letter-spacing: -0.035em;
    }

    .cta-card p {
        color: #241b00;
        line-height: 1.58;
        font-weight: 650;
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 999px !important;
        border: 1px solid rgba(17,17,17,0.13) !important;
        background: linear-gradient(135deg, #111 0%, #2a2100 100%) !important;
        color: #FFD21F !important;
        font-weight: 900 !important;
        padding: 0.72rem 1.1rem !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.18) !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.78);
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 20px;
        padding: 14px 16px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    }

    div[data-testid="stTabs"] button {
        font-weight: 850;
    }

    .footer-note {
        color: #6b5d27;
        text-align: center;
        font-size: 0.86rem;
        margin-top: 24px;
    }

    @media (max-width: 768px) {
        .hero-card { padding: 26px 20px; border-radius: 22px; }
        .glass-card, .dark-card { padding: 18px; border-radius: 20px; }
        .metric-value { font-size: 1.38rem; }
    }


    /* =====================================================
       FINANCIFY MOBILE + READABILITY PATCH
       Keeps the original theme, fixes mobile overflow and invisible text.
       ===================================================== */
    :root { color-scheme: light; }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        -webkit-text-size-adjust: 100%;
        text-rendering: optimizeLegibility;
    }

    *, *::before, *::after {
        box-sizing: border-box !important;
    }

    .main .block-container,
    [data-testid="stAppViewContainer"] .block-container {
        width: 100% !important;
        max-width: min(1260px, 100%) !important;
        padding-left: clamp(0.90rem, 3.2vw, 2.00rem) !important;
        padding-right: clamp(0.90rem, 3.2vw, 2.00rem) !important;
    }

    .block-container p,
    .block-container li,
    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container h4,
    .block-container h5,
    .block-container h6,
    .block-container span,
    .hero-title,
    .hero-subtitle,
    .section-title,
    .section-subtitle,
    .metric-label,
    .metric-value,
    .metric-help,
    .verdict-title,
    .verdict-text,
    .light-text,
    .pill,
    .mini-badge,
    .soft-badge {
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    .hero-card,
    .glass-card,
    .dark-card,
    .metric-card,
    .verdict-box,
    .warning-box,
    .danger-box,
    .cta-card {
        max-width: 100% !important;
        isolation: isolate;
    }

    .hero-card > *,
    .dark-card > *,
    .verdict-box > * {
        position: relative;
        z-index: 1;
    }

    .glass-card,
    .metric-card,
    .warning-box,
    .danger-box,
    .cta-card {
        color: #111111 !important;
    }

    .glass-card p,
    .glass-card li,
    .glass-card span,
    .metric-card p,
    .metric-card li,
    .warning-box p,
    .warning-box li,
    .danger-box p,
    .danger-box li,
    .cta-card p,
    .cta-card li {
        opacity: 1 !important;
    }

    .dark-card,
    .dark-card p,
    .dark-card li,
    .dark-card span,
    .verdict-box,
    .verdict-box p,
    .verdict-box li,
    .verdict-box span,
    .hero-card,
    .hero-card p,
    .hero-card li,
    .hero-card span {
        color: #fff7cf !important;
        -webkit-text-fill-color: #fff7cf !important;
    }

    .hero-title,
    .hero-title span,
    .verdict-title,
    .section-title-light {
        -webkit-text-fill-color: currentColor !important;
    }

    .metric-label { color: #5c4a00 !important; }
    .metric-value { color: #070707 !important; }
    .metric-help { color: #4c4c4c !important; }
    .section-title { color: #111111 !important; }
    .section-subtitle { color: #4d4d4d !important; }
    .warning-box, .warning-box * { color: #2f2600 !important; -webkit-text-fill-color: #2f2600 !important; }
    .danger-box, .danger-box * { color: #3b120a !important; -webkit-text-fill-color: #3b120a !important; }
    .cta-card, .cta-card * { color: #111111 !important; -webkit-text-fill-color: #111111 !important; }

    /* Sidebar: readable labels on dark background, readable input text on light fields. */
    section[data-testid="stSidebar"] {
        min-width: min(22rem, 92vw) !important;
        max-width: 92vw !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
        color: #fff8d8 !important;
        -webkit-text-fill-color: #fff8d8 !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] [data-baseweb="input"] input,
    section[data-testid="stSidebar"] [data-baseweb="textarea"] textarea,
    section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        background: #fffaf0 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        caret-color: #111111 !important;
        border: 1px solid rgba(255, 210, 31, 0.50) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        min-height: 44px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] {
        background: #fffaf0 !important;
        color: #111111 !important;
        border-color: rgba(255, 210, 31, 0.50) !important;
        border-radius: 12px !important;
        min-height: 44px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] * {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="menu"] [role="option"] {
        background: #fffaf0 !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stSelectbox [data-baseweb="select"] > div {
        font-size: 16px !important;
    }

    /* Tables and Plotly should scroll/resize instead of cutting text on phones. */
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"],
    .stDataFrame,
    .stTable {
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        border-radius: 16px !important;
    }

    div[data-testid="stDataFrame"] * {
        font-size: clamp(0.74rem, 2.9vw, 0.92rem) !important;
    }

    .js-plotly-plot,
    .plotly,
    .plot-container,
    div[data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
    }

    div[data-testid="stPlotlyChart"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        gap: 0.35rem !important;
        scrollbar-width: none;
    }

    div[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
        display: none;
    }

    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button p {
        white-space: nowrap !important;
        font-size: clamp(0.78rem, 3.1vw, 0.94rem) !important;
        line-height: 1.2 !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.75rem !important;
            padding-bottom: 2rem !important;
        }

        .hero-card {
            padding: 1.25rem 1rem !important;
            border-radius: 21px !important;
            margin-bottom: 1rem !important;
        }

        .hero-title {
            font-size: clamp(1.72rem, 9vw, 2.35rem) !important;
            letter-spacing: -0.038em !important;
            line-height: 1.07 !important;
            margin-top: 0.95rem !important;
            margin-bottom: 0.75rem !important;
        }

        .hero-subtitle {
            font-size: 0.96rem !important;
            line-height: 1.55 !important;
            margin-bottom: 0.85rem !important;
        }

        .hero-pills {
            gap: 0.45rem !important;
            margin-top: 0.85rem !important;
        }

        .pill,
        .mini-badge,
        .soft-badge {
            font-size: 0.76rem !important;
            line-height: 1.2 !important;
            padding: 0.45rem 0.62rem !important;
        }

        .glass-card,
        .dark-card,
        .metric-card,
        .verdict-box,
        .warning-box,
        .danger-box,
        .cta-card {
            padding: 1rem !important;
            border-radius: 18px !important;
            margin-bottom: 0.95rem !important;
        }

        .metric-card {
            min-height: auto !important;
        }

        .metric-label {
            font-size: 0.73rem !important;
            line-height: 1.18 !important;
            letter-spacing: 0.045em !important;
        }

        .metric-value {
            font-size: clamp(1.15rem, 6.2vw, 1.55rem) !important;
            line-height: 1.13 !important;
        }

        .metric-help,
        .section-subtitle,
        .verdict-text,
        .light-text {
            font-size: 0.91rem !important;
            line-height: 1.50 !important;
        }

        .section-title,
        .section-title-light,
        .verdict-title {
            font-size: 1.18rem !important;
            line-height: 1.20 !important;
            letter-spacing: -0.025em !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.75rem !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        section[data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            min-height: 46px !important;
            padding: 0.75rem 0.95rem !important;
            white-space: normal !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stMetric"] {
            padding: 0.85rem 0.9rem !important;
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] * {
            font-size: 0.76rem !important;
            white-space: normal !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.25rem !important;
            line-height: 1.15 !important;
            overflow-wrap: anywhere !important;
        }

        div[data-testid="stPlotlyChart"] {
            border-radius: 16px !important;
        }

        iframe,
        img,
        video,
        canvas,
        svg {
            max-width: 100% !important;
        }
    }

    @media (max-width: 420px) {
        .hero-title {
            font-size: clamp(1.58rem, 10vw, 2.05rem) !important;
        }

        .eyebrow {
            font-size: 0.74rem !important;
            padding: 0.43rem 0.58rem !important;
        }

        .metric-value {
            font-size: clamp(1.05rem, 7vw, 1.35rem) !important;
        }

        .block-container {
            padding-left: 0.72rem !important;
            padding-right: 0.72rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Helpers
# -------------------------

def money(x):
    try:
        x = float(x)
    except Exception:
        return "—"
    if not np.isfinite(x):
        return "—"
    sign = "-" if x < 0 else ""
    x = abs(x)
    if x >= 10_000_000:
        return f"{sign}₹{x/10_000_000:.2f} Cr"
    if x >= 100_000:
        return f"{sign}₹{x/100_000:.2f} L"
    return f"{sign}₹{x:,.0f}"


def money_full(x):
    try:
        x = float(x)
    except Exception:
        return "—"
    if not np.isfinite(x):
        return "—"
    return f"₹{x:,.0f}"


def pct(x):
    try:
        x = float(x)
    except Exception:
        return "—"
    if not np.isfinite(x):
        return "—"
    return f"{x*100:.2f}%"


def monthly_rate(annual_return):
    return (1 + annual_return) ** (1 / 12) - 1


def simulate_wealth(monthly_sip, lump_sum, years, annual_return, annual_step_up, inflation_rate=0.06, fee_drag=0.0):
    """Monthly simulation with yearly SIP step-up and optional return drag."""
    months = int(round(years * 12))
    r = monthly_rate(max(annual_return - fee_drag, -0.99))
    inflation_m = monthly_rate(inflation_rate)
    rows = []
    corpus = float(lump_sum)
    total_invested = float(lump_sum)
    sip = float(monthly_sip)
    milestone_crossed = {}

    for m in range(1, months + 1):
        year = math.ceil(m / 12)
        if m > 1 and (m - 1) % 12 == 0:
            sip *= (1 + annual_step_up)

        corpus = corpus * (1 + r) + sip
        total_invested += sip
        real_corpus = corpus / ((1 + inflation_m) ** m)
        gains = corpus - total_invested

        for milestone in [100_000, 500_000, 1_000_000, 2_500_000, 5_000_000, 10_000_000, 50_000_000, 100_000_000]:
            if corpus >= milestone and milestone not in milestone_crossed:
                milestone_crossed[milestone] = m

        if m % 12 == 0 or m == 1 or m == months:
            rows.append(
                {
                    "Month": m,
                    "Year": m / 12,
                    "Calendar Year": year,
                    "Monthly SIP": sip,
                    "Total Invested": total_invested,
                    "Estimated Corpus": corpus,
                    "Estimated Gain": gains,
                    "Inflation Adjusted Corpus": real_corpus,
                }
            )

    df = pd.DataFrame(rows)
    return df, milestone_crossed


def final_values(monthly_sip, lump_sum, years, annual_return, annual_step_up, inflation_rate, fee_drag):
    df, milestones = simulate_wealth(monthly_sip, lump_sum, years, annual_return, annual_step_up, inflation_rate, fee_drag)
    if df.empty:
        return {}, milestones, df
    last = df.iloc[-1]
    values = {
        "corpus": float(last["Estimated Corpus"]),
        "invested": float(last["Total Invested"]),
        "gain": float(last["Estimated Gain"]),
        "real_corpus": float(last["Inflation Adjusted Corpus"]),
        "last_sip": float(last["Monthly SIP"]),
    }
    return values, milestones, df


def required_sip_for_goal(goal_amount, lump_sum, years, annual_return, annual_step_up, inflation_rate, fee_drag):
    if goal_amount <= 0 or years <= 0:
        return np.nan
    low, high = 0.0, max(goal_amount, 10_000.0)
    for _ in range(80):
        vals, _, _ = final_values(high, lump_sum, years, annual_return, annual_step_up, inflation_rate, fee_drag)
        if vals.get("corpus", 0) >= goal_amount:
            break
        high *= 2
    for _ in range(80):
        mid = (low + high) / 2
        vals, _, _ = final_values(mid, lump_sum, years, annual_return, annual_step_up, inflation_rate, fee_drag)
        if vals.get("corpus", 0) >= goal_amount:
            high = mid
        else:
            low = mid
    return high


def wealth_score(monthly_sip, monthly_income, years, annual_return, annual_step_up, inflation_rate, final_corpus, goal_amount):
    score = 0
    notes = []
    savings_rate = monthly_sip / monthly_income if monthly_income > 0 else np.nan

    if monthly_income > 0:
        if savings_rate >= 0.30:
            score += 25
            notes.append("Savings rate is strong.")
        elif savings_rate >= 0.20:
            score += 20
            notes.append("Savings rate is healthy.")
        elif savings_rate >= 0.10:
            score += 12
            notes.append("Savings rate is a good start.")
        else:
            score += 5
            notes.append("Savings rate is low. Increase it gradually when possible.")
    else:
        score += 13
        notes.append("Add monthly income to calculate savings rate.")

    if years >= 20:
        score += 22
        notes.append("Time horizon is strong.")
    elif years >= 12:
        score += 16
        notes.append("Time horizon is decent.")
    elif years >= 7:
        score += 10
        notes.append("Time horizon is medium.")
    else:
        score += 4
        notes.append("Short horizon. Keep return assumptions conservative.")

    if annual_step_up >= 0.10:
        score += 18
        notes.append("Annual SIP increase is strong.")
    elif annual_step_up >= 0.05:
        score += 13
        notes.append("Annual SIP increase is useful.")
    elif annual_step_up > 0:
        score += 8
        notes.append("Small annual increase helps.")
    else:
        score += 2
        notes.append("No annual increase added.")

    if annual_return <= 0.10:
        score += 17
        notes.append("Return expectation is conservative.")
    elif annual_return <= 0.13:
        score += 13
        notes.append("Return expectation is reasonable, but not guaranteed.")
    elif annual_return <= 0.16:
        score += 7
        notes.append("Return expectation is aggressive.")
    else:
        score += 2
        notes.append("Return expectation is very aggressive.")

    if inflation_rate >= 0.05:
        score += 8
        notes.append("Inflation-adjusted value is included.")
    else:
        score += 4
        notes.append("Inflation rate is low. Real purchasing power may be overstated.")

    if goal_amount > 0:
        progress = final_corpus / goal_amount
        if progress >= 1:
            score += 10
            notes.append("Goal looks achievable.")
        elif progress >= 0.75:
            score += 7
            notes.append("Goal is close.")
        else:
            score += 3
            notes.append("Goal needs higher SIP, higher step-up or more time.")
    else:
        score += 6
        notes.append("Add a target amount to calculate goal progress.")

    return min(score, 100), notes


def bee_verdict(score, final_corpus, goal_amount, real_corpus, invested):
    if score >= 80:
        title = "Wealth Builder Bee 🐝"
        text = "Your plan looks strong based on the current inputs. Review it once a year."
    elif score >= 60:
        title = "Growing Honey Pot 🍯"
        text = "This is a solid plan. Increasing SIP every year can improve the outcome."
    elif score >= 40:
        title = "Baby Bee Portfolio 🌱"
        text = "The plan needs more monthly investment, more time, or lower goal expectations."
    else:
        title = "Lazy Honey Alert ⚠️"
        text = "The plan looks weak based on the current inputs. Increase SIP, time period, or annual step-up."

    if goal_amount > 0:
        if final_corpus >= goal_amount:
            text += " Your target goal is achievable under these assumptions."
        else:
            gap = goal_amount - final_corpus
            text += f" Your target has a gap of about {money(gap)} under these assumptions."

    if real_corpus < final_corpus * 0.55:
        text += " Inflation reduces future purchasing power."

    if invested > 0 and final_corpus / invested < 1.5:
        text += " More time can improve compounding."

    return title, text


def make_wealth_chart(scenarios_df):
    fig = go.Figure()
    for name, df in scenarios_df.items():
        if not df.empty:
            fig.add_trace(
                go.Scatter(
                    x=df["Year"],
                    y=df["Estimated Corpus"],
                    mode="lines+markers",
                    name=name,
                    hovertemplate="Year %{x:.0f}<br>Corpus %{y:,.0f}<extra></extra>",
                )
            )
    fig.update_layout(
        title="Wealth journey: conservative vs base vs optimistic",
        xaxis_title="Years",
        yaxis_title="Estimated corpus",
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=60, b=50),
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def make_breakup_chart(invested, gains):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Total Invested", "Estimated Gains"],
                values=[max(invested, 0), max(gains, 0)],
                hole=0.62,
                textinfo="label+percent",
                hovertemplate="%{label}: ₹%{value:,.0f}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title="Corpus breakup",
        template="plotly_white",
        height=380,
        margin=dict(l=20, r=20, t=60, b=30),
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        showlegend=True,
    )
    return fig


def make_goal_gauge(final_corpus, goal_amount):
    progress = 0 if goal_amount <= 0 else min(final_corpus / goal_amount * 100, 150)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=progress,
            number={"suffix": "%"},
            title={"text": "Goal progress"},
            gauge={
                "axis": {"range": [0, 150]},
                "bar": {"thickness": 0.26},
                "steps": [
                    {"range": [0, 50], "color": "rgba(255, 210, 31, 0.18)"},
                    {"range": [50, 100], "color": "rgba(255, 210, 31, 0.34)"},
                    {"range": [100, 150], "color": "rgba(255, 210, 31, 0.52)"},
                ],
                "threshold": {"line": {"width": 4}, "thickness": 0.75, "value": 100},
            },
        )
    )
    fig.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=60, b=20),
        font=dict(family="Inter", size=13),
        paper_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def make_stepup_chart(base_df):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=base_df["Year"],
            y=base_df["Monthly SIP"],
            name="Monthly SIP",
            hovertemplate="Year %{x:.0f}<br>SIP ₹%{y:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Step-up SIP ladder",
        xaxis_title="Years",
        yaxis_title="Monthly SIP",
        template="plotly_white",
        height=360,
        margin=dict(l=20, r=20, t=60, b=50),
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def milestone_text(milestones):
    if not milestones:
        return "No major milestone is reached within this period. Increase SIP, step-up or time horizon."
    lines = []
    labels = {
        100_000: "First ₹1 lakh",
        500_000: "₹5 lakh",
        1_000_000: "₹10 lakh",
        2_500_000: "₹25 lakh",
        5_000_000: "₹50 lakh",
        10_000_000: "₹1 crore",
        50_000_000: "₹5 crore",
        100_000_000: "₹10 crore",
    }
    for amount, month in sorted(milestones.items()):
        y = month / 12
        lines.append(f"{labels.get(amount, money(amount))}: around year {y:.1f}")
    return "\n".join(lines)


def build_report(name, age, monthly_sip, lump_sum, monthly_income, years, annual_return, annual_step_up, inflation_rate, fee_drag, goal_amount, vals, score, verdict_title, verdict_text, notes, required_sip):
    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")
    savings_rate = monthly_sip / monthly_income if monthly_income > 0 else np.nan
    return f"""
FINANCIFY SIP + WEALTH BUILDER MINI REPORT
Generated: {generated}

Investor name: {name or 'Not specified'}
Age: {age}
Monthly SIP: {money_full(monthly_sip)}
Initial lump sum: {money_full(lump_sum)}
Monthly income entered: {money_full(monthly_income) if monthly_income > 0 else 'Not entered'}
Savings rate: {pct(savings_rate) if np.isfinite(savings_rate) else 'Not available'}
Time horizon: {years} years
Expected return: {annual_return*100:.2f}%
Annual SIP increase: {annual_step_up*100:.2f}%
Inflation rate: {inflation_rate*100:.2f}%
Return drag/expense assumption: {fee_drag*100:.2f}%
Target goal: {money_full(goal_amount) if goal_amount > 0 else 'Not entered'}

ESTIMATED OUTCOME
Final corpus: {money_full(vals['corpus'])}
Total invested: {money_full(vals['invested'])}
Estimated gains: {money_full(vals['gain'])}
Inflation-adjusted corpus: {money_full(vals['real_corpus'])}
Final monthly SIP after step-ups: {money_full(vals['last_sip'])}
Required SIP for target goal: {money_full(required_sip) if np.isfinite(required_sip) else 'Not calculated'}

FINANCIFY VERDICT
{verdict_title}
{verdict_text}

WEALTH HABIT SCORE
{score}/100

PLAN NOTES
- """ + "\n- ".join(notes) + """

Educational disclaimer: This calculator is for learning and planning only. It is not investment advice, a return guarantee, or a recommendation to invest in any specific product. Market returns are uncertain. Please do your own research or consult a qualified financial adviser.
""".strip()


def build_seo_draft(name, monthly_sip, lump_sum, years, annual_return, annual_step_up, inflation_rate, goal_amount, vals, required_sip):
    title = "SIP + Wealth Builder Calculator: Estimate Future Wealth with Step-Up SIP"
    meta = "Use this free SIP and wealth builder calculator to estimate future corpus, step-up SIP impact, inflation-adjusted wealth and goal-based required SIP."
    excerpt = "Estimate how monthly SIP, annual step-up, lump sum, expected return and inflation can shape your long-term wealth journey."
    body = f"""
# SIP + Wealth Builder Calculator: Estimate Future Wealth with Step-Up SIP

Most SIP calculators show one final number. But real wealth building is not only about a monthly investment amount. It depends on time, return expectation, annual step-up, inflation and discipline.

This free Financify SIP + Wealth Builder Calculator helps you estimate how your monthly SIP can grow over time and how much your future corpus may be worth after inflation.

## Inputs Used

- Monthly SIP: {money_full(monthly_sip)}
- Initial lump sum: {money_full(lump_sum)}
- Investment period: {years} years
- Expected yearly return: {annual_return*100:.2f}%
- Annual SIP increase: {annual_step_up*100:.2f}%
- Inflation rate: {inflation_rate*100:.2f}%
- Target goal: {money_full(goal_amount) if goal_amount > 0 else 'Not entered'}

## Estimated Result

Based on these assumptions, the estimated future corpus is around {money_full(vals['corpus'])}. Out of this, the total invested amount is around {money_full(vals['invested'])}, and the estimated gain is around {money_full(vals['gain'])}.

After adjusting for inflation, the future corpus may feel closer to {money_full(vals['real_corpus'])} in today's purchasing power.

## Step-Up SIP Impact

A step-up SIP increases your monthly investment every year. In this calculation, annual step-up is included in the final corpus estimate.

## Goal Planning

If your target is {money_full(goal_amount) if goal_amount > 0 else 'a specific future amount'}, the required monthly SIP under these assumptions is around {money_full(required_sip) if np.isfinite(required_sip) else 'not calculated'}.

## Important Reminder

SIP does not guarantee returns. The actual outcome depends on market performance, time horizon, asset allocation, investor behaviour and costs. Use this calculator for planning, not prediction.

## Disclaimer

This calculator is for educational purposes only. It is not investment advice, a return guarantee, or a recommendation to invest in any specific financial product. Please do your own research or consult a qualified financial adviser.
""".strip()

    faq_schema = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is a SIP calculator?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A SIP calculator estimates the possible future value of monthly investments based on investment amount, time period and expected return."
      }
    },
    {
      "@type": "Question",
      "name": "What is step-up SIP?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A step-up SIP increases the monthly investment amount every year, usually as income grows. It can significantly improve long-term wealth creation."
      }
    },
    {
      "@type": "Question",
      "name": "Does SIP guarantee returns?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. SIP is an investment method, not a return guarantee. Actual returns depend on market performance and asset allocation."
      }
    }
  ]
}
</script>
""".strip()

    return title, meta, excerpt, body, faq_schema

# -------------------------
# Sidebar inputs
# -------------------------
with st.sidebar:
    st.markdown("### 🐝 Your Details")
    st.caption("Enter your numbers below. Keep optional fields as 0 if you do not want to use them.")

    name = st.text_input("Name (optional)", value="Financify Learner")
    age = st.slider("Current age", min_value=18, max_value=70, value=28, step=1)
    monthly_income = st.number_input("Monthly income (optional)", min_value=0.0, value=80000.0, step=5000.0)

    st.divider()
    st.markdown("### SIP Plan")
    monthly_sip = st.number_input("Monthly SIP", min_value=0.0, value=10000.0, step=1000.0)
    lump_sum = st.number_input("One-time investment (optional)", min_value=0.0, value=0.0, step=10000.0)
    years = st.slider("Investment period (years)", min_value=1, max_value=40, value=20, step=1)
    annual_step_up = st.slider("Annual SIP increase", min_value=0.0, max_value=30.0, value=10.0, step=0.5) / 100

    st.divider()
    st.markdown("### Return Assumptions")
    annual_return = st.slider("Expected yearly return", min_value=1.0, max_value=25.0, value=12.0, step=0.5) / 100
    inflation_rate = st.slider("Inflation rate", min_value=0.0, max_value=12.0, value=6.0, step=0.5) / 100
    fee_drag = st.slider("Annual expense ratio (optional)", min_value=0.0, max_value=3.0, value=0.5, step=0.1) / 100

    st.divider()
    st.markdown("### Target Goal")
    goal_amount = st.number_input("Target amount (optional)", min_value=0.0, value=10_000_000.0, step=100_000.0)

    st.markdown("---")
    st.markdown(f"[🔓 Upgrade to Financify Pro]({SURECART_CHECKOUT_URL})")
    st.markdown(f"[🧰 Explore all tools]({TOOLS_PAGE_URL})")

# -------------------------
# Hero
# -------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">🐝 Free Financify Tool • SIP Planner</div>
        <div class="hero-title">SIP + Wealth Builder Calculator</div>
        <div class="hero-subtitle">
            Enter SIP, one-time investment, yearly return, inflation and target amount. Get estimated corpus, real value, goal progress,
            required SIP and a simple downloadable report.
        </div>
        <div class="hero-pills">
            <div class="pill">SIP Growth</div>
            <div class="pill">Real Value</div>
            <div class="pill">Goal SIP</div>
            <div class="pill">Plan Score</div>
            <div class="pill">Report</div>
            <div class="pill">SEO Draft</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Calculations
# -------------------------
base_vals, base_milestones, base_df = final_values(
    monthly_sip, lump_sum, years, annual_return, annual_step_up, inflation_rate, fee_drag
)
cons_vals, _, cons_df = final_values(
    monthly_sip, lump_sum, years, max(annual_return - 0.03, 0.01), annual_step_up, inflation_rate, fee_drag
)
opt_vals, _, opt_df = final_values(
    monthly_sip, lump_sum, years, annual_return + 0.03, annual_step_up, inflation_rate, fee_drag
)
required_sip = required_sip_for_goal(goal_amount, lump_sum, years, annual_return, annual_step_up, inflation_rate, fee_drag) if goal_amount > 0 else np.nan
score, notes = wealth_score(monthly_sip, monthly_income, years, annual_return, annual_step_up, inflation_rate, base_vals["corpus"], goal_amount)
verdict_title, verdict_text = bee_verdict(score, base_vals["corpus"], goal_amount, base_vals["real_corpus"], base_vals["invested"])

savings_rate = monthly_sip / monthly_income if monthly_income > 0 else np.nan
wealth_multiplier = base_vals["corpus"] / base_vals["invested"] if base_vals["invested"] > 0 else np.nan
real_loss = base_vals["corpus"] - base_vals["real_corpus"]
goal_gap = goal_amount - base_vals["corpus"] if goal_amount > 0 else np.nan
retire_age = age + years

# -------------------------
# Top metrics
# -------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Estimated Corpus</div>
            <div class="metric-value">{money(base_vals['corpus'])}</div>
            <div class="metric-help">Estimated amount after {years} years.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Invested</div>
            <div class="metric-value">{money(base_vals['invested'])}</div>
            <div class="metric-help">Your total contribution.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Estimated Gains</div>
            <div class="metric-value">{money(base_vals['gain'])}</div>
            <div class="metric-help">Estimated gain on investment.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Real Value Today</div>
            <div class="metric-value">{money(base_vals['real_corpus'])}</div>
            <div class="metric-help">Value in today's money.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------
# Verdict + chart
# -------------------------
left, right = st.columns([0.95, 1.35], gap="large")
with left:
    st.markdown(
        f"""
        <div class="dark-card">
            <div class="section-title-light">{verdict_title}</div>
            <div class="light-text">{verdict_text}</div>
            <br>
            <span class="mini-badge">Habit Score: {score}/100</span>
            <span class="mini-badge">Savings Rate: {pct(savings_rate)}</span>
            <span class="mini-badge">Wealth Multiple: {wealth_multiplier:.2f}x</span>
            <span class="mini-badge">Age at Goal: {retire_age}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="glass-card">
            <div class="section-title">🎯 Goal SIP</div>
            <div class="section-subtitle">Monthly SIP needed to reach your target.</div>
            <div class="metric-label">Required SIP for target</div>
            <div class="metric-value">{money(required_sip) if np.isfinite(required_sip) else '—'}</div>
            <div class="metric-help">Based on the same inputs.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if goal_amount > 0:
        st.plotly_chart(make_goal_gauge(base_vals["corpus"], goal_amount), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)

with right:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">📈 Wealth Flight Path</div>
            <div class="section-subtitle">Projected corpus for conservative, base and optimistic returns.</div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(make_wealth_chart({"Conservative": cons_df, "Base": base_df, "Optimistic": opt_df}), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Mission cards
# -------------------------
st.markdown(
    """
    <div class="glass-card">
        <div class="section-title">🍯 Money Bee Mission Control</div>
        <div class="section-subtitle">Quick snapshot of your plan.</div>
    """,
    unsafe_allow_html=True,
)
mc1, mc2, mc3, mc4 = st.columns(4)
mc1.metric("Final Monthly SIP", money(base_vals["last_sip"]))
mc2.metric("Inflation Impact", money(real_loss))
mc3.metric("Goal Gap / Surplus", money(-goal_gap) if goal_amount > 0 and goal_gap < 0 else money(goal_gap) if goal_amount > 0 else "—")
mc4.metric("Retirement/Goal Age", f"{retire_age} yrs")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Wealth Table",
    "🍯 Corpus Breakup",
    "🪜 SIP Ladder",
    "🏁 Milestones",
    "📤 Share Report",
    "📝 SEO Draft",
])

with tab1:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Year-by-Year Wealth Table</div>
            <div class="section-subtitle">Year-wise projection of your plan.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    table_df = base_df.copy()
    table_df["Year"] = table_df["Year"].map(lambda x: f"{x:.0f}")
    for col in ["Monthly SIP", "Total Invested", "Estimated Corpus", "Estimated Gain", "Inflation Adjusted Corpus"]:
        table_df[col] = table_df[col].map(money_full)
    st.dataframe(table_df[["Year", "Monthly SIP", "Total Invested", "Estimated Corpus", "Estimated Gain", "Inflation Adjusted Corpus"]], use_container_width=True, hide_index=True)

    csv = base_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download year-wise CSV", data=csv, file_name="financify_sip_wealth_table.csv", mime="text/csv")

with tab2:
    c1, c2 = st.columns([1.1, 0.9], gap="large")
    with c1:
        st.plotly_chart(make_breakup_chart(base_vals["invested"], base_vals["gain"]), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)
    with c2:
        st.markdown(
            f"""
            <div class="dark-card">
                <div class="section-title-light">Corpus Summary</div>
                <div class="light-text">
                    Total invested: {money(base_vals['invested'])}. Estimated corpus: {money(base_vals['corpus'])}.
                    <br><br>
                    Wealth multiple: <b>{wealth_multiplier:.2f}x</b>. Inflation-adjusted value: {money(base_vals['real_corpus'])}.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab3:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Step-Up SIP Ladder</div>
            <div class="section-subtitle">Shows how your monthly SIP changes every year.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(make_stepup_chart(base_df), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)

with tab4:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Honey Milestone Timeline</div>
            <div class="section-subtitle">Estimated year in which each milestone is reached.</div>
        """,
        unsafe_allow_html=True,
    )
    st.text(milestone_text(base_milestones))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="dark-card">
            <div class="section-title-light">Wealth Habit Notes</div>
            <div class="light-text">
        """,
        unsafe_allow_html=True,
    )
    for note in notes:
        st.markdown(f"- {note}")
    st.markdown("</div></div>", unsafe_allow_html=True)

with tab5:
    report = build_report(name, age, monthly_sip, lump_sum, monthly_income, years, annual_return, annual_step_up, inflation_rate, fee_drag, goal_amount, base_vals, score, verdict_title, verdict_text, notes, required_sip)
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Shareable Wealth Mini Report</div>
            <div class="section-subtitle">Copy or download your summary.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_area("Copy report", value=report, height=390)
    st.download_button("⬇️ Download mini report", data=report, file_name="financify_sip_wealth_builder_report.txt", mime="text/plain")

    share_text = f"I used Financify SIP + Wealth Builder. My estimated corpus: {money(base_vals['corpus'])}, real value: {money(base_vals['real_corpus'])}. Try the free tool: {TOOLS_PAGE_URL}"
    whatsapp_url = f"https://wa.me/?text={quote_plus(share_text)}"
    twitter_url = f"https://twitter.com/intent/tweet?text={quote_plus(share_text)}"
    st.markdown(f"[📲 Share on WhatsApp]({whatsapp_url})  &nbsp;&nbsp; [𝕏 Share on X]({twitter_url})", unsafe_allow_html=True)

with tab6:
    title, meta, excerpt, body, faq_schema = build_seo_draft(name, monthly_sip, lump_sum, years, annual_return, annual_step_up, inflation_rate, goal_amount, base_vals, required_sip)
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">SEO Article Draft Generator</div>
            <div class="section-subtitle">Use this draft under the tool on WordPress.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_input("SEO title", value=title)
    st.text_area("Meta description", value=meta, height=80)
    st.text_area("Excerpt", value=excerpt, height=80)
    st.text_area("Article draft", value=body, height=520)
    st.text_area("Optional FAQ schema", value=faq_schema, height=260)

# -------------------------
# CTA + disclaimer
# -------------------------
st.markdown(
    f"""
    <div class="cta-card">
        <h3>Want to connect your wealth plan with better investing tools?</h3>
        <p>
        Plan your SIP journey here. Use Financify Pro for stock quality checks, intrinsic value, DCF, market cycle reading and risk filters.
        </p>
        <p><b>Free:</b> SIP planning. <b>Pro:</b> deeper investing tools.</p>
        <p>👉 <a href="{SURECART_CHECKOUT_URL}" target="_blank" style="color:#111;font-weight:950;">Upgrade to Financify Pro</a> &nbsp; | &nbsp;
        <a href="{TOOLS_PAGE_URL}" target="_blank" style="color:#111;font-weight:950;">Explore all Financify tools</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="warning-box">
    <b>Educational disclaimer:</b> This calculator is for learning and planning only. It is not investment advice, a return guarantee, or a recommendation to invest in any specific product. SIP returns are market-linked and uncertain. Please do your own research or consult a qualified financial adviser before making financial decisions.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer-note">🐝 Financify • Madness of Money Bees • Free SIP planning tool for practical finance learners</div>
    """,
    unsafe_allow_html=True,
)
