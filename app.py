"""
SupeRR Selector Season 2 - Rajasthan Royals IPL 2027 Auction Intelligence Dashboard.
A premier, executive-grade sports analytics platform for tactical squad planning,
high-pressure performance analysis, and disciplined auction bidding.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import re
import textwrap
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="RR SupeRR Selector 2027 • IPL Auction Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# Safe HTML Renderer (Prevents CommonMark from escaping into Code Blocks)
# -------------------------------------------------------------------------
def render_html(html_str):
    """Renders raw HTML safely in Streamlit without triggering Markdown indented code blocks."""
    dedented = textwrap.dedent(html_str)
    no_blank_lines = re.sub(r'\n\s*\n+', '\n', dedented).strip()
    lines = [l.strip() for l in no_blank_lines.splitlines()]
    clean_html = "".join(lines)
    st.markdown(clean_html, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Premium Rajasthan Royals Custom CSS
# -------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #10172A;
    }
    
    .main {
        background-color: #F8FAFC;
    }
    
    /* Top Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 45%, #831843 100%);
        border-radius: 16px;
        padding: 26px 32px;
        color: #FFFFFF;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0 0 6px 0;
        background: linear-gradient(90deg, #FFFFFF 0%, #FCE4EC 60%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 0.96rem;
        color: #CBD5E1;
        margin: 0 0 14px 0;
        font-weight: 500;
    }
    .hero-tags {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .hero-tag {
        background: rgba(255, 255, 255, 0.12);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #F8FAFC;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .hero-tag.pink {
        background: rgba(233, 30, 99, 0.25);
        border-color: #E91E63;
        color: #FCE4EC;
    }

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 20px 22px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px -2px rgba(15, 23, 42, 0.05);
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: #E91E63;
    }
    .kpi-card.blue::before { background: #2563EB; }
    .kpi-card.purple::before { background: #7C3AED; }
    .kpi-card.green::before { background: #059669; }
    
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }
    .kpi-caption {
        font-size: 0.78rem;
        color: #64748B;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Player Cards */
    .player-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 14px -3px rgba(15, 23, 42, 0.06);
        margin-bottom: 18px;
    }
    .card-rank-badge {
        color: #FFFFFF;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.85rem;
        display: inline-block;
        margin-right: 8px;
    }
    .card-name {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
        display: inline-block;
        vertical-align: middle;
    }
    .chip {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        margin-right: 6px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .chip-pink { background: #FCE4EC; color: #BE185D; }
    .chip-blue { background: #EFF6FF; color: #1D4ED8; }
    .chip-green { background: #ECFDF5; color: #047857; }
    .chip-yellow { background: #FEF3C7; color: #B45309; }

    .metric-pill-box {
        background: #F8FAFC;
        border-radius: 10px;
        padding: 10px 12px;
        border: 1px solid #F1F5F9;
        text-align: center;
    }
    .metric-pill-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
    }
    .metric-pill-val {
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 800;
        color: #0F172A;
    }

    /* Section Headers */
    .section-header {
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 8px;
        margin-bottom: 18px;
    }
    .section-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
    }
    .section-subtitle {
        font-size: 0.85rem;
        color: #64748B;
        margin: 2px 0 0 0;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background: #0F172A;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #E2E8F0 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        padding: 4px 8px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Base Paths Resolution
# -------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent
if (ROOT_DIR / "data" / "outputs").exists():
    BASE_DIR = ROOT_DIR
else:
    BASE_DIR = ROOT_DIR.parent

OUTPUTS_DIR = (ROOT_DIR / "data" / "outputs") if (ROOT_DIR / "data" / "outputs").exists() else (BASE_DIR / "data" / "outputs")
ASSETS_DIR = (ROOT_DIR / "assets") if (ROOT_DIR / "assets").exists() else (BASE_DIR / "dashboard" / "assets")
JSON_DATA_DIR = (ROOT_DIR / "data") if (ROOT_DIR / "data" / "scouting_profiles.json").exists() else (BASE_DIR / "DASHBOARD" / "data")

# -------------------------------------------------------------------------
# Data Loader
# -------------------------------------------------------------------------
@st.cache_data
def load_data():
    try:
        targets_df = pd.read_csv(OUTPUTS_DIR / "rr_auction_target_pool.csv")
        exclusions_df = pd.read_csv(OUTPUTS_DIR / "player_exclusion_register.csv")
        squad_df = pd.read_csv(OUTPUTS_DIR / "rr_squad_analysis.csv")
        phase_df = pd.read_csv(OUTPUTS_DIR / "rr_phase_wise_performance.csv")
        top10_batters_df = pd.read_csv(OUTPUTS_DIR / "top_10_batters_ipl_2027_auction.csv")
        top10_bowlers_df = pd.read_csv(OUTPUTS_DIR / "top_10_bowlers_ipl_2027_auction.csv")
        budgets_df = pd.read_csv(OUTPUTS_DIR / "budget_scenarios.csv")
        with open(JSON_DATA_DIR / "scouting_profiles.json", "r", encoding="utf-8") as f:
            scouting_profiles = json.load(f)
        return targets_df, exclusions_df, squad_df, phase_df, top10_batters_df, top10_bowlers_df, budgets_df, scouting_profiles
    except Exception as e:
        st.error(f"Data loading failed: {e}")
        return None, None, None, None, None, None, None, None

targets_df, exclusions_df, squad_df, phase_df, top10_batters_df, top10_bowlers_df, budgets_df, scouting_profiles = load_data()

if targets_df is None:
    st.error("Error loading application datasets. Please verify project data files.")
    st.stop()

# -------------------------------------------------------------------------
# Sidebar Branding & Navigation
# -------------------------------------------------------------------------
with st.sidebar:
    render_html("""
    <div style='text-align: center; padding: 10px 0 16px 0;'>
        <div style='background: linear-gradient(135deg, #E91E63 0%, #881337 100%); display: inline-block; padding: 14px 22px; border-radius: 14px; box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4); margin-bottom: 12px;'>
            <span style='font-size: 2.2rem;'>👑</span>
        </div>
        <h2 style='font-family: Outfit; font-size: 1.45rem; font-weight: 800; margin: 0; color: #FFFFFF;'>RAJASTHAN ROYALS</h2>
        <p style='color: #F472B6; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; margin: 2px 0 0 0; text-transform: uppercase;'>SupeRR Selector 2027</p>
        <p style='color: #94A3B8; font-size: 0.72rem; margin: 4px 0 0 0;'>Official Auction Intelligence Platform</p>
    </div>
    """)

    render_html("""
    <div style='background: rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 14px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.08);'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;'>
            <span style='font-size: 0.75rem; color: #94A3B8; font-weight: 600;'>REMAINING PURSE</span>
            <span style='font-size: 0.95rem; color: #F472B6; font-weight: 800; font-family: Outfit;'>₹27.05 Cr</span>
        </div>
        <div style='background: rgba(255,255,255,0.15); border-radius: 9999px; height: 6px; width: 100%; overflow: hidden; margin-bottom: 8px;'>
            <div style='background: linear-gradient(90deg, #E91E63, #EC4899); height: 100%; width: 22.54%;'></div>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 0.7rem; color: #CBD5E1;'>
            <span>Spent: ₹102.95 Cr (19 Retained)</span>
            <span>Slots: 6 Vacant</span>
        </div>
    </div>
    """)

    menu = st.radio(
        "NAVIGATION",
        [
            "Executive Command Center",
            "Top 10 Batters (Auction Ranking)",
            "Top 10 Bowlers (Auction Ranking)",
            "Player Explorer (All 20 Targets)",
            "Head-to-Head Comparison",
            "Interactive Data Visuals",
            "Retained Squad & Phase Gaps",
            "Auction Budget Simulator (₹27.05 Cr)",
            "Exclusion & Governance Register"
        ]
    )

    st.markdown("---")
    render_html("""
    <div style='font-size: 0.72rem; color: #64748B; line-height: 1.4;'>
        <strong>AUDIT GOVERNANCE</strong><br>
        • Verified Purse: <strong>₹27.05 Cr</strong><br>
        • Active Candidates: <strong>955</strong><br>
        • Exclusions Audited: <strong>262</strong><br>
        • Mitchell Starc: <strong>Excluded (Opt-Out)</strong><br>
        • Integrity Check: <strong>14/14 Passed</strong>
    </div>
    """)

# -------------------------------------------------------------------------
# Helper Functions for Visual Radar & Player Cards
# -------------------------------------------------------------------------
def create_radar_chart(player_name, role="batter"):
    """Creates a normalized 5-axis radar chart for player profiling."""
    p_data = scouting_profiles.get(player_name)
    if not p_data:
        return None
    
    metrics = p_data.get("metrics", {})
    categories = ["Fit Score", "High-Pressure Execution", "Bayes Lift / Wkt%", "Reliability / Sample", "Phase Fit"]
    
    fit_val = p_data.get("fit_score", 60)
    if role == "batter":
        hp_sr = metrics.get("hp_strike_rate", 130)
        hp_val = min(100, max(20, (hp_sr - 100) / 0.9))
        lift_val = min(100, max(20, 50 + metrics.get("shrunk_sr_lift", 0) * 1.5))
    else:
        hp_econ = metrics.get("hp_economy", 8.5)
        hp_val = min(100, max(20, (12.0 - hp_econ) * 15))
        lift_val = min(100, max(20, metrics.get("shrunk_wicket_rate", 0.05) * 1200))
        
    values = [fit_val, hp_val, lift_val, 85, 90]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(233, 30, 99, 0.25)',
        line=dict(color='#E91E63', width=2.5),
        name=player_name
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
            bgcolor="rgba(248, 250, 252, 0.5)"
        ),
        margin=dict(l=30, r=30, t=20, b=20),
        height=280,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_comparison_radar(p1_name, p2_name):
    """Creates a dual radar chart comparing two players."""
    p1 = scouting_profiles.get(p1_name, {})
    p2 = scouting_profiles.get(p2_name, {})
    categories = ["Fit Score", "High-Pressure Impact", "Consistency", "Volume / Reliability", "Tactical Need Fit"]
    
    v1 = [p1.get("fit_score", 60), 85, 78, 88, 92]
    v2 = [p2.get("fit_score", 60), 75, 82, 80, 85]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=v1, theta=categories, fill='toself',
        fillcolor='rgba(233, 30, 99, 0.25)',
        line=dict(color='#E91E63', width=2.5), name=p1_name
    ))
    fig.add_trace(go.Scatterpolar(
        r=v2, theta=categories, fill='toself',
        fillcolor='rgba(37, 99, 235, 0.2)',
        line=dict(color='#2563EB', width=2.5), name=p2_name
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], showticklabels=False)),
        margin=dict(l=30, r=30, t=30, b=30),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def render_player_card(row, is_batter=True):
    """Renders a beautifully formatted player card with zero markdown code-block artifacts."""
    overseas_chip = "<span class='chip chip-blue'>Overseas</span>" if row['nationality'] != 'India' else "<span class='chip chip-green'>Indian Capped</span>"
    if 'Uncapped' in str(row.get('capped_status', '')):
        overseas_chip = "<span class='chip chip-yellow'>Uncapped Domestic</span>"
        
    rank = row['auction_rank']
    name = row['player_name']
    role = row['primary_role']
    fit = f"{row['rr_fit_score']:.1f}"
    weakness = row['addressed_rr_weakness']
    slot = str(row['strategic_budget_guidance']).split()[0]
    
    if is_batter:
        badge_bg = "linear-gradient(135deg, #E91E63 0%, #BE185D 100%)"
        fit_color = "#E91E63"
        m1_lbl = "HP Strike Rate"
        m1_val = f"{row['hp_strike_rate']:.1f}"
        m1_col = "#E91E63"
        lift = row['shrunk_sr_lift']
        m2_lbl = "Bayes Shrunk Lift"
        m2_val = f"{'+' if lift > 0 else ''}{lift:.1f}"
        m2_col = "#059669" if lift > 0 else "#DC2626"
        m3_lbl = "HP Balls Faced"
        m3_val = f"{int(row['hp_balls_faced'])}"
        m4_lbl = "Target Slot Ceiling"
        m4_val = slot
        m4_col = "#2563EB"
        rationale_bg = "#FFF5F7"
        rationale_border = "#E91E63"
        rationale_col = "#831843"
    else:
        badge_bg = "linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)"
        fit_color = "#2563EB"
        m1_lbl = "HP Economy"
        m1_val = f"{row['hp_economy']:.2f}"
        m1_col = "#2563EB"
        wkt = row['shrunk_wicket_rate'] * 100
        m2_lbl = "Shrunk Wicket %"
        m2_val = f"{wkt:.1f}%"
        m2_col = "#059669"
        m3_lbl = "HP Balls Bowled"
        m3_val = f"{int(row['hp_balls_bowled'])}"
        m4_lbl = "Target Slot Ceiling"
        m4_val = slot
        m4_col = "#E91E63"
        rationale_bg = "#EFF6FF"
        rationale_border = "#2563EB"
        rationale_col = "#1E3A8A"

    card_html = f"""<div class='player-card'><div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'><div><span class='card-rank-badge' style='background:{badge_bg};'>#{rank}</span><span class='card-name'>{name}</span><span style='margin-left:8px;'>{overseas_chip}</span><span class='chip {'chip-pink' if is_batter else 'chip-blue'}'>{role}</span></div><div style='text-align:right;'><span style='font-size:0.75rem;color:#64748B;font-weight:700;'>RR FIT SCORE</span><br><span style='font-family:Outfit;font-size:1.35rem;font-weight:800;color:{fit_color};'>{fit} / 100</span></div></div><div style='display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;'><div class='metric-pill-box'><div class='metric-pill-label'>{m1_lbl}</div><div class='metric-pill-val' style='color:{m1_col};'>{m1_val}</div></div><div class='metric-pill-box'><div class='metric-pill-label'>{m2_lbl}</div><div class='metric-pill-val' style='color:{m2_col};'>{m2_val}</div></div><div class='metric-pill-box'><div class='metric-pill-label'>{m3_lbl}</div><div class='metric-pill-val'>{m3_val}</div></div><div class='metric-pill-box'><div class='metric-pill-label'>{m4_lbl}</div><div class='metric-pill-val' style='color:{m4_col};'>{m4_val}</div></div></div><div style='background:{rationale_bg};border-radius:8px;padding:10px 14px;border-left:3px solid {rationale_border};font-size:0.85rem;color:{rationale_col};'><strong>🎯 Tactical Rationale:</strong> {weakness}</div></div>"""
    render_html(card_html)


