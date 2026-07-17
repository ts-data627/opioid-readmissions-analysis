# Opioid Prescribing & Hospital Readmissions: A State-Level Analysis

## The Question

Do states and hospitals with higher opioid prescribing rates also show higher hospital readmission rates? I investigated this from multiple angles — overall prescribing volume, long-acting opioid prescribing specifically, rural vs. urban prescribing patterns, and facility-level outliers — to see whether opioid prescribing is a meaningful driver of readmissions, or whether the relationship is weaker than the popular narrative suggests.

**[View the interactive dashboard on Tableau Public →](https://public.tableau.com/views/OpioidPrescribingHospitalReadmissionsState-LevelAnalysis/Dashboard1?:language=en-US&:sid=&:redirect=auth&publish=yes&showOnboarding=true&:display_count=n&:origin=viz_share_link)**

## Key Findings

- **Weak correlation, overall.** The 10 states with the highest opioid prescribing rates showed tightly clustered average readmission rates (12–15%), despite a wide spread in prescribing rates. Prescribing volume alone doesn't appear to be a strong predictor of readmissions at the state level.
- **Long-acting opioids tell the same story.** Isolating long-acting opioid prescribing (higher risk for dependency and adverse events) produced the same tight clustering pattern — no stronger relationship than overall prescribing.
- **Rural vs. urban prescribing is nearly identical.** Average prescribing rates differed by only 0.02 percentage points between rural and urban populations — no meaningful gap.
- **Heart failure drives the most total readmissions** across all hospitals, by volume.
- **But hip/knee replacement readmissions are the most severe outliers.** The majority of the top 100 hospital-level "worse than expected" readmission ratios were driven by hip/knee replacement (READM-30-HIP-KNEE-HRRP) — a distinct signal from the volume-based finding above, and one worth deeper investigation.

- **A linear regression model confirms it.** Using opioid prescribing rate to predict average state-level readmission rate, the model explains only ~16% of the variance (R² = 0.158, MAE = 0.78). Opioid prescribing rate alone is not a meaningful predictor of readmission rate.

**Takeaway:** Opioid prescribing rates alone don't explain readmission patterns in this data — this holds up across SQL analysis, visualization, and a regression model. Readmissions are more likely driven by condition-specific care gaps — particularly around hip/knee replacement follow-up — than by prescribing behavior.

## Dashboard

Two state-level choropleth maps (opioid prescribing rate, average readmission rate) and a scatter plot comparing the two, built in Tableau and published to Tableau Public.

## Methodology

**Data sources:**
- CMS Hospital Readmissions Reduction Program (HRRP), FY2026 — 18,330 hospital-level rows, covering 07/01/2021–06/30/2024
- CMS Medicare Part D Opioid Prescribing Rates by Geography, 2023 — 30,902 rows across National, State, County, and ZIP levels

**Pipeline:**
1. **Extract** — raw CMS CSVs loaded into PostgreSQL staging tables (loose typing, to safely hold messy source data like non-numeric placeholder values)
2. **Transform** — null handling, type casting, derived columns (readmission rate buckets via `pd.cut()`), state-name-to-abbreviation mapping for joining across datasets
3. **Load** — cleaned, properly typed data loaded into final tables in AWS RDS PostgreSQL
4. **Analyze** — 6 SQL queries answering distinct business questions (top prescribing states, prescribing vs. readmissions, condition-level readmission drivers, long-acting opioid patterns, rural vs. urban comparison, facility-level outliers)
5. **Visualize** — Tableau dashboard connected directly to the cleaned RDS tables
6. **Model** — a simple linear regression (scikit-learn) testing opioid prescribing rate as a predictor of average state-level readmission rate

All SQL queries are in [`/sql/analysis`](./sql/analysis), each with a comment header explaining the business question it answers.

## Tech Stack

Python (Pandas, SQLAlchemy, scikit-learn) · PostgreSQL (AWS RDS) · SQL · Tableau

## What I'd Explore Next

- Facility-level investigation into *why* hip/knee replacement readmissions are disproportionately severe — discharge planning practices, post-acute care access, or patient risk mix
- A multi-feature model incorporating additional predictors beyond prescribing rate (hospital size, discharge volume, condition mix) to see if readmissions become more predictable
- Multi-year opioid prescribing data (this analysis used a single year, 2023) to see whether trends over time reveal a relationship that a single snapshot misses
