"""Shared cleaning logic for the Mental Health in Tech survey (OSMI 2014)."""
import pandas as pd
import numpy as np
import re

US_STATES = {
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA',
    'ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK',
    'OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC'
}

def normalize_gender(g):
    if pd.isna(g):
        return 'Other/Unspecified'
    g = str(g).strip().lower()
    male_set = {'m','male','man','cis male','cis man','male (cis)','mail','maile','make','mal',
                'malr','msle','male-ish','male leaning androgynous','guy (-ish) ^_^',
                'ostensibly male, unsure what that really means','cis male','male '}
    female_set = {'f','female','woman','cis female','femake','female ','female (cis)',
                  'cis-female/femme','femail'}
    if g in male_set:
        return 'Male'
    if g in female_set:
        return 'Female'
    if g in {'trans woman','trans-female','female (trans)'}:
        return 'Trans Woman'
    if any(k in g for k in ['non-binary','nonbinary','enby','genderqueer','fluid','androgyne',
                             'agender','queer','neuter']):
        return 'Non-binary/Other'
    return 'Other/Unspecified'

def load_and_clean(path='data/survey.csv'):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    # Age: clip absurd values, keep plausible working-age range
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df.loc[(df['Age'] < 15) | (df['Age'] > 80), 'Age'] = np.nan
    df['Age'] = df['Age'].fillna(df['Age'].median()).astype(int)

    def age_band(a):
        if a < 25: return '18-24'
        if a < 35: return '25-34'
        if a < 45: return '35-44'
        if a < 55: return '45-54'
        return '55+'
    df['age_band'] = df['Age'].apply(age_band)

    # Gender normalization
    df['gender_clean'] = df['Gender'].apply(normalize_gender)

    # State: only meaningful for US
    df['state'] = df['state'].fillna('N/A')
    df['is_us'] = df['Country'] == 'United States'

    # self_employed / work_interfere nulls -> explicit category
    df['self_employed'] = df['self_employed'].fillna('No')
    df['work_interfere'] = df['work_interfere'].fillna('Not Applicable')

    # comments: flag whether they left one, drop free text from analytics use
    df['has_comment'] = df['comments'].notna()

    # Binary target
    df['treatment_bin'] = (df['treatment'] == 'Yes').astype(int)

    # Company size ordering
    size_order = ['1-5','6-25','26-100','100-500','500-1000','More than 1000']
    df['no_employees'] = pd.Categorical(df['no_employees'], categories=size_order, ordered=True)

    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    return df

if __name__ == '__main__':
    d = load_and_clean('data/survey.csv')
    print(d.shape)
    print(d[['Age','gender_clean','no_employees']].head())