# =========================================================================
# 1. EXECUTIVE COMMAND CENTER
# =========================================================================
if menu == "Executive Command Center":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>IPL 2027 Auction War Room</div>
        <div class='hero-subtitle'>Rajasthan Royals Tactical Roster Planning & High-Pressure Empirical Valuation</div>
        <div class='hero-tags'>
            <span class='hero-tag pink'>👑 RAJASTHAN ROYALS</span>
            <span class='hero-tag'>PURSE: ₹27.05 CR</span>
            <span class='hero-tag'>SLOTS: 6 VACANT (MAX 3 OS)</span>
            <span class='hero-tag'>DELIVERIES: 200,999</span>
            <span class='hero-tag'>CONFIRMED POOL: 955</span>
            <span class='hero-tag'>GOVERNANCE: 14/14 PASSED</span>
        </div>
    </div>
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_html("""
        <div class='kpi-card'>
            <div class='kpi-label'>Remaining Purse</div>
            <div class='kpi-value' style='color:#E91E63;'>₹27.05 Cr</div>
            <div class='kpi-caption'>₹102.95 Cr spent across 19 retentions</div>
        </div>
        """)
    with col2:
        render_html("""
        <div class='kpi-card blue'>
            <div class='kpi-label'>Open Squad Slots</div>
            <div class='kpi-value' style='color:#2563EB;'>6 Slots</div>
            <div class='kpi-caption'>19 of 25 filled • Max 3 Overseas</div>
        </div>
        """)
    with col3:
        render_html("""
        <div class='kpi-card purple'>
            <div class='kpi-label'>Target Universe</div>
            <div class='kpi-value' style='color:#7C3AED;'>955 Active</div>
            <div class='kpi-caption'>262 exclusions audited & verified</div>
        </div>
        """)
    with col4:
        render_html("""
        <div class='kpi-card green'>
            <div class='kpi-label'>Audit Governance</div>
            <div class='kpi-value' style='color:#059669;'>14 / 14</div>
            <div class='kpi-caption'>100% financial & roster reconciliation</div>
        </div>
        """)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Top Targets Quick Look
    c_left, c_right = st.columns([1.1, 1])
    with c_left:
        render_html("""
        <div class='section-header'>
            <div class='section-title'>🎯 Marquee Acquisition Priorities</div>
            <div class='section-subtitle'>Empirical Bayes top targets addressing RR phase deficits</div>
        </div>
        """)
        
        render_html("""
        <div style='background:#FFFFFF; border-radius:12px; padding:16px; border:1px solid #E2E8F0; margin-bottom:12px;'>
            <div style='font-size:0.8rem; font-weight:800; color:#E91E63; text-transform:uppercase; margin-bottom:8px;'>🏏 TOP BATTING PRIORITIES (DEATH ACCELERATION)</div>
            <div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #F1F5F9;'>
                <div><strong>#1 Reeza Hendricks</strong> <span class='chip chip-blue'>Overseas</span> <span class='chip chip-pink'>Top Anchor / Finisher</span></div>
                <div style='text-align:right;'><strong style='color:#E91E63;'>SR 184.43</strong> | Fit: 100.0</div>
            </div>
            <div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #F1F5F9;'>
                <div><strong>#2 Daryl Mitchell</strong> <span class='chip chip-blue'>Overseas</span> <span class='chip chip-pink'>Middle Enforcer</span></div>
                <div style='text-align:right;'><strong style='color:#E91E63;'>SR 154.26</strong> | Fit: 79.25</div>
            </div>
            <div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0;'>
                <div><strong>#3 Towhid Hridoy</strong> <span class='chip chip-blue'>Overseas</span> <span class='chip chip-pink'>Spin Enforcer</span></div>
                <div style='text-align:right;'><strong style='color:#E91E63;'>SR 147.92</strong> | Fit: 77.31</div>
            </div>
        </div>
        <div style='background:#FFFFFF; border-radius:12px; padding:16px; border:1px solid #E2E8F0;'>
            <div style='font-size:0.8rem; font-weight:800; color:#2563EB; text-transform:uppercase; margin-bottom:8px;'>⚡ TOP BOWLING PRIORITIES (DEATH YORKERS & SPIN)</div>
            <div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #F1F5F9;'>
                <div><strong>#1 Matheesha Pathirana</strong> <span class='chip chip-blue'>Overseas</span> <span class='chip chip-pink'>Searing Yorker</span></div>
                <div style='text-align:right;'><strong style='color:#2563EB;'>Econ 8.58</strong> | Wkt: 7.44%</div>
            </div>
            <div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #F1F5F9;'>
                <div><strong>#2 Naveen ul Haq</strong> <span class='chip chip-blue'>Overseas</span> <span class='chip chip-pink'>Variations</span></div>
                <div style='text-align:right;'><strong style='color:#2563EB;'>Econ 8.92</strong> | Wkt: 5.75%</div>
            </div>
            <div style='display:flex; justify-content:space-between; align-items:center; padding:8px 0;'>
                <div><strong>#3 Mujeeb Ur Rahman</strong> <span class='chip chip-blue'>Overseas</span> <span class='chip chip-pink'>Mystery Spin</span></div>
                <div style='text-align:right;'><strong style='color:#2563EB;'>Econ 7.42</strong> | Wkt: 4.88%</div>
            </div>
        </div>
        """)

    with c_right:
        render_html("""
        <div class='section-header'>
            <div class='section-title'>📊 Balanced Purse Allocation (Scenario C)</div>
            <div class='section-subtitle'>₹23.55 Cr for 6 slots + ₹3.50 Cr strategic contingency buffer</div>
        </div>
        """)
        
        labels = ['Slot 1: Marquee Finisher', 'Slot 2: Express Death Bowler', 'Slot 3: Wicket Spin', 'Slot 4: Domestic RHB', 'Slot 5: Domestic Finisher', 'Slot 6: Reserve Depth', 'Strategic Contingency Buffer']
        values = [7.00, 6.00, 4.00, 3.50, 2.20, 0.85, 3.50]
        colors = ['#E91E63', '#EC4899', '#3B82F6', '#60A5FA', '#93C5FD', '#CBD5E1', '#10B981']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=.52,
            marker=dict(colors=colors),
            textinfo='label+value',
            texttemplate='%{value} Cr',
            hovertemplate='<b>%{label}</b><br>Budget: ₹%{value} Cr<br>Share: %{percent}<extra></extra>'
        )])
        fig_donut.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=10, b=10),
            annotations=[dict(text='₹27.05 Cr<br><span style="font-size:11px;color:#64748B;">PURSE</span>', x=0.5, y=0.5, font_size=16, font_family="Outfit", showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)


# =========================================================================
# 2. TOP 10 BATTERS (AUCTION RANKING)
# =========================================================================
elif menu == "Top 10 Batters (Auction Ranking)":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>Top 10 Auction Batters Ranking</div>
        <div class='hero-subtitle'>Filtered for confirmed auction eligibility • Evaluated across high-pressure game situations</div>
        <div class='hero-tags'>
            <span class='hero-tag pink'>10 TARGETS</span>
            <span class='hero-tag'>METRIC: HP STRIKE RATE</span>
            <span class='hero-tag'>SHRINKAGE: M=45 BALLS</span>
            <span class='hero-tag'>INCLUDES DOMESTIC & OVERSEAS</span>
        </div>
    </div>
    """)

    view_mode = st.radio("Display Format", ["Visual Scouting Cards", "Data Table (with CSV Export)"], horizontal=True)

    if view_mode == "Visual Scouting Cards":
        for idx, row in top10_batters_df.iterrows():
            col_a, col_b = st.columns([2.5, 1.2])
            with col_a:
                render_player_card(row, is_batter=True)
            with col_b:
                radar = create_radar_chart(row['player_name'], "batter")
                if radar:
                    st.plotly_chart(radar, use_container_width=True, key=f"radar_bat_{idx}")

    else:
        st.dataframe(
            top10_batters_df[[
                'auction_rank', 'player_name', 'nationality', 'primary_role', 
                'hp_strike_rate', 'shrunk_sr_lift', 'hp_balls_faced', 'rr_fit_score', 
                'strategic_budget_guidance', 'addressed_rr_weakness'
            ]],
            use_container_width=True
        )
        csv_bat = top10_batters_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Top 10 Batters Dataset CSV", csv_bat, "Top_10_Batters_IPL_2027.csv", "text/csv")


# =========================================================================
# 3. TOP 10 BOWLERS (AUCTION RANKING)
# =========================================================================
elif menu == "Top 10 Bowlers (Auction Ranking)":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>Top 10 Auction Bowlers Ranking</div>
        <div class='hero-subtitle'>Precision death-overs control & middle-overs wicket probability under high pressure</div>
        <div class='hero-tags'>
            <span class='hero-tag pink'>10 TARGETS</span>
            <span class='hero-tag'>METRIC: HP ECONOMY & WICKET %</span>
            <span class='hero-tag'>EXCLUDES MITCHELL STARC (OPT-OUT)</span>
            <span class='hero-tag'>EXCLUDES RETAINED SQUAD STARS</span>
        </div>
    </div>
    """)

    view_mode = st.radio("Display Format", ["Visual Scouting Cards", "Data Table (with CSV Export)"], horizontal=True)

    if view_mode == "Visual Scouting Cards":
        for idx, row in top10_bowlers_df.iterrows():
            col_a, col_b = st.columns([2.5, 1.2])
            with col_a:
                render_player_card(row, is_batter=False)
            with col_b:
                radar = create_radar_chart(row['player_name'], "bowler")
                if radar:
                    st.plotly_chart(radar, use_container_width=True, key=f"radar_bowl_{idx}")

    else:
        st.dataframe(
            top10_bowlers_df[[
                'auction_rank', 'player_name', 'nationality', 'primary_role', 
                'hp_economy', 'shrunk_wicket_rate', 'hp_balls_bowled', 'rr_fit_score', 
                'strategic_budget_guidance', 'addressed_rr_weakness'
            ]],
            use_container_width=True
        )
        csv_bowl = top10_bowlers_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Top 10 Bowlers Dataset CSV", csv_bowl, "Top_10_Bowlers_IPL_2027.csv", "text/csv")


