import streamlit as st
import plotly.express as px
from utils.theme import inject, card
from utils.clean import load_and_clean

st.set_page_config(page_title="State Map · MindScope", page_icon="🗺️", layout="wide")
inject()

st.markdown("# 🗺️ State Map")
card("US respondents only — the survey has no reliable regional breakdown outside the US, "
     "so this view stays honest about its geographic scope.")

df = load_and_clean("data/survey.csv")
us = df[(df["is_us"]) & (df["state"] != "N/A")]

metric = st.radio("Show", ["Treatment rate", "Respondent count"], horizontal=True)

agg = us.groupby("state").agg(
    treatment_rate=("treatment_bin", "mean"),
    respondents=("treatment_bin", "size")
).reset_index()
agg["treatment_rate"] = (agg["treatment_rate"] * 100).round(1)

# only show states with a meaningful sample
agg_shown = agg[agg["respondents"] >= 5]

color_col = "treatment_rate" if metric == "Treatment rate" else "respondents"
colorscale = ["#f6f1e9", "#c98a6b", "#4f6b56"] if metric == "Treatment rate" else \
             ["#f6f1e9", "#8a8578", "#2f3b30"]

fig = px.choropleth(
    agg_shown, locations="state", locationmode="USA-states", scope="usa",
    color=color_col, color_continuous_scale=colorscale,
    hover_data={"respondents": True, "treatment_rate": True, "state": False},
    labels={"treatment_rate": "Treatment rate (%)", "respondents": "Respondents"},
)
fig.update_layout(paper_bgcolor="#fffdf8", font_family="Inter",
                   geo=dict(bgcolor="#fffdf8", lakecolor="#f6f1e9"),
                   margin=dict(t=10, b=10, l=0, r=0), height=520)
st.plotly_chart(fig, use_container_width=True)

st.caption("States with fewer than 5 respondents are excluded from the map to avoid "
           "misleadingly extreme rates from tiny samples.")

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Top 10 states by respondents")
    st.dataframe(agg.sort_values("respondents", ascending=False).head(10)
                 .rename(columns={"state": "State", "respondents": "Respondents",
                                   "treatment_rate": "Treatment rate (%)"})
                 .reset_index(drop=True), use_container_width=True)
with c2:
    st.markdown("#### Highest treatment rate (min. 10 respondents)")
    st.dataframe(agg[agg["respondents"] >= 10].sort_values("treatment_rate", ascending=False).head(10)
                 .rename(columns={"state": "State", "respondents": "Respondents",
                                   "treatment_rate": "Treatment rate (%)"})
                 .reset_index(drop=True), use_container_width=True)
