# important librabries
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# basic configurations
st.set_page_config(
    page_title="F3P Main",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# seaborn graph styling
sns.set_style('darkgrid')


# reading the source file
df = pd.read_csv("main_data.csv")
cover_df = pd.read_csv("Coverage data.csv")


# an apt heading
st.header("Fabric Physical Parameters Predictor")


# column-wise split: article selection & finsih-style selection
col1, col2, col3 = st.columns(3)

all_articles = df['Article No.'].unique()
article_selectbox = col1.selectbox("Select Article:", all_articles)
article_df = df[df['Article No.']==article_selectbox]
finish = col2.selectbox("Select Finish Code:", article_df.Finish.unique())
style = col3.selectbox("Select Style:", article_df.Style.unique())


# column-wise split: weave display & warp-weft count display
col1, col2, col3 = st.columns(3)

article = col1.metric('Weave', article_df.Weave.unique()[0])
count_data = article_df['Warp*Weft'].unique()[0].split("*")
warp_count = count_data[0]
weft_count = count_data[1]
count_wp = col2.metric('Warp Count/Composition', warp_count)
count_wf = col3.metric('Weft Count/Composition', weft_count)


# dataframes merger
selection_df = df.loc[(df['Article No.']==article_selectbox)&(df['Finish']==finish)&(df['Style']==style)]
merged_df = selection_df.merge(cover_df, how='left', left_on=['Print Design', 'Print Color'], right_on=['DESIGN NUMBER', 'Colour Code'])

# plotting function
def box_plot(df_select, col_num, x, y, palette, title):
    fig = plt.figure(figsize=(8, 3))
    value_to_plot = sns.boxplot(data=df_select, x=x, y=y, showcaps=False, width=0.5, linewidth=2, whis=1, palette=palette).set(title=title)
    mean_val = df_select[x].mean()
    plt.axvline(mean_val, c='m', ls='--', lw=3)
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
merged_df_display = st.dataframe(merged_df[[ 'EPI','PPI', 'GSM', 'Total coverage', 'Coverage group', 'Warp Shrinkage','Weft Shrinkage', 'Warp Tear','Weft Tear', 'Warp Tensile', 'Weft Tensile','Warp Slippage', 'Weft Slippage', 'Growth', 'Elongation', 'Finish Width2', 'Warp*Weft']])