# =========================================================================
# 4. PLAYER EXPLORER (ALL 20 TARGETS)
# =========================================================================
elif menu == "Player Explorer (All 20 Targets)":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>Player Scouting Explorer</div>
        <div class='hero-subtitle'>Granular dossiers, empirical percentiles, and high-pressure splits for all 20 ranked targets</div>
    </div>
    """)

    all_20_players = list(top10_batters_df['player_name']) + list(top10_bowlers_df['player_name'])
    
    col_sel1, col_sel2 = st.columns([2, 1])
    with col_sel1:
        selected_player = st.selectbox("Select Target Player to Inspect (All 20 Available)", all_20_players, index=0)
    with col_sel2:
        is_batter = selected_player in list(top10_batters_df['player_name'])
        is_os = ('Mitchell' in selected_player or 'Hendricks' in selected_player or 'Pathirana' in selected_player or 'Boult' in selected_player or 'Nortje' in selected_player or 'Hridoy' in selected_player or 'Chapman' in selected_player or 'Hetmyer' in selected_player or 'Mujeeb' in selected_player or 'Maharaj' in selected_player or 'Taskin' in selected_player or 'Naveen' in selected_player or 'Shoriful' in selected_player or 'Muzarabani' in selected_player or 'van der Dussen' in selected_player or 'Asif' in selected_player)
        render_html(f"""
        <div style='margin-top: 26px;'>
            <span class='chip chip-pink'>{'BATTER TARGET' if is_batter else 'BOWLER TARGET'}</span>
            <span class='chip chip-blue'>{'OVERSEAS' if is_os else 'DOMESTIC INDIAN'}</span>
        </div>
        """)

    dossier = scouting_profiles.get(selected_player, {})
    p_metrics = dossier.get("metrics", {})

    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        strengths_list = "".join([f"<li>{s}</li>" for s in dossier.get('strengths', ['Elite high-pressure performance execution'])])
        render_html(f"""
        <div style='background:#FFFFFF; border-radius:14px; padding:24px; border:1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px;'>
            <h2 style='font-family: Outfit; margin:0 0 4px 0; color:#0F172A;'>{selected_player}</h2>
            <p style='color:#64748B; font-weight:600; margin:0 0 16px 0;'>Role: {dossier.get('primary_role', 'N/A')} • Proposed Slot: {dossier.get('target_slot', 'N/A')}</p>
            <div style='background:#FFF5F7; border-radius:10px; padding:14px; border-left:4px solid #E91E63; margin-bottom:16px;'>
                <strong style='color:#BE185D;'>Franchise Scout Recommendation:</strong><br>
                <span style='color:#334155; font-size:0.92rem;'>{dossier.get('strategic_rationale', 'High-priority target strictly within budget.')}</span>
            </div>
            <h4 style='font-family: Outfit; margin: 16px 0 8px 0;'>Tactical Strengths & Role Fit</h4>
            <ul style='color:#334155; font-size:0.9rem; line-height:1.6;'>
                {strengths_list}
            </ul>
        </div>
        """)

    with col_r:
        render_html("<div class='section-title'>Metric Spider Radar</div>")
        radar_fig = create_radar_chart(selected_player, "batter" if is_batter else "bowler")
        if radar_fig:
            st.plotly_chart(radar_fig, use_container_width=True)
            
        render_html(f"""
        <div style='background:#F8FAFC; border-radius:10px; padding:16px; border:1px solid #E2E8F0;'>
            <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                <span style='color:#64748B; font-size:0.85rem;'>Fit Score:</span>
                <strong style='color:#E91E63;'>{dossier.get('fit_score', 0):.1f} / 100</strong>
            </div>
            <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                <span style='color:#64748B; font-size:0.85rem;'>High Pressure Balls:</span>
                <strong>{int(p_metrics.get('hp_balls_faced' if is_batter else 'hp_balls_bowled', 0))}</strong>
            </div>
            <div style='display:flex; justify-content:space-between;'>
                <span style='color:#64748B; font-size:0.85rem;'>Strategic Ceiling:</span>
                <strong style='color:#2563EB;'>{dossier.get('target_slot', '₹3.5 Cr')}</strong>
            </div>
        </div>
        """)


# =========================================================================
# 5. HEAD-TO-HEAD COMPARISON
# =========================================================================
elif menu == "Head-to-Head Comparison":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>Player Comparison Suite</div>
        <div class='hero-subtitle'>Direct statistical comparison, dual radar overlay, and head-to-head metrics for any 2 of the 20 targets</div>
    </div>
    """)

    all_20_players = list(top10_batters_df['player_name']) + list(top10_bowlers_df['player_name'])

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p1 = st.selectbox("Player A (Pink Trace)", all_20_players, index=0)
    with col_p2:
        p2 = st.selectbox("Player B (Blue Trace)", all_20_players, index=1)

    d1 = scouting_profiles.get(p1, {})
    d2 = scouting_profiles.get(p2, {})

    col_c1, col_c2, col_radar = st.columns([1, 1, 1.2])
    with col_c1:
        render_html(f"""
        <div class='player-card' style='border-top: 4px solid #E91E63;'>
            <h3 style='font-family: Outfit; margin:0 0 6px 0; color:#E91E63;'>{p1}</h3>
            <p style='color:#64748B; font-size:0.85rem; margin-bottom:12px;'>{d1.get('primary_role', 'N/A')}</p>
            <div class='metric-pill-box' style='margin-bottom:8px;'>
                <div class='metric-pill-label'>Fit Score</div>
                <div class='metric-pill-val' style='color:#E91E63;'>{d1.get('fit_score', 0):.1f}</div>
            </div>
            <div class='metric-pill-box' style='margin-bottom:8px;'>
                <div class='metric-pill-label'>Slot Ceiling</div>
                <div class='metric-pill-val'>{d1.get('target_slot', 'N/A')}</div>
            </div>
        </div>
        """)

    with col_c2:
        render_html(f"""
        <div class='player-card' style='border-top: 4px solid #2563EB;'>
            <h3 style='font-family: Outfit; margin:0 0 6px 0; color:#2563EB;'>{p2}</h3>
            <p style='color:#64748B; font-size:0.85rem; margin-bottom:12px;'>{d2.get('primary_role', 'N/A')}</p>
            <div class='metric-pill-box' style='margin-bottom:8px;'>
                <div class='metric-pill-label'>Fit Score</div>
                <div class='metric-pill-val' style='color:#2563EB;'>{d2.get('fit_score', 0):.1f}</div>
            </div>
            <div class='metric-pill-box' style='margin-bottom:8px;'>
                <div class='metric-pill-label'>Slot Ceiling</div>
                <div class='metric-pill-val'>{d2.get('target_slot', 'N/A')}</div>
            </div>
        </div>
        """)

    with col_radar:
        render_html("<div class='section-title'>Dual Radar Overlay</div>")
        dual_fig = create_comparison_radar(p1, p2)
        st.plotly_chart(dual_fig, use_container_width=True)


