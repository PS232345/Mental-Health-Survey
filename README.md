# 🌿 MindScope — Workplace Mental Health Atlas

An interactive Streamlit app exploring the OSMI 2014 Mental Health in Tech Workplace survey
(1,259 respondents, 48 countries).

## Pages
- **Home** — overview stats and sample shape
- **Explorer** — interactive filters (country, company size, remote work) across all charts
- **Risk Lens** — build a workplace profile (benefits, leave policy, anonymity, etc.) and see
  what share of similarly-profiled 2014 respondents sought treatment, plus a single-factor
  sensitivity sweep. Framed explicitly as a historical-pattern tool, not a diagnostic one.
- **State Map** — US choropleth of treatment rate / respondent count by state
- **Voices** — aggregate word-frequency analysis of optional free-text comments (no individual
  comment is ever displayed, to respect respondent privacy)
- **SQL Analytics** — 15 preset SQL queries against an in-memory SQLite copy of the cleaned
  data, plus a free-form read-only SQL box

## Run locally
```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Deploy on Streamlit Community Cloud
1. Push this folder to a public (or private) GitHub repo.
2. Go to https://share.streamlit.io → "New app" → point it at the repo, branch, and `Home.py`.
3. No secrets needed — the app reads `data/survey.csv` bundled in the repo.

## Data
`data/survey.csv` — OSMI 2014 Mental Health in Tech Survey. Cleaning logic (Gender
normalization, Age outlier handling, missing-value recoding) lives in `utils/clean.py` and is
shared with the companion EDA notebook.
