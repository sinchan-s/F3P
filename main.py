
#! important librabries
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

#! basic configurations
st.set_page_config(
    page_title="F3P Main",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#! seaborn graph styling
sns.set_style('darkgrid')

#! reading the source file
df = pd.read_csv("main_data.csv")
cover_df = pd.read_csv("Coverage data.csv")

#! an apt heading
st.header("Fabric Physical Parameters Predictor")

#! column-wise split: article selection & finish-style selection
col1, col2, col3 = st.columns(3)

all_articles = df['Article No.'].unique()
article_selectbox = col1.selectbox("Select Article:", all_articles)
article_df = df[df['Article No.']==article_selectbox]
finish = col2.selectbox("Select Finish Code:", article_df.Finish.unique())
style = col3.selectbox("Select Style:", article_df.Style.unique())

#! column-wise split: weave display & warp-weft count display
col1, col2, col3 = st.columns(3)
weave = article_df.Weave.unique()[0]
gsm = article_df.GSM.unique()[0]
article = col1.metric('Weave || GSM', weave+' || '+str(gsm))
count_data = article_df['Warp*Weft'].unique()[0].split("*")         #!split into a list 
tpi_data = article_df['EPI*PPI'].unique()[0].split("*")
count_both = col2.metric('Warp || Weft', count_data[0]+' || '+count_data[1])
tpi = col3.metric('EPI || PPI', tpi_data[0]+' || '+tpi_data[1])

#! dataframes merger
selection_df = df.loc[(df['Article No.']==article_selectbox)&(df['Finish']==finish)&(df['Style']==style)]

#! plotting function
def box_plot(df_select, col_num, x, y, palette, title, std):
    fig = plt.figure(figsize=(8, 3))
    value_to_plot = sns.boxplot(data=df_select, x=x, y=y, showcaps=False, width=0.5, linewidth=2, whis=1, palette=palette).set(title=title)
    mean_val = df_select[x].mean()
    std_mean_val = df_select[std].mean()
    plt.axvline(mean_val, c='m', ls='--', lw=3)
    plt.axvline(std_mean_val, c='r', ls='-', lw=1)
    #*fig.plot(x = 13, color = 'b', label = '12')
    col_num.pyplot(fig)

#! column-wise split: graphical charts
try:
    st.subheader(f'Tear Strength Parameter plots:')
    col1, col2 = st.columns(2)
    sorted_cover_group = selection_df.sort_values(by=["Coverage group"], ascending=False)
    weft_tear = box_plot(selection_df, col2, 'Weft Tear', sorted_cover_group['Coverage group'], 'rocket', 'Weft Tear Range','STD_Weft_Tear')
    warp_tear = box_plot(selection_df, col1, 'Warp Tear', sorted_cover_group['Coverage group'], 'winter', 'Warp Tear Range','STD_Warp_Tear')

    st.subheader(f'Tensile Strength Parameter plots:')
    col1, col2 = st.columns(2)
    weft_tensile = box_plot(selection_df, col2, 'Weft Tensile', sorted_cover_group['Coverage group'],  'rocket', 'Weft Tensile Range','STD_Weft_Tensile')
    warp_tensile = box_plot(selection_df, col1, 'Warp Tensile', sorted_cover_group['Coverage group'],  'winter', 'Warp Tensile Range','STD_Warp_Tensile')

    st.subheader(f'Stretch Parameter plots:')
    col1, col2 = st.columns(2)
    growth = box_plot(selection_df, col1, 'Growth', sorted_cover_group['Coverage group'], 'rocket', 'Growth Range', 'Growth')
    elongation = box_plot(selection_df, col2, 'Elongation', sorted_cover_group['Coverage group'], 'winter', 'Elongation Range', 'Elongation')
except ValueError:
    df_display = st.write("no data to display")

#! article dataframe display
st.subheader(f'Article raw data: {article_selectbox}')
df_display = st.dataframe(selection_df)
