import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


sns.set_style('whitegrid')

# reading the source file
df = pd.read_csv("Physical data with coverage2.csv")


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
result_df_display = st.dataframe(result_df[['Warp*Weft', 'EPI','PPI', 'Finish Width', 'Coverage group', 'Warp Shrinkage','Weft Shrinkage', 'New Warp Tear','New Weft Tear', 'Warp Tensile', 'Weft Tensile','Warp Slippage', 'Weft Slippage', 'Growth', 'Elongation', 'GSM' ]])

# graphical section
col1, col2 = st.columns(2)
fig1 = plt.figure(figsize=(8, 3))
sns.violinplot(data=result_df, x='EPI', linewidth=3)
col1.pyplot(fig1)

fig2 = plt.figure(figsize=(8, 3))
sns.violinplot(data=result_df, x='PPI', linewidth=3)
col2.pyplot(fig2)

col1, col2 = st.columns(2)
fig3 = plt.figure(figsize=(8, 3))
sns.scatterplot(data=result_df, x='Warp Tensile', y='Weft Tensile', hue='Coverage group', s=100, alpha=0.75)
col1.pyplot(fig3)

fig4 = plt.figure(figsize=(8, 3))
sns.scatterplot(data=result_df, x='New Warp Tear', y='New Weft Tear', hue='Coverage group', s=100, alpha=0.75)
col2.pyplot(fig4)

col1, col2 = st.columns(2)
fig5 = plt.figure(figsize=(8, 3))
sns.lineplot(data=result_df, x='Growth')
col1.pyplot(fig5)

fig6 = plt.figure(figsize=(8, 3))
sns.lineplot(data=result_df, x='Elongation')
col2.pyplot(fig6)