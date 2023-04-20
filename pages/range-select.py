
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
count_list = [6, 7, 8, 10, 12, 14, 16, 20, 21, 30, 32, 40, 45, 60, 80]

#! selection criteria
col1, col2, col3 = st.columns(3)
with col1:
    warp_spin_select = st.selectbox("Warp Spinning", list(spin_dict),  help="Select the warp spinning technology employed")
    warp_count_select = st.select_slider("Warp count", count_list, help="Select the warp count")
    warp_ply_check = st.checkbox('Check for double ply', key=1)
    if warp_ply_check:
        warp_value = '2/{warp_count_select}'
    else:
        warp_value = warp_count_select
with col2:
    weft_spin_select = st.selectbox("Weft Spinning", list(spin_dict),  help="Select the weft spinning technology employed")
    weft_count_select = st.select_slider("Weft count", count_list, help="Select the weft count")
    weft_ply_check = st.checkbox('Check for double ply', key=2)
    if weft_ply_check:
        weft_value = '2/{weft_count_select}'
    else:
        weft_value = weft_count_select
with col3:
    weave_selectbox = st.selectbox("Weave", articles_df['Weave'].unique(), help="Select the weft spinning technology employed")
selection_df = articles_df[articles_df['Warp'].str.contains(pat = spin_dict.get(warp_spin_select)) & articles_df['Weft'].str.contains(spin_dict.get(weft_spin_select))]

#! dataframe display
tab1, tab2 = st.tabs(['Selected Data', 'All Data'])
with tab1:
    df_display = st.dataframe(selection_df)
with tab2:
    df_display = st.dataframe(articles_df)