import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from collections import Counter
from utils.theme import inject, card
from utils.clean import load_and_clean

st.set_page_config(page_title="Voices · MindScope", page_icon="💬", layout="wide")
inject()

st.markdown("# 💬 Voices")
card("""About 13% of respondents left an optional free-text comment. To respect that this is
personal, anonymous text, this page shows only <b>aggregate word patterns</b> — no individual
comment is displayed or quoted here.""")

df = load_and_clean("data/survey.csv")
comments = df["comments"].dropna().astype(str)

STOPWORDS = set("""a an the and or but if to of in on for with is are was were be been being
this that these those i my me we our you your it its as at by from not no so do does did
have has had can could would should will just also very really think feel about work
company mental health people time one get much""".split())

def tokenize(text):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

all_words = []
for c in comments:
    all_words.extend(tokenize(c))

counts = Counter(all_words)

c1, c2 = st.columns([1.2, 1])
with c1:
    st.markdown("### Word cloud of comment themes")
    if counts:
        wc = WordCloud(width=900, height=500, background_color="#fffdf8",
                        colormap=None, color_func=lambda *a, **k: "#4f6b56"
                        if hash(a[0]) % 2 == 0 else "#a9694f",
                        max_words=80).generate_from_frequencies(counts)
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        fig.patch.set_facecolor("#fffdf8")
        st.pyplot(fig)
    else:
        st.info("No comments available to visualize.")

with c2:
    st.markdown("### Top 15 recurring words")
    top = counts.most_common(15)
    import pandas as pd
    top_df = pd.DataFrame(top, columns=["word", "count"])
    import plotly.express as px
    fig = px.bar(top_df.sort_values("count"), x="count", y="word", orientation="h",
                 color_discrete_sequence=["#6d8b74"])
    fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                       plot_bgcolor="#fffdf8", font_family="Inter", height=460)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Who leaves a comment?")
c1, c2 = st.columns(2)
with c1:
    rate = df.groupby("treatment")["has_comment"].mean() * 100
    import plotly.express as px
    fig = px.bar(rate.reset_index(), x="treatment", y="has_comment",
                 labels={"has_comment": "% who left a comment"},
                 color_discrete_sequence=["#c98a6b"])
    fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                       plot_bgcolor="#fffdf8", font_family="Inter",
                       title="Comment rate by treatment status", title_font_family="Lora")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    st.markdown(f"""
    <div class="mindscope-card">
    <b>{len(comments)}</b> respondents ({len(comments)/len(df)*100:.0f}%) left an optional comment.
    People who report having sought treatment are slightly more likely to leave a comment —
    consistent with having more to say once they've engaged with the topic personally.
    </div>
    """, unsafe_allow_html=True)
