import pandas as pd
import streamlit as st

df = pd.read_csv("Physical data with coverage.csv")
st.header("Fabric Physical Parameters Predictor")

articles = df['Article No.'].unique()
s_article = st.selectbox("Select Article", articles)

st.dataframe(data=df[df['Article No.']==s_article])