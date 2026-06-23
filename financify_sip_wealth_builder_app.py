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
    initial_sidebar_state="expanded",
)

SURECART_CHECKOUT_URL = "https://financify.blog/buy/financify-tools"
TOOLS_PAGE_URL = "https://financify.blog/tools"
BLOG_URL = "https://financify.blog"

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

    section[data-testid="stSidebar"] * {
        color: #fff8d8 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    section[data-testid="stSidebar"] [data-testid="stNumberInput"] * {
        color: #111 !important;
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
            notes.append("Savings rate is strong. The bee is collecting honey seriously.")
        elif savings_rate >= 0.20:
            score += 20
            notes.append("Savings rate is healthy. A small step-up can make it powerful.")
        elif savings_rate >= 0.10:
            score += 12
            notes.append("Savings rate is a good start, but the plan needs more fuel.")
        else:
            score += 5
            notes.append("Savings rate is low. Start small, but increase it with income growth.")
    else:
        score += 13
        notes.append("Add monthly income to judge savings discipline more clearly.")

    if years >= 20:
        score += 22
        notes.append("Time horizon is excellent. Compounding loves patience.")
    elif years >= 12:
        score += 16
        notes.append("Time horizon is decent. Staying invested matters now.")
    elif years >= 7:
        score += 10
        notes.append("Time horizon is medium. Return assumptions should be conservative.")
    else:
        score += 4
        notes.append("Short horizon. Market volatility can disturb the plan.")

    if annual_step_up >= 0.10:
        score += 18
        notes.append("Step-up SIP is powerful. This is the hidden wealth accelerator.")
    elif annual_step_up >= 0.05:
        score += 13
        notes.append("Step-up SIP is useful. Increase it when salary grows.")
    elif annual_step_up > 0:
        score += 8
        notes.append("Small step-up helps, but bigger annual increases can change the outcome.")
    else:
        score += 2
        notes.append("No step-up means inflation can slowly reduce your investing power.")

    if annual_return <= 0.10:
        score += 17
        notes.append("Return expectation is conservative and more realistic.")
    elif annual_return <= 0.13:
        score += 13
        notes.append("Return expectation is reasonable for equity-heavy long-term planning, but not guaranteed.")
    elif annual_return <= 0.16:
        score += 7
        notes.append("Return expectation is aggressive. Build safety into your plan.")
    else:
        score += 2
        notes.append("Return expectation is very aggressive. Do not let Excel honey fool you.")

    if inflation_rate >= 0.05:
        score += 8
        notes.append("Good: you are checking inflation-adjusted wealth, not just big nominal numbers.")
    else:
        score += 4
        notes.append("Inflation assumption is low. Real purchasing power may be overstated.")

    if goal_amount > 0:
        progress = final_corpus / goal_amount
        if progress >= 1:
            score += 10
            notes.append("Goal looks achievable with the current assumptions.")
        elif progress >= 0.75:
            score += 7
            notes.append("Goal is close. Increase SIP, step-up or time horizon.")
        else:
            score += 3
            notes.append("Goal needs stronger monthly investing, higher step-up or longer time.")
    else:
        score += 6
        notes.append("Add a target goal to turn this from a calculator into a money mission.")

    return min(score, 100), notes


def bee_verdict(score, final_corpus, goal_amount, real_corpus, invested):
    if score >= 80:
        title = "Wealth Builder Bee 🐝"
        text = "Your plan has strong compounding behaviour: decent discipline, time, and step-up power. Keep assumptions realistic and review once a year."
    elif score >= 60:
        title = "Growing Honey Pot 🍯"
        text = "This is a solid start. The easiest upgrade is usually not chasing higher returns, but increasing SIP step-up every year."
    elif score >= 40:
        title = "Baby Bee Portfolio 🌱"
        text = "The plan can work, but it needs more fuel. Increase monthly SIP gradually and avoid unrealistic return expectations."
    else:
        title = "Lazy Honey Alert ⚠️"
        text = "The plan is either too small, too short, or too dependent on high returns. Build a safer habit before dreaming of giant corpus numbers."

    if goal_amount > 0:
        if final_corpus >= goal_amount:
            text += " Your target goal is achievable under these assumptions."
        else:
            gap = goal_amount - final_corpus
            text += f" Your target has a gap of about {money(gap)} under these assumptions."

    if real_corpus < final_corpus * 0.55:
        text += " Notice how inflation reduces the real value of your future corpus. Nominal crores and real crores are not the same honey jar."

    if invested > 0 and final_corpus / invested < 1.5:
        text += " Compounding is still warming up; more time usually makes the curve bend upward."

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
Annual SIP step-up: {annual_step_up*100:.2f}%
Inflation assumption: {inflation_rate*100:.2f}%
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
- Expected annual return: {annual_return*100:.2f}%
- Annual SIP step-up: {annual_step_up*100:.2f}%
- Inflation assumption: {inflation_rate*100:.2f}%
- Target goal: {money_full(goal_amount) if goal_amount > 0 else 'Not entered'}

## Estimated Result

Based on these assumptions, the estimated future corpus is around {money_full(vals['corpus'])}. Out of this, the total invested amount is around {money_full(vals['invested'])}, and the estimated gain is around {money_full(vals['gain'])}.

After adjusting for inflation, the future corpus may feel closer to {money_full(vals['real_corpus'])} in today's purchasing power.

## Why Step-Up SIP Matters

A step-up SIP increases your monthly investment every year. This can be powerful because income usually grows over time. Instead of depending only on high returns, a step-up SIP improves the plan through better investing discipline.

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
    st.markdown("### 🐝 Wealth Mission Inputs")
    st.caption("Build the plan like a money bee: small honey drops, repeated for years.")

    name = st.text_input("Name optional", value="Financify Learner")
    age = st.slider("Current age", min_value=18, max_value=70, value=28, step=1)
    monthly_income = st.number_input("Monthly income optional", min_value=0.0, value=80000.0, step=5000.0)

    st.divider()
    st.markdown("### Investment Plan")
    monthly_sip = st.number_input("Monthly SIP", min_value=0.0, value=10000.0, step=1000.0)
    lump_sum = st.number_input("Initial lump sum optional", min_value=0.0, value=0.0, step=10000.0)
    years = st.slider("Investment period years", min_value=1, max_value=40, value=20, step=1)
    annual_step_up = st.slider("Annual SIP step-up", min_value=0.0, max_value=30.0, value=10.0, step=0.5) / 100

    st.divider()
    st.markdown("### Return & Reality")
    annual_return = st.slider("Expected annual return", min_value=1.0, max_value=25.0, value=12.0, step=0.5) / 100
    inflation_rate = st.slider("Inflation assumption", min_value=0.0, max_value=12.0, value=6.0, step=0.5) / 100
    fee_drag = st.slider("Expense / return drag", min_value=0.0, max_value=3.0, value=0.5, step=0.1) / 100

    st.divider()
    st.markdown("### Goal Mode")
    goal_amount = st.number_input("Target wealth goal optional", min_value=0.0, value=10_000_000.0, step=100_000.0)

    st.markdown("---")
    st.markdown(f"[🔓 Upgrade to Financify Pro]({SURECART_CHECKOUT_URL})")
    st.markdown(f"[🧰 Explore all tools]({TOOLS_PAGE_URL})")

# -------------------------
# Hero
# -------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">🐝 Free Financify Tool • Wealth Builder Lab</div>
        <div class="hero-title">SIP + Wealth Builder Calculator with <span>Step-Up Power</span></div>
        <div class="hero-subtitle">
            Go beyond a boring SIP number. See your wealth journey, real inflation-adjusted corpus, goal gap, required SIP,
            milestone timeline, savings habit score and shareable mini report — built to make money planning addictive and practical.
        </div>
        <div class="hero-pills">
            <div class="pill">Step-Up SIP Engine</div>
            <div class="pill">Inflation Reality Check</div>
            <div class="pill">Goal Back-Solver</div>
            <div class="pill">Wealth Habit Score</div>
            <div class="pill">Shareable Report</div>
            <div class="pill">SEO Draft Generator</div>
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
            <div class="metric-help">Future wealth at the end of {years} years.</div>
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
            <div class="metric-help">Your own money invested through SIP and lump sum.</div>
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
            <div class="metric-help">Estimated compounding gain, not guaranteed.</div>
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
            <div class="metric-help">Future corpus adjusted for inflation.</div>
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
            <div class="section-title">🎯 Goal Back-Solver</div>
            <div class="section-subtitle">Instead of asking 'how much will I get?', this asks 'how much should I invest?'</div>
            <div class="metric-label">Required SIP for target</div>
            <div class="metric-value">{money(required_sip) if np.isfinite(required_sip) else '—'}</div>
            <div class="metric-help">Assuming same return, step-up, lump sum, fees and time period.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if goal_amount > 0:
        st.plotly_chart(make_goal_gauge(base_vals["corpus"], goal_amount), use_container_width=True)

with right:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">📈 Wealth Flight Path</div>
            <div class="section-subtitle">The boring line becomes exciting after time. That curve is compounding doing its quiet job.</div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(make_wealth_chart({"Conservative": cons_df, "Base": base_df, "Optimistic": opt_df}), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Mission cards
# -------------------------
st.markdown(
    """
    <div class="glass-card">
        <div class="section-title">🍯 Money Bee Mission Control</div>
        <div class="section-subtitle">A premium snapshot that turns a normal SIP plan into a behaviour-driven wealth plan.</div>
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
            <div class="section-subtitle">Use this to show users how money grows slowly at first, then starts bending upward.</div>
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
        st.plotly_chart(make_breakup_chart(base_vals["invested"], base_vals["gain"]), use_container_width=True)
    with c2:
        st.markdown(
            f"""
            <div class="dark-card">
                <div class="section-title-light">The Compounding Truth</div>
                <div class="light-text">
                    You invest {money(base_vals['invested'])}. The plan estimates {money(base_vals['corpus'])}.
                    That means your money may become around <b>{wealth_multiplier:.2f}x</b> of invested capital under these assumptions.
                    <br><br>
                    But inflation changes the real feel of money. The inflation-adjusted value is closer to {money(base_vals['real_corpus'])} in today's purchasing power.
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
            <div class="section-subtitle">The simplest premium wealth habit: increase SIP when income increases.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.plotly_chart(make_stepup_chart(base_df), use_container_width=True)

with tab4:
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">Honey Milestone Timeline</div>
            <div class="section-subtitle">People love milestones. This makes the tool shareable and emotionally sticky.</div>
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
            <div class="section-subtitle">This is the hook layer. Users can copy/download and share their plan, bringing more visitors back to Financify.</div>
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
            <div class="section-subtitle">Use this under the tool on WordPress. Add your own Financify voice before publishing.</div>
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
        This free calculator helps users plan SIP and wealth goals. Financify Pro can guide them deeper with stock quality checks,
        intrinsic value calculators, DCF tools, market cycle reading, and risk filters.
        </p>
        <p><b>Free:</b> plan your wealth journey. <b>Pro:</b> analyse better opportunities and avoid noisy money traps.</p>
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
    <div class="footer-note">🐝 Financify • Madness of Money Bees • Free wealth planning tool for practical finance learners</div>
    """,
    unsafe_allow_html=True,
)
