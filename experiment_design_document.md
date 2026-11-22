# Salon & Spa A/B Experiment Design Document

## Business Context
**Lush & Glow Salon & Spa** is a leading chain operating **22 outlets across Coimbatore**. 

To drive higher customer spend and engagement, Lush & Glow developed an **AI-driven Smart Scheduling & Personalization System**. This feature dynamically recommends tailored add-on services and product bundles during booking.

---

## 1. Hypotheses
* **Null Hypothesis ($H_0$):** The AI-driven booking recommendations have no effect on Revenue per Visit (RPV) compared to the standard booking experience.
* **Alternative Hypothesis ($H_1$):** The AI-driven booking recommendations significantly increase Revenue per Visit (RPV).

---

## 2. Metrics Selection
* **Primary Metric:** **Revenue per Visit (RPV)** (Average spend per appointment including services and cross-sold retail products).
* **Secondary Metric:** 30-day Client Retention Rate.
* **Guardrail Metrics:** 
  - **No-show Rate:** Must not increase (ensures recommendations don't cause friction).
  - **Stylist Capacity / Overcrowding:** Appointment duration buffer compliance must remain high.

---

## 3. Power Analysis & Sample Size
* **Baseline RPV:** INR 2,500
* **MDE:** 5% relative increase.
* **Significance Level ($\alpha$):** 0.05
* **Statistical Power ($1 - \beta$):** 0.80
* **Target Sample Size:** 7,500 clients per group (15,000 total).

---

## 4. Threats to Causal Validity
* **Novelty Effect:** Users might interact more with the system initially because it is new, but return to baseline behavior later.
* **Interference (SUTVA):** Clients might share experiences, leading to behavioral changes in the control group.
* **Selection Bias (Retrospective):** In the retrospective DiD analysis, the regions chosen for the initial rollout might have had different growth trajectories.
* **External Confounders:** Seasonal spikes (e.g., weddings, festivals) in Coimbatore that affect specific services more than others.

---

## 5. ROI Analysis Plan
We will calculate the net revenue uplift and subtract the estimated operational costs (software licensing, staff training) to determine the Return on Investment.

---

## 6. Assumptions & Limitations
* Assumes stylists can handle add-on services without major schedule disruptions.
* Limited to the 30-day observation window.
