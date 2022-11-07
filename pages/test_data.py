
#! important librabries
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

#! basic configurations
st.set_page_config(
    page_title="testing domain",
    page_icon="❓",
    layout="wide",
    initial_sidebar_state="collapsed")

#! seaborn graph styling
sns.set_style('darkgrid')

#! reading the source file
df = pd.read_csv("main_params_data.csv")
main_df = df.dropna(subset=['Warp Tear    (ASTMD1424)'])

#! conditional columns
main_df['style'] = ['Pigment' if x.startswith('P') or x.startswith('DU') else 'Reactive' if x.startswith('R') else 'Discharge' for x in main_df['Print Color']]

#! an apt heading
st.header("experimentation tab")

#! column-wise split: article selection & finsih-style selection
col1, col2, col3 = st.columns(3)

try:
    all_articles = main_df['Article No.'].unique()
    article_selectbox = col1.multiselect("Select Article:", sorted(all_articles), default=all_articles[0], help="Select one or more articles to see the data table")
    article_df = main_df[main_df['Article No.'].isin(article_selectbox)]
    finish = col2.multiselect("Select Finish Code:", article_df.Pattern.unique(), default=article_df.Pattern.unique()[0], help="Select one or more finish codes to see the data table")
    style = col3.radio("Select Style:", article_df['style'].unique())
    #st.write(f"debug : {finish}")
    selection_df = main_df.loc[(main_df['Article No.'].isin(article_selectbox))&(main_df['Pattern'].isin(finish))&(main_df['style']==style)]
except:
    st.error("Please select data to display 👆")


#! dataframe display
tab1, tab2 = st.tabs(["Selected Data", "All Data"])
try:
    df_display = tab1.dataframe(selection_df)
except:
    st.warning("No data to show but still you see All Data")
finally:
    df_display = tab2.dataframe(main_df)

st.file_uploader("Upload latest data", type=['csv','xlsx'], accept_multiple_files=False, help="Only upload Article-Wise param data file")

