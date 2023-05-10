# ! important librabries
import re
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ! basic configurations
st.set_page_config(
    page_title="testing domain",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="collapsed")

#! Clean Footer
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden;}
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# ! reading the source file
df = pd.read_csv("main_params_data.csv")
main_df = df.dropna(subset=['Warp Tear    (ASTMD1424)'])

# ! conditional columns
main_df['style'] = [
    'Pigment' if x.startswith('P') or x.startswith('DU') else 'Reactive' if x.startswith('R') else 'Discharge' for x in
    main_df['Print Color']]

# ! an apt heading
st.header("experimentation tab")


# QTX file uploader
csv_file = st.file_uploader("Upload csv format file only:", type=['csv'], accept_multiple_files=False, help="Only upload CSV file")

# dataframe display
try:
    up_file = pd.read_csv(csv_file)
    col_list = list(map(str.lower, up_file.columns))
    if 'construction' in col_list:
        const_index = col_list.index('construction')
        # st.write(const_index)
        up_file['WARP'] = up_file.iloc[:, const_index].str.extract(r'^([\d\w\s+.\/()]*)[*]')
        up_file['WEFT'] = up_file.iloc[:, const_index].str.extract(r'^[\d\w\s+.\/()]*[*]([\d\w\s+.\/()]+)')
        up_file['EPI'] = up_file.iloc[:, const_index].str.extract(r'[-](\d{2,3})[*]')
        up_file['PPI'] = up_file.iloc[:, const_index].str.extract(r'[*](\d{2,3})[-]')
        up_file['WIDTH'] = up_file.iloc[:, const_index].str.extract(r'[-*](\d{3}\.?\d{0,2})-')
        up_file['WEAVE'] = up_file.iloc[:, const_index].str.extract(r'-(\d?\/?\d?[,\s]?[A-Z]+\s?[A-Z]*\(?[A-Z\s]+\)?)')
        up_file['GSM'] = up_file.iloc[:, const_index].str.extract(r'[-\s](\d{3}\.?\d?)[\s$]*$')
        with st.expander('Data Table'):
            st.dataframe(up_file)
except:
    st.write("Upload a file !")