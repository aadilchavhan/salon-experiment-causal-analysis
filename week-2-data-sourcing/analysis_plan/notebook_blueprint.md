# Week 2 — Notebook Blueprint

**Project:** Lush & Glow Salon & Spa — AI-Driven Smart Booking Recommendation System  
**Purpose:** Turn the Week 1 starter notebook into a traceable data-quality, EDA, and causal-analysis workflow.

> **Status and honesty note:** This file is an implementation blueprint. The examples below are templates, not evidence that these analyses have already been executed. The Week 1 repository contains generated/synthetic CSVs. Before making real-world causal claims, replace or validate the data with authorised first-party records.

## 1. Proposed notebook and output structure

Suggested names if the project is expanded later:

```text
notebooks/
  01_data_inventory_and_quality.ipynb
  02_eda_and_metric_validation.ipynb
  03_randomized_trial_itt_cuped.ipynb
  04_did_parallel_trends_diagnostics.ipynb
reports/
  figures/
  tables/
logs/
  data_manifest.csv
  run_log.txt
```

The current Week 1 `analysis_notebook.ipynb` should be retained. These names describe a possible next-stage structure; they are not files that already exist.

## 2. Stage 0 — Record the data manifest

For every input, record:

- file or API/source name;
- source URL or repository path;
- extraction date and covered date range;
- row count and column count;
- file checksum or version / commit;
- whether the data are synthetic, public benchmark, or authorised first-party data;
- licence, terms, and access restrictions.

Do not put real customer identifiers or confidential fields in a public GitHub repository.

## 3. Stage 1 — Inventory and profile

For each CSV, inspect shape, column names, data types, null percentage, duplicate rows, date coverage, category values, and candidate keys. Confirm the expected grain before joining:

| Dataset | Expected grain | Important checks |
|---|---|---|
| `client_records.csv` | One row per client | Client key uniqueness; missing membership/history fields. |
| `appointment_records.csv` | One row per appointment | Appointment key; client/outlet/stylist key coverage; status values and dates. |
| `experiment_dataset.csv` | Depends on generator schema; inspect first | Assignment grain; treatment/control labels; assignment uniqueness at the randomisation unit. |
| `service_transactions.csv` | Service transaction or transaction line | Revenue fields, refunds/discounts, appointment/visit link. |
| `product_sales.csv` | Retail transaction line | SKU/product, quantity, discount/refund, appointment/visit link. |
| `stylists_information.csv` | One row per stylist or stylist record | Stylist key and outlet mapping. |
| `outlets.csv` | One row per outlet | Outlet key uniqueness and outlet metadata. |
| `did_dataset.csv` / `retrospective_dataset.csv` | Inspect actual panel grain | Outlet/time uniqueness, treated indicator, intervention date, outcome coverage. |

The expected grain must be confirmed from the actual file schema; do not assume that a filename guarantees its structure.

## 4. Stage 2 — Data validation before analysis

Create explicit assertions or validation checks for:

1. unique primary keys at the documented grain;
2. valid foreign-key coverage between clients, appointments, visits, transactions, stylists, and outlets;
3. allowed treatment/control labels and assignment counts;
4. valid timestamps and consistent timezone (`Asia/Kolkata` for the case study);
5. non-negative quantities where appropriate and documented treatment of refunds/voids;
6. revenue reconciliation from POS line items to visit and outlet totals;
7. one-to-many joins that do not multiply revenue unexpectedly;
8. outcome-window maturity, especially for 30-day retention.

Keep unmatched records in an exception report. Do not silently drop them.

## 5. Stage 3 — Define analysis metrics before looking at treatment effects

