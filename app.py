"""
SupeRR Selector Season 2 - Rajasthan Royals IPL 2027 Auction Intelligence Dashboard (REBUILT).
A production-grade Streamlit application for tactical squad planning, pressure analytics, and target filtering.
Features dedicated Top 10 Batters, Top 10 Bowlers, 20-Player Explorer, Comparison Suite, and Visual Analytics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path

st.set_page_config(
    page_title="RR SupeRR Selector 2027 • IPL Auction Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Rajasthan Royals Royal Pink & Royal Navy)
st.markdown("""
<style>
    .main { background-color: #F8F9FA; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 8px; border-left: 5px solid #E91E63; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
    h1, h2, h3 { color: #10172A; }
    .highlight-pink { color: #E91E63; font-weight: bold; }
    .badge-pink { background-color: #FCE4EC; color: #E91E63; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .badge-navy { background-color: #EFF6FF; color: #1D4ED8; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
    .badge-green { background-color: #ECFDF5; color: #047857; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# Resolve Base Paths (supports both standalone repo and multi-tier project structures)
ROOT_DIR = Path(__file__).resolve().parent
if (ROOT_DIR / "data" / "outputs").exists():
    BASE_DIR = ROOT_DIR
else:
    BASE_DIR = ROOT_DIR.parent

OUTPUTS_DIR = (ROOT_DIR / "data" / "outputs") if (ROOT_DIR / "data" / "outputs").exists() else (BASE_DIR / "data" / "outputs")
ASSETS_DIR = (ROOT_DIR / "assets") if (ROOT_DIR / "assets").exists() else (BASE_DIR / "dashboard" / "assets")
JSON_DATA_DIR = (ROOT_DIR / "data") if (ROOT_DIR / "data" / "scouting_profiles.json").exists() else (BASE_DIR / "DASHBOARD" / "data")

# Helper for Safe Loading
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
    st.error("Pipeline outputs missing. Please run `python src/pipeline.py` first.")
    st.stop()

# Sidebar Navigation
st.sidebar.markdown("<h2 style='color:#E91E63; margin-bottom:0;'>Rajasthan Royals</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#64748B; font-size:0.85rem; font-weight:600;'>SupeRR Selector 2027 • IPL Auction Intelligence</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Menu",
    [
        "Executive Summary",
        "Top 10 Batters (Auction Ranking)",
        "Top 10 Bowlers (Auction Ranking)",
        "Player Explorer (All 20 Targets)",
        "Player Comparison Suite",
        "Data Analysis Visuals Gallery",
        "Retained Squad & Phase Gaps",
        "Interactive Budget Simulator (₹27.05 Cr)",
        "Exclusion & Governance Register"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Purse Remaining:** <span style='color:#E91E63; font-weight:700;'>₹27.05 Cr</span>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Purse Committed:** ₹102.95 Cr (19 retained)")
st.sidebar.markdown(f"**Open Slots:** 6 Slots (Max 3 Overseas)")
st.sidebar.markdown(f"**Governance:** 14/14 Checks Passed")

# -------------------------------------------------------------------------
# 1. Executive Summary
# -------------------------------------------------------------------------
if menu == "Executive Summary":
    st.title("Rajasthan Royals: IPL 2027 Auction Intelligence")
    st.markdown("### Dual Auction Rankings for Batters and Bowlers Under Pressure")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Remaining Purse", "₹27.05 Crore", "₹102.95 Cr spent (19 retained)")
    col2.metric("Squad Slots Vacant", "6 Slots", "19/25 retained (max 3 OS)")
    col3.metric("Confirmed Target Pool", f"{len(targets_df)} Players", "from 1,217 universe")
    col4.metric("Governance Integrity", "14 / 14 Passed", "0 validation errors")
    
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🏏 Marquee Target: Top Batter")
        st.info("**#1 Reeza Hendricks (Overseas - South Africa)**\n\n"
                "- **High-Pressure Strike Rate:** **184.43** (167 HP balls faced)\n"
                "- **Shrunk Strike Rate Lift:** **+35.69** over expected phase baseline\n"
                "- **Tactical Fit Score:** **100.00 / 100**\n"
                "- **Proposed Maximum Ceiling:** **₹7.00 Crore**\n"
                "- *Addresses RR's middle-overs acceleration void.*")
        
    with col_b:
        st.subheader("🎯 Marquee Target: Top Bowler")
        st.success("**#1 Matheesha Pathirana (Overseas - Sri Lanka)**\n\n"
                   "- **High-Pressure Economy:** **8.58** (212 HP balls bowled)\n"
                   "- **Shrunk Wicket Rate:** **7.44%** in clutch death overs\n"
                   "- **Tactical Fit Score:** **62.62 / 100**\n"
                   "- **Proposed Maximum Ceiling:** **₹6.00 Crore**\n"
                   "- *Directly fixes RR's death overs leakage (+0.24 deficit).*")

    st.markdown("---")
    st.subheader("📊 Empirical Data Analysis: Batting & Bowling Clusters")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if (ASSETS_DIR / "chart_batting_bubble.png").exists():
            st.image(str(ASSETS_DIR / "chart_batting_bubble.png"), caption="Batting Cluster: High-Pressure Strike Rate vs Shrunk Lift", use_container_width=True)
    with col_c2:
        if (ASSETS_DIR / "chart_bowling_bubble.png").exists():
            st.image(str(ASSETS_DIR / "chart_bowling_bubble.png"), caption="Bowling Cluster: High-Pressure Economy vs Shrunk Wicket %", use_container_width=True)

# -------------------------------------------------------------------------
# 2. Top 10 Batters (Auction Ranking)
# -------------------------------------------------------------------------
elif menu == "Top 10 Batters (Auction Ranking)":
    st.title("Top 10 Batters for IPL 2027 Auction")
    st.markdown("Audited ranking based on High-Pressure Strike Rate, Empirical Bayes Shrunk Lift, and Tactical Squad Need.")
    
    disp_cols = [
        "auction_rank", "player_name", "nationality", "capped_status",
        "hp_strike_rate", "shrunk_sr_lift", "hp_balls_faced", "hp_boundary_pct",
        "rr_fit_score", "strategic_budget_guidance", "addressed_rr_weakness"
    ]
    renames = {
        "auction_rank": "Rank",
        "player_name": "Player Name",
        "nationality": "Nationality",
        "capped_status": "Status",
        "hp_strike_rate": "HP Strike Rate",
        "shrunk_sr_lift": "Shrunk Lift",
        "hp_balls_faced": "HP Balls",
        "hp_boundary_pct": "Boundary %",
        "rr_fit_score": "Fit Score",
        "strategic_budget_guidance": "Proposed Ceiling",
        "addressed_rr_weakness": "Addressed RR Gap"
    }
    st.dataframe(top10_batters_df[disp_cols].rename(columns=renames).reset_index(drop=True), use_container_width=True)
    
    csv_b = top10_batters_df[disp_cols].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Top 10 Batters CSV", csv_b, "Top_10_Batters_IPL_2027_Auction.csv", "text/csv")

# -------------------------------------------------------------------------
# 3. Top 10 Bowlers (Auction Ranking)
# -------------------------------------------------------------------------
elif menu == "Top 10 Bowlers (Auction Ranking)":
    st.title("Top 10 Bowlers for IPL 2027 Auction")
    st.markdown("Audited ranking based on High-Pressure Economy, Shrunk Wicket Rate, and Death-Overs Containment.")
    
    disp_cols = [
        "auction_rank", "player_name", "nationality", "capped_status",
        "hp_economy", "shrunk_wicket_rate", "hp_balls_bowled",
        "bowling_consistency_score", "rr_fit_score", "strategic_budget_guidance", "addressed_rr_weakness"
    ]
    renames = {
        "auction_rank": "Rank",
        "player_name": "Player Name",
        "nationality": "Nationality",
        "capped_status": "Status",
        "hp_economy": "HP Economy",
        "shrunk_wicket_rate": "Shrunk Wkt %",
        "hp_balls_bowled": "HP Balls",
        "bowling_consistency_score": "Consistency",
        "rr_fit_score": "Fit Score",
        "strategic_budget_guidance": "Proposed Ceiling",
        "addressed_rr_weakness": "Addressed RR Gap"
    }
    st.dataframe(top10_bowlers_df[disp_cols].rename(columns=renames).reset_index(drop=True), use_container_width=True)
    
    csv_w = top10_bowlers_df[disp_cols].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Top 10 Bowlers CSV", csv_w, "Top_10_Bowlers_IPL_2027_Auction.csv", "text/csv")

# -------------------------------------------------------------------------
# 4. Player Explorer (All 20 Ranked Targets)
# -------------------------------------------------------------------------
elif menu == "Player Explorer (All 20 Targets)":
    st.title("Scouting Dossier: All 20 Ranked Auction Targets")
    st.markdown("Detailed scouting profiles across all 10 Batters and 10 Bowlers from our validated rankings.")
    
    all_players = list(scouting_profiles.keys())
    selected_player = st.selectbox("Select Player from Top 20 Targets", all_players, index=0)
    
    p = scouting_profiles[selected_player]
    
    st.markdown(f"## {selected_player} <span class='badge-pink'>Rank #{p['rank']} {p['player_type']}</span> <span class='badge-navy'>{p['nationality']}</span>", unsafe_allow_html=True)
    st.markdown(f"**Tactical Role:** {p['role']}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tactical Fit Score", f"{p['fit_score']} / 100")
    if p['player_type'] == 'Batter':
        c2.metric("HP Strike Rate", f"{p['hp_sr']}")
        c3.metric("Shrunk Lift", f"{p['shrunk_lift']}")
    else:
        c2.metric("HP Economy", f"{p['hp_econ']}")
        c3.metric("Shrunk Wicket Rate", f"{p['shrunk_wkt_pct']}")
    c4.metric("HP Sample Size", f"{p['hp_balls']} Balls")
    
    st.markdown("---")
    
    col_str, col_lim = st.columns(2)
    with col_str:
        st.subheader("✅ Scouted Strengths")
        for s in p['strengths']:
            st.markdown(f"- {s}")
            
    with col_lim:
        st.subheader("⚠️ Known Limitations")
        for l in p['limitations']:
            st.markdown(f"- {l}")
            
    st.subheader("🎯 Rajasthan Royals Tactical Role & Budget Envelope")
    st.info(f"**Tactical Fit:** {p['rr_tactical_fit']}\n\n**Proposed Max Bid Ceiling:** **{p['budget_ceiling']}**")

# -------------------------------------------------------------------------
# 5. Player Comparison Suite
# -------------------------------------------------------------------------
elif menu == "Player Comparison Suite":
    st.title("Head-to-Head Multi-Player Comparison Suite")
    st.markdown("Compare 2 to 4 candidates across our 20 ranked targets to evaluate trade-offs in strike rate, economy, and sample sizes.")
    
    all_players = list(scouting_profiles.keys())
    default_picks = ["Reeza Hendricks", "Daryl Mitchell", "Matheesha Pathirana", "M Shahrukh Khan"]
    selected_picks = st.multiselect("Select 2 to 4 Players to Compare", all_players, default=default_picks)
    
    if len(selected_picks) < 2:
        st.warning("Please select at least 2 players to compare.")
    else:
        comp_data = []
        for name in selected_picks:
            prof = scouting_profiles[name]
            comp_data.append({
                "Player Name": name,
                "Type": prof["player_type"],
                "Rank": f"#{prof['rank']}",
                "Nationality": prof["nationality"],
                "Fit Score": prof["fit_score"],
                "HP Metric": f"SR: {prof['hp_sr']}" if prof['player_type'] == 'Batter' else f"Econ: {prof['hp_econ']}",
                "Shrunk Lift / Wkt%": prof.get("shrunk_lift") or prof.get("shrunk_wkt_pct"),
                "HP Balls": prof["hp_balls"],
                "Boundary %": f"{prof['hp_boundary_pct']}%",
                "Dot %": f"{prof['hp_dot_pct']}%",
                "Proposed Ceiling": prof["budget_ceiling"]
            })
        
        comp_df = pd.DataFrame(comp_data)
        st.dataframe(comp_df, use_container_width=True)
        
        # Interactive Bar Chart of Fit Scores
        st.subheader("📊 Comparative Fit Scores")
        st.bar_chart(comp_df.set_index("Player Name")["Fit Score"])

# -------------------------------------------------------------------------
# 6. Data Analysis Visuals Gallery
# -------------------------------------------------------------------------
elif menu == "Data Analysis Visuals Gallery":
    st.title("Data Analysis Visualizations Gallery")
    st.markdown("Real data evidence generated across 200,999 competition deliveries and empirical Bayes modeling.")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Batting Scatter Bubble",
        "Bowling Scatter Bubble",
        "RR Phase Weaknesses",
        "Capital Allocation Bar",
        "Sensitivity Overlap Curve"
    ])
    
    with tab1:
        st.subheader("Batting Performance: HP Strike Rate vs Shrunk Lift")
        st.image(str(ASSETS_DIR / "chart_batting_bubble.png"), caption="Bubble size indicates HP balls faced. Highlights Reeza Hendricks (+35.69) and Daryl Mitchell (+16.06).", use_container_width=True)
        
    with tab2:
        st.subheader("Bowling Performance: HP Economy vs Shrunk Wicket %")
        st.image(str(ASSETS_DIR / "chart_bowling_bubble.png"), caption="Bubble size indicates HP balls bowled. Highlights Matheesha Pathirana (8.58 Econ, 7.44% Wkt).", use_container_width=True)
        
    with tab3:
        st.subheader("Empirical Phase Weaknesses: RR vs League Baseline")
        st.image(str(ASSETS_DIR / "chart_phase_weaknesses.png"), caption="Diagnosing Innings 1 Middle Overs (+0.41 rpo deficit) and Death Overs (+0.24 rpo deficit).", use_container_width=True)
        
    with tab4:
        st.subheader("Purse Allocation: 6 Slot Ceilings + Buffer = ₹27.05 Cr")
        st.image(str(ASSETS_DIR / "chart_purse_allocation.png"), caption="Scenario C strictly reconciles to ₹27.05 Cr total remaining purse.", use_container_width=True)
        
    with tab5:
        st.subheader("Model Robustness: Empirical Bayes Shrinkage Overlap %")
        st.image(str(ASSETS_DIR / "chart_sensitivity_overlap.png"), caption="Shows ranking stability across M in [15, 75] prior balls.", use_container_width=True)

# -------------------------------------------------------------------------
# 7. Retained Squad & Phase Gaps
# -------------------------------------------------------------------------
elif menu == "Retained Squad & Phase Gaps":
    st.title("RR Retained Squad (19 Contracts) & Empirical Phase Gaps")
    st.markdown("Analysis of Rajasthan Royals' retained squad balance and phase-wise run rates across 200,999 competition deliveries.")
    
    st.subheader("Official Retained Roster (19 Players • ₹102.95 Cr Outlay)")
    st.dataframe(squad_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Empirical Phase Performance Matrix (RR vs League)")
    st.dataframe(phase_df, use_container_width=True)

# -------------------------------------------------------------------------
# 8. Interactive Budget Simulator (₹27.05 Cr Purse)
# -------------------------------------------------------------------------
elif menu == "Interactive Budget Simulator (₹27.05 Cr Purse)":
    st.title("RR Auction Budget Simulator (₹27.05 Crore Purse)")
    st.markdown("Adjust hypothetical bid ceilings across RR's 6 vacant squad slots to dynamically verify adherence to the purse limit.")
    
    scenario_choice = st.radio("Pre-Set Strategy Scenarios", ["Scenario C: Balanced Tactical (RECOMMENDED)", "Scenario A: Pace All-Rounder Heavy", "Scenario B: Batting-First Heavy"], horizontal=True)
    
    if "Scenario C" in scenario_choice:
        def_s1, def_s2, def_s3, def_s4, def_s5, def_s6, def_buf = 7.00, 6.00, 4.00, 3.50, 2.20, 0.85, 3.50
    elif "Scenario A" in scenario_choice:
        def_s1, def_s2, def_s3, def_s4, def_s5, def_s6, def_buf = 9.00, 5.00, 4.00, 3.20, 1.80, 1.00, 3.05
    else:
        def_s1, def_s2, def_s3, def_s4, def_s5, def_s6, def_buf = 8.00, 5.00, 4.00, 3.50, 2.00, 1.00, 3.55
        
    col_s1, col_s2, col_s3 = st.columns(3)
    s1 = col_s1.slider("Slot 1: Marquee Finisher (Hendricks/Mitchell)", 3.0, 10.0, float(def_s1), 0.1)
    s2 = col_s2.slider("Slot 2: Express Death Bowler (Pathirana/Nortje)", 3.0, 9.0, float(def_s2), 0.1)
    s3 = col_s3.slider("Slot 3: Wicket-Taking Spin (Mujeeb/Maharaj)", 1.5, 6.0, float(def_s3), 0.1)
    
    col_s4, col_s5, col_s6 = st.columns(3)
    s4 = col_s4.slider("Slot 4: Domestic RHB Anchor (Shankar/Rahane)", 1.0, 5.0, float(def_s4), 0.1)
    s5 = col_s5.slider("Slot 5: Uncapped Indian Finisher (Shahrukh Khan)", 0.8, 4.0, float(def_s5), 0.1)
    s6 = col_s6.slider("Slot 6: Reserve WK / Squad Depth", 0.5, 2.0, float(def_s6), 0.05)
    
    buf = st.slider("Unallocated Strategic Buffer (Contingency Reserve)", 1.0, 7.0, float(def_buf), 0.1)
    
    total_slots = s1 + s2 + s3 + s4 + s5 + s6
    total_committed = total_slots + buf
    diff = 27.05 - total_committed
    
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Available Purse", "₹27.05 Cr")
    m2.metric("Total Slot Ceilings", f"₹{total_slots:.2f} Cr")
    m3.metric("Unallocated Buffer", f"₹{buf:.2f} Cr")
    m4.metric("Grand Total Outlay", f"₹{total_committed:.2f} Cr")
    
    if total_committed <= 27.05:
        st.success(f"✅ **FEASIBLE & BALANCED:** Proposed allocation fits comfortably within the ₹27.05 Cr purse with **₹{diff:.2f} Cr** unused buffer.")
    else:
        st.error(f"❌ **BUDGET OVERRUN:** Proposed allocation exceeds the ₹27.05 Cr purse by **₹{abs(diff):.2f} Cr**! Adjust sliders downward.")

# -------------------------------------------------------------------------
# 9. Exclusion & Governance Register
# -------------------------------------------------------------------------
elif menu == "Exclusion & Governance Register":
    st.title("Player Exclusion Register & Governance Audit")
    st.markdown(f"Complete audit trail of all {len(exclusions_df)} excluded players from the 1,217-player master universe.")
    
    cat_filter = st.selectbox("Filter by Exclusion Category", options=["All"] + list(exclusions_df["exclusion_category"].unique()))
    search_q = st.text_input("Search Excluded Player by Name", "")
    
    disp_df = exclusions_df
    if cat_filter != "All":
        disp_df = disp_df[disp_df["exclusion_category"] == cat_filter]
    if search_q.strip():
        disp_df = disp_df[disp_df["player_name"].str.contains(search_q, case=False, na=False)]
        
    st.dataframe(disp_df[["player_name", "exclusion_category", "relevant_franchise", "reason_detail", "confidence_level", "verification_date"]], use_container_width=True)
    
    csv_ex = disp_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Exclusion Register CSV", csv_ex, "Player_Exclusion_Register.csv", "text/csv")
