"""In-memory SQLite backend built from the cleaned survey data, so the
SQL Analytics page runs real SQL (not pandas) against the dataset -
mirroring the query-bank pattern used in the Cricbuzz LiveStats project."""
import sqlite3
import streamlit as st
from utils.clean import load_and_clean


@st.cache_resource
def get_connection():
    df = load_and_clean("data/survey.csv")
    df = df.copy()
    df["Timestamp"] = df["Timestamp"].astype(str)
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    df.to_sql("survey", conn, index=False, if_exists="replace")
    return conn


def run_query(sql):
    conn = get_connection()
    import pandas as pd
    return pd.read_sql_query(sql, conn)


QUERIES = {
    "Treatment rate by company size": """
        SELECT no_employees AS company_size,
               ROUND(AVG(treatment_bin)*100, 1) AS treatment_rate_pct,
               COUNT(*) AS respondents
        FROM survey
        GROUP BY no_employees
        ORDER BY treatment_rate_pct DESC;
    """,
    "Treatment rate by family history": """
        SELECT family_history,
               ROUND(AVG(treatment_bin)*100, 1) AS treatment_rate_pct,
               COUNT(*) AS respondents
        FROM survey GROUP BY family_history;
    """,
    "Top 10 countries by respondent count": """
        SELECT Country, COUNT(*) AS respondents
        FROM survey GROUP BY Country
        ORDER BY respondents DESC LIMIT 10;
    """,
    "Benefits awareness vs treatment rate": """
        SELECT benefits,
               ROUND(AVG(treatment_bin)*100, 1) AS treatment_rate_pct,
               COUNT(*) AS respondents
        FROM survey GROUP BY benefits
        ORDER BY treatment_rate_pct DESC;
    """,
    "Fear of consequences: mental vs physical (counts)": """
        SELECT mental_health_consequence, COUNT(*) AS respondents
        FROM survey GROUP BY mental_health_consequence
        ORDER BY respondents DESC;
    """,
    "Average age by treatment status": """
        SELECT treatment, ROUND(AVG(Age),1) AS avg_age, COUNT(*) AS respondents
        FROM survey GROUP BY treatment;
    """,
    "Remote work vs treatment rate": """
        SELECT remote_work,
               ROUND(AVG(treatment_bin)*100, 1) AS treatment_rate_pct,
               COUNT(*) AS respondents
        FROM survey GROUP BY remote_work;
    """,
    "Care options awareness by company size": """
        SELECT no_employees AS company_size, care_options, COUNT(*) AS respondents
        FROM survey GROUP BY no_employees, care_options
        ORDER BY no_employees;
    """,
    "Work interference distribution": """
        SELECT work_interfere, COUNT(*) AS respondents,
               ROUND(AVG(treatment_bin)*100,1) AS treatment_rate_pct
        FROM survey GROUP BY work_interfere
        ORDER BY treatment_rate_pct DESC;
    """,
    "Top 10 US states by respondent count": """
        SELECT state, COUNT(*) AS respondents
        FROM survey WHERE is_us = 1 AND state != 'N/A'
        GROUP BY state ORDER BY respondents DESC LIMIT 10;
    """,
    "Gender distribution (cleaned)": """
        SELECT gender_clean AS gender, COUNT(*) AS respondents,
               ROUND(AVG(treatment_bin)*100,1) AS treatment_rate_pct
        FROM survey GROUP BY gender_clean
        ORDER BY respondents DESC;
    """,
    "Ease of leave vs treatment rate": """
        SELECT leave, ROUND(AVG(treatment_bin)*100,1) AS treatment_rate_pct,
               COUNT(*) AS respondents
        FROM survey GROUP BY leave
        ORDER BY treatment_rate_pct DESC;
    """,
    "Tech company vs non-tech: treatment rate": """
        SELECT tech_company,
               ROUND(AVG(treatment_bin)*100,1) AS treatment_rate_pct,
               COUNT(*) AS respondents
        FROM survey GROUP BY tech_company;
    """,
    "Respondents who observed negative consequences, by company size": """
        SELECT no_employees AS company_size,
               SUM(CASE WHEN obs_consequence='Yes' THEN 1 ELSE 0 END) AS observed_consequences,
               COUNT(*) AS respondents
        FROM survey GROUP BY no_employees
        ORDER BY no_employees;
    """,
    "Age band vs treatment rate": """
        SELECT age_band, ROUND(AVG(treatment_bin)*100,1) AS treatment_rate_pct,
               COUNT(*) AS respondents
        FROM survey GROUP BY age_band
        ORDER BY age_band;
    """,
}
