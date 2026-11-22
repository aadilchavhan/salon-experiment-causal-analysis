# Lush & Glow Salon Chain: AI-Driven Experimentation & Causal Analysis

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)

## 🏢 Project Overview
This repository contains a comprehensive data science project evaluating the impact of an **AI-driven Smart Booking Recommendation System** for **Lush & Glow**, a fictional salon and spa chain with 22 outlets across **Coimbatore, India**. 

The project demonstrates advanced experimentation techniques, including randomized A/B testing, Difference-in-Differences (DiD) for retrospective causal inference, and CUPED for variance reduction.

## 🚀 Key Business Findings
*   **Primary Metric:** Revenue per Visit (RPV) increased by **+INR 217.46 (+8.60%)**.
*   **Guardrail Success:** No-show rates decreased from **0.36 to 0.22** per client; stylist capacity remained safe at **94.2%** buffer compliance.
*   **Retrospective Impact:** Difference-in-Differences analysis on past data confirmed a robust causal uplift of **INR 117.91** in treatment regions.
*   **Commercial ROI:** Projected annual revenue increase of **INR 8.22 Crores** against a cost of INR 15 Lakhs (**5,380% Net ROI**).

## 🛠️ Methodology & Statistics
*   **A/B Testing:** Randomized controlled trial (RCT) with 15,000 clients.
*   **SRM Check:** Verified sample ratio mismatch via Chi-Square (p = 0.98).
*   **CUPED:** Applied variance reduction using pre-experiment data, achieving **90%+ reduction** in noise.
*   **Causal Inference:** Used **Difference-in-Differences (DiD)** to estimate the effect of non-randomized historical changes.
*   **Segmentation:** Analyzed heterogeneous treatment effects across membership tiers (Standard, Silver, Gold, Platinum).

## 📂 Repository Structure
```text
├── Lush_and_Glow_Experiment_Report.docx  # Final executive project report
├── analysis_notebook.ipynb               # Complete analysis workflow in Python
├── run_salon_analysis.py                 # Main analysis execution script
├── generate_salon_data.py                # Synthetic dataset generator (messy data included)
├── experiment_design_document.md         # Detailed experiment design & hypotheses
├── decision_memo.md                      # Executive recommendation memo
├── *.csv                                 # Generated datasets (appointments, stylists, sales, etc.)
└── *.png                                 # Visualizations (RPV comparison, Parallel Trends)
```

## 💻 How to Run
1. **Clone the repository:**
   ```bash
   git clone https://github.com/aadilchavhan/salon-experiment-causal-analysis.git
   ```
2. **Install dependencies:**
   ```bash
   pip install pandas numpy scipy statsmodels matplotlib python-docx
   ```
3. **Generate the data:**
   ```bash
   python generate_salon_data.py
   ```
4. **Run the analysis:**
   ```bash
   python run_salon_analysis.py
   ```

## 🛡️ Threats to Causal Validity
*   **Novelty Effects:** Potential for engagement decay over 6+ months.
*   **Selection Bias:** Addressed via DiD for historical non-randomized data.
*   **SUTVA:** Risk of cross-contamination between clients at the same outlet.

---
*Created as part of a Data Science Internship project.*
