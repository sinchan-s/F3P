
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
    initial_sidebar_state="collapsed",
)

#! seaborn graph styling
sns.set_style('darkgrid')

#! reading the source file
df = pd.read_csv("main_params_data.csv")

#! an apt heading
st.header("experimentation domain")

#! column-wise split: article selection & finsih-style selection
col1, col2, col3 = st.columns(3)

all_articles = df['Article No.'].unique()
article_selectbox = col1.selectbox("Select Article:", all_articles)
article_df = df[df['Article No.']==article_selectbox]

#?finish = col2.selectbox("Select Finish Code:", article_df.Finish.unique())
#?style = col3.selectbox("Select Style:", article_df.Style.unique())