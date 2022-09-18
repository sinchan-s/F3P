import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


# seaborn graph styling
sns.set_style('darkgrid')


# reading the source file
df = pd.read_csv("main_data.csv")
cover_df = pd.read_csv("Coverage data.csv")


# an apt heading
st.header("Fabric Physical Parameters Predictor: Range-Select")

col1, col2, col3 = st.columns(3)

# more finer selection
all_weaves = df['Weave'].unique()
weave_selectbox = col1.selectbox("Different Weaves:", all_weaves)
df['warp'], df['weft'] = df['Warp*Weft'].str.split("*",1).str
all_warp_list = df['warp'].unique()
warp_selectbox = col2.selectbox("Warp select:", all_warp_list)
all_weft_list = df['weft'].unique()
weft_selectbox = col3.selectbox("Weft select:", all_weft_list)
