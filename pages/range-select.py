# important librabries
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# basic configurations
st.set_page_config(
    page_title="F3P Main : Range Select",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# seaborn graph styling
sns.set_style('darkgrid')


# reading the source file
df = pd.read_csv("main_data.csv")
cover_df = pd.read_csv("Coverage data.csv")
articles_df = pd.read_csv("articles.csv")

# an apt heading
st.header("Fabric Physical Parameters Predictor: Range-Select")

col1, col2, col3, col4, col5 = st.columns(5)

# more finer selection
df['warp'], df['weft'] = df['Warp*Weft'].str.split("*",1).str
all_warp_list = df['warp'].unique()
warp_count_select = col1.selectbox("Warp count:", all_warp_list)
warp_spun_select = col2.selectbox("Warp compo:", all_warp_list)
all_weft_list = df['weft'].unique()
weft_count_select = col3.selectbox("Weft count:", all_weft_list)
weft_spun_select = col4.selectbox("Weft compo:", all_weft_list)
all_weaves = df['Weave'].unique()
weave_selectbox = col5.selectbox("Weave select:", all_weaves)
all_articles = articles_df['K1'].unique()
article_select = col1.selectbox("Articles", all_articles)

selection_df = articles_df.loc[(articles_df['K1']==article_select)]
df_display = st.table(selection_df)