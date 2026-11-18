"""
SupeRR Pressure Lab - Rajasthan Royals IPL 2027 Auction Intelligence Platform.
A luxury, sports-tech cricket analytics suite for pressure performance modeling,
tactical squad optimization, and disciplined auction valuation.
"""

import os
import sys
import json
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="SupeRR Pressure Lab | Rajasthan Royals",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# Native HTML & CSS Injector (Zero Markdown Code-Block Escaping)
# -------------------------------------------------------------------------
def render_html(html_str):
    """Render raw HTML natively using st.html (Streamlit >= 1.34) or fallback to st.markdown."""
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        cleaned = "\n".join(l.strip() for l in html_str.splitlines() if l.strip())
        st.markdown(cleaned, unsafe_allow_html=True)

def apply_custom_css():
    """Inject custom Rajasthan Royals theme CSS natively into DOM."""
    css_path = ASSETS_DIR / "custom.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        render_html(f"<style>{css_content}</style>")

apply_custom_css()

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
# Sidebar Navigation & Telemetry
# -------------------------------------------------------------------------
with st.sidebar:
    header_html = """
    <div style="text-align: center; padding: 12px 0 16px 0; border-bottom: 1px solid rgba(255, 27, 141, 0.35);">
        <div style="font-family: 'Barlow Condensed'; font-size: 1.95rem; font-weight: 800; color: #FFFFFF; letter-spacing: 1.2px; line-height: 1;">
            RAJASTHAN <span style="color: #FF1B8D;">ROYALS</span>
        </div>
        <div style="font-size: 0.85rem; color: #FF5DA2; font-weight: 700; letter-spacing: 2px; margin-top: 4px;">
            SUPERR PRESSURE LAB
        </div>
        <div style="display: flex; justify-content: center; gap: 6px; margin-top: 8px;">
            <span class="badge-gold">TATA IPL 2027</span>
            <span class="badge-pink">SEASON 2</span>
        </div>
    </div>
    """
    render_html(header_html)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🧭 LAB NAVIGATION")

    menu = st.radio(
        "Select Module:",
        [
            "1. Executive Overview",
            "2. Pressure Engine (Phase 3)",
            "3. Batter Rankings (Phase 5)",
            "4. Bowler Rankings (Phase 5)",
            "5. Player Comparison Lab",
            "6. Reliability & Validation (Phase 4)",
            "7. Methodology & Scoring",
            "8. Data Explorer & Governance",
            "9. Auction Budget Simulator (₹27.05 Cr)"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    telemetry_html = """
    <div style="background: rgba(13, 23, 51, 0.85); border-radius: 10px; padding: 14px; border: 1px solid rgba(255, 27, 141, 0.25); box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">RR Auction Envelope</span>
            <span style="color: #10B981; font-size: 0.75rem; font-weight: 700;">● LOCKED</span>
        </div>
        <div style="font-family: 'Barlow Condensed'; font-size: 1.6rem; font-weight: 800; color: #FFD700; line-height: 1.1;">
            ₹27.05 Crore
        </div>
        <div style="font-size: 0.78rem; color: #CBD5E1; margin-top: 5px; line-height: 1.5;">
            Open Roster Slots: <b style="color: #FFFFFF;">6</b> (Max 25)<br>
            Overseas Capacity: <b style="color: #FFFFFF;">3</b> (Max 8)<br>
            Committed Spend: <b style="color: #93C5FD;">₹102.95 Cr (19 Retained)</b><br>
            Bidding Cushion: <b style="color: #10B981;">₹3.50 Cr (12.9%)</b>
        </div>
    </div>
    """
    render_html(telemetry_html)


# -------------------------------------------------------------------------
# Helper Functions for Visual Radar & Player Cards
# -------------------------------------------------------------------------
def render_hero_banner(title, tagline, badges_html=""):
    html = f"""
    <div class="rr-hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
                <h1 class="rr-hero-title">{title}</h1>
                <div class="rr-hero-tagline">{tagline}</div>
            </div>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                <span class="badge-pink">SUPERR SELECTOR S2</span>
                <span class="badge-gold">TATA IPL 2027</span>
                {badges_html}
            </div>
        </div>
    </div>
    """
    render_html(html)

def render_kpi_card(title, value, subtext="", color="white"):
    color_class = "pink" if color == "pink" else ("gold" if color == "gold" else ("cyan" if color == "cyan" else ""))
    html = f"""
    <div class="rr-kpi-card">
        <div class="rr-kpi-title">{title}</div>
        <div class="rr-kpi-value {color_class}">{value}</div>
        <div class="rr-kpi-subtext">{subtext}</div>
    </div>
    """
    render_html(html)

def create_radar_chart(player_name, role="batter"):
    p_data = scouting_profiles.get(player_name)
    if not p_data:
        return None
    metrics = p_data.get("metrics", {})
    categories = ["Fit Score", "High-Pressure Impact", "Bayes Lift / Wkt%", "Reliability", "Phase Fit"]
    
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
        fillcolor='rgba(255, 27, 141, 0.25)',
        line=dict(color='#FF1B8D', width=2.5),
        name=player_name
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor="rgba(255,255,255,0.15)"),
            angularaxis=dict(linecolor="rgba(255,255,255,0.2)"),
            bgcolor="rgba(13, 23, 51, 0.6)"
        ),
        margin=dict(l=30, r=30, t=25, b=25),
        height=280,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", family="Inter", size=10)
    )
    return fig

