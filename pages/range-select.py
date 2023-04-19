
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
st.header("Article Reference")

#! single column for single article select
articles_df['EPI-PPI'] = articles_df['Construction'].str.extract(r'[-*/]{1}([\d]{2,3}[*][\d]{2,3})[-*\s\b]{1}')
articles_df['GSM'] = articles_df['Construction'].str.extract(r'[\w]+[.]?([\d]{3}[.][\d]?)$')

spin_dict = {'Carded':'\d+K[.]',
            'Carded Compact': 'K.COM', 
            'Combed': '\d+C[.]', 
            'Combed Compact': 'C.COM', 
            'Vortex':'VOR',
            'Open-End':'OE'}
all_weaves = articles_df['Weave'].unique()

#! selection criteria
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    warp_spin_select = st.selectbox("Warp Spinning", list(spin_dict),  help="Select the warp spinning technology employed")
with col3:
    weft_spin_select = st.selectbox("Weft Spinning", list(spin_dict),  help="Select the weft spinning technology employed")
# st.write(str(spin_dict.get(warp_spin_select)))
selection_df = articles_df[articles_df['Warp'].str.contains(pat = spin_dict.get(warp_spin_select), regex = True) & articles_df['Weft'].str.contains(spin_dict.get(weft_spin_select))]
with col2:
    warp_count_select = st.selectbox("Warp counts", selection_df['Warp'].unique())
with col4:
    weft_count_select = st.selectbox("Weft counts", selection_df['Weft'].unique())
with col5:
    weave_selectbox = st.selectbox("Weave", selection_df['Weave'].unique())
# selection_df = selection_df[selection_df['Warp'].str.contains(warp_count_select) &   selection_df['Weft'].str.contains(weft_count_select)]


#! dataframe display
tab1, tab2 = st.tabs(['Selected Data', 'All Data'])
with tab1:
    df_display = st.dataframe(selection_df)
with tab2:
    df_display = st.dataframe(articles_df)