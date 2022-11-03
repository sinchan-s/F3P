
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

#! conditional columns
df['style'] = ['Pigment' if x.startswith('P') or x.startswith('DU') else 'Reactive' if x.startswith('R') else 'Discharge' for x in df['Print Color']]

#! an apt heading
st.header("experimentation tab")

#! column-wise split: article selection & finsih-style selection
col1, col2, col3 = st.columns(3)

try:
    all_articles = df['Article No.'].unique()
    article_selectbox = col1.multiselect("Select Article:", all_articles, default='14015')
    article_df = df[df['Article No.'].isin(article_selectbox)]
    finish = col2.multiselect("Select Finish Code:", article_df.Pattern.unique(), default=article_df.Pattern.unique()[0])
    style = col3.radio("Select Style:", article_df['style'].unique())
    st.write(f"debug : {finish}")
    selection_df = df.loc[(df['Article No.'].isin(article_selectbox))&(df['Pattern'].isin(finish))&(df['style']==style)]
except:
    st.subheader("Please select data to display 👆")

#! dataframe display
try:
    df_display = st.dataframe(selection_df)
except:
    st.subheader("No table to show 😔")