- **RPV:** net service revenue plus linked retail revenue for the visit, divided by eligible completed visits. Freeze tax, refund, discount, and void rules.
- **ITT companion outcome:** 30-day net revenue per randomised client, including zero revenue where the client has no completed visit in the window. This avoids reporting only on a post-treatment subset.
- **30-day retention:** at least one subsequent completed visit within 30 days among clients with a fully matured follow-up window.
- **No-show rate:** no-show appointments divided by appointments scheduled and due; cancellations and reschedules reported separately.
- **Capacity:** utilisation, overtime, and proportion of bookings meeting the pre-agreed minimum buffer.

## 6. Stage 4 — EDA and descriptive statistics

Calculate, at minimum:

- row counts, unique entities, means, medians, standard deviations, quartiles, min/max, and selected percentiles;
- null and duplicate rates by field/table;
- counts by date, outlet, treatment arm, membership tier, appointment status, and service category;
- revenue distribution and zero/negative/refund frequency;
- retention and no-show numerators and denominators;
- join-match rates and reconciliation differences;
- stylist/outlet utilisation and buffer distributions.

Recommended figures:

1. sample-flow diagram from eligibility to randomisation and matured outcomes;
2. missingness heatmap and join-coverage chart;
3. RPV histogram/ECDF and boxplot by arm;
4. weekly booking and revenue trends by arm;
5. retention and no-show rates with confidence intervals and denominators;
6. outlet/day capacity heatmap;
7. DiD pre-period trends and event-study coefficients with confidence intervals.

## 7. Stage 5 — Randomised experiment checks

### 7.1 Sample-ratio mismatch (SRM)

Compare observed treatment/control counts with the allocation ratio fixed in the experiment design document. Use a chi-square goodness-of-fit test as a diagnostic. A very small p-value (for example, below a pre-specified operational threshold such as 0.001) should trigger investigation of eligibility, assignment logging, exposure logging, and join duplication. Do not proceed as though randomisation is valid until the mismatch is understood.

### 7.2 Intention-to-treat (ITT)

Analyse each client according to their assigned arm, not according to whether they viewed or accepted a recommendation. Report the arm means, absolute difference, relative uplift, confidence interval, sample size, and outcome coverage. Show the unadjusted result before adjusted models.

## 8. Stage 6 — CUPED and regression adjustment

CUPED uses a pre-treatment covariate correlated with the outcome to reduce variance. For a client-level trial, define:

\[
Y_{cuped,i}=Y_i-\theta(X_i-\bar X),\qquad
\theta=\frac{\operatorname{Cov}(Y,X)}{\operatorname{Var}(X)}
\]

where `Y` is the post-assignment outcome and `X` is a baseline measure, such as pre-period net revenue per client. Only pre-treatment variables may be used for adjustment. Estimate theta using treatment-blinded pooled data, and preserve an indicator for missing baseline history.

Illustrative Python template (rename columns to match the actual, inspected schema):

```python
import numpy as np
import statsmodels.formula.api as smf

# One row per randomised client. All covariates must be pre-treatment.
analysis = trial.loc[
    trial["outcome_matured"] & trial["post_30d_net_revenue"].notna()
].copy()

assert analysis["client_id"].is_unique

analysis["pre_history_missing"] = (
    analysis["pre_30d_net_revenue"].isna().astype(int)
)
x_mean = analysis["pre_30d_net_revenue"].mean()
analysis["x_pre"] = analysis["pre_30d_net_revenue"].fillna(x_mean)
analysis["x_centered"] = analysis["x_pre"] - analysis["x_pre"].mean()

y = analysis["post_30d_net_revenue"]
x = analysis["x_pre"]
theta = np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1)
analysis["y_cuped"] = y - theta * analysis["x_centered"]

cuped_fit = smf.ols(
    "y_cuped ~ treatment + pre_history_missing + C(outlet_id) + C(membership_tier)",
    data=analysis,
).fit(cov_type="HC3")
print(cuped_fit.summary())

adjusted_fit = smf.ols(
    "post_30d_net_revenue ~ treatment + x_pre + pre_history_missing "
    "+ C(outlet_id) + C(membership_tier)",
    data=analysis,
).fit(cov_type="HC3")
print(adjusted_fit.summary())
```

