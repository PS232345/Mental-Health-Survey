import streamlit as st
import plotly.express as px
from utils.theme import inject, card
from utils.db import QUERIES, run_query

st.set_page_config(page_title="SQL Analytics · MindScope", page_icon="🗃️", layout="wide")
inject()

st.markdown("# 🗃️ SQL Analytics")
card("A bank of real SQL queries running against an in-memory SQLite copy of the cleaned "
     "survey — pick one, or write your own read-only query against the <code>survey</code> table.")

tab1, tab2 = st.tabs(["Query bank", "Run your own SQL"])

with tab1:
    choice = st.selectbox("Choose a query", list(QUERIES.keys()))
    sql = QUERIES[choice]
    st.code(sql.strip(), language="sql")
    result = run_query(sql)
    st.dataframe(result, use_container_width=True)

    numeric_cols = [c for c in result.columns if result[c].dtype != object][:1]
    if numeric_cols and result.shape[0] <= 25 and result.shape[1] >= 2:
        label_col = result.columns[0]
        val_col = numeric_cols[0]
        fig = px.bar(result, x=label_col, y=val_col, color_discrete_sequence=["#6d8b74"])
        fig.update_layout(template="simple_white", paper_bgcolor="#fffdf8",
                           plot_bgcolor="#fffdf8", font_family="Inter")
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.caption("Table: `survey` — columns include Age, gender_clean, Country, state, "
               "no_employees, remote_work, benefits, care_options, anonymity, leave, "
               "family_history, work_interfere, treatment, treatment_bin, age_band, has_comment.")
    user_sql = st.text_area("SQL query", "SELECT gender_clean, COUNT(*) FROM survey GROUP BY gender_clean;",
                             height=100)
    if st.button("Run query"):
        forbidden = ["drop", "delete", "update", "insert", "alter", "attach"]
        if any(k in user_sql.lower() for k in forbidden):
            st.error("Only read-only SELECT queries are allowed here.")
        else:
            try:
                st.dataframe(run_query(user_sql), use_container_width=True)
            except Exception as e:
                st.error(f"Query error: {e}")
