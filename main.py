import pandas as pd
import streamlit as st

# reading the source file
df = pd.read_csv("Physical data with coverage.csv")

# an apt heading
st.header("Fabric Physical Parameters Predictor")

# article selection
all_articles = df['Article No.'].unique()
select_article = st.selectbox("Select Article", all_articles)
article_df = df[df['Article No.']==select_article]

col1, col2, col3 = st.columns(3)
article = col1.metric('Weave', article_df.Weave.unique()[0])
count = col1.metric('Count',article_df['Warp*Weft'][0])
finish = col2.selectbox("Select Finish Code", article_df.Finish.unique())
style = col2.selectbox("Select Style", article_df.Style.unique())
result_df = df.loc[(df['Article No.']==select_article)&(df['Finish']==finish)&(df['Style']==style)]
result_df_display = st.dataframe(result_df[['EPI','PPI', 'F_Width', 'Warp Shrinkage','Weft Shrinkage', 'Warp Tear','Weft Tear', 'Warp Tensile', 'Weft Tensile','Warp Slippage', 'Weft Slippage', 'Growth', 'Elongation', 'GSM']])



#st.dataframe(data=result_df)