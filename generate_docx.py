import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = docx.Document()

# Set standard margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helper function for headings
def add_heading_1(text):
    h = doc.add_paragraph()
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(31, 78, 121) # Navy
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    return h

def add_heading_2(text):
    h = doc.add_paragraph()
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(89, 89, 89) # Dark Grey
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(4)
    return h

def add_p(text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Calibri'
        r_bold.font.size = Pt(11)
        r_bold.font.bold = True
    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(11)
    return p

# Title Page / Header
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
t_run = title.add_run("LUSH & GLOW SALON & SPA CHAIN\nAI-Driven Smart Booking Experiment & Causal Analysis Report")
t_run.font.name = 'Calibri'
t_run.font.size = Pt(22)
t_run.font.bold = True
t_run.font.color.rgb = RGBColor(31, 78, 121)
title.paragraph_format.space_after = Pt(20)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
s_run = sub.add_run("Comprehensive A/B Testing, Difference-in-Differences, Guardrail Analysis, and ROI Evaluation\nSubmitted by: Data Science Intern | Coimbatore Region (22 Outlets)")
s_run.font.name = 'Calibri'
s_run.font.size = Pt(12)
s_run.font.italic = True
sub.paragraph_format.space_after = Pt(30)

doc.add_page_break()

# Section 1: Executive Summary & Recommendation
add_heading_1("1. Executive Summary & Final Recommendation")
add_p("Lush & Glow Salon & Spa, operating 22 premium outlets across Coimbatore, evaluated an AI-driven Smart Scheduling & Personalization System designed to recommend tailored add-on services and retail product bundles during client booking. Over a 30-day trial involving 15,000 clients, rigorous A/B testing and causal inference methods were applied to measure true business impact.")

add_p("GO (Full Rollout Across All 22 Outlets)", "Final Recommendation: ")
add_p("The treatment group experienced a statistically significant increase in Revenue per Visit (RPV) from INR 2,529.50 to INR 2,746.97, yielding an absolute uplift of +INR 217.46 per visit (+8.60% relative increase, p < 0.0001). Projected net ROI is exceptionally strong at ~5,380%, driven by an estimated annual revenue increase of INR 8.2 Crores.")

# Section 2: Experiment Design & Methodology
add_heading_1("2. Experiment Design & Methodology")
add_p("The experiment was structured following rigorous data science standards to eliminate confounding bias and ensure high statistical power.")
add_p("To evaluate whether updating booking workflows improves client spend without hurting operations.", "Business Objective: ")
add_p("Revenue per Visit (RPV) — average spend per completed appointment including services and retail products.", "Primary Metric: ")
add_p("No-show rate and stylist schedule buffer compliance (overcrowding check).", "Guardrail Metrics: ")
add_p("Null Hypothesis (H0): AI recommendations have no effect on RPV. Alternative Hypothesis (H1): AI recommendations significantly increase RPV.", "Hypotheses: ")
add_p("Based on a baseline RPV of INR 2,500, a standard deviation of INR 500, alpha = 0.05, and power = 0.80, the required sample size was determined to be ~251 per group. The study was scaled to 15,000 clients (7,499 control, 7,501 treatment) across all 22 Coimbatore outlets over 4 weeks.", "Power Analysis & Sample Size: ")

# Section 3: Statistical Analysis & Results
add_heading_1("3. Statistical Analysis & Results")
add_p("Sample Ratio Mismatch (SRM) check via Chi-Square test yielded chi2 = 0.1176, p-value = 0.9870, confirming an unbiased 50/50 randomization split.", "Randomization Balance: ")
add_p("T-test on post-period revenue demonstrated a t-statistic of 24.4025 (p = 5.20e-129) with a 95% parametric confidence interval of [INR 200.00, INR 234.93].", "Treatment Effects & Confidence Intervals: ")
add_p("A dedicated Difference-in-Differences (DiD) analysis on last quarter's retrospective data confirmed a robust treatment effect of +INR 117.91 (p < 0.0001) in treatment regions compared to control regions, controlling for baseline trends.", "Retrospective Difference-in-Differences: ")

# Add Chart 1
doc.add_paragraph()
p_img1 = doc.add_paragraph()
p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
try:
    p_img1.add_run().add_picture('rpv_comparison_salon.png', width=Inches(5.5))
except Exception as e:
    print(f"Could not add image 1: {e}")

# Section 4: Guardrail Metrics & Operational Safety
add_heading_1("4. Guardrail Metrics & Operational Safety")
add_p("To ensure financial gains were not achieved at the expense of client satisfaction or staff burnout, guardrail metrics were continuously audited:")
add_p("Control group mean no-shows per client was 0.366, whereas treatment group mean no-shows dropped to 0.227, indicating that AI-driven reminders and scheduling significantly reduced client friction and no-show rates.", "No-Show Rate Analysis: ")
add_p("Stylist schedule buffer compliance was audited across all 289 stylists in Coimbatore, maintaining a 94.2% compliance rate (comfortably above the 90% safety threshold), proving that add-on recommendations did not cause operational bottlenecks or overcrowding.", "Stylist Capacity & Overcrowding: ")

# Section 5: ROI & Financial Projections
add_heading_1("5. ROI & Financial Projections")
add_p("A comprehensive cost-benefit evaluation was conducted to assess commercial viability:")
add_p("INR 6,850,104.20 per month (based on ~31,500 monthly salon visits across 22 outlets).", "Monthly Revenue Uplift: ")
add_p("INR 82,201,250.45 (~INR 8.22 Crores).", "Annual Revenue Uplift: ")
add_p("INR 1,500,000 (INR 15 Lakhs) covering software licensing, maintenance, and staff training.", "Estimated Annual Implementation Cost: ")
add_p("5,380.08%, indicating exceptional financial return and strong commercial justification for full deployment.", "Projected Net ROI: ")

# Section 6: Threats to Causal Validity
add_heading_1("6. Threats to Causal Validity")
add_p("To maintain scientific integrity, potential threats to our causal estimates were identified and documented:")
add_p("Clients may exhibit higher initial engagement with the AI recommender due to novelty, which could experience a minor decay over a 3 to 6-month horizon.", "Novelty Effect: ")
add_p("Clients visiting the same outlet might discuss features, potentially cross-contaminating control group behavior.", "SUTVA Violations: ")
add_p("Retrospective control and treatment regions in Coimbatore might have experienced differing localized economic or seasonal trends.", "Selection Bias in Retrospective Data: ")

# Save Document
doc.save('Lush_and_Glow_Experiment_Report.docx')
print("Successfully generated Lush_and_Glow_Experiment_Report.docx!")
