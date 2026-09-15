import streamlit as st
import plotly.express as px
from utils.theme import inject, card
from utils.clean import load_and_clean

st.set_page_config(page_title="Explorer · MindScope", page_icon="🔍", layout="wide")
inject()
df = load_and_clean("data/survey.csv")

st.markdown("# 🔍 Explorer")
card("Filter the sample and watch every chart update — a live version of the bivariate/"
     "multivariate analysis from the EDA notebook.")

with st.sidebar:
    st.markdown("### Filters")
    countries = st.multiselect("Country", sorted(df["Country"].unique()),
                                default=["United States", "United Kingdom"]
                                if "United Kingdom" in df["Country"].unique() else None)
    sizes = st.multiselect("Company size", df["no_employees"].cat.categories.tolist(),
                            default=df["no_employees"].cat.categories.tolist())
    remote_only = st.checkbox("Remote workers only")

f = df.copy()
if countries:
    f = f[f["Country"].isin(countries)]
if sizes:
    f = f[f["no_employees"].isin(sizes)]
if remote_only:
    f = f[f["remote_work"] == "Yes"]

st.caption(f"{len(f)} respondents match current filters")

if len(f) == 0:
    st.warning("No respondents match these filters — widen your selection.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Treatment patterns", "Workplace factors", "Stigma & disclosure"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(f.groupby("family_history")["treatment_bin"].mean().reset_index(),
                     x="family_history", y="treatment_bin",
                     color_discrete_sequence=["#6d8b74"],
                     labels={"treatment_bin": "Treatment rate", "family_history": "Family history"})
        fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                           plot_bgcolor="#fffdf8", font_family="Inter")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        order = ["Not Applicable", "Never", "Rarely", "Sometimes", "Often"]
        g = f.groupby("work_interfere")["treatment_bin"].mean().reindex(order).reset_index()
        fig = px.line(g, x="work_interfere", y="treatment_bin", markers=True,
                      color_discrete_sequence=["#c98a6b"],
                      labels={"treatment_bin": "Treatment rate", "work_interfere": "Work interference"})
        fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                           plot_bgcolor="#fffdf8", font_family="Inter")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        g = f.groupby("no_employees", observed=True)["treatment_bin"].mean().reset_index()
        fig = px.bar(g, x="no_employees", y="treatment_bin", color_discrete_sequence=["#6d8b74"],
                     labels={"treatment_bin": "Treatment rate", "no_employees": "Company size"})
        fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                           plot_bgcolor="#fffdf8", font_family="Inter")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(f.groupby("benefits")["treatment_bin"].mean().reset_index(),
                     x="benefits", y="treatment_bin", color_discrete_sequence=["#c98a6b"],
                     labels={"treatment_bin": "Treatment rate", "benefits": "Benefits offered"})
        fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                           plot_bgcolor="#fffdf8", font_family="Inter")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(f, x="mental_health_consequence", color_discrete_sequence=["#6d8b74"],
                           title="Fear of consequences (mental)")
        fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                           plot_bgcolor="#fffdf8", font_family="Inter", title_font_family="Lora")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.histogram(f, x="supervisor", color_discrete_sequence=["#c98a6b"],
                           title="Willing to discuss with supervisor")
        fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                           plot_bgcolor="#fffdf8", font_family="Inter", title_font_family="Lora")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("### Filtered data")
st.dataframe(f[["Age", "gender_clean", "Country", "no_employees", "remote_work",
                "benefits", "treatment", "work_interfere"]].reset_index(drop=True),
             use_container_width=True, height=300)
