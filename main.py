# important librabries
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
st.header("Fabric Physical Parameters Predictor")


# column-wise split: article selection & warp-weft count display
col1, col2, col3 = st.columns(3)

all_articles = df['Article No.'].unique()
article_selectbox = col1.selectbox("Select Article:", all_articles)
article_df = df[df['Article No.']==article_selectbox]
# warp-weft display
count_data = article_df['Warp*Weft'].unique()[0].split("*")
warp_count = count_data[0]
weft_count = count_data[1]
count1 = col2.metric('Warp Count/Composition', warp_count)
count2 = col3.metric('Weft Count/Composition', weft_count)
# more finer selection
all_weaves = df['Weave'].unique()
weave_selectbox = col1.selectbox("Different Weaves:", all_weaves)
df['warp'], df['weft'] = df['Warp*Weft'].str.split("*",1).str
all_warp_list = df['warp'].unique()
warp_selectbox = col2.selectbox("Warp select:", all_warp_list)
all_weft_list = df['weft'].unique()
weft_selectbox = col3.selectbox("Weft select:", all_weft_list)

# column-wise split: weave display & finsih-style selection
col1, col2, col3 = st.columns(3)

article = col1.metric('Weave', article_df.Weave.unique()[0])
finish = col2.selectbox("Select Finish Code:", article_df.Finish.unique())
style = col3.selectbox("Select Style:", article_df.Style.unique())


# dataframes merger
selection_df = df.loc[(df['Article No.']==article_selectbox)&(df['Finish']==finish)&(df['Style']==style)]
merged_df = selection_df.merge(cover_df, how='left', left_on=['Print Design', 'Print Color'], right_on=['DESIGN NUMBER', 'Colour Code'])

# plotting function
def box_plot(df_select, col_num, x, y, palette, title):
    fig = plt.figure(figsize=(8, 3))
    value_to_plot = sns.boxplot(data=df_select, x=x, y=y, showmeans=True, meanprops={"marker":"|", "markerfacecolor":"white", "markeredgecolor":"darkviolet", "markersize":"300"}, showcaps=False, width=0.5, linewidth=2, whis=1, palette=palette).set(title=title)
    #fig.plot(x = 13, color = 'b', label = '12')
    col_num.pyplot(fig)

# column-wise split: graphical charts
st.subheader(f'Tear Strength Parameter plots:')
col1, col2 = st.columns(2)

weft_tear = box_plot(selection_df, col1, 'Weft Tear', 'Coverage group', 'rocket', 'Weft Tear Range')

warp_tear = box_plot(selection_df, col2, 'Warp Tear', 'Coverage group', 'winter', 'Warp Tear Range')

st.subheader(f'Tensile Strength Parameter plots:')
col1, col2 = st.columns(2)

weft_tensile = box_plot(selection_df, col1, 'Weft Tensile', 'Coverage group',  'rocket', 'Weft Tensile Range')

warp_tensile = box_plot(selection_df, col2, 'Warp Tensile', 'Coverage group',  'winter', 'Warp Tensile Range')

st.subheader(f'Stretch Parameter plots:')
col1, col2 = st.columns(2)

growth = box_plot(selection_df, col1, 'Growth', 'Coverage group', 'rocket', 'Growth Range')

elongation = box_plot(selection_df, col2, 'Elongation', 'Coverage group', 'winter', 'Elogation Range')


# article dataframe display
st.subheader(f'Article raw data: {article_selectbox}')
merged_df_display = st.dataframe(merged_df[[ 'EPI','PPI', 'Finish Width', 'Total coverage', 'Coverage group', 'Warp Shrinkage','Weft Shrinkage', 'Warp Tear','Weft Tear', 'Warp Tensile', 'Weft Tensile','Warp Slippage', 'Weft Slippage', 'Growth', 'Elongation', 'GSM', 'Warp*Weft']])