# important librabries
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


# seaborn graph styling
sns.set_style('darkgrid')


# reading the source file
df = pd.read_csv("Physical data with coverage2.csv")
cover_df = pd.read_csv("Coverage data.csv")


# an apt heading
st.header("Fabric Physical Parameters Predictor")


# column-wise split: article selection & warp-weft count display
col1, col2, col3 = st.columns(3)

all_articles = df['Article No.'].unique()
select_article = col1.selectbox("Select Article:", all_articles)
article_df = df[df['Article No.']==select_article]
count_data = article_df['Warp*Weft'].unique()[0].split("*")
warp_count = count_data[0]
weft_count = count_data[1]
count1 = col2.metric('Warp Count/Composition', warp_count)
count2 = col3.metric('Weft Count/Composition', weft_count)


# column-wise split: weave display & finsih-style selection
col1, col2, col3 = st.columns(3)

article = col1.metric('Weave', article_df.Weave.unique()[0])
finish = col2.selectbox("Select Finish Code:", article_df.Finish.unique())
style = col3.selectbox("Select Style:", article_df.Style.unique())


# dataframes merger
selection_df = df.loc[(df['Article No.']==select_article)&(df['Finish']==finish)&(df['Style']==style)]
merged_df = selection_df.merge(cover_df, how='left', left_on=['Print Design', 'Print Color'], right_on=['DESIGN NUMBER', 'Colour Code'])


# column-wise split: graphical charts
st.subheader(f'Tear Strength Parameter plots:')
col1, col2 = st.columns(2)
# Weft tear plot
fig1 = plt.figure(figsize=(8, 3))
weft_tear = sns.boxplot(data=selection_df, x='Weft Tear', y='Coverage group', width=0.5, linewidth=2, whis=1, palette='rocket').set(title='Weft Tear range')
col1.pyplot(fig1)
# Warp tear plot
fig2 = plt.figure(figsize=(8, 3))
warp_tear = sns.boxplot(data=selection_df, x='Warp Tear', y='Coverage group', width=0.5, linewidth=2, whis=1, palette='winter').set(title='Warp Tear range')
col2.pyplot(fig2)

st.subheader(f'Tensile Strength Parameter plots:')
col1, col2 = st.columns(2)
# Weft tensile plot
fig3 = plt.figure(figsize=(8, 3))
weft_tens = sns.boxplot(data=selection_df, y='Weft Tensile', x='Coverage group', width=0.5, linewidth=2, palette='rocket', whis=1).set(title='Weft Tensile range')
col1.pyplot(fig3)
# Warp tensile plot
fig4 = plt.figure(figsize=(8, 3))
warp_tens = sns.boxplot(data=selection_df, y='Warp Tensile', x='Coverage group', width=0.5, linewidth=2, whis=1, palette='winter').set(title='Warp Tensile range')
col2.pyplot(fig4)

st.subheader(f'Stretch Parameter plots:')
col1, col2 = st.columns(2)
# Growth plot
fig5 = plt.figure(figsize=(8, 3))
growth = sns.scatterplot(data=selection_df, x='Growth', y='Coverage group', hue='Coverage group', palette='rocket').set(title='Growth range')
col1.pyplot(fig5)
# Elongation plot
fig6 = plt.figure(figsize=(8, 3))
elong = sns.scatterplot(data=selection_df, x='Elongation', y='Coverage group', hue='Coverage group', palette='winter').set(title='Elongation range')
col2.pyplot(fig6)


# article dataframe display
st.subheader(f'Article raw data: {select_article}')
merged_df_display = st.dataframe(merged_df[[ 'EPI','PPI', 'Finish Width', 'Total coverage', 'Coverage group', 'Warp Shrinkage','Weft Shrinkage', 'Warp Tear','Weft Tear', 'Warp Tensile', 'Weft Tensile','Warp Slippage', 'Weft Slippage', 'Growth', 'Elongation', 'GSM', 'Warp*Weft']])