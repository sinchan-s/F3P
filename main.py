import pandas as pd
import streamlit as st

df = pd.read_csv("Physical data with coverage.csv")
st.header("Fabric Physical Parameters Predictor")

total_articles = df['Article No.'].unique()
s_article = st.selectbox("Select Article", total_articles)
article_df = df[df['Article No.']==s_article]

col1, col2, col3 = st.columns(3)
article = col1.metric('', article_df.Weave.unique()[0])
finish = col2.selectbox("Finish Code", article_df.Finish.unique())
style = col3.selectbox("Style", article_df.Style.unique())
result_df = st.dataframe(article_df[['Warp Shrinkage','Weft Shrinkage', 'Warp Tear','Weft Tear', 'Warp Tensile', 'Weft Tensile','Warp Slippage', 'Weft Slippage', 'Growth', 'Elongation', 'GSM']])

#st.dataframe(data=article_df)