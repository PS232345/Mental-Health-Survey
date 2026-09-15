import streamlit as st
import plotly.graph_objects as go
from utils.theme import inject, card
from utils.model import get_model_and_data, FEATURES

st.set_page_config(page_title="Risk Lens · MindScope", page_icon="🧭", layout="wide")
inject()

st.markdown("# 🧭 Risk Lens")
card("""
This is a <b>workplace-conditions explorer</b>, not a mental health screening tool.
Pick a combination of workplace conditions below (company size, benefits, leave policy, etc.)
and see what share of survey respondents with a <i>similar workplace profile</i> reported
having sought treatment historically. It describes a pattern in 2014 survey data — it does not
assess, diagnose, or predict anything about you or any individual.
""", clay=True)

pipe, df = get_model_and_data()

st.markdown("### Build a workplace profile")
c1, c2, c3, c4 = st.columns(4)
with c1:
    no_employees = st.selectbox("Company size", df["no_employees"].cat.categories.tolist(), index=2)
    remote_work = st.selectbox("Remote work", sorted(df["remote_work"].unique()))
with c2:
    benefits = st.selectbox("Mental health benefits offered", sorted(df["benefits"].unique()))
    care_options = st.selectbox("Care options known", sorted(df["care_options"].unique()))
with c3:
    anonymity = st.selectbox("Anonymity protected", sorted(df["anonymity"].unique()))
    leave = st.selectbox("Ease of taking leave",
                          ["Very difficult", "Somewhat difficult", "Don't know",
                           "Somewhat easy", "Very easy"])
with c4:
    family_history = st.selectbox("Family history of mental illness", sorted(df["family_history"].unique()))
    work_interfere = st.selectbox("Work interference reported",
                                   ["Not Applicable", "Never", "Rarely", "Sometimes", "Often"])

selections = dict(no_employees=no_employees, remote_work=remote_work, benefits=benefits,
                   care_options=care_options, anonymity=anonymity, leave=leave,
                   family_history=family_history, work_interfere=work_interfere)

proba = pipe.predict_proba(
    __import__("pandas").DataFrame([selections])[FEATURES]
)[0][1]

st.markdown("### Historical pattern match")
gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=round(proba * 100, 1),
    number={"suffix": "%", "font": {"family": "Lora", "size": 44, "color": "#4f6b56"}},
    gauge={
        "axis": {"range": [0, 100], "tickcolor": "#8a8578"},
        "bar": {"color": "#6d8b74"},
        "bgcolor": "#fffdf8",
        "borderwidth": 1,
        "bordercolor": "#e4dcc9",
        "steps": [
            {"range": [0, 33], "color": "#f2ece0"},
            {"range": [33, 66], "color": "#e8e0cf"},
            {"range": [66, 100], "color": "#ded3b8"},
        ],
    },
    domain={"x": [0, 1], "y": [0, 1]},
))
gauge.update_layout(height=280, margin=dict(t=10, b=10, l=10, r=10),
                     paper_bgcolor="#fffdf8", font_family="Inter")
c1, c2 = st.columns([1, 1.4])
with c1:
    st.plotly_chart(gauge, use_container_width=True)
with c2:
    st.markdown(f"""
    <div class="mindscope-card">
    <b>{proba*100:.0f}% of respondents</b> with this workplace profile (in the 2014 OSMI survey)
    reported having sought mental health treatment.
    <br><br>
    Try toggling one factor at a time — e.g. switch <i>benefits</i> from "Don't know" to "Yes",
    or <i>leave</i> from "Don't know" to "Very easy" — and watch how much the pattern shifts.
    That's the whole point of this page: showing which workplace levers move the needle most,
    within this dataset.
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Sensitivity: changing one factor at a time")
base = selections.copy()
factor = st.selectbox("Pick a factor to sweep", FEATURES, index=2,
                       format_func=lambda x: x.replace("_", " ").title())

options_map = {
    "no_employees": df["no_employees"].cat.categories.tolist(),
    "remote_work": sorted(df["remote_work"].unique()),
    "benefits": sorted(df["benefits"].unique()),
    "care_options": sorted(df["care_options"].unique()),
    "anonymity": sorted(df["anonymity"].unique()),
    "leave": ["Very difficult", "Somewhat difficult", "Don't know", "Somewhat easy", "Very easy"],
    "family_history": sorted(df["family_history"].unique()),
    "work_interfere": ["Not Applicable", "Never", "Rarely", "Sometimes", "Often"],
}

import pandas as pd
rows = []
for opt in options_map[factor]:
    trial = base.copy()
    trial[factor] = opt
    p = pipe.predict_proba(pd.DataFrame([trial])[FEATURES])[0][1]
    rows.append({"option": opt, "rate": p * 100})
sweep_df = pd.DataFrame(rows)

import plotly.express as px
fig = px.bar(sweep_df, x="option", y="rate", color_discrete_sequence=["#6d8b74"],
             labels={"rate": "Historical treatment-seeking %", "option": factor.replace("_", " ").title()})
fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8", plot_bgcolor="#fffdf8",
                   font_family="Inter")
st.plotly_chart(fig, use_container_width=True)
