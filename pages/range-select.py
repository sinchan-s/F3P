
#! important librabries
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import re

#! basic configurations
st.set_page_config(
    page_title="F3P Main : Range Select",       #! similar to <title> tag
    page_icon="🔍",                             #! page icon
    layout="wide",                              #! widen-out view of the layout
    initial_sidebar_state="collapsed")          #! side-bar state when page-load


#! seaborn graph styling
sns.set_style('darkgrid')

#! reading the source file
df = pd.read_csv("main_data.csv")
cover_df = pd.read_csv("Coverage data.csv")
articles_df = pd.read_csv("articles.csv")

#! an apt heading
st.header("Fabric Physical Parameters Predictor: Range-Select")

#! single column for single article select
all_articles = articles_df['K1'].unique()
article_select = st.selectbox("Articles", all_articles)
selection_df = articles_df.loc[(articles_df['K1']==article_select)]
selection_df['warp'], selection_df['weft'] = selection_df['Warp*Weft'].str.split("*",1).str

#! more finer selection
col1, col2, col3, col4, col5 = st.columns(5)
wa_match = r"\d+"
all_warp_list = selection_df['warp'].unique()
wa_count_search = re.search(wa_match, all_warp_list[0])
warp_count_select = col1.selectbox("Warp count:", all_warp_list)
warp_spun_select = col2.selectbox("Warp composition:", all_warp_list)
all_weft_list = selection_df['weft'].unique()
weft_count_select = col3.selectbox("Weft count:", all_weft_list)
weft_spun_select = col4.selectbox("Weft composition:", all_weft_list)
all_weaves = selection_df['Weave'].unique()
weave_selectbox = col5.selectbox("Weave select:", all_weaves)

#! metrics display
#wa_count_display = st.metric('Warp Count',wa_count_search[0])
#wa_disp = st.write(wa_count_search)
#! dataframe display
df_display = st.table(selection_df)