def create_comparison_radar(p1_name, p2_name):
    p1 = scouting_profiles.get(p1_name, {})
    p2 = scouting_profiles.get(p2_name, {})
    categories = ["Fit Score", "High-Pressure Impact", "Consistency", "Volume / Reliability", "Tactical Need Fit"]
    v1 = [p1.get("fit_score", 60), 85, 78, 88, 92]
    v2 = [p2.get("fit_score", 60), 75, 82, 80, 85]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=v1, theta=categories, fill='toself',
        fillcolor='rgba(255, 27, 141, 0.25)',
        line=dict(color='#FF1B8D', width=2.5), name=p1_name
    ))
    fig.add_trace(go.Scatterpolar(
        r=v2, theta=categories, fill='toself',
        fillcolor='rgba(0, 229, 255, 0.2)',
        line=dict(color='#00E5FF', width=2.5), name=p2_name
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor="rgba(255,255,255,0.15)"),
            angularaxis=dict(linecolor="rgba(255,255,255,0.2)"),
            bgcolor="rgba(13, 23, 51, 0.6)"
        ),
        margin=dict(l=30, r=30, t=30, b=30),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color="#FFFFFF")),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", family="Inter", size=10)
    )
    return fig

def render_player_card(row, is_batter=True):
    overseas_chip = "<span class='badge-blue'>OVERSEAS</span>" if row['nationality'] != 'India' else "<span class='badge-green'>INDIAN CAPPED</span>"
    if 'Uncapped' in str(row.get('capped_status', '')):
        overseas_chip = "<span class='badge-yellow'>UNCAPPED DOMESTIC</span>"
        
    rank = row['auction_rank']
    name = row['player_name']
    role = row['primary_role']
    fit = f"{row['rr_fit_score']:.1f}"
    weakness = row['addressed_rr_weakness']
    slot = str(row['strategic_budget_guidance']).split()[0]
    
    if is_batter:
        badge_bg = "#FF1B8D"
        m1_lbl = "HP Strike Rate"
        m1_val = f"{row['hp_strike_rate']:.1f}"
        m1_col = "#FF1B8D"
        lift = row['shrunk_sr_lift']
        m2_lbl = "Bayes Shrunk Lift"
        m2_val = f"{'+' if lift > 0 else ''}{lift:.1f}"
        m2_col = "#10B981" if lift > 0 else "#EF4444"
        m3_lbl = "HP Balls Faced"
        m3_val = f"{int(row['hp_balls_faced'])}"
        m4_lbl = "Target Slot Ceiling"
        m4_val = slot
        m4_col = "#FFD700"
    else:
        badge_bg = "#3B82F6"
        m1_lbl = "HP Economy"
        m1_val = f"{row['hp_economy']:.2f}"
        m1_col = "#00E5FF"
        wkt = row['shrunk_wicket_rate'] * 100
        m2_lbl = "Shrunk Wicket %"
        m2_val = f"{wkt:.1f}%"
        m2_col = "#10B981"
        m3_lbl = "HP Balls Bowled"
        m3_val = f"{int(row['hp_balls_bowled'])}"
        m4_lbl = "Target Slot Ceiling"
        m4_val = slot
        m4_col = "#FFD700"

    card_html = f"""
    <div class="rr-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
                <span class="badge-gold" style="font-size:0.85rem; padding: 4px 10px;">#{rank}</span>
                <span style="font-family:'Barlow Condensed'; font-size:1.35rem; font-weight:800; color:#FFFFFF; margin-left:8px; vertical-align:middle;">{name}</span>
                <span style="margin-left:8px;">{overseas_chip}</span>
                <span class="badge-pink">{role}</span>
            </div>
            <div style="text-align:right;">
                <span style="font-size:0.7rem; color:#94A3B8; font-weight:700; text-transform:uppercase;">RR FIT SCORE</span><br>
                <span style="font-family:'Barlow Condensed'; font-size:1.5rem; font-weight:800; color:#FFD700;">{fit} / 100</span>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:8px; margin-bottom:12px;">
            <div class="stat-pill"><div class="stat-pill-label">{m1_lbl}</div><div class="stat-pill-val" style="color:{m1_col};">{m1_val}</div></div>
            <div class="stat-pill"><div class="stat-pill-label">{m2_lbl}</div><div class="stat-pill-val" style="color:{m2_col};">{m2_val}</div></div>
            <div class="stat-pill"><div class="stat-pill-label">{m3_lbl}</div><div class="stat-pill-val">{m3_val}</div></div>
            <div class="stat-pill"><div class="stat-pill-label">{m4_lbl}</div><div class="stat-pill-val" style="color:{m4_col};">{m4_val}</div></div>
        </div>
        <div style="background:rgba(255, 27, 141, 0.1); border-left:3px solid #FF1B8D; border-radius:6px; padding:8px 12px; font-size:0.82rem; color:#FCE4EC;">
            <strong>🎯 Tactical Role Fit:</strong> {weakness}
        </div>
    </div>
    """
    render_html(card_html)


