
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

#! Clean Footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden;}
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

#! seaborn graph styling
sns.set_style('darkgrid')

#! reading the source file
df = pd.read_csv("main_data.csv")
cover_df = pd.read_csv("Coverage data.csv")
articles_df = pd.read_csv("articles.csv")

#! an apt heading
st.header("Quality Predictor")

#! single column for single article select
all_articles = articles_df['K1'].unique()
# article_select = st.selectbox("Articles", all_articles)
articles_df['EPI-PPI'] = articles_df['Construction'].str.extract(r'[-*/]{1}([\d]{2,3}[*][\d]{2,3})[-*\s\b]{1}')
spin_dict = {'Carded':'K',
            'Carded Compact': 'K.COM', 
            'Combed': 'C', 
            'Combed Compact': 'C.COM', 
            'Vortex':'VOR', 
            'Open-End':'OE'}
spin_select = st.selectbox("Select Spinning Tech", list(spin_dict),  help="--to be updated--")
selection_df = articles_df[articles_df['Construction'].str.contains(spin_dict.get(spin_select)) & articles_df['Construction'].str.contains('*')]
# st.dataframe(test_df)
# selection_df = articles_df.loc[(articles_df['K1']==article_select)]
selection_df['Warp'], selection_df['Weft'] = selection_df['Warp*Weft'].str.split("*",1).str

#! more finer selection
wa_match = r"\d+"
# all_warp_list = selection_df['warp'].unique()
# all_weft_list = selection_df['weft'].unique()
all_weaves = articles_df['Weave'].unique()
# wa_count_search = re.search(wa_match, all_warp_list[0])
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    warp_count_select = st.selectbox("Warp count-comp:", selection_df['Warp'].unique())
    # warp_count_select2 = st.selectbox("Warp count2:", all_warp_list)
with col2:
    weft_count_select = st.selectbox("Weft count:", selection_df['Weft'].unique())
with col3:
    weave_selectbox = st.selectbox("Weave select:", selection_df['Weave'].unique())
# with col4:
# with col5:

#! metrics display
#wa_count_display = st.metric('Warp Count',wa_count_search[0])
#wa_disp = st.write(wa_count_search)
#! dataframe display
tab1, tab2 = st.tabs(['Selected Data', 'All Data'])
with tab1:
    df_display = st.dataframe(selection_df)
with tab2:
    df_display = st.dataframe(articles_df)