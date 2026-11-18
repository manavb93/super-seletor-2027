# SupeRR Selector 2027 — Streamlit Dashboard Deployment & User Guide

## 1. Live Public Application (Immediate Competition Submission)

The interactive dashboard is currently deployed live on the public web and ready for judges:

> 🌐 **Live Public URL:** [https://c1cf40e3c8b1ac.app.lhr.life](https://c1cf40e3c8b1ac.app.lhr.life)

*No login or installation required. Open in any modern web browser.*

---

## 2. What's Included in This Rebuilt Dashboard

### Complete 20-Player Target Pool (Expanded from 6 to All 20 Ranked Targets)
- **Top 10 Batters (Auction Ranking):**
  1. Reeza Hendricks (Fit Score: 100.0, HP Strike Rate: 184.43, Shrunk Lift: +35.69, Est. Slot: ₹5.50–7.50 Cr)
  2. Daryl Mitchell (Fit: 79.25, HP SR: 154.26, Shrunk Lift: +16.06, Est. Slot: ₹5.00–6.50 Cr)
  3. Towhid Hridoy (Fit: 77.31, HP SR: 147.92, Shrunk Lift: +12.38, Est. Slot: ₹3.00–4.50 Cr)
  4. Mark Chapman (Fit: 75.69, HP SR: 146.34, Shrunk Lift: +11.39, Est. Slot: ₹2.50–3.80 Cr)
  5. Shimron Hetmyer (Fit: 75.68, HP SR: 145.83, Shrunk Lift: +11.08, Est. Slot: ₹4.50–6.00 Cr)
  6. Vijay Shankar (Fit: 65.94, HP SR: 135.00, Shrunk Lift: +4.32, Est. Slot: ₹2.50–3.50 Cr)
  7. Ajinkya Rahane (Fit: 63.41, HP SR: 132.00, Shrunk Lift: +2.45, Est. Slot: ₹2.00–3.00 Cr)
  8. Rassie van der Dussen (Fit: 60.51, HP SR: 129.50, Shrunk Lift: +0.89, Est. Slot: ₹2.00–3.20 Cr)
  9. Asif Khan (Fit: 60.14, HP SR: 128.00, Shrunk Lift: -0.05, Est. Slot: ₹0.80–1.50 Cr)
  10. M Shahrukh Khan (Fit: 60.14, HP SR: 128.00, Shrunk Lift: -0.05, Est. Slot: ₹1.80–2.80 Cr)

- **Top 10 Bowlers (Auction Ranking):**
  1. Matheesha Pathirana (Fit Score: 62.62, HP Economy: 8.58, Shrunk Wicket %: 7.44%, Est. Slot: ₹5.00–7.00 Cr)
  2. Naveen ul Haq (Fit: 52.13, HP Econ: 8.92, Shrunk Wkt %: 5.75%, Est. Slot: ₹3.50–4.80 Cr)
  3. Mujeeb Ur Rahman (Fit: 52.10, HP Econ: 7.42, Shrunk Wkt %: 4.88%, Est. Slot: ₹3.00–4.20 Cr)
  4. Keshav Maharaj (Fit: 52.00, HP Econ: 7.35, Shrunk Wkt %: 4.80%, Est. Slot: ₹2.50–3.80 Cr)
  5. Taskin Ahmed (Fit: 51.47, HP Econ: 8.75, Shrunk Wkt %: 5.30%, Est. Slot: ₹2.50–3.50 Cr)
  6. Trent Boult (Fit: 50.85, HP Econ: 8.40, Shrunk Wkt %: 4.85%, Est. Slot: ₹3.50–5.00 Cr)
  7. Tushar Deshpande (Fit: 50.49, HP Econ: 9.15, Shrunk Wkt %: 5.25%, Est. Slot: ₹2.00–3.20 Cr)
  8. Shoriful Islam (Fit: 49.11, HP Econ: 8.80, Shrunk Wkt %: 4.65%, Est. Slot: ₹1.80–2.80 Cr)
  9. Blessing Muzarabani (Fit: 48.31, HP Econ: 8.65, Shrunk Wkt %: 4.30%, Est. Slot: ₹1.20–2.20 Cr)
  10. Anrich Nortje (Fit: 47.50, HP Econ: 9.30, Shrunk Wkt %: 4.80%, Est. Slot: ₹3.00–4.50 Cr)

---

### Analytical Visualizations Embedded in Dashboard
1. **Batting Bubble Chart:** High-pressure strike rate vs. empirical Bayes shrunk lift (sized by high-pressure balls faced).
2. **Bowling Bubble Chart:** High-pressure economy rate vs. shrunk wicket probability % (sized by balls bowled).
3. **Phase-Wise Deficit Breakdown:** Rajasthan Royals' run-rate differential vs. IPL league average across Powerplay, Middle, and Death overs.
4. **Stacked Purse Allocation (Scenario C):** Strict reconciliation of 6 open slots + contingency reserve to exactly ₹27.05 Cr.
5. **Bayesian Shrinkage Sensitivity Curve:** Overlap percentage of top targets across prior sample weights $M \in [15, 75]$.

---

### Interactive Features
- **Player Explorer (20 Players):** Deep-dive into any of the 20 players with granular high-pressure metrics, base stats, role classification, and tactical scout recommendations.
- **Player Comparison Suite:** Side-by-side metric comparison and visual comparative bar charts for any two players among all 20 ranked candidates.
- **Dynamic Auction Budget Simulator:** Sliders for all 6 vacant slots + unallocated strategic contingency buffer. Live budget overrun alerts verifying spending stays within ₹27.05 Crore.
- **Audited Exclusion Register:** Searchable register of 262 excluded players with categorized reasons and IPL franchise status.

---

## 3. How to Deploy to Streamlit Community Cloud (`share.streamlit.io`)

If you want a permanent `https://<your-name>-superr-selector-2027.streamlit.app` link connected to your GitHub account (`manavb93`):

1. **Push this folder to GitHub:**
   ```bash
   cd SUBMISSION_READY/07_DASHBOARD/Streamlit_App
   git init
   git add .
   git commit -m "Initial commit of SupeRR Selector 2027 Streamlit Dashboard"
   git branch -M main
   git remote add origin https://github.com/manavb93/superr-selector-2027.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Community Cloud:**
   - Log in to [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
   - Click **"New app"**.
   - Select repository: `manavb93/superr-selector-2027`.
   - Branch: `main`.
   - Main file path: `app.py`.
   - Click **"Deploy!"**.
   - Within 60 seconds, your application will be live at `https://superr-selector-2027.streamlit.app`!

---

## 4. How to Run Locally

```bash
cd SUBMISSION_READY/07_DASHBOARD/Streamlit_App
pip install -r requirements.txt
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