The example assumes one row per client and the named fields. Validate the outcome and baseline windows, coding of `treatment`, sample maturity, and covariates before running. Do not include post-treatment variables such as recommendation acceptance as adjustment covariates in the primary ITT model. Report the unadjusted, CUPED, and regression-adjusted estimates on the same eligible cohort.

## 9. Stage 7 — DiD and parallel-trends diagnostics

For the retrospective DiD dataset, first establish the panel grain (ideally one row per outlet-week), intervention date, treatment/control outlet definitions, and stable outcome formula. Use multiple pre-intervention periods; 8–12 or more is a planning target where reliable history exists, not a guarantee that the assumption holds.

Diagnostics to report:

1. plot treated and comparison-group outcomes across every pre-period;
2. estimate the differential pre-period slope and its confidence interval;
3. fit an event-study model with relative-time indicators, omitting a reference pre-period;
4. jointly test the pre-treatment lead coefficients;
5. run placebo intervention dates inside the pre-period;
6. repeat with reasonable alternative control groups, outcome definitions, and time windows;
7. document the number of independent outlets/clusters and use small-cluster-appropriate inference (for example, wild cluster bootstrap) when feasible.

A non-significant pre-trend test does not prove parallel trends; it may simply have low power. Evaluate the size and uncertainty of pre-period differences and use subject-matter reasoning. If trends diverge materially, do not present the simple DiD estimate as a credible causal effect without a justified redesign or sensitivity analysis.

Illustrative setup code (complete event-study formula depends on the actual panel and treatment timing):

```python
import statsmodels.formula.api as smf

panel["event_time"] = panel["week_index"] - panel["intervention_week"]
pre = panel.loc[panel["event_time"] < 0].copy()
pre["week_num"] = pre["week_index"] - pre["week_index"].min()

pretrend_fit = smf.ols(
    "rpv ~ C(outlet_id) + C(week_index) + treated:week_num",
    data=pre,
).fit(
    cov_type="cluster",
    cov_kwds={"groups": pre["outlet_id"]},
)
print(pretrend_fit.summary())
```

This slope model is a diagnostic, not the complete event-study. The event-study should estimate treatment-by-relative-week coefficients, include outlet and calendar-week fixed effects, omit a clearly stated reference period, plot coefficients and 95% confidence intervals, and jointly test the pre-treatment leads. With only 22 outlets, conventional cluster-robust standard errors can be unreliable; report the small number of clusters and use an appropriate small-cluster sensitivity method where feasible.

## 10. Stage 8 — Save auditable outputs

At the end of each stage, save:

| Stage | Output evidence |
|---|---|
| Inventory | Source manifest, schema profile, file hashes. |
| Validation | Key checks, SRM result, join audit, POS reconciliation, exception counts. |
| EDA | Summary-statistics table and documented figures. |
| ITT | Arm counts, unadjusted estimate, standard error and confidence interval. |
| CUPED / regression | Model table, cohort size, covariates, standard-error method, variance-reduction comparison. |
| DiD | Pre-trend plot, slope estimate, event-study plot, joint lead test, placebo and sensitivity results. |
| Reproducibility | Package versions, random seed, clean run log, output index. |

## 11. Final execution checklist

- [ ] Confirm every file's actual schema and observation grain.
- [ ] Confirm synthetic versus real/public data labels.
- [ ] Freeze outcome definitions and denominators.
- [ ] Validate identifiers, joins, assignment, refunds, and outcome maturity.
- [ ] Publish EDA and quality outputs before treatment-effect interpretation.
- [ ] Run unadjusted ITT, CUPED, and regression adjustment on a consistent cohort.
- [ ] Run DiD pre-trend/event-study/placebo/sensitivity diagnostics.
- [ ] Record limitations and avoid causal claims if assumptions or data quality fail.
- [ ] Restart the notebook kernel and execute all cells from top to bottom.
