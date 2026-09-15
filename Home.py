import streamlit as st
import plotly.express as px
from utils.theme import inject, card, badge
from utils.clean import load_and_clean

st.set_page_config(page_title="MindScope · Workplace Mental Health Atlas",
                    page_icon="🌿", layout="wide")
inject()

df = load_and_clean("data/survey.csv")

st.markdown("# 🌿 MindScope")
st.markdown("##### A field notebook on mental health in the tech workplace &nbsp;·&nbsp; OSMI 2014 Survey")

card(f"""
{badge("1,259 respondents")}{badge("48 countries", clay=True)}{badge("27 questions")}
<p style="margin-top:10px; font-family:'Lora',serif; font-size:1.02rem;">
This is not a dashboard of charts for their own sake — it's an atlas of how tech employees
experience mental health support at work: who asks for help, who doesn't, and what quietly
gets in the way. Walk through the pages on the left: explore the raw patterns, see how workplace
conditions combine, look at it on a map, run real SQL against it, and read what people actually
wrote in their own words.
</p>
""")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Sought treatment", f"{df['treatment_bin'].mean()*100:.0f}%")
c2.metric("Report family history", f"{(df['family_history']=='Yes').mean()*100:.0f}%")
c3.metric("Work remotely", f"{(df['remote_work']=='Yes').mean()*100:.0f}%")
dont_know_share = (df["benefits"] == "Don't know").mean() * 100
c4.metric("Unsure if benefits exist", f"{dont_know_share:.0f}%")

st.markdown("### The shape of the sample")
col1, col2 = st.columns(2)

with col1:
    age_fig = px.histogram(df, x="Age", nbins=25, color_discrete_sequence=["#6d8b74"])
    age_fig.update_layout(template="simple_white", title="Age distribution",
                           paper_bgcolor="#fffdf8", plot_bgcolor="#fffdf8",
                           font_family="Inter", title_font_family="Lora")
    st.plotly_chart(age_fig, use_container_width=True)

with col2:
    treat_fig = px.pie(df, names="treatment", color="treatment", hole=0.5,
                        color_discrete_map={"Yes": "#6d8b74", "No": "#c98a6b"})
    treat_fig.update_layout(template="simple_white", title="Sought treatment?",
                             paper_bgcolor="#fffdf8", font_family="Inter",
                             title_font_family="Lora")
    st.plotly_chart(treat_fig, use_container_width=True)

st.markdown("""
<div class="mindscope-quote">
"Explore, don't diagnose." Every view here describes patterns in a historical, anonymous survey —
none of it is a clinical tool, and nothing here should be read as advice about any individual.
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🌿 MindScope")
st.sidebar.caption("Workplace Mental Health Atlas — OSMI 2014")
