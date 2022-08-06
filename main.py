import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# reading the source file
df = pd.read_csv("Physical data with coverage.csv")


# an apt heading
st.header("Fabric Physical Parameters Predictor")


# article selection
all_articles = df['Article No.'].unique()
select_article = st.selectbox("Select Article", all_articles)
article_df = df[df['Article No.']==select_article]


# warp-weft count segregation and identification
#count = article_df['Warp*Weft'][0].split('*')
#warp_count = count[0]
#weft_count = count[1]
count = article_df['Warp*Weft']

# column-wise display & selection
col1, col2, col3 = st.columns(3)
article = col1.metric('Weave', article_df.Weave.unique()[0])
#count_warp = col1.metric('Warp Count',warp_count)
#count_weft = col1.metric('Weft Count',weft_count)
#count_const = col1.metric('Const', count)
finish = col2.selectbox("Select Finish Code", article_df.Finish.unique())
style = col3.selectbox("Select Style", article_df.Style.unique())


# final display dataframe
result_df = df.loc[(df['Article No.']==select_article)&(df['Finish']==finish)&(df['Style']==style)]
result_df_display = st.dataframe(result_df[['Warp*Weft', 'EPI','PPI', 'Finish Width', 'Coverage group', 'Warp Shrinkage','Weft Shrinkage', 'Warp Tear','Weft Tear', 'Warp Tensile', 'Weft Tensile','Warp Slippage', 'Weft Slippage', 'Growth', 'Elongation', 'GSM']])

fig1 = px.scatter(result_df, x='EPI', y='PPI')
st.plotly_chart(fig1)

fig2 = px.scatter(result_df, x='Warp Tensile', y='Weft Tensile')
st.plotly_chart(fig2)
#st.dataframe(data=count)