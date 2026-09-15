"""Trains a small logistic regression on the survey's WORKPLACE factors
(never demographic/medical framing about an individual) to illustrate which
combinations of workplace conditions are associated with higher treatment-
seeking rates *within this historical dataset*. Explicitly a pattern-
exploration tool, not a diagnostic or predictive tool about any real person.
"""
import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from utils.clean import load_and_clean

FEATURES = [
    "no_employees", "remote_work", "benefits", "care_options",
    "anonymity", "leave", "family_history", "work_interfere",
]


@st.cache_resource
def get_model_and_data():
    df = load_and_clean("data/survey.csv")
    X = df[FEATURES]
    y = df["treatment_bin"]

    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), FEATURES)
    ])
    pipe = Pipeline([
        ("prep", pre),
        ("clf", LogisticRegression(max_iter=1000))
    ])
    pipe.fit(X, y)
    return pipe, df


def predict_share(pipe, selections: dict):
    row = pd.DataFrame([selections])[FEATURES]
    proba = pipe.predict_proba(row)[0][1]
    return proba