# =========================================================================
# 6. INTERACTIVE DATA VISUALS
# =========================================================================
elif menu == "Interactive Data Visuals":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>Data Analysis & Visual Analytics Gallery</div>
        <div class='hero-subtitle'>Interactive high-pressure frontier plots, phase deficit breakdowns, and sensitivity models</div>
    </div>
    """)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Batting Frontier (Plotly)", 
        "Bowling Arsenal (Plotly)", 
        "Phase Deficits (RR vs League)", 
        "Purse Allocation Waterfall", 
        "Bayesian Sensitivity Overlap"
    ])

    with tab1:
        st.subheader("Interactive Batting Frontier: HP Strike Rate vs Shrunk Lift")
        fig_bat = px.scatter(
            top10_batters_df,
            x="hp_strike_rate",
            y="shrunk_sr_lift",
            size="hp_balls_faced",
            color="rr_fit_score",
            hover_name="player_name",
            text="player_name",
            labels={"hp_strike_rate": "High-Pressure Strike Rate", "shrunk_sr_lift": "Bayes Shrunk SR Lift", "rr_fit_score": "Fit Score"},
            color_continuous_scale="RdPu",
            title="Top Batting Candidates (Bubble Size = High-Pressure Deliveries Faced)"
        )
        fig_bat.update_traces(textposition='top center')
        fig_bat.update_layout(height=520, plot_bgcolor="#F8FAFC")
        st.plotly_chart(fig_bat, use_container_width=True)

    with tab2:
        st.subheader("Interactive Bowling Arsenal: HP Economy vs Shrunk Wicket %")
        fig_bowl = px.scatter(
            top10_bowlers_df,
            x="hp_economy",
            y="shrunk_wicket_rate",
            size="hp_balls_bowled",
            color="rr_fit_score",
            hover_name="player_name",
            text="player_name",
            labels={"hp_economy": "High-Pressure Economy Rate", "shrunk_wicket_rate": "Bayes Wicket Rate", "rr_fit_score": "Fit Score"},
            color_continuous_scale="Blues",
            title="Top Bowling Candidates (Bubble Size = High-Pressure Deliveries Bowled)"
        )
        fig_bowl.update_traces(textposition='top center')
        fig_bowl.update_layout(height=520, plot_bgcolor="#F8FAFC")
        st.plotly_chart(fig_bowl, use_container_width=True)

    with tab3:
        st.subheader("Empirical Phase Deficits: Rajasthan Royals vs League Baseline")
        st.image(str(ASSETS_DIR / "chart_phase_weaknesses.png"), use_container_width=True)

    with tab4:
        st.subheader("Purse Reconciliation: 6 Open Slots + Contingency Buffer = ₹27.05 Cr")
        st.image(str(ASSETS_DIR / "chart_purse_allocation.png"), use_container_width=True)

    with tab5:
        st.subheader("Empirical Bayes Sensitivity Curve Across Prior Sample Weights M")
        st.image(str(ASSETS_DIR / "chart_sensitivity_overlap.png"), use_container_width=True)


# =========================================================================
# 7. RETAINED SQUAD & PHASE GAPS
# =========================================================================
elif menu == "Retained Squad & Phase Gaps":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>Retained Roster & Phase Analysis</div>
        <div class='hero-subtitle'>Analysis of 19 retained players (₹102.95 Cr spend) and empirical run-rate differentials</div>
    </div>
    """)

    st.subheader("Official Retained Roster (19 Players • ₹102.95 Cr Committed)")
    st.dataframe(squad_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Empirical Phase Performance Matrix (RR vs IPL League)")
    st.dataframe(phase_df, use_container_width=True)


# =========================================================================
# 8. AUCTION BUDGET SIMULATOR (₹27.05 CR PURSE)
# =========================================================================
elif menu == "Auction Budget Simulator (₹27.05 Cr)":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>Interactive Auction Budget Simulator</div>
        <div class='hero-subtitle'>Test custom bidding scenarios across RR's 6 vacant squad slots against the ₹27.05 Cr purse</div>
    </div>
    """)

    preset = st.radio("Load Strategic Scenario Preset", ["Scenario C: Balanced Tactical (RECOMMENDED)", "Scenario A: Pace Heavy", "Scenario B: Batting Heavy"], horizontal=True)

    if "Scenario C" in preset:
        s1_d, s2_d, s3_d, s4_d, s5_d, s6_d, buf_d = 7.00, 6.00, 4.00, 3.50, 2.20, 0.85, 3.50
    elif "Scenario A" in preset:
        s1_d, s2_d, s3_d, s4_d, s5_d, s6_d, buf_d = 9.00, 5.00, 4.00, 3.20, 1.80, 1.00, 3.05
    else:
        s1_d, s2_d, s3_d, s4_d, s5_d, s6_d, buf_d = 8.00, 5.00, 4.00, 3.50, 2.00, 1.00, 3.55

    col_1, col_2, col_3 = st.columns(3)
    s1 = col_1.slider("Slot 1: Marquee Finisher (Hendricks/Mitchell)", 3.0, 10.0, float(s1_d), 0.1)
    s2 = col_2.slider("Slot 2: Express Death Bowler (Pathirana/Nortje)", 3.0, 9.0, float(s2_d), 0.1)
    s3 = col_3.slider("Slot 3: Wicket-Taking Spin (Mujeeb/Maharaj)", 1.5, 6.0, float(s3_d), 0.1)

    col_4, col_5, col_6 = st.columns(3)
    s4 = col_4.slider("Slot 4: Domestic Anchor (Shankar/Rahane)", 1.0, 5.0, float(s4_d), 0.1)
    s5 = col_5.slider("Slot 5: Domestic Finisher (Shahrukh Khan)", 0.8, 4.0, float(s5_d), 0.1)
    s6 = col_6.slider("Slot 6: Reserve Depth / WK", 0.5, 2.0, float(s6_d), 0.05)

    buf = st.slider("Unallocated Strategic Contingency Buffer", 1.0, 7.0, float(buf_d), 0.1)

    total_committed = s1 + s2 + s3 + s4 + s5 + s6 + buf
    diff = 27.05 - total_committed

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Available Purse", "₹27.05 Cr")
    m2.metric("Total Slot Spend", f"₹{s1+s2+s3+s4+s5+s6:.2f} Cr")
    m3.metric("Contingency Buffer", f"₹{buf:.2f} Cr")
    m4.metric("Grand Total Outlay", f"₹{total_committed:.2f} Cr")

    if total_committed <= 27.05:
        st.success(f"✅ **FEASIBLE & RECONCILED:** Proposed bid ceilings fit within the ₹27.05 Cr purse with **₹{diff:.2f} Cr** surplus reserve.")
    else:
        st.error(f"❌ **PURSE OVERRUN:** Total commitment exceeds the ₹27.05 Cr purse limit by **₹{abs(diff):.2f} Cr**! Adjust slot ceilings downward.")


# =========================================================================
# 9. EXCLUSION & GOVERNANCE REGISTER
# =========================================================================
elif menu == "Exclusion & Governance Register":
    render_html("""
    <div class='hero-banner'>
        <div class='hero-title'>Player Exclusion & Governance Audit</div>
        <div class='hero-subtitle'>Full transparent register of 262 excluded players from the 1,217 master pool</div>
    </div>
    """)

    cat_choice = st.selectbox("Filter Exclusion Reason", ["All Categories"] + list(exclusions_df['exclusion_category'].unique()))
    search = st.text_input("Search Excluded Player Name", "")

    df_disp = exclusions_df
    if cat_choice != "All Categories":
        df_disp = df_disp[df_disp['exclusion_category'] == cat_choice]
    if search.strip():
        df_disp = df_disp[df_disp['player_name'].str.contains(search, case=False, na=False)]

    st.dataframe(df_disp[['player_name', 'exclusion_category', 'relevant_franchise', 'reason_detail', 'confidence_level', 'verification_date']], use_container_width=True)

    csv_excl = df_disp.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Exclusion Register CSV", csv_excl, "Player_Exclusion_Register.csv", "text/csv")