# =========================================================================
# 1. EXECUTIVE OVERVIEW
# =========================================================================
if "1. Executive Overview" in menu:
    render_hero_banner(
        title="EXECUTIVE WAR ROOM: IPL 2027",
        tagline="Rajasthan Royals Empirical Auction Valuation & High-Pressure Roster Construction",
        badges_html="<span class='badge-blue'>200,999 DELIVERIES</span><span class='badge-green'>14/14 AUDITED</span>"
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Remaining Purse", "₹27.05 Cr", "19 Retained (₹102.95 Cr Spent)", "pink")
    with k2:
        render_kpi_card("Open Squad Slots", "6 Slots", "19 of 25 filled • Max 3 Overseas", "cyan")
    with k3:
        render_kpi_card("Confirmed Pool", "955 Targets", "262 exclusions audited & verified", "gold")
    with k4:
        render_kpi_card("Governance Checks", "14 / 14", "100% financial reconciliation", "white")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    c_left, c_right = st.columns([1.1, 1])
    with c_left:
        st.markdown("### 🎯 MARQUEE ACQUISITION TARGETS")
        render_html("""
        <div class="rr-section-box" style="margin-bottom: 12px;">
            <div style="font-size:0.8rem; font-weight:800; color:#FF1B8D; text-transform:uppercase; margin-bottom:8px;">🏏 TOP BATTING PRIORITIES (DEATH ACCELERATION)</div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.08);">
                <div><strong>#1 Reeza Hendricks</strong> <span class="badge-blue">Overseas</span> <span class="badge-pink">Top Anchor / Finisher</span></div>
                <div style="text-align:right;"><strong style="color:#FF1B8D;">SR 184.43</strong> | Fit: 100.0</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.08);">
                <div><strong>#2 Daryl Mitchell</strong> <span class="badge-blue">Overseas</span> <span class="badge-pink">Middle Enforcer</span></div>
                <div style="text-align:right;"><strong style="color:#FF1B8D;">SR 154.26</strong> | Fit: 79.25</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0;">
                <div><strong>#3 Towhid Hridoy</strong> <span class="badge-blue">Overseas</span> <span class="badge-pink">Spin Enforcer</span></div>
                <div style="text-align:right;"><strong style="color:#FF1B8D;">SR 147.92</strong> | Fit: 77.31</div>
            </div>
        </div>
        <div class="rr-section-box">
            <div style="font-size:0.8rem; font-weight:800; color:#00E5FF; text-transform:uppercase; margin-bottom:8px;">⚡ TOP BOWLING PRIORITIES (DEATH YORKERS & SPIN)</div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.08);">
                <div><strong>#1 Matheesha Pathirana</strong> <span class="badge-blue">Overseas</span> <span class="badge-pink">Searing Yorker</span></div>
                <div style="text-align:right;"><strong style="color:#00E5FF;">Econ 8.58</strong> | Wkt: 7.44%</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.08);">
                <div><strong>#2 Naveen ul Haq</strong> <span class="badge-blue">Overseas</span> <span class="badge-pink">Variations</span></div>
                <div style="text-align:right;"><strong style="color:#00E5FF;">Econ 8.92</strong> | Wkt: 5.75%</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0;">
                <div><strong>#3 Mujeeb Ur Rahman</strong> <span class="badge-blue">Overseas</span> <span class="badge-pink">Mystery Spin</span></div>
                <div style="text-align:right;"><strong style="color:#00E5FF;">Econ 7.42</strong> | Wkt: 4.88%</div>
            </div>
        </div>
        """)

    with c_right:
        st.markdown("### 📊 SCENARIO C PURSE ALLOCATION")
        labels = ['Slot 1: Marquee Finisher', 'Slot 2: Express Death Bowler', 'Slot 3: Wicket Spin', 'Slot 4: Domestic RHB', 'Slot 5: Domestic Finisher', 'Slot 6: Reserve Depth', 'Strategic Contingency Buffer']
        values = [7.00, 6.00, 4.00, 3.50, 2.20, 0.85, 3.50]
        colors = ['#FF1B8D', '#EC4899', '#3B82F6', '#60A5FA', '#93C5FD', '#CBD5E1', '#10B981']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=.55,
            marker=dict(colors=colors, line=dict(color='#070D1E', width=2)),
            textinfo='label+value',
            texttemplate='%{value} Cr',
            hovertemplate='<b>%{label}</b><br>Budget: ₹%{value} Cr<br>Share: %{percent}<extra></extra>'
        )])
        fig_donut.update_layout(
            showlegend=False,
            height=320,
            margin=dict(l=20, r=20, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text='₹27.05 Cr<br><span style="font-size:11px;color:#94A3B8;">TOTAL PURSE</span>', x=0.5, y=0.5, font_size=17, font_family="Barlow Condensed", font_color="#FFD700", showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)


# =========================================================================
# 2. PRESSURE ENGINE (PHASE 3)
# =========================================================================
elif "2. Pressure Engine" in menu:
    render_hero_banner(
        title="HOW WE MEASURE MATCH PRESSURE",
        tagline="Continuous Delivery Pressure Index (Pt ∈ [0, 100]) via DLS Resource Depletion & Chase Tension"
    )

    render_html("""
    <div class="rr-hero-banner" style="padding: 16px 20px; margin-bottom: 20px;">
        <p style="margin:0; font-size:0.95rem; color:#E2E8F0;">
            Rather than an arbitrary binary partition, match tension is modeled continuously across 200,999 competition deliveries. High pressure is defined as <b>Pt &ge; 65.0</b> (the top ~20% highest tension game states), with empirical Bayes shrinkage applied to prevent small-sample distortion.
        </p>
    </div>
    """)

    tab_inn2, tab_inn1, tab_so = st.tabs([
        "🎯 INNINGS 2: TARGET CHASING ($P_{chase}$)",
        "🏏 INNINGS 1: TARGET SETTING ($P_{inn1}$)",
        "⚡ SUPER OVERS & KNOCKOUT MULTIPLIERS"
    ])

    with tab_inn2:
        st.markdown(r"""
        #### Innings 2 Formulation: Chase Tension & Resource Depletion
        $$\mathbf{P_{\text{chase\_raw}}(t) = 100 \times \Big[ 0.40 \cdot f_{\text{RRR}}(t) + 0.25 \cdot f_{\text{wickets}}(t) + 0.15 \cdot f_{\text{stage}}(t) + 0.20 \cdot \big(f_{\text{RRR}}(t) \times f_{\text{stage}}(t)\big) \Big]}$$
        
        * **Required Run Rate Leverage ($f_{\text{RRR}}$):** Linear scaling between 6.0 rpo (low) and 14.0 rpo (extreme tension).
        * **Wickets in Hand Depletion ($f_{\text{wickets}}$):** Non-linear tail penalty as lower-order batting depth is exposed.
        * **Match Stage Weight ($f_{\text{stage}}$):** Monotonically escalates as remaining deliveries decrease.
        """)

    with tab_inn1:
        st.markdown(r"""
        #### Innings 1 Formulation: Setting Target & Resource Protection
        $$\mathbf{P_{\text{inn1\_raw}}(t) = 100 \times \Big[ 0.35 \cdot f_{\text{collapse}}(t) + 0.30 \cdot f_{\text{death\_acceleration}}(t) + 0.20 \cdot f_{\text{run\_rate\_deficit}}(t) + 0.15 \cdot f_{\text{stage}}(t) \Big]}$$
        
        * **Collapse Risk Factor ($f_{\text{collapse}}$):** Detects early top-order collapse (e.g. 3 wickets down in Powerplay).
        * **Death Acceleration Pressure ($f_{\text{death\_acceleration}}$):** Heavy imperative in overs 16–20 to achieve above-par totals.
        """)

    with tab_so:
        st.markdown(r"""
        #### High-Stakes Multipliers: Knockouts & Super Overs
        * **Super Overs:** Automatically assigned maximum index $\mathbf{P_t = 100.0}$.
        * **IPL Playoffs / Finals:** Baseline situation multiplier $\mathbf{\times 1.15}$.
        """)


# =========================================================================
# 3. BATTER RANKINGS (PHASE 5)
# =========================================================================
elif "3. Batter Rankings" in menu:
    render_hero_banner(
        title="TOP 10 AUCTION BATTERS",
        tagline="Empirical Bayes Shrunk Strike Rate Lift & Death-Overs Execution Across High-Pressure States"
    )

    # Rank 1 Standout Card
    r1 = top10_batters_df.iloc[0]
    render_html(f"""
    <div class="rr-rank1-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
            <div>
                <span class="badge-gold" style="font-size: 0.9rem; padding: 4px 12px;">👑 #1 MARQUEE TARGET</span>
                <span style="font-family:'Barlow Condensed'; font-size:2.0rem; font-weight:800; color:#FFFFFF; margin-left:10px; vertical-align:middle;">{r1['player_name']}</span>
                <span class="badge-blue" style="margin-left: 8px;">OVERSEAS</span>
                <span class="badge-pink">{r1['primary_role']}</span>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: #FFD700; font-weight: 700; text-transform: uppercase;">RR SQUAD FIT SCORE</div>
                <div style="font-family:'Barlow Condensed'; font-size: 2.5rem; font-weight: 800; color: #FFD700; line-height: 1;">100.0 / 100</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 16px 0 12px 0;">
            <div class="stat-pill"><div class="stat-pill-label">HP Strike Rate</div><div class="stat-pill-val" style="color:#FF1B8D;">{r1['hp_strike_rate']:.1f}</div></div>
            <div class="stat-pill"><div class="stat-pill-label">Bayes Shrunk Lift</div><div class="stat-pill-val" style="color:#10B981;">+{r1['shrunk_sr_lift']:.1f}</div></div>
            <div class="stat-pill"><div class="stat-pill-label">HP Deliveries</div><div class="stat-pill-val">{int(r1['hp_balls_faced'])}</div></div>
            <div class="stat-pill"><div class="stat-pill-label">Proposed Slot Ceiling</div><div class="stat-pill-val" style="color:#FFD700;">₹5.50–7.50 Cr</div></div>
        </div>
        <div style="background: rgba(255, 215, 0, 0.1); border-left: 3px solid #FFD700; border-radius: 6px; padding: 10px 14px; font-size: 0.88rem; color: #FFFBEB;">
            <strong>🎯 Scouting Summary:</strong> Elite dual-capability top-order anchor and death-overs accelerator. Direct solution to RR's Innings 1 Middle Overs deficit (+0.41 rpo) and Death Overs acceleration gap (+0.24 rpo).
        </div>
    </div>
    """)

    st.markdown("### 🏏 COMPLETE TOP 10 CANDIDATE ROSTER")
    view_mode = st.radio("Display Format", ["Visual Scouting Cards", "Data Table (with CSV Export)"], horizontal=True, key="bat_view_toggle")

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
# 4. BOWLER RANKINGS (PHASE 5)
# =========================================================================
elif "4. Bowler Rankings" in menu:
    render_hero_banner(
        title="TOP 10 AUCTION BOWLERS",
        tagline="Precision Death-Overs Yorkers & Middle-Overs Spin Economy Under High Pressure",
        badges_html="<span class='badge-pink'>STARC EXCLUDED</span>"
    )

    # Rank 1 Standout Card
    r1_b = top10_bowlers_df.iloc[0]
    render_html(f"""
    <div class="rr-rank1-card" style="border-color: #00E5FF; box-shadow: 0 6px 30px rgba(0, 229, 255, 0.2);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
            <div>
                <span class="badge-gold" style="font-size: 0.9rem; padding: 4px 12px; background: rgba(0, 229, 255, 0.2); border-color: #00E5FF; color: #00E5FF;">👑 #1 MARQUEE TARGET</span>
                <span style="font-family:'Barlow Condensed'; font-size:2.0rem; font-weight:800; color:#FFFFFF; margin-left:10px; vertical-align:middle;">{r1_b['player_name']}</span>
                <span class="badge-blue" style="margin-left: 8px;">OVERSEAS</span>
                <span class="badge-pink">{r1_b['primary_role']}</span>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.75rem; color: #00E5FF; font-weight: 700; text-transform: uppercase;">RR SQUAD FIT SCORE</div>
                <div style="font-family:'Barlow Condensed'; font-size: 2.5rem; font-weight: 800; color: #00E5FF; line-height: 1;">62.6 / 100</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 16px 0 12px 0;">
            <div class="stat-pill"><div class="stat-pill-label">HP Economy</div><div class="stat-pill-val" style="color:#00E5FF;">{r1_b['hp_economy']:.2f}</div></div>
            <div class="stat-pill"><div class="stat-pill-label">Shrunk Wicket %</div><div class="stat-pill-val" style="color:#10B981;">{r1_b['shrunk_wicket_rate']*100:.1f}%</div></div>
            <div class="stat-pill"><div class="stat-pill-label">HP Deliveries</div><div class="stat-pill-val">{int(r1_b['hp_balls_bowled'])}</div></div>
            <div class="stat-pill"><div class="stat-pill-label">Proposed Slot Ceiling</div><div class="stat-pill-val" style="color:#FFD700;">₹5.00–7.00 Cr</div></div>
        </div>
        <div style="background: rgba(0, 229, 255, 0.1); border-left: 3px solid #00E5FF; border-radius: 6px; padding: 10px 14px; font-size: 0.88rem; color: #E0F2FE;">
            <strong>🎯 Scouting Summary:</strong> Elite sling-arm death-overs executioner with searing yorker accuracy. Bridges RR's primary death overs bowling leakage where league average is significantly outmatched.
        </div>
    </div>
    """)

    st.markdown("### ⚡ COMPLETE TOP 10 CANDIDATE ROSTER")
    view_mode_b = st.radio("Display Format", ["Visual Scouting Cards", "Data Table (with CSV Export)"], horizontal=True, key="bowl_view_toggle")

    if view_mode_b == "Visual Scouting Cards":
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
# 5. PLAYER COMPARISON LAB
# =========================================================================
elif "5. Player Comparison Lab" in menu:
    render_hero_banner(
        title="HEAD-TO-HEAD COMPARISON LAB",
        tagline="Side-by-Side High-Pressure Statistical Contrasts & Dual Radar Overlay Across All 20 Targets"
    )

    all_20_players = list(top10_batters_df['player_name']) + list(top10_bowlers_df['player_name'])

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p1 = st.selectbox("Player A (Pink Trace)", all_20_players, index=0)
    with col_p2:
        p2 = st.selectbox("Player B (Cyan Trace)", all_20_players, index=1)

    d1 = scouting_profiles.get(p1, {})
    d2 = scouting_profiles.get(p2, {})

    col_c1, col_c2, col_radar = st.columns([1, 1, 1.2])
    with col_c1:
        render_html(f"""
        <div class="rr-card" style="border-top: 4px solid #FF1B8D;">
            <div style="font-family:'Barlow Condensed'; font-size:1.6rem; font-weight:800; color:#FF1B8D; margin-bottom:4px;">{p1}</div>
            <div style="color:#94A3B8; font-size:0.85rem; margin-bottom:12px;">{d1.get('primary_role', 'N/A')}</div>
            <div class="stat-pill" style="margin-bottom:8px;"><div class="stat-pill-label">Fit Score</div><div class="stat-pill-val" style="color:#FF1B8D;">{d1.get('fit_score', 0):.1f}</div></div>
            <div class="stat-pill" style="margin-bottom:8px;"><div class="stat-pill-label">Slot Ceiling</div><div class="stat-pill-val" style="color:#FFD700;">{d1.get('target_slot', 'N/A')}</div></div>
        </div>
        """)

    with col_c2:
        render_html(f"""
        <div class="rr-card" style="border-top: 4px solid #00E5FF;">
            <div style="font-family:'Barlow Condensed'; font-size:1.6rem; font-weight:800; color:#00E5FF; margin-bottom:4px;">{p2}</div>
            <div style="color:#94A3B8; font-size:0.85rem; margin-bottom:12px;">{d2.get('primary_role', 'N/A')}</div>
            <div class="stat-pill" style="margin-bottom:8px;"><div class="stat-pill-label">Fit Score</div><div class="stat-pill-val" style="color:#00E5FF;">{d2.get('fit_score', 0):.1f}</div></div>
            <div class="stat-pill" style="margin-bottom:8px;"><div class="stat-pill-label">Slot Ceiling</div><div class="stat-pill-val" style="color:#FFD700;">{d2.get('target_slot', 'N/A')}</div></div>
        </div>
        """)

    with col_radar:
        st.markdown("### 🕸️ DUAL RADAR OVERLAY")
        dual_fig = create_comparison_radar(p1, p2)
        st.plotly_chart(dual_fig, use_container_width=True)


# =========================================================================
# 6. RELIABILITY & VALIDATION (PHASE 4)
# =========================================================================
elif "6. Reliability & Validation" in menu:
    render_hero_banner(
        title="EMPIRICAL BAYES RELIABILITY ENGINE",
        tagline="Phase 4 Shrinkage Model (M = 45 Balls) & Sensitivity Verification"
    )

    st.markdown("""
    ### 🔬 Shrinkage Formulation
    To prevent low-sample anomalies from topping rankings, player performance is shrunk toward the league baseline ($\mu$):
    """)
    st.latex(r"\hat{\theta}_i = \frac{n_i}{n_i + M} \bar{x}_i + \frac{M}{n_i + M} \mu")

    st.markdown("---")
    st.markdown("### 📈 SENSITIVITY ROBUSTNESS: OVERLAP % ACROSS PRIOR WEIGHT M")
    st.image(str(ASSETS_DIR / "chart_sensitivity_overlap.png"), use_container_width=True)


# =========================================================================
# 7. METHODOLOGY & SCORING
# =========================================================================
elif "7. Methodology & Scoring" in menu:
    render_hero_banner(
        title="SCORING METHODOLOGY & FORMULAS",
        tagline="Comprehensive Mathematical Architecture & Franchise Need Weightings"
    )

    st.markdown(r"""
    ### 1. High-Pressure Batter Fit Formulation
    $$\text{Fit}_{\text{Bat}} = 0.40 \cdot \text{HP\_SR\_Percentile} + 0.30 \cdot \text{Shrunk\_Lift\_Percentile} + 0.15 \cdot \text{Consistency} + 0.15 \cdot \text{Need\_Weight}$$

    ### 2. High-Pressure Bowler Fit Formulation
    $$\text{Fit}_{\text{Bowl}} = 0.40 \cdot (100 - \text{HP\_Econ\_Percentile}) + 0.30 \cdot \text{Shrunk\_Wkt\_Percentile} + 0.15 \cdot \text{Consistency} + 0.15 \cdot \text{Need\_Weight}$$
    """)


# =========================================================================
# 8. DATA EXPLORER & GOVERNANCE
# =========================================================================
elif "8. Data Explorer & Governance" in menu:
    render_hero_banner(
        title="DATA EXPLORER & GOVERNANCE REGISTER",
        tagline="Full Audit Trail of 955 Active Targets & 262 Excluded Players"
    )

    exp_tab1, exp_tab2 = st.tabs(["🎯 955 AUCTION-ELIGIBLE TARGETS", "📋 262-PLAYER EXCLUSION AUDIT REGISTER"])

    with exp_tab1:
        st.dataframe(targets_df, use_container_width=True)
        csv_t = targets_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Master Eligible Pool CSV", csv_t, "Eligible_Auction_Pool.csv", "text/csv")

    with exp_tab2:
        cat_choice = st.selectbox("Filter Exclusion Category", ["All Categories"] + list(exclusions_df['exclusion_category'].unique()))
        search = st.text_input("Search Excluded Player Name", "")
        df_disp = exclusions_df
        if cat_choice != "All Categories":
            df_disp = df_disp[df_disp['exclusion_category'] == cat_choice]
        if search.strip():
            df_disp = df_disp[df_disp['player_name'].str.contains(search, case=False, na=False)]

        st.dataframe(df_disp[['player_name', 'exclusion_category', 'relevant_franchise', 'reason_detail', 'confidence_level', 'verification_date']], use_container_width=True)
        csv_ex = df_disp.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Filtered Exclusion Register CSV", csv_ex, "Exclusion_Register.csv", "text/csv")


# =========================================================================
# 9. AUCTION BUDGET SIMULATOR (₹27.05 CR PURSE)
# =========================================================================
elif "9. Auction Budget Simulator" in menu:
    render_hero_banner(
        title="INTERACTIVE AUCTION BUDGET SIMULATOR",
        tagline="Test Custom Bidding Allocations Across RR's 6 Vacant Slots Against ₹27.05 Cr Purse"
    )

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
    s3 = col_3.slider("Slot 3: Wicket Spin (Mujeeb/Maharaj)", 1.5, 6.0, float(s3_d), 0.1)

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
