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


# ! column-wise split: article selection & finsih-style selection
col1, col2, col3 = st.columns(3)

try:
    all_articles = main_df['Article No.'].unique()
    article_selectbox = col1.multiselect("Select Article:", sorted(all_articles), default=all_articles[0],
                                         help="Choose one or more articles to see the data table")
    article_df = main_df[main_df['Article No.'].isin(article_selectbox)]
    finish = col2.multiselect("Select Finish Code:", article_df.Pattern.unique(),
                              default=article_df.Pattern.unique()[0],
                              help="Choose one or more finish codes to see the data table")
    style = col3.radio("Select Style:", article_df['style'].unique(), help="Choose any print style")
    # st.write(f"debug : {finish}")
    selection_df = main_df.loc[(main_df['Article No.'].isin(article_selectbox)) & (main_df['Pattern'].isin(finish)) & (
            main_df['style'] == style)]
except:
    st.error("Please select data to display 👆")

# ! dataframe display
with st.expander("Data Tables", expanded=False):
    tab1, tab2 = st.tabs(["Selected Data", "All Data"])
    try:
        df_display = tab1.dataframe(selection_df)
    except:
        st.warning("No data to show but still you can see All Data")
    finally:
        df_display = tab2.dataframe(main_df)

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
    st.dataframe(up_file)
    
except:
    st.write("Upload a file !")